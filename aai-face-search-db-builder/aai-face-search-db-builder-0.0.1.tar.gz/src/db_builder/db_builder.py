import os
import argparse
import sqlite3
import abc
import base64
import requests
import logging
import boto3
import oss2

from typing import List

from requests.api import head

MODE_DIRECTORY = "dir"
MODE_S3 = "s3"
MODE_OSS = "oss"

MODES = {MODE_DIRECTORY: "directory", MODE_S3: "Amazon S3", MODE_OSS: "AliCloud OSS"}
VALID_EXT = (".jpg", ".JPG", ".jpeg", ".JPEG", ".png", ".PNG")


class BaseDbBuilder(metaclass=abc.ABCMeta):
    def __init__(self, mode: str, location: str, api_args: dict):
        self.mode = mode
        self.location = location
        self.api_args = api_args
        self.resume = False
        self.connection = sqlite3.connect("images.db")

    def __del__(self):
        if self.connection:
            self.connection.close()

    def _handle_config(self):
        self.connection.cursor().execute(
            "CREATE TABLE IF NOT EXISTS config(mode TEXT NOT NULL, location TEXT NOT NULL)"
        )
        self.connection.commit()

        for row in self.connection.cursor().execute("SELECT * FROM config limit 1"):
            if self.mode != row[0]:
                raise Exception(f"Please keep the same mode {row[0]} if you are continuing the program.")
            if self.location != row[1]:
                raise Exception(f"Please keep the same location {row[1]} if you are continuing the program.")
            self.resume = True

        if not self.resume:
            self.connection.cursor().execute(f'INSERT INTO config VALUES ("{self.mode}", "{self.location}")')
            self.connection.commit()

    def _read_list(self):
        self.connection.cursor().execute(
            "CREATE TABLE IF NOT EXISTS image(name TEXT NOT NULL UNIQUE, completed INT NULL)"
        )
        self.connection.commit()

        # uncomment 2 lines below if you don't want to read files list again
        # if self.resume:
        #     return

        image_names = self._get_image_names()
        for name in image_names:
            try:
                self.connection.cursor().execute(f'INSERT INTO image (name) VALUES ("{name}")')
            except sqlite3.IntegrityError:
                continue

        self.connection.commit()

    @abc.abstractmethod
    def _get_image_names(self) -> List:
        pass

    def _process(self):
        for row in self.connection.cursor().execute("SELECT * FROM image WHERE completed IS NULL"):
            image_name = row[0]
            id_number = image_name[0 : image_name.rfind(".")]

            try:
                # logging.info(f"Calling DB build API for: {image_name} ...")
                # img_content = self._get_image_content(image_name)
                # json = {
                #     self.api_args.get("img_parameter"): img_content,
                #     self.api_args.get("id_number_parameter"): id_number,
                #     self.api_args.get("refer_id_parameter"): id_number,
                # }
                # resp = requests.post(self.api_args.get("url"), json=json)

                image_location = self._get_image_location(image_name)
                headers = {"X-ADVAI-KEY": self.api_args.get("x_advai_key")}
                files = {self.api_args.get("img_parameter"): open(image_location, "rb")}
                data = {
                    self.api_args.get("id_number_parameter"): id_number,
                    self.api_args.get("refer_id_parameter"): id_number,
                    "imageType": "PHOTO_FACE",  # https://doc.advance.ai/face_search_db.html#face-search-db
                }
                resp = requests.post(self.api_args.get("url"), headers=headers, files=files, data=data)

                if resp.status_code == 200 and str(resp.json().get("status")) == self.api_args.get(
                    "success_status_code"
                ):
                    logging.info(f"Marking as completed for the image {image_name} ...")
                    self.connection.cursor().execute(
                        f'UPDATE image SET completed=strftime("%s", "now") WHERE name="{image_name}"'
                    )
                    self.connection.commit()
                else:
                    logging.error(
                        f"Error while calling the API with status {resp.status_code} and response: {resp.json()}"
                    )
            except Exception as e:
                logging.error(e)

    @abc.abstractmethod
    def _get_image_content(self, image_name: str) -> str:
        pass

    @abc.abstractmethod
    def _get_image_location(self, image_name: str) -> str:
        pass

    def build(self):
        self._handle_config()
        self._read_list()
        self._process()


class DirDbBuilder(BaseDbBuilder):
    def __init__(self, location: str, api_args: dict):
        super().__init__(MODE_DIRECTORY, location, api_args)

    def _get_image_names(self) -> List:
        return [x for x in os.listdir(self.location) if x.endswith(VALID_EXT)]

    def _get_image_content(self, image_name: str) -> str:
        with open(f"{self.location}/{image_name}", "rb") as file:
            content = base64.b64encode(file.read())
            return content.decode("utf-8")

    def _get_image_location(self, image_name: str) -> str:
        return f"{self.location}/{image_name}"


class S3DbBuilder(BaseDbBuilder):
    def __init__(
        self,
        location: str,
        api_args: dict,
        access_key: str,
        secret: str,
        bucket: str,
    ):
        super().__init__(MODE_S3, location + "/" if not location.endswith("/") else location, api_args)
        if not access_key or not secret or not bucket:
            raise Exception("Please provide S3 credentials and bucket name.")

        self.s3 = boto3.resource("s3", aws_access_key_id=access_key, aws_secret_access_key=secret)
        self.bucket = self.s3.Bucket(name=bucket)

    def _get_image_names(self) -> List:
        lst = []
        for obj in self.bucket.objects.filter(Prefix=self.location):
            name = obj.key
            if name.endswith(VALID_EXT):
                lst.append(name.replace(self.location, ""))

        return lst

    def _get_image_content(self, image_name: str) -> str:
        temp_file = "temp_file"
        self.bucket.download_file(f"{self.location}{image_name}", temp_file)
        with open(temp_file, "rb") as file:
            content = base64.b64encode(file.read())
            return content.decode("utf-8")

    def _get_image_location(self, image_name: str) -> str:
        temp_file = "temp_file"
        self.bucket.download_file(f"{self.location}{image_name}", temp_file)
        return temp_file


class OssDbBuilder(BaseDbBuilder):
    def __init__(
        self,
        location: str,
        api_args: dict,
        access_key: str,
        secret: str,
        bucket: str,
        endpoint: str,
    ):
        super().__init__(MODE_OSS, location + "/" if not location.endswith("/") else location, api_args)
        if not access_key or not secret or not bucket or not endpoint:
            raise Exception("Please provide Alibaba Cloud credentials, bucket name and endpoint.")

        auth = oss2.Auth(access_key, secret)
        self.bucket = oss2.Bucket(auth, endpoint, bucket)

    def _get_image_names(self) -> List:
        lst = []
        for obj in oss2.ObjectIterator(self.bucket, prefix=self.location):
            name = obj.key
            if name.endswith(VALID_EXT):
                lst.append(name.replace(self.location, ""))

        return lst

    def _get_image_content(self, image_name: str) -> str:
        temp_file = "temp_file"
        self.bucket.get_object_to_file(f"{self.location}{image_name}", temp_file)
        with open(temp_file, "rb") as file:
            content = base64.b64encode(file.read())
            return content.decode("utf-8")

    def _get_image_location(self, image_name: str) -> str:
        temp_file = "temp_file"
        self.bucket.get_object_to_file(f"{self.location}{image_name}", temp_file)
        return temp_file


def run():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, help="mode of upload: 'dir', 's3' or 'oss'")
    parser.add_argument("location", type=str, help="images location. Images inside must have extension .jpg or .png.")
    parser.add_argument(
        "url",
        type=str,
        help="URL of JSON POST (non multipart) db build API e.g. http://127.0.0.1:8127/face-search/v1/form/db-build",
    )
    parser.add_argument("--img_parameter", help="Parameter name for the image. Default: 'img'.")
    parser.add_argument(
        "--id_number_parameter",
        help="ID number parameter. Default: 'idNumber'. The image name without extension will be used. E.g. for 'photo.jpg', 'photo' will be sent as 'idNumber'.",
    )
    parser.add_argument(
        "--refer_id_parameter",
        help="Reference parameter. Default: 'referId'. The image name without extension will be used. E.g. for 'photo.jpg', 'photo' will be sent as 'referId'.",
    )
    parser.add_argument("--success_status_code", help="Success status code of the API. Default: '0'.")
    parser.add_argument("--x_advai_key", help="X-ADVAI-KEY header value for your access key. Default is empty.")
    parser.add_argument("--access_key", help="AWS / Alibaba Cloud access key")
    parser.add_argument("--secret", help="AWS / Alibaba Cloud secret")
    parser.add_argument("--bucket", help="AWS / Alibaba Cloud bucket name")
    parser.add_argument("--endpoint", help="Alibaba Cloud OSS endpoint")
    args = parser.parse_args()

    if args.mode not in MODES:
        raise Exception("Invalid mode")

    api_args = {
        "url": args.url,
        "img_parameter": args.img_parameter if args.img_parameter else "img",
        "id_number_parameter": args.id_number_parameter if args.id_number_parameter else "idNumber",
        "refer_id_parameter": args.refer_id_parameter if args.refer_id_parameter else "referId",
        "success_status_code": args.success_status_code if args.success_status_code else "0",
        "x_advai_key": args.x_advai_key,
    }

    db_builder = None
    if args.mode == MODE_DIRECTORY:
        db_builder = DirDbBuilder(args.location, api_args)
    elif args.mode == MODE_S3:
        db_builder = S3DbBuilder(
            args.location,
            api_args,
            args.access_key,
            args.secret,
            args.bucket,
        )
    elif args.mode == MODE_OSS:
        db_builder = OssDbBuilder(
            args.location,
            api_args,
            args.access_key,
            args.secret,
            args.bucket,
            args.endpoint,
        )

    db_builder.build()


if __name__ == "__main__":
    run()

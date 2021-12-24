# Luca de Alfaro, Massimo Di Pierro 2019
# BSD License

__all__ = ['NQGCS']

from google.cloud import storage
from google.oauth2 import service_account

class NQGCS(object):

    def __init__(self, json_key_path=None, keys=None):
        """
        Builds an NQGCS access controller.
        :param json_key_path: path to a json key to create the client.
        :param
        On appengine, one can avoid it.
        Another way is to provide the path to the json via:
        export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
        """
        if json_key_path is not None:
            self.client = storage.Client.from_service_account_json(json_key_path)
        elif keys is not None:
            credentials = service_account.Credentials.from_service_account_info(keys)
            kwargs = {}
            kwargs["project"] = keys.get("project_id")
            kwargs["credentials"] = credentials
            self.client = storage.Client(**kwargs)
        else:
            self.client = storage.Client()

    def write(self, bucketname, filename, content, type='text/plain'):
        """
        Writes content to GCS from a string
        :param bucketname: Bucket name.
        :param filename: File name in GCS.
        :param content: Content to be written.
        :param type: Type (default: text/plain).
        :return: Nothing.
        """
        bucket = self.client.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        blob.upload_from_string(content, content_type=type)

    def upload(self, bucketname, filename, local_file, type='text/plain'):
        """
        Writes content to GCS from a local file, presumed open.
        :param bucketname: Bucket name.
        :param filename: desination filename in GCS.
        :param local_file: file-like object.
        :param type: Type of file.  Consider 'application/octet-stream' if you don't know.
        :return: Nothing.
        """
        bucket = self.client.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        blob.upload_from_file(local_file, content_type=type)

    def read(self, bucketname, filename):
        """
        Reads content from GCS.
        :param bucketname: Bucket name.
        :param filename: File name.
        :return: The content read.
        """
        bucket = self.client.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        return blob.download_as_string() # returns None if not present

    def download(self, bucketname, filename, local_file):
        """
        Download blob to a local file.
        :param bucketname: Bucket name in GCS.
        :param filename: File name in GCS.
        :param local_file: Local file (open for writing).
        :return: Nothing.
        """
        bucket = self.client.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        blob.download_to_file(local_file)

    def delete(self, bucketname, filename):
        """
        Deletes a file.
        :param bucketname: Bucket name.
        :param filename: File name.
        :return: Nothing.  Raises error if not present.
        """
        bucket = self.client.get_bucket(bucketname)
        blob = storage.Blob(filename, bucket)
        blob.delete() # raises error if not present

    def listfiles(self, bucketname, maximum=None):
        """
        Lists files in a given bucket.
        :param bucketname: Name of the bucket.
        :param maximum: Maximum number of files to list.
        :return: A list of file names.
        """
        bucket = self.client.get_bucket(bucketname)
        return [blob.name for k, blob in enumerate(bucket.list_blobs())
                if maximum is None or k < maximum]

import cv2
import numpy as np
from os.path import splitext, isfile

from jcopvision.exception import MediaToArrayError


class MediaReader:
    """
    An all around media reader built on top of opencv.

    === Example Usage ===
    media = MediaReader("video.mp4")
    for frame in media.read():
        # do something
    media.close()

    === Input ===
    source: "webcam" or str or int
        media source.
        - "webcam": access default webcam, or specify the webcam integer id as in opencv.
        - int: webcam integer id as in opencv
        - str: image or video filepath, or rtsp url
    """
    def __init__(self, source="webcam"):
        self.input_type, self.cam = self._parse_source(source)
        self._parse_prop()

    def _parse_source(self, source):
        _ext = lambda source: splitext(source)[-1]
        source = 0 if source == "webcam" else source

        if isinstance(source, int) or source.startswith("rtsp://"):
            input_type = "camera"
            cam = cv2.VideoCapture(source)
        elif _ext(source) in [".mp4", ".avi"]:
            input_type = "video"
            if isfile(source):
                cam = cv2.VideoCapture(source)
            else:
                raise FileNotFoundError(f"Please check if {source} exists")
        elif _ext(source) in [".bmp", ".dib", ".jpg", ".jpeg", ".jp2", ".jpe", ".png", ".pbm", ".pgm",
                              ".ppm", ".sr", ".ras", ".tiff", ".tif"]:
            input_type = "image"
            if isfile(source):
                cam = cv2.imread(source, cv2.IMREAD_UNCHANGED)
            else:
                raise FileNotFoundError(f"Please check if {source} exists")
        else:
            raise Exception("File type not supported")
        return input_type, cam

    def _parse_prop(self):
        if self.input_type == "image":
            h, w, c = self.cam.shape
            self.aspect_ratio = w / h
            self.height = int(h)
            self.width = int(w)
        else:
            self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.aspect_ratio = self.width / self.height
            self.frame_count = self.cam.get(cv2.CAP_PROP_FRAME_COUNT)
            self.frame_rate = self.cam.get(cv2.CAP_PROP_FPS)

    def read(self):
        if self.input_type == "image":
            return self.cam
        else:
            def iter_func():
                while True:
                    cam_on, frame = self.cam.read()
                    if cam_on:
                        yield frame
                    else:
                        break
            return iter_func()

    def capture(self):
        if self.input_type != "image":
            return next(iter(self.read()))

    def stream(self, transform=None):
        while True:
            cam_on, frame = self.cam.read()
            if cam_on:
                if transform is not None:
                    frame = transform(frame)
                success, frame = cv2.imencode(".jpg", frame)
                yield b'--frame\r\n' \
                      b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n'
            else:
                break

    def close(self):
        if self.input_type in ['video', "camera"]:
            self.cam.release()

    def to_array(self, mode="rgb"):
        if self.input_type == "video":
            frames = [frame for frame in self.read()]
            frames = np.array(frames).transpose(0, 3, 1, 2)
            if mode == "rgb":
                frames = frames[:, ::-1, :, :]
            return frames
        else:
            raise MediaToArrayError("Image / webcam stream could not be converted to array. Input should be a video.")


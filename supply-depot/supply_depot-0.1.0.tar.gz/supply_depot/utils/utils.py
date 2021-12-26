import os

import cv2
import numpy as np
import requests


def makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def fullname(c):
    module = c.__module__
    if module == "builtins":
        return c.__qualname__  # avoid outputs like 'builtins.str'
    return module + "." + c.__qualname__


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={"id": id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"id": id, "confirm": token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def draw_text(
    img,
    text,
    font=cv2.FONT_HERSHEY_COMPLEX_SMALL,
    pos=(0, 0),
    font_scale=1,
    font_thickness=1,
    text_color=(0, 0, 0),
    text_color_bg=(255, 255, 255),
):
    image = np.copy(img)
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(image, pos, (x + text_w + 5, y + text_h + 5), text_color_bg, -1)
    cv2.putText(
        image,
        text,
        (x, y + text_h + font_scale - 1),
        font,
        font_scale,
        text_color,
        font_thickness,
    )

    return image

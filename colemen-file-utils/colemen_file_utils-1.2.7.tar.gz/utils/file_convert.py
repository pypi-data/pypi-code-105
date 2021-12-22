# pylint: disable=bare-except
# pylint: disable=line-too-long

'''
    Module for file conversions
'''

# import subprocess
# import json
# import shutil
import os
import ffmpeg
# import re
# from pathlib import Path
import utils.file as f
import utils.objectUtils as obj
# import utils.file_read as read
# import colemen_string_utils as strUtils
# from threading import Thread


# def to(input_path, extension):
#     extension = strUtils.format.extension(extension)
#     input_list = input
#     if isinstance(input, (str)):
#         input_list = [input]

#     for path in input_list:
#         if f.exists(path) is False:
#             print(f"    Could not find file: {path}")
#             return False
#         name_no_ext = f.get_name_no_ext(path)
#         # ext = f.get_ext(path)
#         ffmpeg.input(path).output(f"{name_no_ext}.{extension}", vcodec='copy').run(overwrite_output=True)


def to_mp4(input_value, **kwargs):
    '''
        Convert an audio/video file to mp4

        ----------

        Arguments
        -------------------------
        `input_value` {str|list}
            The path or list of paths to convert.

        Keyword Arguments
        -------------------------
        [`delete_after`=False] {bool}
            If True, the original file is deleted after conversion.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12\\21\\2021 17:32:39
        `memberOf`: file_convert
        `version`: 1.0
        `method_name`: to_mp4
    '''

    delete_original_after = obj.get_kwarg(['delete after'], False, (bool), **kwargs)

    input_list = input_value
    if isinstance(input_value, (str)):
        input_list = [input_value]

    for path in input_list:
        if f.exists(path) is False:
            print(f"Could not find file: {path}")
            continue

        output_path = f"{os.path.dirname(path)}/{f.get_name_no_ext(path)}.mp4"
        try:
            ffmpeg.input(path).output(output_path, vcodec='copy').run(overwrite_output=True)
            if delete_original_after:
                f.delete(path)
        except:
            print(f"There was an error converting: {path}")


def to_mp3(input_value, **kwargs):
    '''
        Convert an audio/video file to mp3

        ----------

        Arguments
        -------------------------
        `input_value` {str|list}
            The path or list of paths to convert.

        Keyword Arguments
        -------------------------
        [`delete_after`=False] {bool}
            If True, the original file is deleted after conversion.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-21-2021 17:29:36
        `memberOf`: file_convert
        `version`: 1.0
        `method_name`: to_mp3
    '''
    delete_original_after = obj.get_kwarg(['delete after'], False, (bool), **kwargs)

    input_list = input_value
    if isinstance(input_value, (str)):
        input_list = [input_value]

    for path in input_list:
        if f.exists(path) is False:
            print(f"Could not find file: {path}")
            continue

        output_path = f"{os.path.dirname(path)}/{f.get_name_no_ext(path)}.mp3"
        try:
            ffmpeg.input(path).output(output_path, vcodec='copy').run(overwrite_output=True)
            if delete_original_after:
                f.delete(path)
        except:
            print(f"There was an error converting: {path}")

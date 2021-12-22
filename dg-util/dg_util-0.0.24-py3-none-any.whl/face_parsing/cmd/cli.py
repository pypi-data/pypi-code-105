import argparse
import glob
import os
from distutils.util import strtobool

import filetype
from tqdm import tqdm

from ..interfaces import parsing_face, parsing_faces


def main():
    # model_path = os.environ.get(
    #     "U2NETP_PATH",
    #     os.path.expanduser(os.path.join("~", ".u2net")),
    # )
    model_path='.cache/face_parsing/79999_iter.pth'
    model_choices = [
        os.path.splitext(os.path.basename(x))[0]
        for x in set(glob.glob(model_path + "/*"))
    ]

    model_choices = list(set(model_choices + ["BiSeNet"]))

    ap = argparse.ArgumentParser()

    ap.add_argument(
        "-m",
        "--model",
        default="BiSeNet",
        type=str,
        choices=model_choices,
        help="The model name.",
    )

    ap.add_argument(
        "-p",
        "--path",
        nargs=2,
        help="An input folder and an output folder.",
    )

    ap.add_argument(
        "-o",
        "--output",
        nargs="?",
        default="-",
        type=argparse.FileType("wb"),
        help="Path to the output png image.",
    )

    ap.add_argument(
        "input",
        nargs="?",
        default="-",
        type=argparse.FileType("rb"),
        help="Path to the input image.",
    )

    args = ap.parse_args()

    r = lambda i: i.buffer.read() if hasattr(i, "buffer") else i.read()
    w = lambda o, data: o.buffer.write(data) if hasattr(o, "buffer") else o.write(data)

    if args.path:
        full_paths = [os.path.abspath(path) for path in args.path]

        input_paths = [full_paths[0]]
        output_path = full_paths[1]

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        files = set()

        for path in input_paths:
            if os.path.isfile(path):
                files.add(path)
            else:
                input_paths += set(glob.glob(path + "/*"))

        for fi in tqdm(files):
            fi_type = filetype.guess(fi)

            if fi_type is None:
                continue
            elif fi_type.mime.find("image") < 0:
                continue

            with open(fi, "rb") as input:
                with open(
                    os.path.join(
                        output_path, os.path.splitext(os.path.basename(fi))[0] + ".png"
                    ),
                    "wb",
                ) as output:
                    w(
                        output,
                        parsing_face(
                            r(input)
                    )

    else:
        w(
            args.output,
            parsing_face(
                r(args.input)
            ),
        )


if __name__ == "__main__":
    main()

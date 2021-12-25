import argparse
import os
import pathlib
import time
import h5py
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from typing import NoReturn

from bytesep.utils import float32_to_int16


def pack_audios_to_hdf5s(args) -> NoReturn:
    r"""Pack (resampled) audio files into hdf5 files to speed up loading.

    Args:
        dataset_dir: str
        split: str, 'train' | 'test'
        hdf5s_dir: str, directory to write out hdf5 files
        sample_rate: int
        channels_num: int
        mono: bool

    Returns:
        NoReturn
    """

    # arguments & parameters
    hdf5s_dir = args.hdf5s_dir
    sample_rate = args.sample_rate
    channels = args.channels
    mono = True if channels == 1 else False

    segment_seconds = 10.0
    segments_num = 1000
    source_type = "silence"

    assert channels == 1

    os.makedirs(hdf5s_dir, exist_ok=True)

    params = []
    audio_index = 0

    pack_hdf5s_time = time.time()

    for audio_index in range(segments_num):

        audio_name = "{:04d}".format(audio_index)
        hdf5_path = os.path.join(hdf5s_dir, "{}.h5".format(audio_name))

        with h5py.File(hdf5_path, "w") as hf:

            hf.attrs.create("audio_name", data=audio_name, dtype="S100")
            hf.attrs.create("sample_rate", data=sample_rate, dtype=np.int32)

            audio = np.zeros((1, int(sample_rate * segment_seconds)))

            hf.create_dataset(
                name=source_type, data=float32_to_int16(audio), dtype=np.int16
            )

        print(audio_index, "write out to {}".format(hdf5_path))

    print("Pack hdf5 time: {:.3f} s".format(time.time() - pack_hdf5s_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--hdf5s_dir",
        type=str,
        required=True,
        help="Directory to write out hdf5 files.",
    )
    parser.add_argument("--sample_rate", type=int, required=True, help="Sample rate.")
    parser.add_argument(
        "--channels", type=int, required=True, help="Use 1 for mono, 2 for stereo."
    )

    # Parse arguments.
    args = parser.parse_args()

    # Pack audios into hdf5 files.
    pack_audios_to_hdf5s(args)

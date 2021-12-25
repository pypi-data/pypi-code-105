import argparse
import os
import pathlib
import time
import pandas as pd
import csv
from concurrent.futures import ProcessPoolExecutor
from typing import NoReturn

from bytesep.dataset_creation.pack_audios_to_hdf5s.instruments_solo import (
    write_single_audio_to_hdf5,
)


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
    dataset_dir = args.dataset_dir
    split = args.split
    hdf5s_dir = args.hdf5s_dir
    sample_rate = args.sample_rate
    channels = args.channels
    mono = True if channels == 1 else False

    source_type = "speech"

    # Only pack data for training data.
    assert split == "train"

    assert channels == 1

    csv_path = os.path.join(
        dataset_dir, "FSD50K.metadata/collection/collection_dev.csv"
    )
    audios_dir = os.path.join(dataset_dir, "FSD50K.dev_audio")

    # with open(csv_path, 'r') as fr:
    #     reader = csv.reader(fr)
    #     lines = list(reader)

    df = pd.read_csv(csv_path)
    df = pd.DataFrame(df)

    audios_num = len(df)

    params = []

    for n in range(audios_num):
        print(n)
        bare_name = df['fname'][n]
        audio_path = os.path.join(audios_dir, "{}.wav".format(bare_name))

        try:
            labels = df['labels'][n].split(',')

            for label in labels:

                sub_hdf5s_dir = os.path.join(hdf5s_dir, label)
                os.makedirs(sub_hdf5s_dir, exist_ok=True)
                hdf5_path = os.path.join(sub_hdf5s_dir, "{}.h5".format(bare_name))

                source_type = "waveform"
                param = (
                    n,
                    bare_name,
                    source_type,
                    audio_path,
                    mono,
                    sample_rate,
                    hdf5_path,
                )

                params.append(param)
        except:
            pass

    # Uncomment for debug.
    # write_single_audio_to_hdf5(params[0])
    # os._exit(0)

    pack_hdf5s_time = time.time()

    with ProcessPoolExecutor(max_workers=None) as pool:
        # Maximum works on the machine
        pool.map(write_single_audio_to_hdf5, params)

    print("Pack hdf5 time: {:.3f} s".format(time.time() - pack_hdf5s_time))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset_dir",
        type=str,
        required=True,
        help="Directory of the VCTK dataset.",
    )
    parser.add_argument("--split", type=str, required=True, choices=["train", "test"])
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

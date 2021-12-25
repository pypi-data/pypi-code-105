import argparse
import os
import numpy as np
import pathlib
import time
import h5py
from concurrent.futures import ProcessPoolExecutor
from typing import NoReturn

import librosa
from panns_inference import AudioTagging

from bytesep.dataset_creation.pack_audios_to_hdf5s.instruments_solo import (
    write_single_audio_to_hdf5,
)
from bytesep.utils import int16_to_float32, float32_to_int16


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
    audioset_hdf5_path = args.audioset_hdf5_path
    output_hdf5s_dir = args.hdf5s_dir
    sample_rate = args.sample_rate
    channels_num = args.channels

    assert channels_num == 1

    original_sample_rate = 32000
    # sample_rate = 44100

    os.makedirs(output_hdf5s_dir, exist_ok=True)

    at = AudioTagging(checkpoint_path=None, device='cuda')

    with h5py.File(audioset_hdf5_path, 'r') as hf:
        audios_num = len(hf['audio_name'])

        for n in range(audios_num):
            audio_name = hf['audio_name'][n].decode()
            target = hf['target'][n]
            audio = int16_to_float32(hf['waveform'][n])

            segments = audio.reshape(10, 32000)

            # clipwise_output, embedding = at.inference(audio[None, :])
            clipwise_output, embedding = at.inference(segments)

            # max_speech_prob = np.max(clipwise_output[0][0 : 72])
            max_speech_prob = np.max(np.max(clipwise_output, axis=0)[0:72])

            if max_speech_prob < 0.1 and np.max(target[0:72]) == 0:

                audio = librosa.resample(
                    y=audio,
                    orig_sr=original_sample_rate,
                    target_sr=sample_rate,
                    res_type='kaiser_fast',
                )
                # (audio_samples,) | (channels_num, audio_samples)

                audio *= 0.3

                if audio.ndim == 1:
                    audio = audio[None, :]
                    # (1, audio_samples,)

                bare_name = pathlib.Path(audio_name).stem
                output_hdf5_path = os.path.join(
                    output_hdf5s_dir, "{}.h5".format(bare_name)
                )

                with h5py.File(output_hdf5_path, "w") as hf_write:
                    hf_write.attrs.create("audio_name", data=audio_name, dtype="S100")
                    hf_write.attrs.create(
                        "sample_rate", data=sample_rate, dtype=np.int32
                    )

                    hf_write.create_dataset(
                        name="nonspeech", data=float32_to_int16(audio), dtype=np.int16
                    )

                print("{} Write out to {}".format(n, output_hdf5_path))

                # from IPython import embed; embed(using=False); os._exit(0)
                # import soundfile
                # soundfile.write(file='_tmp/{:05d}.wav'.format(n), data=audio[0], samplerate=sample_rate)

            # if n == 100:
            #     break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--audioset_hdf5_path",
        type=str,
        required=True,
        help="",
    )
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

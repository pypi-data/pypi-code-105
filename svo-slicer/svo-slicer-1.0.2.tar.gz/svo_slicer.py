from datetime import datetime
import os
import shutil
import pyzed.sl as sl
import numpy as np
import cv2
import random
import string
import argparse
import zipfile


def zipdir(ziph, output_path):
    shuffled_files = sorted(os.listdir(output_path), key = lambda k: random.random())
    for n, file in enumerate(shuffled_files):
        ziph.write(os.path.join(output_path, file), os.path.relpath(os.path.join(output_path, file), output_path))

def slice_image(filepath, output_path_name, per_svo_sample):
    counter = 0
    input_type = sl.InputType()
    input_type.set_from_svo_file(filepath)
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    cam = sl.Camera()
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()
    runtime = sl.RuntimeParameters()
    mat = sl.Mat()
    key = ''
    while counter < per_svo_sample:  # for 'q' key
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS and np.random.randint(0,30) == 0:
            cam.retrieve_image(mat)
            generated_name = filepath.split("/")[-1].replace(".svo", "_") + ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=12)) + '.jpg'
            generated_path = os.path.join(output_path_name, generated_name)
            image = mat.get_data()
            cv2.imwrite(generated_path, image[:,:,:3])
            counter+=1
    cam.close()

def main(opt):
    input_path, output_path, sample_size = opt.input, opt.output, opt.sample
    print("Starting process...")
    now = datetime.now().strftime("%d%m%Y_%H%M%S")
    output_path_name = os.path.join(output_path, f"sliced_{now}")
    try:
        os.mkdir(output_path_name)
    except FileExistsError:
        pass
    print("slicing...")
    svo_list = [n for n in os.listdir(input_path) if n.endswith(".svo")]
    per_svo_sample = sample_size / len(svo_list)
    for svo in svo_list:
        slice_image(os.path.join(input_path,svo), output_path_name, per_svo_sample)
    print("zipping...")
    zipf = zipfile.ZipFile(output_path_name+".zip", "w", zipfile.ZIP_DEFLATED)
    zipdir(zipf, output_path_name)
    zipf.close()
    shutil.rmtree(output_path_name)
    print("slicing done...")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='./', help='path to the folder that contains all the .svo files')
    parser.add_argument('--output', type=str, default='./', help='path to which a .zip file will be written')
    parser.add_argument('--sample', type=int, default=500, help='number of images that will be rendered ')
    opt = parser.parse_args()
    main(opt)
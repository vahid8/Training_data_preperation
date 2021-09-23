#!/usr/bin/env python
""" Get the detection texts paths (edited and original ones) and compare the content
input : edited and original texts dir paths, splitted image dir paths
output : text ones that are changed (means the model labeling was not ok) and its related images from separated image
dir
"""

import os
import filecmp
import shutil
import tqdm
import yaml

__author__ = "vahid jani"
__copyright__ = "Copyright 2021, The Blurring Project"
__credits__ = ["Vahid jani"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Vahid jani"
__email__ = "aghajanivahid1@gmail.com"
__status__ = "Development"


if __name__ == '__main__':
    # ----------------------------------------- Read and load the inputs config --------------------------------------------------
    with open(r'compare_text_files_config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    input_dir = config["input_dir"]

    edited_text_path = os.path.join(input_dir,"detections")
    original_text_path = os.path.join(input_dir,"original_detections")
    splitted_images_path = os.path.join(input_dir,"images")

    # Create folders inside output_dir
    try:
        os.mkdir(os.path.join(input_dir, "final"))
    except OSError as error:
        print(error)

    for item in list(["images", "detections"]):
        try:
            os.mkdir(os.path.join(input_dir, "final", item))
        except OSError as error:
            print(error)

    output_images_dir = os.path.join(input_dir, "final", "images")
    output_detection_dir = os.path.join(input_dir, "final", "detections")

    editedt_files = [item for item in os.listdir(edited_text_path)]
    original_files = [item for item in os.listdir(original_text_path)]

    changed_files=list()
    for item in editedt_files:
        if item not in original_files:
            # it is 100% new label
            changed_files.append(item)
        else:
            if not filecmp.cmp(os.path.join(edited_text_path,item), os.path.join(original_text_path,item)):
                changed_files.append(item)


    print("number of all text files: ",len(editedt_files))
    print("number of edited files: ",len(changed_files))
    for item in tqdm.tqdm(changed_files):
        shutil.copy(os.path.join(edited_text_path,item), output_detection_dir)
        shutil.copy(os.path.join(splitted_images_path, item[:-3]+"jpg"), output_images_dir)



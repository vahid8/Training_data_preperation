#!/usr/bin/env python
"""
Create two folders of train and val from one input folder
"""
import os

import tqdm
from sklearn.utils import shuffle
from shutil import copyfile
from typing import Dict

__author__ = "vahid jani"
__Date__ = "29.10.2021"
__copyright__ = "Copyright 2021"
__credits__ = ["Vahid jani"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Vahid jani"
__email__ = "aghajanivahid1@gmail.com"
__status__ = "Development"


# -------------------------------------------------
# Functions
# -------------------------------------------------
def split_data(config:Dict,val_percentage:int=0.1) -> None:
    """
    Split data to two folder naming train and val
    ----------
    config [Dict]: Configuration file containing the input and output dir
    val_percentage [int]: splitting percentage for validation

    Returns
    --------
    None
    """
    image_in_path = os.path.join(config.get("input_dir"),"images")
    label_in_path = os.path.join(config.get("input_dir"),"labels")
    # Get all data in images and labels
    images = [item for item in os.listdir(image_in_path) if item.endswith(".jpg")]
    labels = [item for item in os.listdir(label_in_path) if item.endswith(".json")]
    print(f"Number of images, labels: {len(images)},{len(labels)}")
    labels_raw_name = [item[:-4] for item in labels]
    missing_labels = list()
    # Check the files
    for item in images:
        if item[:-3] not in labels_raw_name:
            missing_labels.append(item)
    if len(missing_labels):
        print(f"Number of images without label {len(missing_labels)}")

    # Create Val and train folder
    parent_train_dir = os.path.join(config.get("output_dir"), "train")
    parent_val_dir = os.path.join(config.get("output_dir"), "val")
    train_images_out = os.path.join(config.get("output_dir"), "train", "images")
    train_labels_out = os.path.join(config.get("output_dir"), "train", "labels")
    val_images_out = os.path.join(config.get("output_dir"), "val", "images")
    val_labels_out = os.path.join(config.get("output_dir"), "val", "labels")

    for item in [parent_train_dir, parent_val_dir,
                 train_images_out, train_labels_out,
                 val_images_out, val_labels_out]:
        try:
            os.mkdir(item)
        except FileExistsError:
            pass
    # shuffle data in image list and select randomly in between
    val_num = int(val_percentage*len(images))
    images = shuffle(images)
    val_images = images[:val_num]
    train_images = images[val_num:]
    for item in tqdm.tqdm(train_images, desc="Copy train data"):
        copyfile(os.path.join(image_in_path,item),
                 os.path.join(train_images_out,item))
        copyfile(os.path.join(label_in_path,item[:-3]+"json"),
                 os.path.join(train_labels_out,item[:-3]+"json"))

    for item in tqdm.tqdm(val_images, desc="Copy val data"):
        copyfile(os.path.join(image_in_path,item),
                 os.path.join(val_images_out,item))
        copyfile(os.path.join(label_in_path,item[:-3]+"json"),
                 os.path.join(val_labels_out,item[:-3]+"json"))



# -------------------------------------------------
# Main Function
# -------------------------------------------------
if __name__ == '__main__':
    config = {}
    config["input_dir"] = "/media/vahid/Elements/Data/segmentation_training/series1"
    config["output_dir"] = "/media/vahid/Elements/Data/segmentation_training/splitted"
    split_data(config,val_percentage=0.1)
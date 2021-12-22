#!/usr/bin/env python
"""
Create two folders of train and val from one input folder
input:
- Dataset
    -- images
    -- labels

the output will be like this
- Dataset
    -- train
        --images
        --labels
    -- val
        --images
        --labels
"""
import os

import tqdm
from sklearn.utils import shuffle
from shutil import copyfile
from typing import Dict

__author__ = "vahid jani"
__Date__ = "19.11.2021"
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
    image_in_path = os.path.join(config.get("input_dir"), "train")
    label_in_path = os.path.join(config.get("input_dir"), "labels")
    # Get all data in images and labels
    images = [item for item in os.listdir(image_in_path) if item.endswith(".jpg")]
    labels = [item for item in os.listdir(label_in_path) if item.endswith(".txt")]
    print(f"Number of images, labels: {len(images)},{len(labels)}")
    labels_raw_name = [item[:-4] for item in labels]
    missing_labels = list()
    # Check the files
    # create base names for images and labels
    image_names_base = [os.path.splitext(item)[0] for item in images]
    label_names_base = [os.path.splitext(item)[0] for item in labels]
    # Check for images without txt and labels without image
    images_without_label = [item for item in image_names_base if item not in label_names_base]
    labels_without_images = [item for item in label_names_base if item not in image_names_base]

    #  print out the result:
    if len(images_without_label) > 0:
        print(f" number of images without label are {len(images_without_label)}")
        print(*images_without_label)
    else:
        print("All images have a correspondence txt file")

    if len(labels_without_images) > 0:
        print(f" number of txt without images are {len(labels_without_images)}")
        print(*labels_without_images)
    else:
        print("All txt files have a correspondence images file")

    # Exclude images without label
    images = [item for item in images if os.path.splitext(item)[0] in label_names_base]


    # Create Val and train output folder
    parent_train_dir = os.path.join(config.get("output_dir"), "train")
    parent_val_dir = os.path.join(config.get("output_dir"), "val")
    train_images_out = os.path.join(config.get("output_dir"), "train", "images")
    train_labels_out = os.path.join(config.get("output_dir"), "train", "labels")
    val_images_out = os.path.join(config.get("output_dir"), "val", "images")
    val_labels_out = os.path.join(config.get("output_dir"), "val", "labels")

    # Create paths if dont exist
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
        copyfile(os.path.join(label_in_path,item[:-3]+"txt"),
                 os.path.join(train_labels_out,item[:-3]+"txt"))

    for item in tqdm.tqdm(val_images, desc="Copy val data"):
        copyfile(os.path.join(image_in_path,item),
                 os.path.join(val_images_out,item))
        copyfile(os.path.join(label_in_path,item[:-3]+"txt"),
                 os.path.join(val_labels_out,item[:-3]+"txt"))

# -------------------------------------------------
# Main Function
# -------------------------------------------------
if __name__ == '__main__':
    config = {}
    config["input_dir"] = "/media/vahid/Elements/Data/Training data_2"
    config["output_dir"] = "/media/vahid/Elements/Data/yolo_face_plate_dataset/new_data"
    split_data(config,val_percentage=0.1)
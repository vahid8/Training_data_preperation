#!/usr/bin/env python
""" Copy the images in from a folder to subfolders with 1000 images in each
    input : images and detections paths, output path for images
    output : None
"""

import os
from shutil import copyfile
import tqdm


__author__ = "vahid jani"
__copyright__ = "Copyright 2021"
__credits__ = ["Vahid jani"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Vahid jani"
__email__ = "aghajanivahid1@gmail.com"
__status__ = "Development"


if __name__ == '__main__':
    # Define input and output dir paths
    detections_dir = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/all_labels"
    source_images_dir = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/all_images"
    output_dir = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/splitted_1000"

    # Get the name of available images inside source dir
    images = [item for item in os.listdir(source_images_dir) if item.endswith(".jpg")
              or item.endswith(".jpeg") or item.endswith(".png")  or item.endswith(".JPEG")]

    a = len(images) % 1000
    if a<500:
        Folders_num = int(len(images)/1000)
    else :
        Folders_num = int(len(images) / 1000)+1

    print(Folders_num)
    if Folders_num == 0:
        Folders_num =1 # we need at least one folder
    #split images to folders
    folder_image_pair = {}
    for item in range(Folders_num-1):
        #create folder inside out_dir
        os.mkdir(os.path.join(output_dir, str(item)))
        os.mkdir(os.path.join(output_dir,str(item),"img"))
        os.mkdir(os.path.join(output_dir, str(item),"txt"))

        for i in range(item*1000,(item+1)*1000):
            copyfile(os.path.join(source_images_dir, images[i]), os.path.join(output_dir,str(item), "img",images[i]))
            copyfile(os.path.join(detections_dir, os.path.splitext(images[i])[0]+".txt"), os.path.join(output_dir,str(item), "txt", os.path.splitext(images[i])[0]+".txt"))
    #the last files
    item = Folders_num-1
    # create folder inside out_dir
    os.mkdir(os.path.join(output_dir, str(item)))
    os.mkdir(os.path.join(output_dir, str(item), "img"))
    os.mkdir(os.path.join(output_dir, str(item), "txt"))

    for i in range(item * 1000, len(images)):
        copyfile(os.path.join(source_images_dir, images[i]), os.path.join(output_dir, str(item),"img", images[i]))
        copyfile(os.path.join(detections_dir, os.path.splitext(images[i])[0] + ".txt"),os.path.join(output_dir,str(item), "txt", os.path.splitext(images[i])[0] + ".txt"))

#!/usr/bin/env python
""" Copy the images that have detection texts from one dir to another
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
    detections_dir = "/media/vahid/Elements/Data/sample_images/sample_detections/texts"
    source_images_dir = "/media/vahid/Elements/Data/sample_images/sample_detections/img"
    output_images_dir = "/media/vahid/Elements/Data/sample_images/sample_detections/n_img"
    output_text_dir = "/media/vahid/Elements/Data/sample_images/sample_detections/n_txt"

    # Get the name of available texts and convert it to .jpg
    detections = [os.path.splitext(item)[0] for item in os.listdir(detections_dir) if item.endswith(".txt")]

    # Get the name of available images inside source dir
    images = [item for item in os.listdir(source_images_dir) if item.endswith(".jpg")
              or item.endswith(".jpeg") or item.endswith(".png")  or item.endswith(".JPEG")]

    for image in tqdm.tqdm(images):
        if os.path.splitext(image)[0] in detections: # check if the image has a detection
            copyfile(os.path.join(source_images_dir,image),os.path.join(output_images_dir,image))
            copyfile(os.path.join(detections_dir, os.path.splitext(image)[0]+".txt"), os.path.join(output_text_dir, os.path.splitext(image)[0]+".txt"))

    images_number = len([item for item in os.listdir(output_images_dir)])
    text_number = len([item for item in os.listdir(output_images_dir)])
    print("Number of images: {}".format(images_number))
    print("Number of texts: {}".format(text_number))
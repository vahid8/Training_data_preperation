#!/usr/bin/env python
""" Copy the images that have detection texts from one dir to another
    input : images and detections paths, output path for images
    output : None
"""

import os
from shutil import copyfile


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
    detections_dir = "/media/vahid/Elements/Softwaress/Flask_blurring/project/static/uploads/vahid/person/detections2"
    source_images_dir = "/media/vahid/Elements/Softwaress/Flask_blurring/project/static/uploads/vahid/person/src"
    output_images_dir = "/media/vahid/Elements/Softwaress/Flask_blurring/project/static/uploads/vahid/person/src2"

    # Get the name of available texts and convert it to .jpg
    detections = [item[:-3]+"jpg" for item in os.listdir(detections_dir) if item.endswith(".txt")]

    # Get the name of available images inside source dir
    images = [item for item in os.listdir(source_images_dir) if item.endswith(".jpg")]

    for detect in detections:
        if detect in images: # check if the image is available there
            copyfile(os.path.join(source_images_dir,detect),os.path.join(output_images_dir,detect))

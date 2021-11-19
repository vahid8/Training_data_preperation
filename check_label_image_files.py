#!/usr/bin/env python
"""
read two folder -> image , labels
number of images
number of txt files
print out which image has no txt file + which txt has no image
"""
# Import external libs
import os


__author__ = "vahid jani"
__copyright__ = "Copyright 2021, The labeling tools"
__credits__ = ["Vahid jani"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Vahid jani"
__email__ = "aghajanivahid1@gmail.com"
__status__ = "Development"


# ==============================================================================
# Classes
# ==============================================================================
if __name__ == '__main__':
    image_folder = "/media/vahid/Elements/Data/blurring_training_data/Training data - Blurring/series2_2/src"
    label_folder = "/media/vahid/Elements/Data/blurring_training_data/Training data - Blurring/series2_2/detections"
    # Get all image names and label names
    image_names = [item for item in os.listdir(image_folder) if item.endswith(".jpg") or item.endswith(".jpeg") or
                   item.endswith(".png")]
    label_names = [item for item in os.listdir(label_folder) if item.endswith(".txt")]

    print(f" Number of images: {len(image_names)}")
    print(f" Number of labls: {len(label_names)}")

    # create base names for images and labels
    image_names_base = [os.path.splitext(item)[0] for item in image_names]
    label_names_base = [os.path.splitext(item)[0] for item in label_names]

    # Check for images without txt and labels without image
    images_without_label = [item for item in image_names_base if item not in label_names_base]
    labels_without_images = [item for item in label_names_base if item not in image_names_base]

    #  print out the result:
    if len(images_without_label) > 0:
        print(f" number of images without label are {len(images_without_label)}")
    else:
        print("All images have a correspondence txt file")
        print(*images_without_label)

    if len(labels_without_images) > 0:
        print(f" number of txt without images are {len(labels_without_images)}")
        print(*labels_without_images)
    else:
        print("All txt files have a correspondence images file")
#!/usr/bin/env python
""" Get the images and detection texts and divide images to smaller parts
    input image : Trimble MX9 Panorama 8000*400 ->image_A.jpg
    output images : 4 images in 2000*2000 ->image_A_1.jpg,image_A_2.jpg, image_A_3.jpg, image_A_4.jpg
                    im1 = im[1100:3100, 0:2000]
                    im2 = im[1100:3100, 2000:4000]
                    im3 = im[1100:3100, 4000:6000]
                    im4 = im[1100:3100, 6000:8000]
    input_texts : detection in the original image dimensions
    output_texts :  detections on new image formats
"""

import cv2
import os
import pandas as pd
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


def content_to_pandas(content, img_shape):
    idx = list()
    cls = list()
    conf = list()
    cnt = list()
    area = list()
    bbox = list()
    try:
        for num, line in enumerate(content):
            if len(line) > 1:
                l = line.split(" ")
                idx.append(num)
                cls.append(l[0])  # class_names[content[0]]
                cnt.append((int(float(l[1]) * img_shape[1]), int(float(l[2]) * img_shape[0])))
                area.append(int(float(l[3]) * float(l[4]) * img_shape[0] * img_shape[1]))
                bbox_xstart = int(float(l[1]) * img_shape[1] - float(l[3]) * img_shape[1] / 2)
                bbox_ystart = int(float(l[2]) * img_shape[0] - float(l[4]) * img_shape[0] / 2)
                bb = (bbox_xstart, bbox_ystart, bbox_xstart + int(float(l[3]) * img_shape[1]),
                      bbox_ystart + int(float(l[4]) * img_shape[0]))
                bbox.append(bb)
        # There is at least one object there
        if len(idx) > 0:
            dict = {"idx": idx, "cls": cls, "cnt": cnt, "area": area, "bbox": bbox}
            df = pd.DataFrame(dict)
            success = True
        else:
            df = pd.DataFrame()
    except:
        df = pd.DataFrame()

    return df

if __name__ == '__main__':

    # ----------------------------------------- Read and load the inputs config --------------------------------------------------
    with open(r'config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    image_path = config["image_path"]
    detection_path = config["detection_path"]
    output_image_path = config["output_image_path"]
    output_detection_path = config["output_detection_path"]
    create_new_images = config["output_detection_path"]

    zones = [[(0, 1100), (2000, 3100)], [(2000, 1100), (4000, 3100)], [(4000, 1100), (6000, 3100)],
             [(6000, 1100), (8000, 3100)]]
    # 1. read the image
    images = [item for item in os.listdir(image_path)]
    detections = [os.path.join(image_path, item) for item in os.listdir(detection_path)]
    # 2. split image into 4 images
    for item in tqdm.tqdm(images):
        image_name_path = os.path.join(image_path, item)
        detect = os.path.join(detection_path, item[:-3] + "txt")
        im = cv2.imread(image_name_path)
        if create_new_images:
            im1 = im[1100:3100, 0:2000]
            im2 = im[1100:3100, 2000:4000]
            im3 = im[1100:3100, 4000:6000]
            im4 = im[1100:3100, 6000:8000]

            cv2.imwrite(os.path.join(output_image_path, item[:-4] + "_1.jpg"), im1)
            cv2.imwrite(os.path.join(output_image_path, item[:-4] + "_2.jpg"), im2)
            cv2.imwrite(os.path.join(output_image_path, item[:-4] + "_3.jpg"), im3)
            cv2.imwrite(os.path.join(output_image_path, item[:-4] + "_4.jpg"), im4)
        # 3. split texts in 4 texts and in correct positions
        with open(detect) as file:
            content = file.read().split("\n")
            df = content_to_pandas(content, im.shape)
            boxes = [[], [], [], []]
            if len(df) > 0:
                # Get bounding boxes
                for index, row in df.iterrows():
                    # Get class
                    if row.cls == "1" or row.cls == "3":
                        # start_point = row.bbox[0],row.bbox[1]
                        # end_point = row.bbox[2],row.bbox[3]
                        for num, zone in enumerate(zones):

                            if zone[0][0] < row.bbox[0] < zone[1][0] and zone[0][1] < row.bbox[1] < zone[1][1]:
                                # if the upper left point is inside the zone

                                if zone[0][0] < row.bbox[2] < zone[1][0] and zone[0][1] < row.bbox[3] < zone[1][1]:
                                    # if the bottom right corner is also in the image
                                    a_x = (row.bbox[0] - zone[0][0]) / 2000
                                    b_x = (row.bbox[2] - zone[0][0]) / 2000
                                    a_y = (row.bbox[1] - zone[0][1]) / 2000
                                    b_y = (row.bbox[3] - zone[0][1]) / 2000
                                    cnt_x = (a_x + b_x) / 2
                                    w_x = b_x - a_x
                                    cnt_y = (a_y + b_y) / 2
                                    w_y = b_y - a_y
                                    boxes[num].append(
                                        [row.cls, round(cnt_x, 6), round(cnt_y, 6), round(w_x, 6), round(w_y, 6)])
                                else:
                                    # if the bottom right corner is outside
                                    a_x = (row.bbox[0] - zone[0][0]) / 2000
                                    a_y = (row.bbox[1] - zone[0][1]) / 2000

                                    b_x = (row.bbox[2] - zone[0][0]) / 2000 if zone[0][0] < row.bbox[2] < zone[1][0] else 1
                                    b_y = (row.bbox[3] - zone[0][1]) / 2000 if zone[0][1] < row.bbox[3] < zone[1][1] else 1

                                    cnt_x = (a_x + b_x) / 2
                                    w_x = b_x - a_x
                                    cnt_y = (a_y + b_y) / 2
                                    w_y = b_y - a_y
                                    if w_x > 0.008 and w_y > 0.008:  # skip narrow boxes
                                        boxes[num].append(
                                            [row.cls, round(cnt_x, 6), round(cnt_y, 6), round(w_x, 6), round(w_y, 6)])


                            elif zone[0][0] < row.bbox[2] < zone[1][0] and zone[0][1] < row.bbox[3] < zone[1][1]:
                                # if the bottom right corner is also in the image and the upper left point is outside
                                a_x = (row.bbox[0] - zone[0][0]) / 2000 if zone[0][0] < row.bbox[0] < zone[1][0] else 0
                                a_y = (row.bbox[1] - zone[0][1]) / 2000 if zone[0][1] < row.bbox[1] < zone[1][1] else 0

                                b_x = (row.bbox[2] - zone[0][0]) / 2000
                                b_y = (row.bbox[3] - zone[0][1]) / 2000
                                cnt_x = (a_x + b_x) / 2
                                w_x = b_x - a_x
                                cnt_y = (a_y + b_y) / 2
                                w_y = b_y - a_y

                                if w_x > 0.008 and w_y > 0.008:  # skip narrow boxes
                                    boxes[num].append(
                                        [row.cls, round(cnt_x, 6), round(cnt_y, 6), round(w_x, 6), round(w_y, 6)])

                # write the new boxes to related text files
                for num, it in enumerate(boxes):
                    with open(os.path.join(output_detection_path, item[:-4] + "_" + str(num + 1) + ".txt"), "w") as f:
                        for L in it:
                            st = ""
                            for s in L:
                                st += str(s) + " "

                            f.write(st + "\n")
            else:
                print("following image has no label:", item)

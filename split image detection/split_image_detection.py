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
__copyright__ = "Copyright 2021"
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


def split_text(src_text_path:str,out_text_dir:str, zones:list,output_image_size:int)->None:
    '''
    Split text into 4 texts based on their position on the image
    :param src_text_path:
    :param out_text_dir:
    :return:
    '''

    base_name = os.path.basename(src_text_path)
    with open(src_text_path) as file:
        content = file.read().split("\n")
        df = content_to_pandas(content, im.shape)
        boxes = list()
        for i in range(len(zones)):
            boxes.append([])

        #print(boxes)
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
                                a_x = (row.bbox[0] - zone[0][0]) / output_image_size
                                b_x = (row.bbox[2] - zone[0][0]) / output_image_size
                                a_y = (row.bbox[1] - zone[0][1]) / output_image_size
                                b_y = (row.bbox[3] - zone[0][1]) / output_image_size
                                cnt_x = (a_x + b_x) / 2
                                w_x = b_x - a_x
                                cnt_y = (a_y + b_y) / 2
                                w_y = b_y - a_y
                                boxes[num].append(
                                    [row.cls, round(cnt_x, 6), round(cnt_y, 6), round(w_x, 6), round(w_y, 6)])
                            else:
                                # if the bottom right corner is outside
                                a_x = (row.bbox[0] - zone[0][0]) / output_image_size
                                a_y = (row.bbox[1] - zone[0][1]) / output_image_size

                                b_x = (row.bbox[2] - zone[0][0]) / output_image_size if zone[0][0] < row.bbox[2] < zone[1][0] else 1
                                b_y = (row.bbox[3] - zone[0][1]) / output_image_size if zone[0][1] < row.bbox[3] < zone[1][1] else 1

                                cnt_x = (a_x + b_x) / 2
                                w_x = b_x - a_x
                                cnt_y = (a_y + b_y) / 2
                                w_y = b_y - a_y
                                if w_x > 0.008 and w_y > 0.008:  # skip narrow boxes
                                    boxes[num].append(
                                        [row.cls, round(cnt_x, 6), round(cnt_y, 6), round(w_x, 6), round(w_y, 6)])


                        elif zone[0][0] < row.bbox[2] < zone[1][0] and zone[0][1] < row.bbox[3] < zone[1][1]:
                            # if the bottom right corner is also in the image and the upper left point is outside
                            a_x = (row.bbox[0] - zone[0][0]) / output_image_size if zone[0][0] < row.bbox[0] < zone[1][0] else 0
                            a_y = (row.bbox[1] - zone[0][1]) / output_image_size if zone[0][1] < row.bbox[1] < zone[1][1] else 0

                            b_x = (row.bbox[2] - zone[0][0]) / output_image_size
                            b_y = (row.bbox[3] - zone[0][1]) / output_image_size
                            cnt_x = (a_x + b_x) / 2
                            w_x = b_x - a_x
                            cnt_y = (a_y + b_y) / 2
                            w_y = b_y - a_y

                            if w_x > 0.008 and w_y > 0.008:  # skip narrow boxes
                                boxes[num].append(
                                    [row.cls, round(cnt_x, 6), round(cnt_y, 6), round(w_x, 6), round(w_y, 6)])

            # write the new boxes to related text files
            for num, it in enumerate(boxes):
                with open(os.path.join(out_text_dir, base_name[:-4] + "_" + str(num + 1) + ".txt"), "w") as f:
                    for L in it:
                        st = ""
                        for s in L:
                            st += str(s) + " "

                        f.write(st + "\n")


if __name__ == '__main__':
    # ----------------------------------------- Read and load the inputs config --------------------------------------------------
    with open(r'split_image_detection_config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    input_dir = config["input_dir"]
    src_image_path = os.path.join(input_dir,"images")
    src_detection_path = os.path.join(input_dir,"detections")
    src_original_detection_path = os.path.join(input_dir, "original_detections")

    output_dir = config["output_dir"]
    out_image_path = os.path.join(output_dir, "images")
    out_detection_path = os.path.join(output_dir, "detections")
    out_original_detection_path = os.path.join(output_dir, "original_detections")

    # Change the zones for different images
    zones_4000_8000 = [[(0, 1100), (2000, 3100)], [(2000, 1100), (4000, 3100)], [(4000, 1100), (6000, 3100)],
             [(6000, 1100), (8000, 3100)]]
    zones_2400_4800 = [[(0, 0), (2400, 2400)], [(2400, 0), (4800, 2400)]]
    zones_info = {"4000_8000":zones_4000_8000, "2400_4800":zones_2400_4800}
    output_image_size_info ={"4000_8000":2000, "2400_4800":2400}

    zones = zones_info[config["image_size"]]
    output_image_size = output_image_size_info[config["image_size"]]

    # Create folders inside output_dir
    for item in list([out_image_path, out_detection_path, out_original_detection_path]):
        try:
            os.mkdir(item)
        except OSError as error:
            print(error)


    # 1. read the image
    images = [item for item in os.listdir(src_image_path) if item.endswith(".jpg")]
    detections = [item for item in os.listdir(src_detection_path) if item.endswith(".txt")]
    original_detections = [item for item in os.listdir(src_original_detection_path) if item.endswith(".txt")]

    print("1. Number of images inside source image dir: {}".format(len(images)))
    print("2. Number of detections inside source detection dir: {}".format(len(detections)))
    print("3. Number of original detections inside source original detection dir: {}".format(len(original_detections)))
    # split images and texts into 4
    for item in tqdm.tqdm(images):
        image_name_path = os.path.join(src_image_path, item)
        detect = os.path.join(src_detection_path, item[:-3] + "txt")
        original_detect = os.path.join(src_original_detection_path, item[:-3] + "txt")
        im = cv2.imread(image_name_path)


        #split the images
        for number, part in enumerate(zones):
            start = part[0]
            end = part[1]
            temp_im = im[start[1]:end[1], start[0]:end[0]]
            cv2.imwrite(os.path.join(out_image_path, item[:-4] + "_"+str(number+1)+".jpg"), temp_im)

        # im1 = im[1100:3100, 0:2000]
        # im2 = im[1100:3100, 2000:4000]
        # im3 = im[1100:3100, 4000:6000]
        # im4 = im[1100:3100, 6000:8000]
        #
        # cv2.imwrite(os.path.join(out_image_path, item[:-4] + "_1.jpg"), im1)
        # cv2.imwrite(os.path.join(out_image_path, item[:-4] + "_2.jpg"), im2)
        # cv2.imwrite(os.path.join(out_image_path, item[:-4] + "_3.jpg"), im3)
        # cv2.imwrite(os.path.join(out_image_path, item[:-4] + "_4.jpg"), im4)

        # split texts in 4 texts and in correct positions
        split_text(detect,out_detection_path,zones,output_image_size)

        # split original texts in 4 texts and in correct positions
        split_text(original_detect, out_original_detection_path,zones,output_image_size)

import cv2
import os
import pandas as pd
import tqdm


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

def change_label(src_text_path, img_shape, out_txt):

    boxes = list()
    output_image_size = 2000
    # print(src_text_path)
    with open(src_text_path,"r") as file:

        content = file.read().split("\n")
        df = content_to_pandas(content, img_shape)
        # print(boxes)
        if len(df) > 0:

            # Get bounding boxes
            for index, row in df.iterrows():
                BOB = [row.bbox[0],row.bbox[1],row.bbox[2],row.bbox[3]]
                for jj in range(4):
                    # set every coordinate larger than 2000 to 2000
                    if BOB[jj] >2000:
                        BOB[jj] = 2000
                # Check the area if area smaller than 10 pixel drop the line
                area = (BOB[2]-BOB[0])*(BOB[3]-BOB[1])
                if area > 20 :
                    # if the bottom right corner is also in the image
                    a_x = (BOB[0]) / output_image_size
                    b_x = (BOB[2]) / output_image_size
                    a_y = (BOB[1]) / output_image_size
                    b_y = (BOB[3]) / output_image_size
                    cnt_x = (a_x + b_x) / 2
                    w_x = b_x - a_x
                    cnt_y = (a_y + b_y) / 2
                    w_y = b_y - a_y
                    boxes.append(
                        [row.cls, round(cnt_x, 6), round(cnt_y, 6), round(w_x, 6), round(w_y, 6)])


            # write the new boxes to related text files
            with open(os.path.join(out_txt, os.path.basename(src_text_path)), "w") as file:
                st = ""
                for num, it in enumerate(boxes):
                    for L in it:
                        st += str(L) + " "

                file.write(st + "\n")
        else:
            print("Warning : this image has no detection {}".format(os.path.basename(src_text_path)))

if __name__ == '__main__':
    image_dir = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/images_2048"
    detection_dir = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/labels_2048"
    output_img = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/test/images"
    output_txt = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/test/labels"
    images = [item for item in os.listdir(image_dir) if item.endswith(".jpg") or item.endswith(".png")
              or item.endswith(".jpeg")]

    print("Number of files inside this folder : {}".format(len(images)))

    sizes = {(2048,2048,3) : 0,(2000,2000,3) : 0 ,(2400,2400,3) : 0}
    problems = []
    for item in tqdm.tqdm(images):
        # try:
            img = cv2.imread(os.path.join(image_dir,item))
            if img.shape != (2000,2000,3):
                #change the lable
                try:
                    change_label(os.path.join(detection_dir,os.path.splitext(item)[0]+".txt"),img.shape,output_txt)
                except FileNotFoundError:
                    pass
                #change the image
                img = img[0:2000,0:2000]
                cv2.imwrite(os.path.join(output_img,item),img)
        # except Exception as e:
        #     print(e)
        #     problems.append(item)

    # print("all available sizes are :{}".format(sizes))
    # print("Images that have problem :{}".format(problems))

import os
import pandas as pd
import cv2
from tqdm import tqdm
import yaml
import numpy as np

def content_to_pandas(content,img_shape):
    idx = list()
    cls = list()
    conf = list()
    cnt = list()
    area = list()
    bbox = list()
    for num, line in enumerate(content):
        if len(line) > 1:
            l = line.split(" ")
            idx.append(num)
            cls.append(l[0])  # class_names[content[0]]
            cnt.append((int(float(l[1]) * img_shape[1]),int(float(l[2]) * img_shape[0])))
            area.append(int(float(l[3]) * float(l[4])* img_shape[0]* img_shape[1]))
            bbox_xstart = int(float(l[1]) * img_shape[1] - float(l[3])*img_shape[1]/2)
            bbox_ystart = int(float(l[2]) * img_shape[0] - float(l[4]) * img_shape[0] / 2)
            bb = (bbox_xstart,bbox_ystart,int(float(l[3])*img_shape[1]),int(float(l[4])*img_shape[0]))
            bbox.append(bb)

    # There is at least one object there
    if len(idx) >0 :
        dict = {"idx":idx,"cls":cls,"cnt":cnt,"area":area,"bbox":bbox}
        df= pd.DataFrame(dict)
        success =True
    else:
        df = pd.DataFrame()


    return df

def draw_label_on_image(classes_array,cls_path,cls_images,img1, row):
    # find the image related to the class
    class_name = classes_array[int(row.cls)]+".png"
    shift = 5
    if  class_name in cls_images:
        class_image = cv2.imread(os.path.join(cls_path,class_name))
        class_image = cv2.resize(class_image,(row.bbox[2],row.bbox[3]))
        #print label on the left for objects in the right
        try :
            if row.bbox[0]>img1.shape[1]/2:
                img1[row.bbox[1] :row.bbox[1]+ row.bbox[3],row.bbox[0]- row.bbox[2]-shift:row.bbox[0]-shift] = class_image
            else:
                img1[row.bbox[1] :row.bbox[1]+ row.bbox[3],row.bbox[0]+row.bbox[2]+shift:row.bbox[0]+2*row.bbox[2]+shift] = class_image
        except:
            pass


    return img1



if __name__ == '__main__':
    # //////////////////////////  Read the yaml file /////////////////////////////
    with open(r'config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    # ----------------------------------------- Read and load the inputs config --------------------------------------------------
    source_img_folder = config["images_folders"]
    labels_folder = config["detection_folder"]
    classes_path = config["classes_txt_path"]
    output_path = os.path.join(config["DIR_OUT"],"all_images")



    classes_array = np.loadtxt(classes_path,dtype=str)

    images = [item for item in os.listdir(source_img_folder) if item.endswith('.jpg')]
    txts = [item for item in os.listdir(labels_folder) if item.endswith('.txt')]


    print("Total images :{}".format(len(images)))
    print("Total texts :{}".format(len(txts)-1))


    for item in tqdm(images,desc ="In Progress"):
        # Get the image Shape:
        img = cv2.imread(source_img_folder + "/" + item)
        # check if the image has labels
        if item[:-3] + "txt" in txts:
            with open(labels_folder+"/"+item[:-3] + "txt", "r") as f:
                content = f.read().split("\n")
                df = content_to_pandas(content, img.shape)
                if len(df) > 0:
                    # Get and Draw the bboxes
                    for index, row in df.iterrows():
                        # Get color
                        if row.cls == "0":
                            color = (204,0,77)
                        elif row.cls == "1":
                            color = (204, 0, 153)
                        elif row.cls == "2":
                            color = (160, 80, 0)
                        elif row.cls == "3":
                            color = (0,0, 255)

                        img = cv2.rectangle(img, (row.bbox[0], row.bbox[1]),(row.bbox[0] + row.bbox[2], row.bbox[1] + row.bbox[3]),color, 3, cv2.LINE_4)
                else:
                    pass



        cv2.imwrite(os.path.join(output_path, item), img)



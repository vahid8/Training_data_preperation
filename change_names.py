import os
from datetime import date

def change_image_names(path,today):
    ending = ".jpg"
    files = [item for item in os.listdir(path) if item.endswith(ending)]
    for item in files:
        os.rename(path+"/"+item, path+"/"+str(today)+"_"+item)

def change_txt_names(path,today):
    ending = ".txt"
    files = [item for item in os.listdir(path) if item.endswith(ending)]
    for item in files:
        os.rename(path + "/" + item, path + "/" + str(today) + "_" + item)

if __name__ == '__main__':
    today = date.today()
    images_path = "/media/vahid/Elements/Data/yolo_face_plate_dataset/new_data_2/data"
    txt_path = "/media/vahid/Elements/Data/yolo_face_plate_dataset/new_data_2/data"

    change_image_names(images_path, today)
    change_txt_names(txt_path, today)


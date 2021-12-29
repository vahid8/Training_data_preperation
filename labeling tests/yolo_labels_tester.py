import pandas as pd
import numpy as np
import os


def check_item(coord):
    if coord < 0:
        status = "minus"
        print(coord)
        return 0, status
    elif coord > 1:
        status = "bigger than 1"
        print(coord)
        return 1, status
    else:
        status = "unchanged"
        return coord, status

if __name__ == '__main__':
    label_path = "/home/tower/Codes/Facter_RCNN_pytorch/FaceCar_detector/labels/train/"
    output_path = "/home/tower/Codes/Facter_RCNN_pytorch/FaceCar_detector/labels/train2/"
    txt_files = [item for item in os.listdir(label_path) if item.endswith(".txt")]
    for item in txt_files:
        data = list()
        with open(os.path.join(label_path,item),"r") as f:
            for line in f.readlines():
                if len(line)>1:
                    line = line.split()
                    label = int(line[0])

                    cnt_w_h = [float(item) for item in line[1:5]]
                    x1 = cnt_w_h[0] - cnt_w_h[2]
                    y1 = cnt_w_h[1] - cnt_w_h[3]
                    x2 = cnt_w_h[0] + cnt_w_h[2]
                    y2 = cnt_w_h[1] + cnt_w_h[3]
                    x1, status1 = check_item(x1)
                    x2, status2 = check_item(x2)
                    y1, status3 = check_item(y1)
                    y2, status4 = check_item(y2)

                    x_length = (x2-x1)/2
                    y_length = (y2-y1)/2
                    if x_length > 0 and y_length > 0: #length should be positive x2>x1,y2>y1
                        data.append([label, x2-x_length, y2-y_length, x_length, y_length])

        with open(os.path.join(output_path,item),"w") as new_txt_file:
            for element in data:
                to_write = str(element[0])+" "+str(round(element[1],6))+" "+str(round(element[2],6)) + " "+str(round(element[3],6))+" "+str(round(element[4], 6))+"\n"
                new_txt_file.write(to_write)




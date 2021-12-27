import os
import pandas as pd
import yaml


def Get_one_folder_statistics(txt_path,classes_txt_path,output_folder):

    txt_files = [txt_path+"/"+x for x in os.listdir(txt_path) if x.endswith(".txt")]
    print("Total Number of txt files: {}".format(len(txt_files)-1))

    # Get number of Total labels
    lb = list()
    for item in txt_files:
        if item[-11:] != "classes.txt":
            with open(item,"r") as file :
                content = file.read().split("\n")
                for x in content:
                    if len(x)>1:
                        lb.append(x)

    print("Total Number of labels are :{}".format(len(lb)))

    # Read the calsses
    with open(classes_txt_path,"r") as file:
        content = file.read().split("\n")

    labels_dic ={}
    # count number of each label
    for num in range(len(content)):
        labels_dic[num] = 0

    for item in lb:
        class_id = int(item.split(" ")[0])
        try:
            labels_dic[class_id] += 1
        except:
            print(f'new id detected {class_id}')
            labels_dic[class_id] = 1

    data =[]
    for key, value in labels_dic.items():
        data.append([content[key],key,value])

    All_labels_df = pd.DataFrame(data,columns =['Class', 'id', 'frequency'])
    Non_zero_labels_df = All_labels_df[All_labels_df['frequency']!= 0]
    Non_zero_labels_df.to_csv(os.path.join(output_folder,'statistics.csv'), index=False)

def main():
    # //////////////////////////  Read the yaml file /////////////////////////////
    with open(r'config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    # ----------------------------------------- Read and load the inputs config --------------------------------------------------
    image_path = config["images_folders"]
    txt_path = config["detection_folder"]
    classes_txt_path = config["classes_txt_path"]
    output_folder = os.path.join(config["DIR_OUT"])

    Get_one_folder_statistics(txt_path, classes_txt_path, output_folder)

if __name__ == '__main__':
    main()

import os,shutil
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import yaml
import tqdm
import multiprocessing
import numpy as np



def create_code_base_data(image_path,txt_path,classes_txt_path):

    # read all txt files
    txt_files =  [txt_path+"/"+x for x in os.listdir(txt_path) if x.endswith(".txt")]
    print("Total Number of txt files: {}".format(len(txt_files)-1))

    # Read the calsses
    with open(classes_txt_path, "r") as file:
        classes = file.read().split("\n")

    # Get number of Total labels
    lb = list()
    for item in txt_files:
        if item[-11:] != "classes.txt":
            with open(item,"r") as file :
                content = file.read().split("\n")
                for x in content:
                    if len(x)>1:
                        lb.append([os.path.join(image_path,item.split("/")[-1][:-4]+".jpg"),item.split("/")[-1][:-4],int(x.split(" ")[0]),
                                   classes[int(x.split(" ")[0])],x.split(" ")[1:]])

    print("Total Number of labels are :{}".format(len(lb)))
    df = pd.DataFrame(lb,columns=["image_path","image_name","Code","Code_name","bbox"])
    df.sort_values(by=['Code'], inplace=True)

    return df

def show_image_plt(output_folder,title: str,img_path, lable_code,lable_code_name, lable_img_name, bbox,iter):

    fig = plt.figure(figsize=(15, 10))
    plt.subplots_adjust(left=0.02, bottom=0.03, right=0.98, top=0.99, wspace=None, hspace=None)
    fig.canvas.set_window_title(title)

    image_num = 0
    image_names = []
    for i in range(min(25,len(img_path))):
        plt.subplot(5, 5, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        img = mpimg.imread(img_path[i])
        #crop image
        width = img.shape[0]
        height = img.shape[1]
        coord_bbox =list()
        for item in bbox[i][:4]:

                coord_bbox.append(int(float(item)*width))


        crp_img = img[max(coord_bbox[1]-coord_bbox[3],0):min(coord_bbox[1]+coord_bbox[3],width),
                  max(coord_bbox[0]-coord_bbox[2],0):min(coord_bbox[0]+coord_bbox[2],width)]
        try :
            plt.imshow(crp_img)
        except :
            print(img.shape)
            print(crp_img.shape)
            print(img_path[i])
            print(lable_code_name[i])
            print(bbox[i])
            print(coord_bbox)
            break
        #if images[i].shape[-1] == 3:
        #    plt.imshow(img)
        #else:
        #    plt.imshow(img, cmap='gray', vmin=0, vmax=max)

        txt = lable_code_name [i] +"("+ str(image_num)+")"
        plt.xlabel(txt)
        image_num += 1
        image_names.append([iter,image_num,lable_img_name[i]])

    #plt.show()
    plt.savefig(os.path.join(output_folder, iter+".png"))
    plt.close()
    df = pd.DataFrame(image_names, columns=["image name", "number", "original image"])
    df.to_csv(os.path.join(output_folder,"image_names.csv"), mode='a', index =False)


def plot_codes(num,output_folder,df):

    for i in tqdm.tqdm(range(0, len(df), 25),desc = "<<<<< Processing >>>>>"):
        img_path = df["image_path"].iloc[i:].tolist()
        lable_code = df["Code"].iloc[i:].tolist()
        lable_code_name = df["Code_name"].iloc[i:].tolist()
        lable_img_name = df["image_name"].iloc[i:].tolist()
        bbox = df["bbox"].iloc[i:].tolist()
        show_image_plt(output_folder, "Codes", img_path, lable_code, lable_code_name, lable_img_name, bbox, iter=str(num)+"_"+str(i))



def main():
    # //////////////////////////  Read the yaml file /////////////////////////////
    with open(r'config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    # ----------------------------------------- Read and load the inputs config --------------------------------------------------
    image_path = config["images_folders"]
    txt_path = config["detection_folder"]
    classes_txt_path = config["classes_txt_path"]
    output_folder = os.path.join(config["DIR_OUT"],"all_labels")

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)  # delete output folder
    os.makedirs(output_folder)  # make new output folder

    cores = config["cores"]
    # 1. Create a panda dataframe with name of txt(image) | code | bbox
    df = create_code_base_data(image_path,txt_path,classes_txt_path)

    #2. divide df to list dfs with 25 rows
    # cores = 1
    # df_lists = np.array_split(df, cores)

    plot_codes(0,output_folder,df)
    # print("dividing {} labels into {} cores -> Creating {} image per core and total {} images".format(len(df),cores,int(len(df)/(cores*25)),int(len(df)/25)))
    # jobs = []
    # for i in range(cores):
    #     p = multiprocessing.Process(target=plot_codes, args=(i,output_folder,df_lists[i],))
    #     jobs.append(p)
    #     p.start()
    #
    # # Make sure that process are closed
    # for i in range(cores):
    #     jobs[i].join()

if __name__ == '__main__':
    main()


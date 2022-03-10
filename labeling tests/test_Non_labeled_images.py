import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tqdm
import yaml

def show_image_plt(output_folder,title: str,img_path, iter):

    fig = plt.figure(figsize=(15, 10))
    plt.subplots_adjust(left=0.02, bottom=0.03, right=0.98, top=0.99, wspace=None, hspace=None)
    fig.canvas.set_window_title(title)

    for i in range(min(4,len(img_path))):
        plt.subplot(2, 2, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        img = mpimg.imread(img_path[i])
        plt.imshow(img)
        #if images[i].shape[-1] == 3:
        #    plt.imshow(img)
        #else:
        #    plt.imshow(img, cmap='gray', vmin=0, vmax=max)
        txt = img_path[i].split("/")[-1][:-4]
        plt.xlabel(txt)

    #plt.show()
    plt.savefig(os.path.join(output_folder,iter+".png"))
    plt.close()

def main():

    # //////////////////////////  Read the yaml file /////////////////////////////
    with open(r'config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    # ----------------------------------------- Read and load the inputs config --------------------------------------------------
    image_folders = config["images_folders"]
    txt_folders = config["detection_folder"]
    output_folder = os.path.join(config["DIR_OUT"], "no_label")

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)  # delete output folder
    os.makedirs(output_folder)  # make new output folder

    images_without_label = True #False

    # find all txt files
    txt_files =  [x[:-4] for x in os.listdir(txt_folders) if x.endswith(".txt")]
    # find image files
    img_files =  [x[:-4] for x in os.listdir(image_folders) if x.endswith(".jpg")]

    txt_files.sort()
    img_files.sort()

    print("Total images :{}".format(len(img_files)))
    print("Total txts :{}".format(len(txt_files)))
    # find images without txt files
    only_images = list()
    only_images_names = list()
    for item in img_files:
        if item not in txt_files:
            only_images.append(os.path.join(image_folders,item+".jpg"))
            only_images_names.append(item+".jpg")

    print("Total {} images without label:".format(len(only_images_names)))
    for item in only_images_names:
        print(item)

    print("///////////////////////\n///////////////////////")
    only_txt_names = list()
    for item in txt_files:
        if item not in img_files:
            #only_images.append(folder_path+"/"+item+".jpg")
            only_txt_names.append(item+".txt")

    print("Total {} txts without image:".format(len(only_txt_names)))
    for item in only_txt_names:
        print(item)

    if images_without_label:
        for i in tqdm.tqdm(range(int(len(only_images)/4)), desc="<<<<< Processing >>>>>"):
            img_path = only_images[4*i:min(4*(i+1),len(only_images))]
            show_image_plt(output_folder, "Images with no label", img_path,iter=str(i))


    # move them to a new folder
    for image,name in zip(only_images,only_images_names):
       shutil.move(image, os.path.join(output_folder, name))

if __name__ == '__main__':
    main()
import matplotlib.pyplot as plt
import os
import re
import matplotlib.image as mpimg

def Get_image_class_path(directory:str):
    # Find avilable Folders (Classes)  with the name
    folders = [x[0] for x in os.walk(directory)]
    folder_names = [item.split('/')[-1] for item in folders if len(item.split('/')[-1])>0 ]
    folder_names.sort()
    print("Total number of {} folders (classes) found".format(len(folder_names)))
    # prepare first image path
    images_path = list()

    for item in folder_names:
        path = directory+item + "/00000.ppm"
        images_path.append(path)


    labels = list([i for i in range(len(folder_names))])

    return images_path,labels



def show_image_plt(title: str, images, labels):
    fig = plt.figure(figsize=(10, 10))
    plt.subplots_adjust(left=0.02, bottom=0.03, right=0.98, top=0.99, wspace=None, hspace=None)
    fig.canvas.set_window_title(title)

    for i in range(min(9*14,len(images))):
        plt.subplot(9, 14, i + 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        img = mpimg.imread(images[i])
        plt.imshow(img)

        #if images[i].shape[-1] == 3:
        #    plt.imshow(img)
        #else:
        #    plt.imshow(img, cmap='gray', vmin=0, vmax=max)

        txt = labels[i]
        plt.xlabel(txt)

    plt.show()

if __name__ == '__main__':
    directory = "/home/vahid/Development/python/Projects/TrafficSign/german signals/"
    labels = [x[:-4] for x in os.listdir(directory) if x.endswith('.png')]
    # split data base on length of name
    lb1,lb2 =list(),list()
    for item in labels:
        dd = item .split("-")[0]
        dd = dd.split(".")[0]
        if len(dd) == 4:
            lb1.append(item)
        else :
            lb2.append(item)
    lb1.sort()
    lb2.sort()
    lb1 .extend(lb2)


    images_path = list(map(lambda x: directory+ x+".png",lb1))


    print("Total images :{}".format(len(images_path)))
    for i in range(0,len(images_path),9*14):
        print(i)
        img_path = images_path[i:]
        lable =  lb1[i:]
        show_image_plt("Classes Preview", img_path, lable)
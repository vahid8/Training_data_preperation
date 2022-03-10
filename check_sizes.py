import cv2
import os,shutil
import tqdm

if __name__ == '__main__':
    image_dir = "/media/vahid/Elements/Data/intenistat/test"

    sizes = dict()

    images = [item for item in os.listdir(image_dir)]
    print("Number of files inside this folder : {}".format(len(images)))


    problems = []
    for item in tqdm.tqdm(images):
        try:
            img = cv2.imread(os.path.join(image_dir,item))
            if img.shape in sizes.keys():
                sizes[img.shape] += 1
            else:
                sizes[img.shape] = 0
        except:
            problems.append(item)

    print(f"all available sizes are :{sizes}")
    if len(problems)>0:
        print("--"*10)
        print("Images that have problem :")
        for item in problems:
            print(item)
    # print(sizes[])

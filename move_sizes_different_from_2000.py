import cv2
import os,shutil
import tqdm

if __name__ == '__main__':
    image_dir = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/images"
    detection_dir = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/labels"

    output_img = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/images_2048"
    output_txt = "/media/vahid/Elements/Data/GE_signs_training_data/Traffic_sign_GE/labels_2048"

    images = [item for item in os.listdir(image_dir)]
    print("Number of files inside this folder : {}".format(len(images)))

    sizes = {(2048,2048,3) : 0,(2000,2000,3) : 0 ,(2400,2400,3) : 0}
    problems = []
    for item in tqdm.tqdm(images):
        try:
            img = cv2.imread(os.path.join(image_dir,item))
            sizes[img.shape]+=1

            if img.shape != (2000,2000,3):
                shutil.move(os.path.join(image_dir,item), output_img)
                shutil.move(os.path.join(detection_dir,  os.path.splitext(item)[0]+".txt"), output_txt)
        except:
            problems.append(item)

    print("all available sizes are :{}".format(sizes))
    print("Images that have problem :{}".format(problems))

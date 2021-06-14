# Training_data_preperation
All handy scripts related to training data preperation and labeling. Deciption of functions:
#### 1. split_image_detection.py: The purpose of this script is to split images and already detected boxes into smaller pieces ready for training with yolo
```More description:
Get the images and detection texts and divide images to smaller parts
input image : Trimble MX9 Panorama 8000*400 ->image_A.jpg
output images : 4 images in 2000*2000 ->image_A_1.jpg,image_A_2.jpg, image_A_3.jpg, image_A_4.jpg
                im1 = im[1100:3100, 0:2000]
                im2 = im[1100:3100, 2000:4000]
                im3 = im[1100:3100, 4000:6000]
                im4 = im[1100:3100, 6000:8000]
input_texts : detection in the original image dimensions
output_texts :  detections on new image formats
```
#### 2. Compare textfiles.py: check if two detction texts are the same or not in case of changed file, it copies both text and image to output folder
```More description:
Get the detection texts paths (edited and original ones) and compare the content
input : edited and original texts dir paths, splitted image dir paths
output : text ones that are changed (means the model labeling was not ok) and its related images from seperated image dir
```

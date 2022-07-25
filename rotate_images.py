import os
import cv2


if __name__ == '__main__':

    images_path = "/media/vahid/Elements/Softwaress/Training_data_preperation/test/img_in"
    out_path = "/media/vahid/Elements/Softwaress/Training_data_preperation/test/im_out"
    imgs = [item for item in os.listdir(images_path) if item.endswith(".jpg")]

    for item in imgs:
        image = cv2.imread(os.path.join(images_path, item))
        image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        cv2.imwrite(os.path.join(out_path, item), image)


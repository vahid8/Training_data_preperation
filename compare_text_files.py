import os
import filecmp
import shutil
import tqdm

edited_text_path = "/media/dev2/A/improvements/improvements_splitted/Stadt Essen_2021_2/detections"
original_text_path = "/media/dev2/A/improvements/improvements_splitted/Stadt Essen_2021_2/original_detections"

splitted_images_path = "/media/dev2/A/improvements/improvements_splitted/Stadt Essen_2021_2/images"

output_images_dir = "/media/dev2/A/improvements/improvements_splitted/Stadt Essen_2021_2/final/images"
output_detection_dir = "/media/dev2/A/improvements/improvements_splitted/Stadt Essen_2021_2/final/detections"

editedt_files = [item for item in os.listdir(edited_text_path)]
original_files = [item for item in os.listdir(original_text_path)]

changed_files=list()
for item in editedt_files:
    if item not in original_files:
        # it is 100% new label
        changed_files.append(item)
    else:
        if not filecmp.cmp(os.path.join(edited_text_path,item), os.path.join(original_text_path,item)):
            changed_files.append(item)


print("number of all text files: ",len(editedt_files))
print("number of edited files: ",len(changed_files))
for item in tqdm.tqdm(changed_files):
    shutil.copy(os.path.join(edited_text_path,item), output_detection_dir)
    shutil.copy(os.path.join(splitted_images_path, item[:-3]+"jpg"), output_images_dir)



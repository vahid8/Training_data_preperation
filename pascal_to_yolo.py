import os, shutil
import xml.etree.ElementTree as ET

def read_xml(path):
    tree = ET.parse(path)
    return tree.getroot()


def convert_coord(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_label(xml_path, classes):
    xml_object = read_xml(xml_path)
    size = xml_object.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    labels = list()
    for obj in xml_object.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes:
            classes.append(cls)
            print(f"warning : new class detected---> {cls}")

        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert_coord((w,h), b)
        labels.append(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

    return labels
        # return bb
        # out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

if __name__ == '__main__':
    folder_path = "/media/vahid/Elements/Data_Essen/KI_Trainingsdaten/Intensitaet/test"
    out_dir =  "/media/vahid/Elements/Data_Essen/KI_Trainingsdaten/Intensitaet/test_yolo"
    files = [item for item in os.listdir(folder_path) if item.endswith(".xml")]
    # classes = ['einzelriss', 'flickstelle_aufgelegt', 'sinkkasten', 'schachtdeckel_rund', 'netzriss', 'ausbruch',
    #            'risshaeufung', 'unterflurschieber_klein', 'unterflurschieber_gross']
    classes = ['fahrstreifenbegrenzung', 'furtmarkierung_fussgaenger', 'furtmarkierung_rad', 'pfeil_g', 'haltelinie', 'unterflurschieber_gross', 'unterflurschieber_klein', 'piktogramm_fahrrad', 'fahrstreifenbegrenzung_kreuzung', 'schachtdeckel_eckig', 'schachtdeckel_rund', 'sinkkasten', 'begrenzungslinie', 'buchstabe_b', 'buchstabe_u', 'pfeil_g_r', 'fahrstreifenbegrenzung_lang', 'pfeil_g_l', 'pfeil_r', 'pfeil_l', 'buchstabe_s', 'pfeil_vorankuendigung_r', 'wartelinie', 'fussgaenger_ueberweg', 'pfeil_g_l_r', 'pfeil_l_r', 'pfeil_vorankuendigung_l']


    for item in files:
        new_labels = convert_label(os.path.join(folder_path,item), classes)
        with open(os.path.join(out_dir, ".".join(item.split(".")[:-1])+".txt"), "w") as out_file:
            for line in new_labels:
                out_file.write(line)

    for item in classes:
        print(item)

    images = [item for item in os.listdir(folder_path) if item.endswith(".jpg")]
    for item in images:
        shutil.copy(os.path.join(folder_path,item), os.path.join(out_dir, item))

    print(classes)

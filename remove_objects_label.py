#!/usr/bin/env python
""" Get the detection texts and remove labels you dont want to be present anymore there
    input : Texts with full labels
    output : Texts with just arbitrary labels rearranged from 0
"""

import os

__author__ = "vahid jani"
__copyright__ = "Copyright 2021"
__credits__ = ["Vahid jani"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Vahid jani"
__email__ = "aghajanivahid1@gmail.com"
__status__ = "Development"


if __name__ == '__main__':
    # Define input and output dir paths
    detections_input_dir = "/media/vahid/Elements/Softwaress/Flask_blurring/project/static/uploads/vahid/person/detections"
    detections_output_dir = "/media/vahid/Elements/Softwaress/Flask_blurring/project/static/uploads/vahid/person/detections2"

    detections = [os.path.join(detections_input_dir, item) for item in os.listdir(detections_input_dir) if item.endswith(".txt")]

    for detect in detections:
        with open(detect) as file:
            # read the text file
            content = file.read().split("\n")
            new_lines = list()
            if len(content)>0:  # if the file is not empty
                for line in content:
                    if len(line) > 0:  # if line has some content is not just one space
                        # only get label 1(plate) and 3(face) and skip labels 0 (car), 2(person)
                        if int(line[0]) == 1:  # if the label is 1(plate) change it to 0
                            new_lines.append("0"+line[1:])
                        elif int(line[0]) == 3:  # if the label is 3(face) change it to 1
                            new_lines.append("1"+line[1:])

            if len(new_lines) > 0:  # if there is something to write to text files
                # write the new texts to related text files
                with open(os.path.join(detections_output_dir, os.path.basename(detect)), "w") as f:
                    for L in new_lines:
                        f.write(L + "\n")





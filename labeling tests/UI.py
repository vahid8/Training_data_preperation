# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 15:19:08 2019

@author: vaghajan
"""

import print_codes_testing,test_Non_labeled_images,Yolo_visualizer, labeling_statistics
from tkinter.filedialog import askdirectory, askopenfilename
import tkinter, os
import tkinter.ttk as tk
from tkinter import ttk


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master = master
        self.master.title('Testing Tool')  # Title of window
        #self.master.geometry('400x250')

        self.tab_parent = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tab_parent)

        self.tab_parent.add(self.tab1, text="Main")
        self.tab_parent.pack(fill='both')
        self.create_frames()


    def create_frames(self):
        labelframe2 = tkinter.LabelFrame(self.tab1, text="Operation")
        labelframe2.pack(fill=tkinter.X, pady=5)
        self.create_widgets_frame_2(labelframe2)

    def create_widgets_frame_2(self, frame):

        # bt    ..... 1
        b100 = tkinter.Button(frame, text='Yolo visualizer', bg="gray80")
        b100.pack(fill=tkinter.X, pady=0.2)
        b100["command"] = self.yolo_visualizer

        # bt    ..... 2
        b101 = tkinter.Button(frame, text='print all labels', bg="gray80")
        b101.pack(fill=tkinter.X, pady=0.2)
        b101["command"] = self.all_labels

        # bt    ..... 1
        b102 = tkinter.Button(frame, text='Images without label', bg="gray80")
        b102.pack(fill=tkinter.X, pady=0.2)
        b102["command"] = self.no_label

        # # bt    ..... 2
        b103 = tkinter.Button(frame, text='labeling_statistics', bg="gray80")
        b103.pack(fill=tkinter.X, pady=0.2)
        b103["command"] = self.labeling_statistics

    def yolo_visualizer(self):
        Yolo_visualizer.main()

    def all_labels(self):
        print_codes_testing.main()

    def no_label(self):
        test_Non_labeled_images.main()

    def labeling_statistics(self):
        labeling_statistics.main()


root = tkinter.Tk()
app = Application(master=root)
app.mainloop()

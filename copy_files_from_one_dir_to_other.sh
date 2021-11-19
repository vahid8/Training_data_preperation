#!/bin/bash        
input_dir="/media/vahid/Elements/Data/blurring_training_data/series1_1/detections"
output_dir="/media/vahid/Elements/Data/blurring_training_data//labels"
echo 1.Input dir: $input_dir
echo 2.Number of files inside input dir : $(ls $input_dir | wc -l)

echo 3.output dir: $output_dir
echo 4.Number of files inside output dir : $(ls $output_dir | wc -l)


echo Coping file from src to dst ....
cp -a $input_dir/. $output_dir

echo 5.Number of files inside output dir after copy : $(ls $output_dir | wc -l)

#!/bin/bash
mkdir input
mv we* input

rm -r ~/output/*
mkdir ~/output

cd ~/openpose

for filename_ext in "$search_dir"~/input/*
do
  filename=${filename_ext:8:4}
  echo ${filename}
	mkdir ~/output/${filename}
	
	./build/examples/openpose/openpose.bin \
	--video ~/input/${filename}.mp4 \
	--write_json ~/output/${filename}/ \
	--write_video ~/output/${filename}/res.avi \
	--number_people_max 1 \
	--display 0 \
	--logging_level 3

done

cd ~/
tar cf  ~/res.tar "output"



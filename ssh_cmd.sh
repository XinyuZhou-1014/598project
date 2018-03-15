rm -r ~/output/*

cd openpose
for filename in "we_1" "we_2" "we_3" "we_4" "we_5"
do
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
tar cf  ~/res.tar "~/output/"



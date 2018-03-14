#!/bin/bash

if [ -z "$1" ]; then
	echo "Please provide an image"
	exit 1
fi

if [ ! -r "$1" ]; then
	echo "Unable to read file $1"
	exit 1
fi

python usercode

title=$(cut -d'.' -f1 <<< "$1")
new_image=$title-annotated.bmp

echo "Converting from JPG to BMP file"
convert $1 -fill black -gravity Southwest -pointsize 30 -resize 'x320' $new_image

echo "Finding dimensions of image"

W=$(identify -format '%w' $new_image) #width

fourth=$((W/4))
half=$((W/2))
threefourths=$((3*W/4))

echo "Annotating Image"
mogrify\
	-fill white \
	-gravity Southwest \
	-pointsize 30 \
	-annotate +0+0 'North' \
	-annotate +$fourth+0 'East' \
	-annotate +$half+0 'South' \
	-annotate +$threefourths+0 'West'\
	$new_image

# mogrify \
# 	-fill white \
# 	-gravity Northwest \
# 	-pointsize 30 \
# 	-type truecolor \
# 	-annotate +$((W*X/36))+0 '|' \
#	$new_image	

ten_deg_px=$((W/36))
for i in $(seq 0 36); do
	px_pos=$((i*ten_deg_px))
	mogrify\
		-fill white \
		-gravity Northwest \
		-pointsize 30 \
		-type truecolor \
		-annotate +$px_pos+0 '|' \
		-pointsize 15 \
		-annotate +$((px_pos-20))+30 $((i*10)) \
		$new_image 
done

xdg-open $new_image

exit 

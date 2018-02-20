#!/bin/bash

echo "Converting from JPG to BMP file"
convert panorama.jpg -fill black -gravity Southwest -pointsize 30 -resize 'x320' panorama.bmp

echo "Finding dimensions of image"

W=$(identify -format '%w' panorama.bmp) #width

fourth=$((W/4))
half=$((W/2))
threefourths=$((3*W/4))


echo "Annotating Image"
convert panorama.bmp -fill white -gravity Southwest -pointsize 30 -annotate +0+0 'North' -annotate +$fourth+0 'East' -annotate +$half+0 'South' -annotate +$threefourths+0 'West' panorama-ann.bmp   


convert panorama-ann.bmp -fill white -gravity Northwest -pointsize 30 -type truecolor -annotate +$((W*X/36))+0 '|' degreeoutput.bmp

X=1

while [ $((W*X/36)) -lt $W ];
do
	convert degreeoutput.bmp -fill white -gravity Northwest -pointsize 30 -type truecolor -annotate +$((W*X/36))+0 '|' degreeoutput.bmp
	let X=$X+1
done

convert degreeoutput.bmp +flip -rotate 90 -type truecolor -gravity Southwest rotate.bmp

COUNTER=0

while [ $((480*$COUNTER)) -lt  $W ];
do
	convert rotate.bmp -crop 320x480+0+$((480*$COUNTER)) -type truecolor crop$COUNTER.bmp
	let COUNTER=$COUNTER+1
done

xdg-open rotate.bmp

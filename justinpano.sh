#!/bin/bash
#echo "Converting into panorama"
#convert img*.jpg +append panorama.jpg

python usercode.py

i=0
k=-30
#dec="5.4"
while [ $i -lt 10 ]; do
        old_image=img$((i+1)).jpg
        #new_image=annotated$((i+1)).bmp

        #echo "Converting Image"$((i+1))" from JPG to BMP file"
        mogrify $old_image -fill black -gravity Southwest -pointsize 30 -resize 'x320'

        echo "Finding dimensions of image"

        W=$(identify -format '%w' $old_image) #width

        fourth=$((W/4))
        half=$((W/2))
        threefourths=$((3*W/4))

        echo "Annotating Image"
        if [ $i -eq 0 ]; then
        mogrify\
                -fill white \
                -gravity Southwest \
                -pointsize 30 \
                -annotate +$((half-50))+0 'North' \
                $old_image
        #elif [ $i -eq 1 ]; then
        #k=$((k-10))
        elif [ $i -eq 2 ]; then
        mogrify\
                -fill white \
                -gravity Southwest \
                -pointsize 30 \
                -annotate +$((fourth+140))+0 'East' \
                $old_image
        #k=$((k+10))
        #elif [ $i -eq 3 ]
	elif [ $i -eq 5 ]; then
		mogrify\
		-fill white \
                -gravity Southwest \
                -pointsize 30 \
                -annotate +$((fourth+140))+0 'South' \
                $old_image
        elif [ $i -eq 5 ]; then
        mogrify\
                -fill white \
                -gravity Southwest \			-pointsize 30 \
                -annotate +$((half+190))+0 'West'\
                $old_image
        fi

        ten_deg_px=$((W/5))
        for j in $(seq 0 5); do
                px_pos=$((j*ten_deg_px))
                m=$(((j*10)+k))
                while [ $m -lt 0 ]; do
                        m=$((m+360)); done
                while [ $m -gt 360 ]; do
                        m=$((m-360)); done
                mogrify\
					-fill white \
					-gravity Northwest \
					-pointsize 30 \
					-type truecolor \
					-annotate +$((px_pos-a))+0 '|' \
					-pointsize 15 \
					-annotate +$((px_pos-b))+30 $m \
					$old_image
        done
        if [ $i -eq 7 ]; then
                echo "Cropping Image"$((i+1))
                mogrify $old_image -crop 20%x+0
        fi
        i=$((i+1))
        k=$((k+50))
done

echo "Converting into panorama"
convert img*.jpg +append panorama.bmp

#mogrify -resize x900\! panorama.bmp
#xdg-open panorama.bmp

../BMPtoFramebuffer/bmpread panorama.bmp /dev/fb1

exit

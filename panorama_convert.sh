#!/bin/bash

python usercode.py

convert img*.jpg +append -resize 'x320' panorama.bmp
mogrify -flip panorama.bmp

../BMPtoFramebuffer/bmpread panorama.bmp /dev/fb1

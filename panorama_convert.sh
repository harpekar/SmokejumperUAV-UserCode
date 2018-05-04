python usercode.py

convert img*.jpg +append panorama.bmp
mogrify -flip panorama.bmp

../BMPtoFramebuffer/bmpread panorama.bmp /dev/fb1

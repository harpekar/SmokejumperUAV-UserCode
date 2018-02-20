# SmokejumperUAV-UserCode

This repository contains the code to operate the User Interface on the UAV for Smokejumpers ECE Senior Design project. The UI code block takes in pictures from the Camera and runs them through a Stitching algorithm in the OpenCV code base, then preps this new panorama for display by converting it to truecolor BMP, writing heading data over it, and then cropping it at the necessary increments to display well on the ILI9486 3.5" TFT Screen.    

The Dependencies of this code are as follows: 
- imagemagick

Contained in this repository are: 
- panorama.sh: Bash script that takes in a jpg panorama image, scales it for a 320 pixel tall display, overlays heading data onto it (one notch every 10 degrees), converts it to truecolor BMP, and crops it to prepare it for display on the TFT display. 
- panorama.jpg: Provided example panorama for testing

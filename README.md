# RaspberryPi-HomeSecuritySystem
Motion-Detection-OpenCV

A DIY Raspberry Pi security system that utilizes a motion detection algorithm using OpenCV, and notifies the user on WhatsApp via the Twilio and Imgur api's.

Created for @BitnPi

Libraries needed:

OpenCV (2.0 + )
Numpy
PiCamera
Twilio
Pyimgur
Installation:

On a fresh install on the Pi, you're going to need to download all the essential libraries and fundamentals.

sudo apt update sudo apt upgrade

Then if you're using Raspbian, you can simply download OpenCV from the Raspbian repositories, via:

sudo apt install python'x'-opencv

where 'x' is the python version you have insalled.

However, if you are on any other OS, you will need to install OpenCV from the source, or their repository, in which we recommend following a guide such as this one: https://pimylifeup.com/raspberry-pi-opencv/.

Then for PiCamera:

Raspbian: sudo apt-get install python-picamera python3-picamera

Other OS: sudo pip install picamera

Twilio:

Raspbian: sudo apt install twilio

Other OS: pip install twilio

PyImgur:

Raspbian: sudo apt install pyimgur

Other OS: pip install pyimgur

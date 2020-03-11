import cv2
import json, requests, os, random
import time
from PIL import Image, ImageDraw
import requests
import subprocess
import numpy as np
from picamera import PiCamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 20
GPIO_ECHO = 21

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

camera = PiCamera()

    
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

while True:
        
    dist = distance()
    print ("Measured Distance = %.1f cm" % dist)
    time.sleep(1)

    if dist < 10:
        print("captured")

        camera.start_preview()
        time.sleep(5)
        camera.capture('/home/pi/Desktop/objectdetection/in12.JPG')
        camera.stop_preview()

        #camera = cv2.VideoCapture(0)
        #for i in range(4):
        #    return_value, image = camera.read()
        #    j = cv2.imwrite(str(i)+'.JPG', image)
        #    cv2.imshow('Input Image',j);
        #del(camera)

        url = 'https://app.nanonets.com/api/v2/ImageCategorization/LabelFile/'

        data = {'file': open('/home/pi/Desktop/objectdetection/in.JPG', 'rb'), 'modelId': ('', '336e0c53-829b-4359-af00-9394ccfb1ed8')}

        response = requests.post(url, auth= requests.auth.HTTPBasicAuth('zTAH0vW5TbLuFKa_FY_OFVO1IWx9RkGH', ''), files=data)

        print(response.text)

        s=str(response.text)
        f=open('data1.txt','w')
        f.write(s)
        f.close()

        subprocess.call('sudo festival --tts data1.txt', shell=True)

    #draw boxes on the image
    #response = json.loads(response.text)
    #im = Image.open("/home/pi/Desktop/objectdetection/in.JPG")
    #draw = ImageDraw.Draw(im, mode="RGBA")
    #prediction = response["result"][0]["prediction"]

    else:
        print("waiting for captured")



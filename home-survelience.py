import RPi.GPIO as GPIO
from time import sleep
#import to convert image to binary format
import base64
#import for pushbullet
import os
#imports for google drive uploads
import json
import requests
#import for mysql database
import pymysql
#import for capturing image
from picamera import PiCamera  
camera=PiCamera()
camera.resolution=(640,480) #setting reolution of picture which we will take

GPIO.setmode(GPIO.BOARD) # use always BCM header when using RELAY module
GPIO.setwarnings(False)
GPIO.setup(3,GPIO.IN) # PIR Motion sensor
#GPIO.setup(5,GPIO.OUT) # Connect 220 bulb via RELAY module 
a=0
while True:
    # turining bulb off if it remains open from the previous one
    #GPIO.output(5,0)
    i=GPIO.input(3)  #getting value of motion sensor either 1 when motion detcted or 0 when
                      # not detected any motion    
    if i==1:
        a=a+1
        #capturing image of detection
        camera.capture('/home/pi/home_servelience_project/motion images/detected{}.png'.format(a))
        #GPIO.output(5,1)
        print('intruder detected')
        sleep(5)
        
        
        
        # pushing notification on mobile if mobile is connected using pushbullet
        os.system('/home/pi/home_servelience_project/pushbullet.sh "Alert Motion Detected"')
        
        
        
        # uploading image to google drive i.e. (emmadsiddiqui6@gmai.com)
        #after bearer provide access token of google drive api from google api playground
        headers = {"Authorization": "Bearer ya29.a0ARrdaM-kjRMKM-2fJI3budzUuiO0KN-01kqlL_w5jOSGCu3vN9lIDTPyY2_X3B082U4yJtiTz3uag5u_dAd5qMo8w5DUmde7ej1K62VWl416C5Bu--ub5C2LPXVrJCC1ATsIM1h7o9zBRqkVpVFRh9qJBzHq "}
        para = {"name": "motion_detected{}".format(a),          #in name provide name to be
                "parents":["1JpsWUM7GYgOIyNYeMl6Bsrt-CpChX7l3"]} #in parents provide link of folder if any
        files = {'data': ('metadata', json.dumps(para),
                          'application/json; charset=UTF-8'),
                          'file': open("/home/pi/home_servelience_project/motion images/detected{}.png".format(a), "rb")}
        r = requests.post("https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
                          headers=headers,files=files)
        print(r.text)
        
        
        
        # converting image to base64 in binary format
        with open("/home/pi/home_servelience_project/motion images/detected{}.png".format(a),"rb") as imagefile:
            byteform=base64.b64encode(imagefile.read())   #encoding it to byteform 
        f=open('/home/pi/home_servelience_project/motion images encoded/encodedimage{}.bin'.format(a),'wb')  #opening a new binary file where we will store our image byteform we converted earlier
        f.write(byteform) #writing byteform in file name output.bin
        f.close()
        
        # uploading image to database via converted into base64 and save it as binary file i.e .bin
        
        db = pymysql.connect(
            host="localhost",
            user="anas",
            passwd="emad123",
            database="record1"
        )
        mycursor = db.cursor()
        insertQuery = "INSERT INTO test(customer) VALUES ('/home/pi/home_servelience_project/motion images encoded/encodedimage{}.bin');".format(a)
        mycursor.execute(insertQuery)
        print("No of Record Inserted :", mycursor.rowcount)
        print("Inserted Id :", mycursor.lastrowid)
        db.commit()
        db.close()
                

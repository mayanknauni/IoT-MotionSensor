###############################################################
# Designed and Maintained by Mayank Nauni                     # 
#                                                             #
#     Raspberry Pi Sending Data to IoT Core                   # 
#                                                             #
#     All rights reserved.                                    # 
#     Revision history:                                       #  
#     29 Aug 2022 |  1.0 - initial release                    #   
###############################################################   

import RPi.GPIO as GPIO
from datetime import datetime

global message
import requests
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

ledPin = 12       # define ledPin
sensorPin = 11    # define sensorPin

myMQTTClient = AWSIoTMQTTClient("ClientID")
myMQTTClient.configureEndpoint("aa53ilkz42xlh-ats.iot.ap-southeast-1.amazonaws.com", 8883)

myMQTTClient.configureCredentials("/home/admin/pi-projects/AmazonRootCA1.pem", "/home/admin/pi-projects/a949e525556b9d6d349771827ab0e3fafd8961c2cb5c88ea766d6887f8cb8fbc-private.pem.key", "/home/admin/pi-projects/a949e525556b9d6d349771827ab0e3fafd8961c2cb5c88ea766d6887f8cb8fbc-certificate.pem.crt")
 
print ('Initiating Realtime Data Transfer From Raspberry Pi...')

Myvar = myMQTTClient.connect()

date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
print (f"Timestamp:{date}")

def setup():
    GPIO.setmode(GPIO.BOARD)        # use PHYSICAL GPIO Numbering
    GPIO.setup(ledPin, GPIO.OUT)    # set ledPin to OUTPUT mode
    GPIO.setup(sensorPin, GPIO.IN)  # set sensorPin to INPUT mode

def loop():
    while True:
        if GPIO.input(sensorPin)==GPIO.HIGH:
            GPIO.output(ledPin,GPIO.HIGH) # turn on led
            print ('Motion Detected >>>')
            message = 'Motion Detected'
            myMQTTClient.publish("topic/motionsensor", "{\"MotionMessage\":\""+ message + "\", \"Timestamp\" :\""+ str(date)+ "\"}", 0)
        else :
            GPIO.output(ledPin,GPIO.LOW) # turn off led
            print ('No Motion >>>')
            message = 'No Motion'
            myMQTTClient.publish("topic/motionsensor", "{\"MotionMessage\":\""+ message + "\", \"Timestamp\" :\""+ str(date)+ "\"}", 0)

def destroy():
    GPIO.cleanup()                     # Release GPIO resource

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()

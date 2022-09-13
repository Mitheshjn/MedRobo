import cv2
import numpy as np
import pyzbar.pyzbar as qr
from PIL import Image
from gpiozero import Servo
import RPi.GPIO as GPIO
import pigpio
import time
from time import sleep
"""
#====== in terminal type "sudo pigpiod" before running this !========
#======servo=Servo(17)
servo = 17 
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
#======servo.min()
"""

cap=cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

while True:
  ret,frame = cap.read()
  #flipped = cv2.flip(frame, flipCode=2)
  frame1=cv2.resize(frame,(640,480))
  qrdetect=qr.decode(frame1)
  #======print(qrdetect)
  #======print(qrdetect[0].data.decode("ascii"))
  for i in qrdetect:
    #print (i.rect.left,i.rect.top,i.rect.width,i.rect.height)
    #print(i.data[0])
    if (i.data[0]==104 and i.data[1]==101 and i.data[2]==108 and i.data[3]==108 and i.data[4]==111):
      print("yess")
      print( "0 deg" )
      #time.sleep( 3 )
      #servo.mid()
      sleep(0.5)
      continue
              
    if(i.data[0]==104 and i.data[1]==105):
      print("no")
      print( "180 deg" )
      #pwm.set_servo_pulsewidth( servo, 2500 ) 
      #time.sleep( 3 )
      #servo.max()
      sleep(0.5)
      continue

    cv2.rectangle(frame1,(i.rect.left,i.rect.top),(i.rect.left+i.rect.width,i.rect.top+i.rect.height),(0,255,0),3)
    cv2.putText(frame1,str(i.data),(20,20),font,2,(255,0,0),2) 
  cv2.imshow("Frame", frame1)
  key = cv2.waitKey(1) & 0xFF
  if key == ord("q"):
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
    break



"""
img=Image.open("./New/hello.png")
out=qr.decode(img)
for i in out:
  print(i.data)
  #if(i.data[0]==104 and i.data[1]==101 and i.data[2]==108 and i.data[3]==108 and i.data[4]==111):
  #  print("yess")
"""
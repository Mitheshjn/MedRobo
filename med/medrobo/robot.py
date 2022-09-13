import cv2
import numpy as np
import pyzbar.pyzbar as qr
from PIL import Image
import gpiozero
from gpiozero import Servo
import RPi.GPIO as GPIO
import pigpio
import time
from time import sleep

TRIG=23
ECHO=24
trigger=gpiozero.OutputDevice(TRIG)
echo=gpiozero.DigitalInputDevice(ECHO)
#====== in terminal type "sudo pigpiod" before running this !========
servo1 = 1 #put servo pin num
servo2 = 2
servo3 = 3
servo4 = 4
servo5 = 5
servo6 = 6

pwm = pigpio.pi() 

pwm.set_mode(servo1, pigpio.OUTPUT)
pwm.set_mode(servo2, pigpio.OUTPUT)
pwm.set_mode(servo3, pigpio.OUTPUT)
pwm.set_mode(servo4, pigpio.OUTPUT)
pwm.set_mode(servo5, pigpio.OUTPUT)
pwm.set_mode(servo6, pigpio.OUTPUT)

cap=cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

pwm.set_PWM_frequency( servo1, 50 )
pwm.set_PWM_frequency( servo2, 50 )
pwm.set_PWM_frequency( servo3, 50 )
pwm.set_PWM_frequency( servo4, 50 )
pwm.set_PWM_frequency( servo5, 50 )
pwm.set_PWM_frequency( servo6, 50 )

robot=gpiozero.Robot(left=(22,27),right=(17,18))

def get_distance(trigger,echo):
  trigger.on()
  sleep(0.00001)
  trigger.off()

  while echo.is_active == False:
    pulse_start=time.time()

  while echo.is_active == True:  
    pulse_end=time.time()
  
  pulse_duration=pulse_end - pulse_start
  distance = 34300 * (pulse_duration/2)
  round_duration=round(distance,2)
  return(round_duration)

while True:
  ret,frame = cap.read()
  flipped = cv2.flip(frame, flipCode=-1)
  frame1=cv2.resize(flipped,(640,480))
  qrdetect=qr.decode(frame1)

  distance_to_obj=get_distance(trigger,echo)
  #======print(qrdetect)
  #======print(qrdetect[0].data.decode("ascii"))
  for i in qrdetect:
    #print (i.rect.left,i.rect.top,i.rect.width,i.rect.height)
    #print(i.data[0])
    
    if (i.data[0]==115 and i.data[1]==116 and i.data[1]==97 and i.data[1]==114 and i.data[1]==116):
      print("start")
      pwm.set_servo_pulsewidth( servo1, 500 )#turn camera servo
      #==add command to move the rover to a distance till w1==
      if distance_to_obj > 15:
      	robot.forward(0.5)
      	sleep(0.25)
      if distance_to_obj<=15:
      	robot.stop()
                   
        if(i.data[0]==119 and i.data[1]==49):
          print("way1")
          robot.right()
          #pwm.set_servo_pulsewidth( servo, 2500 ) 
          sleep(0.25)
        
        if(i.data[0]==119 and i.data[1]==50):
          print("way2")
          #pwm.set_servo_pulsewidth( servo, 2500 ) 
          sleep(0.5)
        
        if(i.data[0]==100 and i.data[1]==49):
          print("door1")
          #pwm.set_servo_pulsewidth( servo, 2500 ) 
          sleep(0.5)
        
        if(i.data[0]==100 and i.data[1]==50):
          print("door2")
          #pwm.set_servo_pulsewidth( servo, 2500 ) 
          sleep(0.5)
      
      continue

    cv2.rectangle(frame1,(i.rect.left,i.rect.top),(i.rect.left+i.rect.width,i.rect.top+i.rect.height),(0,255,0),3)
    #cv2.putText(frame1,str(i.data),(20,20),font,2,(255,0,0),2) 
  cv2.imshow("Frame", frame1)
  key = cv2.waitKey(1) & 0xFF
  if key == ord("q"):
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
    break


# turning off servo
pwm.set_PWM_dutycycle(servo1, 0)
pwm.set_PWM_dutycycle(servo2, 0)
pwm.set_PWM_dutycycle(servo3, 0)
pwm.set_PWM_dutycycle(servo4, 0)
pwm.set_PWM_dutycycle(servo5, 0)
pwm.set_PWM_dutycycle(servo6, 0)

pwm.set_PWM_frequency( servo1, 0 )
pwm.set_PWM_frequency( servo2, 0 )
pwm.set_PWM_frequency( servo3, 0 )
pwm.set_PWM_frequency( servo4, 0 )
pwm.set_PWM_frequency( servo5, 0 )
pwm.set_PWM_frequency( servo6, 0 )

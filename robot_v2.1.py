import cv2
import numpy as np
import pyzbar.pyzbar as qr
from PIL import Image
import gpiozero
from gpiozero import Servo
import time
from time import sleep
import serial
from serial import Serial
import sqlite3
import threading
import pyautogui
import RPi.GPIO as GPIO

conn = sqlite3.connect('/home/pi/Desktop/python/med/medrobo/db.sqlite3')
cursor = conn.cursor()

cap=cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def print_patient_details():
	result = """SELECT * from med_details where id = ?"""
	for i in range(1,7):
		cursor.execute(result, (i,))
		records = cursor.fetchall()
		print("Printing ID ", id)
		for row in records:
		    print("Name = ", row[1])
		    print("Disease = ", row[2])
		    print("Door no = ", row[3])
		    print("bed no = ", row[4])
		    print("m1 = ", row[5])
		    print("m2 = ", row[6])
		    print("m3 = ", row[7])
		    print("m4 = ", row[8])
		    print("m5 = ", row[9])
		    print("m6 = ", row[10])

def get_bed_no():
	global a
	a=[]
	result = """SELECT * from med_details where id = ?"""
	for i in range(1,7):
		cursor.execute(result, (i,))
		records = cursor.fetchall()
		for row in records:
		    if(row[4]!=None):
		    	#add data to array or store it some where
		    	a.insert(i,"b"+row[4])
		    	print(a)
		    	#print(a[i-1])
	a.append(None)
	a.append(None)
	a.append(None)
	a.append(None)
	a.append(None)
	return a

def get_med_info():
	global m
	m=[]
	result = """SELECT * from med_details where id = ?"""
	for i in range(1,7):
		cursor.execute(result, (i,))
		records = cursor.fetchall()
		for row in records:
		    if(row[5]!=None):
		    	#add data to array or store it some where
		    	a.insert(i,row[5])
		    	print(a)
		    	#print(a[i-1])
	a.append(None)
	a.append(None)
	a.append(None)
	a.append(None)
	a.append(None)
	return a

def print_med_details(id):
	result = """SELECT * from med_details where id = ?"""
	global b
	b=[]	
	cursor.execute(result, (id,))
	records = cursor.fetchall()
	print("Printing ID ", id)
	print(records)
	for row in records:
	    for i in range(1,7):
	    	b.insert(i,row[i+4])
	    	print(b)

def med_disp():
	if(b[0]!=None):
		ser.write(b"M")
		time.sleep(3)
		ser.write(b"Q")
		time.sleep(1)

	if(b[1]!=None):
		ser.write(b"N")
		time.sleep(3)
		ser.write(b"Q")
		time.sleep(1)

	if(b[2]!=None):
		ser.write(b"O")
		time.sleep(3)
		ser.write(b"Q")
		time.sleep(1)

	if(b[3]!=None):
		ser.write(b"P")
		time.sleep(3)
		ser.write(b"Q")
		time.sleep(1)

def current_pos(pos):
	global current_poss
	current_poss = pos

def camera():
	print("turning on camera")
	time.sleep(5)
	threading.Thread(target=autopresser).start()
	while True:
		ret,frame = cap.read()
		global frame1
		frame1 = cv2.resize(frame,(640,480))
		qrdetect = qr.decode(frame1)
		for i in qrdetect:
			if(i.data==None):
				print("No qr/error detected . unknown location")
			
			elif (i.data[0]==115 and i.data[1]==116 and i.data[2]==97 and i.data[3]==114 and i.data[4]==116):
				print("start")
				a="start"
				current_pos(a)

			elif (i.data[0]==119 and i.data[1]==49):
				print("w1")
				a="w1"
				current_pos(a)

			elif (i.data[0]==119 and i.data[1]==50):
				print("w2")
				a="w2"
				current_pos(a)

			elif (i.data[0]==119 and i.data[1]==51):
				print("w3")
				a="w3"
				current_pos(a)

			elif (i.data[0]==100 and i.data[1]==49):
				print("d1")
				current_pos("d1")

			elif (i.data[0]==100 and i.data[1]==50):
				print("d2")
				current_pos("d2")

			elif (i.data[0]==98 and i.data[1]==49):
				print("b1")
				current_pos("b1")

			elif (i.data[0]==98 and i.data[1]==50):
				print("b2")
				current_pos(qrdetect.data)

			elif (i.data[0]==98 and i.data[1]==51):
				print("b3")
				current_pos(qrdetect.data)

			elif (i.data[0]==98 and i.data[1]==52):
				print("b4")
				current_pos(qrdetect.data)

			cv2.rectangle(frame1,(i.rect.left,i.rect.top),(i.rect.left+i.rect.width,i.rect.top+i.rect.height),(0,255,0),3)
			cv2.putText(frame1,str(i.data),(20,20),font,2,(255,0,0),2) 
		cv2.imshow("Frame", frame1)
		key = cv2.waitKey(10) & 0xFF
		if key == ord("q"):
			#cv2.waitKey(10)
			cv2.destroyAllWindows()
			print("turning off camera")
			break

def autopresser():
	for i in range(0,6):
		time.sleep(1)
		print(i)
	pyautogui.press("q")

def get_distance():
	GPIO.output(GPIO_TRIGGER, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	StartTime = time.time()
	StopTime = time.time()

	while GPIO.input(GPIO_ECHO) == 0:
	    StartTime = time.time()

	while GPIO.input(GPIO_ECHO) == 1:
	    StopTime = time.time()

	TimeElapsed = StopTime - StartTime
	distance = (TimeElapsed * 34300) / 2 
	return distance

def distance():
	while True:
		dist = get_distance()
		print ("Measured Distance = %.1f cm" % dist)
		time.sleep(0.5)
		if dist<1 :
			ser.write(b"S")
			print("obstacle detected... exiting")
			exit()
		else:
			continue

def check_start():
	print("checking location ...")
	if (current_poss!="start"):
		print("wrong location")
		exit()

def check_w1():
	print("checking location ...")
	if (current_poss!="w1"):
		print("wrong location")
		exit()

def check_w2():
	print("checking location ...")
	if (current_poss!="w2"):
		print("wrong location")
		exit()

def check_w3():
	print("checking location ...")
	if (current_poss!="w3"):
		print("wrong location")
		exit()

def check_d1():
	print("checking location ...")
	if (current_poss!="d1"):
		print("wrong location")
		exit()

def check_d2():
	print("checking location ...")
	if (current_poss!="d2"):
		print("wrong location")
		exit()

def check_b1():
	print("checking location ...")
	if (current_poss!="b1"):
		print("wrong location")
		exit()

def check_b2():
	print("checking location ...")
	if (current_poss!="b2"):
		print("wrong location")
		exit()

def check_b3():
	print("checking location ...")
	if (current_poss!="b3"):
		print("wrong location")
		exit()

def check_b4():
	print("checking location ...")
	if (current_poss!="b4"):
		print("wrong location")
		exit()

def check_b5():
	print("checking location ...")
	if (current_pos!="b5"):
		print("wrong location")
		exit()

def check_b6():
	print("checking location ...")
	if (current_pos!="b6"):
		print("wrong location")
		exit()

def path_planning():
	if(a[0]==0 or a[0]==None):#1
		#dont start
		exit()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b3" and a[3]=="b4" and a[4]=="b5" and a[5]=="b6"):#2
		#start
		print("123456")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()
		#end

	elif(a[0]=="b1" and a[1]==None and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#3
		#start
		print("1")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_d1()
		d1_to_w2()
		w2_to_w1_to_s()

	elif(a[0]=="b2" and a[1]==None and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#4
		print("2")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w1_to_s()

	elif(a[0]=="b3" and a[1]==None and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#5
		print("3")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w1_to_s()

	elif(a[0]=="b4" and a[1]==None and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#6
		print("4")
		s_to_w1()
		w1_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b5" and a[1]==None and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#7
		print("5")
		s_to_w1()
		w1_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b6" and a[1]==None and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#8
		print("6")
		s_to_w1()
		w1_to_w3()
		w3_to_d2()
		d2_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#9
		print("12")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b3" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#10
		print("13")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b4" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#11
		print("14")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()
		
	elif(a[0]=="b1" and a[1]=="b5" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#12
		print("15")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b6" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#13
		print("16")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b3" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#14
		print("23")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b4" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#15
		print("24")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b5" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#16
		print("25")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b6" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#17
		print("26")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b3" and a[1]=="b4" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#18
		print("34")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b3" and a[1]=="b5" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#19
		print("35")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b3" and a[1]=="b6" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#20
		print("36")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b4" and a[1]=="b5" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#21
		print("45")
		s_to_w1()
		w1_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b4" and a[1]=="b6" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#22
		print("46")
		s_to_w1()
		w1_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b6()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b5" and a[1]=="b6" and a[2]==None and a[3]==None and a[4]==None and a[5]==None):#23
		print("56")
		s_to_w1()
		w1_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b3" and a[3]==None and a[4]==None and a[5]==None):#24
		print("123")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b4" and a[3]==None and a[4]==None and a[5]==None):#25
		print("124")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b5" and a[3]==None and a[4]==None and a[5]==None):#26
		print("125")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b6" and a[3]==None and a[4]==None and a[5]==None):#27
		print("126")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b3" and a[2]=="b4" and a[3]==None and a[4]==None and a[5]==None):#28
		print("134")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b3" and a[2]=="b5" and a[3]==None and a[4]==None and a[5]==None):#29
		print("135")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b3" and a[2]=="b6" and a[3]==None and a[4]==None and a[5]==None):#30
		print("136")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b4" and a[2]=="b5" and a[3]==None and a[4]==None and a[5]==None):#31
		print("145")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b4" and a[2]=="b6" and a[3]==None and a[4]==None and a[5]==None):#32
		print("146")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b5" and a[2]=="b6" and a[3]==None and a[4]==None and a[5]==None):#33
		print("156")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b3" and a[2]=="b4" and a[3]==None and a[4]==None and a[5]==None):#34
		print("234")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b3" and a[2]=="b5" and a[3]==None and a[4]==None and a[5]==None):#35
		print("235")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b3" and a[2]=="b6" and a[3]==None and a[4]==None and a[5]==None):#36
		print("236")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b4" and a[2]=="b5" and a[3]==None and a[4]==None and a[5]==None):#37
		print("245")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b4" and a[2]=="b6" and a[3]==None and a[4]==None and a[5]==None):#38
		print("246")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b5" and a[2]=="b6" and a[3]==None and a[4]==None and a[5]==None):#39
		print("256")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b3" and a[1]=="b4" and a[2]=="b5" and a[3]==None and a[4]==None and a[5]==None):#40
		print("345")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b3" and a[1]=="b4" and a[2]=="b6" and a[3]==None and a[4]==None and a[5]==None):#41
		print("346")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b3" and a[1]=="b5" and a[2]=="b6" and a[3]==None and a[4]==None and a[5]==None):#42
		print("356")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b4" and a[1]=="b5" and a[2]=="b6" and a[3]==None and a[4]==None and a[5]==None):#43
		print("456")
		s_to_w1()
		w1_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b3" and a[3]=="b4" and a[4]==None and a[5]==None):#44
		print("1234")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b3" and a[3]=="b5" and a[4]==None and a[5]==None):#45
		print("1235")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b3" and a[3]=="b6" and a[4]==None and a[5]==None):#46
		print("1236")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b4" and a[3]=="b5" and a[4]==None and a[5]==None):#47
		print("1245")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b4" and a[3]=="b6" and a[4]==None and a[5]==None):#48
		print("1246")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b5" and a[3]=="b6" and a[4]==None and a[5]==None):#49
		print("1256")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b3" and a[2]=="b4" and a[3]=="b5" and a[4]==None and a[5]==None):#50
		print("2345")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b3" and a[2]=="b4" and a[3]=="b6" and a[4]==None and a[5]==None):#51
		print("2346")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b3" and a[2]=="b4" and a[3]=="b5" and a[4]==None and a[5]==None):#52
		print("1345")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b3" and a[2]=="b4" and a[3]=="b6" and a[4]==None and a[5]==None):#53
		print("1346")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b3" and a[2]=="b5" and a[3]=="b6" and a[4]==None and a[5]==None):#54
		print("1356")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b3()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b4" and a[2]=="b5" and a[3]=="b6" and a[4]==None and a[5]==None):#55
		print("1456")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b3" and a[1]=="b4" and a[2]=="b5" and a[3]=="b6" and a[4]==None and a[5]==None):#56
		print("3456")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b3" and a[3]=="b4" and a[4]=="b5" and a[5]==None):#57
		print("12345")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b3" and a[3]=="b4" and a[4]=="b6" and a[5]==None):#58
		print("12346")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b3" and a[2]=="b4" and a[3]=="b5" and a[4]=="b6" and a[5]==None):#59
		print("13456")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b2" and a[1]=="b3" and a[2]=="b4" and a[3]=="b5" and a[4]=="b6" and a[5]==None):#60
		print("23456")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b2()
		b2_to_b3()
		b3_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

	elif(a[0]=="b1" and a[1]=="b2" and a[2]=="b4" and a[3]=="b5" and a[4]=="b6" and a[5]==None):#60
		print("12456")
		s_to_w1()
		w1_to_w2()
		w2_to_d1()
		d1_to_b1()
		b1_to_b2()
		b2_to_d1()
		d1_to_w2()
		w2_to_w3()
		w3_to_d2()
		d2_to_b4()
		b4_to_b5()
		b5_to_b6()
		b6_to_d2()
		d2_to_w3()
		w3_to_w1_to_s()

def s_to_w1():#start to way1
	print("s to w1 \n start")
	camera()
	check_start()
	ser.write(b"F")
	time.sleep(1.5)
	ser.write(b"S")
	time.sleep(0.5)

def w1_to_w2():#way1 to way2
	print("w1 to w2 \n w1")
	camera()
	check_w1()
	ser.write(b"L")
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def w1_to_w3():#way1 to way3
	camera()
	check_w1()
	ser.write(b"R")
	time.sleep(0.7)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def w2_to_d1():#way2 to door1
	print("w2 to d1 \n w2")
	camera()
	check_w2()
	ser.write(b"L")
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def d1_to_b1():#door1 to bed1
	print("d1 to b1 \n d1")
	camera()
	check_d1()
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"L")
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def d1_to_b2():#door1 to bed2
	camera()
	check_d1()
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"L")
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def d1_to_b3():#door1 to bed3
	camera()
	check_d1()
	ser.write(b"F")
	time.sleep(2)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"L")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b1_to_b2():#bed1 to bed2
	camera()
	check_b1()

	print_med_details(1)#getting medicine information
	med_disp()#dispense the medicine
	time.sleep(5)

	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"L")
	time.sleep(0.9)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"L")
	time.sleep(0.9)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b1_to_b3():#bed1 to bed3
	camera()
	check_b1()

	print_med_details(1)#getting medicine information
	med_disp()#dispense the medicine
	time.sleep(5)

	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(4)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b2_to_b3():#bed2 to bed3
	camera()
	check_b2()

	print_med_details(2)#getting medicine information
	med_disp()#dispense the medicine
	time.sleep(5)

	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(2)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b1_to_d1():#bed1 to door1
	print("b1 to d1 \n b1")
	camera()
	check_b1()

	print_med_details(1)#getting medicine information
	med_disp()#dispense the medicine
	time.sleep(3)

	ser.write(b"R") #turn robot 180deg 
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b2_to_d1():#bed2 to door1
	camera()
	check_b2()
	
	print_med_details(2)#getting medicine information
	med_disp()#dispense the medicine
	time.sleep(5)

	ser.write(b"R") #turn robot 180deg 
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b3_to_d1():#bed3 to door1
	camera()
	check_b3()
	print_med_details(3)#getting medicine information
	med_disp()#dispense the medicine
	time.sleep(5)

	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(5)
	ser.write(b"S")
	time.sleep(0.5)

def w3_to_d2():#way3 to door2
	camera()
	check_w2()
	ser.write(b"L")
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(0.1)
	ser.write(b"S")
	time.sleep(0.5)

def d2_to_b4():#door2 to bed4
	camera()
	check_d2()
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def d2_to_b5():#door2 to bed5
	camera()
	check_d2()
	ser.write(b"F")
	time.sleep(3)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def d2_to_b6():#door2 to bed6
	camera()
	check_d2()
	ser.write(b"F")
	time.sleep(5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b4_to_b5():#bed4 to bed5
	camera()
	check_b4()
	ser.write(b"L") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(2)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b4_to_b6():#bed4 to bed6
	camera()
	check_b4()
	ser.write(b"L") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(4)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b5_to_b6():#bed5 to bed6
	camera()
	check_b5()
	ser.write(b"L") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(3)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b4_to_d2():#bed4 to door2
	camera()
	check_b4()
	ser.write(b"L") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)

def b5_to_d2():#bed5 to door2
	camera()
	check_b5()
	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(3)
	ser.write(b"S")
	time.sleep(0.5)

def b6_to_d2():#bed6 to door2
	camera()
	check_b6()
	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(5)
	ser.write(b"S")
	time.sleep(0.5)

def d1_to_w2():#door1 to way2
	print("d1 to w2 \n d1")
	camera()
	check_d1()
	ser.write(b"F")
	time.sleep(0.1)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)

def d2_to_w3():#door2 to way3
	camera()
	check_d2()
	ser.write(b"F")
	time.sleep(0.75)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)

def w2_to_w1_to_s():#way2 to way1 to start
	print("w2 to w1 \n w2")
	camera()
	check_w2()
	ser.write(b"F")
	time.sleep(2)
	ser.write(b"S")
	time.sleep(0.5)
	print("w1 to start \n w1")
	camera()
	check_w1()
	ser.write(b"R")
	time.sleep(0.8)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(2)
	ser.write(b"S")
	print("check start \n start")
	camera()
	check_start()
	time.sleep(0.5)

def w2_to_w3():#way2 to way3
	camera()
	check_w2()
	ser.write(b"F")
	time.sleep(5)
	ser.write(b"S")
	time.sleep(0.5)

def w3_to_w1_to_s():#way3 to way1 to start
	camera()
	check_w3()
	ser.write(b"F")
	time.sleep(1.25)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	time.sleep(0.5)
	ser.write(b"F")
	time.sleep(1.25)
	ser.write(b"S")
	time.sleep(0.5)

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	ser.reset_input_buffer()
	print_patient_details()
	get_bed_no()
	# threading.Thread(target=path_planning).start()
	#threading.Thread(target=distance).start()
	path_planning()
	cursor.close()
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

conn = sqlite3.connect('/home/pi/Desktop/python/med/medrobo/db.sqlite3')
cursor = conn.cursor()

cap=cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

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
		    	a.insert(i,row[4])
		    	print(a)
		    	#print(a[i-1])
	a.append(None)
	a.append(None)
	a.append(None)
	a.append(None)
	a.append(None)
	return a

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

def scan_qrcode():
	ret,frame = cap.read()
	global frame1
	frame1 = cv2.resize(frame,(640,480))
	qrdetect = qr.decode(frame1)
	return qrdetect

def current_pos(pos):
	global current_pos
	current_pos = pos

def s_to_w1():#start to way1
	#pass
	ser.write(b"F")
	time.sleep(1.25)
	ser.write(b"S")

def w1_to_w2():#way1 to way2
	#pass
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1.25)
	ser.write(b"S")

def w1_to_w3():#way1 to way3
	#pass
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1.25)
	ser.write(b"S")

def w2_to_d1():#way2 to door1
	#pass
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(0.75)
	ser.write(b"S")

def d1_to_b1():#door1 to bed1
	#pass
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def d1_to_b2():#door1 to bed2
	#pass
	ser.write(b"F")
	time.sleep(3)
	ser.write(b"S")
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def d1_to_b3():#door1 to bed3
	#pass
	ser.write(b"F")
	time.sleep(5)
	ser.write(b"S")
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")#door1 to bed3

def b1_to_b2():#bed1 to bed2
	#pass
	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(2)
	ser.write(b"S")
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def b1_to_b3():#bed1 to bed3
	#pass
	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(4)
	ser.write(b"S")
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def b2_to_b3():#bed2 to bed3
	#pass
	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(2)
	ser.write(b"S")
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	#ser.write(b"S")

def b1_to_d1():#bed1 to door1
	#pass
	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def b2_to_d1():#bed2 to door1
	#pass
	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(3)
	ser.write(b"S")

def b3_to_d1():#bed3 to door1
	#pass
	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(5)
	ser.write(b"S")

def w3_to_d2():#way3 to door2
	#pass
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(0.75)
	ser.write(b"S")

def d2_to_b4():#door2 to bed4
	#pass
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def d2_to_b5():#door2 to bed5
	#pass
	ser.write(b"F")
	time.sleep(3)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def d2_to_b6():#door2 to bed6
	#pass
	ser.write(b"F")
	time.sleep(5)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def b4_to_b5():#bed4 to bed5
	#pass
	ser.write(b"L") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(2)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def b4_to_b6():#bed4 to bed6
	#pass
	ser.write(b"L") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(4)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")	

def b5_to_b6():#bed5 to bed6
	#pass
	ser.write(b"L") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(3)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def b4_to_d2():#bed4 to door2
	#pass	
	ser.write(b"L") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")

def b5_to_d2():#bed5 to door2
	#pass
	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(3)
	ser.write(b"S")

def b6_to_d2():#bed6 to door2
	#pass
	ser.write(b"R") #turn robot 180deg 
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(5)
	ser.write(b"S")

def d1_to_w2():#door1 to way2
	#pass
	ser.write(b"F")
	time.sleep(0.75)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")

def d2_to_w3():#door2 to way3
	#pass
	ser.write(b"F")
	time.sleep(0.75)
	ser.write(b"S")
	ser.write(b"L")
	time.sleep(0.5)
	ser.write(b"S")

def w2_to_w1_to_s():#way2 to way1 to start
	#pass
	ser.write(b"F")
	time.sleep(1.25)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1.25)
	ser.write(b"S")

def w2_to_w3():#way2 to way3
	#pass
	ser.write(b"F")
	time.sleep(5)
	ser.write(b"S")

def w3_to_w1_to_s():#way3 to way1 to start
	#pass
	ser.write(b"F")
	time.sleep(1.25)
	ser.write(b"S")
	ser.write(b"R")
	time.sleep(0.5)
	ser.write(b"S")
	ser.write(b"F")
	time.sleep(1.25)
	ser.write(b"S")

def get_distance(trigger,echo):
  trigger.on()
  sleep(0.00001)
  trigger.off()

  while echo.is_active == False:
    pulse_start=time.time()

  while echo.is_active == True:  
    pulse_end=time.time()
  
  pulseq_duration=pulse_end - pulse_start
  distance = 34300 * (pulse_duration/2)
  round_duration=round(distance,2)
  return(round_duration)

if __name__ == '__main__':
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
	ser.reset_input_buffer()

	while True:
		qrdetect = scan_qrcode()
		print_patient_details()
		get_bed_no()
		#path_planning()
		#get_distance()

		#dist = get_distance(trigger,echo)
    #distance_to_obj=get_distance(trigger,echo)
    #if (dist<=15):
    #  ser.write(b"S")

		for i in qrdetect:
			if (i.data[0]==115 and i.data[1]==116 and i.data[2]==97 and i.data[3]==114 and i.data[4]==116):
				print("start")
				current_pos(data)

			elif (i.data[0]==119 and i.data[1]==49):
				print("w1")
				current_pos(data)

			elif (i.data[0]==119 and i.data[1]==50):
				print("w2")
				current_pos(data)

			elif (i.data[0]==100 and i.data[1]==49):
				print("d1")
				current_pos(data)

			elif (i.data[0]==100 and i.data[1]==50):
				print("d2")
				current_pos(data)

			elif (i.data[0]==98 and i.data[1]==49):
				print("b1")
				current_pos(data)

			elif (i.data[0]==98 and i.data[1]==50):
				print("b2")
				current_pos(data)

			elif (i.data[0]==98 and i.data[1]==51):
				print("b3")
				current_pos(data)

			elif (i.data[0]==98 and i.data[1]==52):
				print("b4")
				current_pos(data)

			cv2.rectangle(frame1,(i.rect.left,i.rect.top),(i.rect.left+i.rect.width,i.rect.top+i.rect.height),(0,255,0),3)
			cv2.putText(frame1,str(i.data),(20,20),font,2,(255,0,0),2) 

		cv2.imshow("Frame", frame1)

		key = cv2.waitKey(10) & 0xFF
		if key == ord("q"):
			#cv2.waitKey(0)
			cv2.destroyAllWindows()
			break

	cursor.close()
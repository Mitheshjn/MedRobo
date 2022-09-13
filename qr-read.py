import cv2
import numpy as np
import pyzbar.pyzbar as qr
from PIL import Image
import time
from time import sleep
img=Image.open("./New/d1.png")
out=qr.decode(img)
for i in out:
  print(i.data)

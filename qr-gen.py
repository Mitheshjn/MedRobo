import qrcode
import cv2
qr=qrcode.QRCode()
text=input("Enter text :")
qr.add_data(text)
qr.make()
img=qr.make_image(fill_color="#000000",back_colour="#ffffff")
img.save('/home/pi/Desktop/python/New/w3.png')
img=cv2.imread('/home/pi/Desktop/python/New/w3.png')
cv2.imshow('QR Code',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
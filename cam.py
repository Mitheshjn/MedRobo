import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame1=cv2.resize(frame,(1280,720))
    # Display the resulting frame
    cv2.imshow('frame',frame1)
    #cv2.imshow('gray',gray)
    #if cv2.waitKey(20) & 0xFF == ord("q") :
     #   cv2.destroyAllWindows()
      #  break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
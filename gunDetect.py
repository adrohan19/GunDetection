import numpy as np
import cv2
import imutils
import datetime
  
# cascade is old one, cascades is new one (cascades seems to work better)
# still some false positives
gun_cascade = cv2.CascadeClassifier('cascades.xml')
camera = cv2.VideoCapture(0)
   
firstFrame = None
gun_exist = False
gunCounter = 0
detectionRequirement = 60
   
while True:
      
    ret, frame = camera.read()
   
    frame = imutils.resize(frame, width = 500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       
    gun = gun_cascade.detectMultiScale(gray,1.3, 5,minSize = (100, 100))
       
    if len(gun) > 0:
        gun_exist = True
    else:
        gun_exist = False

    for (x, y, w, h) in gun:
          
        frame = cv2.rectangle(frame,(x, y),(x + w, y + h),(255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]    
   
    if firstFrame is None:
        firstFrame = gray
        continue
    #print(gunCounter)
    if gun_exist:
            #print("guns detected")
            gunCounter+=1
            if gunCounter >= detectionRequirement:
                print("gun detected")
                gunCounter = 0 #might want to remove this if it repeatedly tries to turn around
    else: gunCounter = 0
    # print(datetime.date(2019))
    # draw the text and timestamp on the frame
    #cv2.putText(frame, datetime.datetime.now().strftime("% A % d % B % Y % I:% M:% S % p"),(10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
   
    cv2.imshow("Security Feed", frame)
    key = cv2.waitKey(1) & 0xFF
      
    if key == ord('q'):
        break
  
        if gun_exist:
            print("You reached that last gun_exist")
            #print("guns detected")
            #gunCounter+=1
            #if gunCounter >= 30:
            #    print("gun detected")
            #    gunCounter = 0 #might want to remove this if it repeatedly tries to turn around
else:
    print("guns NOT detected")
    gunCounter = 0
  
camera.release()
cv2.destroyAllWindows()
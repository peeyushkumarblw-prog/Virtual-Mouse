"""Author: Peeyush Kumar"""

import mediapipe as mp
import cv2
import numpy as np
# import autopy
import pyautogui as pag
import HandTrackingModule as htm
from pynput.mouse import Controller, Button
import time

##  Variables  ###################################
DRAW = True
dead_zone = 6
accel = 0.002
width = 1280 #Camera w
height = 720 #Camera h

prevTime = 0

widthScr , heightScr = pag.size()
# print(widthScr,heightScr)

# Frame Reduction: Ineraction box
frr = 400 #200 # Width
frrt = 200 #100 # Height top
frrb = 350 #300 # Height bottom

smoothening = 7
plocX,plocY = 0,0
clocX,clocY = 0,0

tx,ty = 0,0
ix,iy = 0,0
mx,my = 0,0
#################################################

##  Objects  ####################################
cap = cv2.VideoCapture(0) #0 for single camera source
cap.set(3,width)
cap.set(4,height)

mouse = Controller()
detector = htm.handDetector(maxHands=1)
#################################################

while True:
    ##  Hand Landmarks 
    success,img = cap.read()
    if not success:
        continue
    
    img = detector.findHands(img, draw= DRAW)
    lmList, bbox = detector.findPosition(img, draw= DRAW)
    
    if len(lmList)== 0:
        cv2.imshow("Image",img)
        if cv2.waitKey(1) & 0xFF == ord('d'):
            DRAW = not DRAW
        continue
    
    
    ##  Tip of Thumb, middle and index finger   
    tx,ty = lmList[4][1:] #Thumb
    ix,iy = lmList[8][1:] #Index
    mx,my = lmList[12][1:] #Middle
    # print(tx,ty," # ",ix,iy," $ ",mx,my)
    
    
    ##  Fingers up
    fingers = detector.fingersUp()
    # print(fingers)
    
    if DRAW:
        cv2.rectangle(img,(frr,frrt),(width-frr,height-frrb),(0,200,0),2)
    
    
    ##  Only Index Finger : Pointer Mode
    if fingers[1]==1 and fingers[2]==0 and fingers[4]==0:
        # Convert coordinates (fingers to screen)
        x3 = np.interp(ix,(frr,width-frr),(0,widthScr))
        y3 = np.interp(iy,(frrt,height-frrb),(0,heightScr))
        
        dx = x3 - plocX
        dy = y3 - plocY
        
        # Dead Zone
        if abs(dx) < dead_zone:
            dx= 0
        if abs(dy) < dead_zone:
            dy= 0
        
        # Linear Acceleration
        speed = abs(dx) + abs(dy)
        factor = 1 + speed*accel
        dx *= factor
        dy *= factor
        
        # Smoothen Values
        clocX = plocX + dx /smoothening
        clocY = plocY + dy /smoothening
        
        # Move Mouse
        mouse.position = (int(widthScr- clocX),int(clocY))
        plocX = clocX #Updation
        plocY = clocY
        
        if DRAW:
            cv2.circle(img,(ix,iy),15,(255,0,0),cv2.FILLED)
            cv2.putText(img,str("Pointer"),(20,100),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(0,0,0),3)
        
    
    ##  Thumb to Left click
    if fingers[1]==1 and fingers[2]==0 and fingers[4]==0:
        ## Distance between fingers
        length,img,line = detector.findDistance(4,5,img,draw=DRAW)
        # print(length)
        ## mouse click
        if length<35:
            mouse.click(Button.left,1)
            time.sleep(0.15)
            if DRAW:
                cv2.circle(img,(ix,iy),15,(0,0,255),cv2.FILLED)
                cv2.putText(img,str("Click"),(20,150),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(0,0,0),3)
    
    
    ##  Index+Middle then Thumb to right click
    if fingers[1]==1 and fingers[2]==1 and fingers[3]==0 and fingers[4]==0:
        if DRAW:
            cv2.circle(img,(mx,my),15,(255,0,0),cv2.FILLED)
            cv2.circle(img,(ix,iy),15,(255,0,0),cv2.FILLED)
        # Distance between fingers
        length,img,line = detector.findDistance(4,5,img,draw=DRAW)
        # print(length)
        # Click mouse
        if length<40:
            mouse.click(Button.right,10)
            time.sleep(0.2)
            if DRAW:
                cv2.circle(img,(ix,iy),15,(0,0,255),cv2.FILLED)
                cv2.circle(img,(mx,my),15,(0,0,255),cv2.FILLED)
                cv2.putText(img,str("Right Click"),(20,150),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(0,0,0),3)
    
    
    ##  Rock&Roll to scroll
    if fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==1:
        # Distance between fingers
        length,img,line = detector.findDistance(4,5,img,draw=DRAW)
        # print(length)
        # Click mouse
        if length<50:
            # pag.press('pageup')
            mouse.scroll(0,10)
            time.sleep(0.2)
            if DRAW:
                cv2.putText(img,str("Scroll up"),(20,100),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(0,0,0),3)
        else:
            # pag.press("pagedown")
            mouse.scroll(0,-10)
            time.sleep(0.2)
            if DRAW:
                cv2.putText(img,str("Scroll down"),(20,100),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(0,0,0),3)
    
    
    ##  FrameRate
    currTime = time.time()
    fps=1/(currTime-prevTime) if prevTime !=0 else 0
    prevTime = currTime #Updation
    if DRAW:
        cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_COMPLEX_SMALL,3,(0,0,0),3)
    
    
    ##  Display
    cv2.imshow("Image",img)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('d'):
        DRAW = not DRAW
    elif key == 27:
        break
    
    
cap.release()
cv2.destroyAllWindows()



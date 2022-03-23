import random
import time
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import cvzone

#webcam
cap= cv.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
click=0
clickNO=0




#hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

#finding function Ax^2 +Bx + c  when we draw this data
computerDis=[300,245,200,170,145,130,112,103,93,87,80,75,70,67,62,59,57]
realDis=[20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(computerDis,realDis,2) #A , B , C
score=0
counter = 0
timeStart = time.time()
gameTime =20
def game(img,dis,x,y,w,h):


    global Cx
    global Cy
    color=(255,0,255)
    global score
    global counter

    if dis < 40: #cliked
        if x<Cx<x+w and y<Cy<y+h:
            counter = 1




    if counter :
        counter +=1
        color= (0, 255, 0)


        if counter >=3 and dis>40:
            score += 1
            Cx=random.randint(100,1100)
            Cy=random.randint(100,600)
            color = (255, 0, 255)
            counter=0
            #print(counter)


    cv.circle(img,(Cx,Cy),30,(color),cv.FILLED)
    cv.circle(img, (Cx, Cy), 10, (255,255,255), cv.FILLED)
    cvzone.putTextRect(img,f"time : {int(time.time()-timeStart)}",(900,75),scale=3)
    cvzone.putTextRect(img, f"score : {str(score).zfill(2)}", (100, 75), scale=3)

#loop
Cx,Cy = 250 ,250
stop =False
Start = False

while True:
    sucess,img = cap.read()
    img=cv.flip(img, 1)
    hands, img = detector.findHands(img)
    if hands :
        lmlist = hands[0]['lmList']
        #print(hands[0])
        bbox=hands[0]['bbox']
        Xb, yB, Wb, Hb = bbox
        #we can see the detials on the mediapip website
        # for the hand we need the point number 17 and 5
        x,y,z = lmlist[5]
        x1,y1,z1 = lmlist[17]
        distance =  round(((x1-x)**2+(y1-y)**2)**0.5)
        A, B, C = coff
        distanceCm= int(A*(distance**2) + B*distance + C)


        cvzone.putTextRect(img,f"{distanceCm}",(Xb+100,yB))
        if time.time()-timeStart<gameTime:
            game(img,distanceCm,Xb,yB,Wb,Hb)

        else:
            img = cv.cvtColor(img,cv.COLOR_BGR2XYZ)
            cvzone.putTextRect(img, f"Game over score : {score}", (300, 100), scale=3, offset=20)
            cvzone.putTextRect(img,"do you want to play again ?",(300,200),scale=3,offset=20)
            cvzone.putTextRect(img, "yes", (300, 500), scale=3, offset=20)
            cvzone.putTextRect(img, "no", (1000, 500), scale=3, offset=20)
            if distanceCm < 40:  # cliked
                if Xb < 300 < Xb + Wb and yB < 500 < yB + Hb:
                    click +=1
                    c,vzone.putTextRect(img, f"yes{int((50 - click)/10)}", (300, 500), scale=5, offset=20, colorB=(0, 255, 255),colorR=(0, 200, 200))
                else:
                    click = 0


            if click>=50:
                click += 1


                if click >= 52 :

                    Start = True
                    click=0

            if distanceCm < 40:  # cliked
                if Xb < 1000 < Xb + Wb and yB < 500 < yB + Hb:
                    clickNO +=1
                    cvzone.putTextRect(img, f"no{int((50-clickNO)/10)}", (1000, 500), scale=5, offset=20, colorB=(0, 255, 255),colorR=(0, 200, 200))
                else:
                    clickNO = 0
            if clickNO>=50:
                clickNO += 1

                if clickNO >= 52:
                    stop = True
                    clickNO=0



    cv.imshow("org", img)
    if stop == True :
        break
    if Start ==True:
        score = 0
        clickNO=0
        click=0
        timeStart=time.time()
        #print("starrt")
        Start = False
    if cv.waitKey(1) & 0xFF ==ord('q'):
        break

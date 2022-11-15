import cv2
import mediapipe as mp

# WORKS FOR THE LEFT HAND

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

finger_tips =[8, 12, 16, 20]
thumb_tip= 4

finger_fold_status = []

while True:
    ret,img = cap.read()
    img = cv2.flip(img, 1)
    h,w,c = img.shape
    results = hands.process(img)


    if results.multi_hand_landmarks:
        for hand_landmark in results.multi_hand_landmarks:
            #accessing the landmarks by their position
            lm_list=[]
            for id ,lm in enumerate(hand_landmark.landmark):
                lm_list.append(lm)

             #Code goes here 
            for tip in finger_tips:

                xPos,yPos = int(lm_list[tip].x*w), int(lm_list[tip].y*h) 
                baseYPos = int(lm_list[tip-2].y*h)
                print(yPos - baseYPos)
                if lm_list[tip].x < lm_list[tip-2].x and (abs(yPos - baseYPos)<30):
                    cv2.circle(img, (xPos,yPos), 15, (0, 0,0), cv2.FILLED)
                    finger_fold_status.append(True)
                    #print("true")
                else:
                    finger_fold_status.append(False)
                    #print("false")
                
                if (finger_fold_status[-1] == True and finger_fold_status[-2] == True and finger_fold_status[-3] == True and finger_fold_status[-4] == True):   
                    if lm_list[thumb_tip].y < lm_list[thumb_tip-1].y < lm_list[thumb_tip-2].y:
                        cv2.putText(img, "Like", (20,30), cv2.FONT_ITALIC, 1, (0,255,0),3)
                        print("Like")
                
                    if lm_list[4].y > lm_list[3].y > lm_list[2].y:
                        cv2.putText(img, "Dislike", (20,30), cv2.FONT_ITALIC, 1, (0,0,255),3)
                        print("DIslike")

             



            mp_draw.draw_landmarks(img, hand_landmark,
            mp_hands.HAND_CONNECTIONS, mp_draw.DrawingSpec((0,0,255),2,2),
            mp_draw.DrawingSpec((0,255,0),4,2))
    

    cv2.imshow("hand tracking", img)
    cv2.waitKey(1)
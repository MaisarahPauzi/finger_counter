import cv2
import numpy as np 
from hand_detector import HandDetector

camera = cv2.VideoCapture(0)
hd = HandDetector()

'''
Reference: https://google.github.io/mediapipe/solutions/hands.html
'''
tipsId = [4, 8, 12, 16, 20]


while True:
    _, frame = camera.read()
    frame = hd.find_hands(frame)
    hand_mark_list = hd.find_position(frame)
    
    if len(hand_mark_list) > 0:
        fingers = []

        # Thumb
        if hand_mark_list[tipsId[0]]['x'] < hand_mark_list[tipsId[0]-1]['x']:
            fingers.append(0)
        else:
            fingers.append(1)
        
        # Other fingers
        for id in range(1,5):
            if hand_mark_list[tipsId[id]]['y'] < hand_mark_list[tipsId[id]-2]['y']:
                fingers.append(1)
            else:
                fingers.append(0)
        
        '''
        according to Malaysian Sign Language
        https://malaysiansignlanguage.weebly.com/uploads/1/0/5/8/105863499/editor/bimno_1.jpg?1496377606
        '''
        zero = [0,0,0,0,0]
        one = [0,1,0,0,0]
        two = [0,1,1,0,0]
        three = [1,1,1,0,0]
        four = [0,1,1,1,1]
        five = [1,1,1,1,1]
        six = [0,1,1,1,0]
        seven = [0,1,1,0,1]
        eight = [0,1,0,1,1]
        nine = [0,0,1,1,1]
        ten = [1,0,0,0,0]

        if fingers == zero:
            total_fingers = 0
        if fingers == one:
            total_fingers = 1
        if fingers == two:
            total_fingers = 2
        if fingers == three:
            total_fingers = 3
        if fingers == four:
            total_fingers = 4
        if fingers == five:
            total_fingers = 5
        if fingers == six:
            total_fingers = 6
        if fingers == seven:
            total_fingers = 7
        if fingers == eight:
            total_fingers = 8
        if fingers == nine:
            total_fingers = 9
        if fingers == ten:
            total_fingers = 10
        
        text = f'Total fingers: {total_fingers}'
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (100,100), font, 2, (0,0,255), 2)

    # show window frame contain live camera video
    cv2.imshow("frame", frame)

    reference  = cv2.imread('sign.jpg')
    cv2.imshow("reference", reference)


    # wait for key every 1 millisecond
    key = cv2.waitKey(1)

    # close window when click exit button
    if cv2.getWindowProperty("frame",cv2.WND_PROP_VISIBLE) == 0:        
        break

camera.release()
cv2.destroyAllWindows()
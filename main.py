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
        
        total_fingers = fingers.count(1)
        text = f'Total fingers: {total_fingers}'
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, text, (100,100), font, 2, (0,0,255), 2)

    # show window frame contain live camera video
    cv2.imshow("frame", frame)


    # wait for key every 1 millisecond
    key = cv2.waitKey(1)

    # close window when click exit button
    if cv2.getWindowProperty("frame",cv2.WND_PROP_VISIBLE) == 0:        
        break

camera.release()
cv2.destroyAllWindows()
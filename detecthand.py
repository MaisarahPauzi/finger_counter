import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

def get_hand_labels(hand_process_results, labels_array):
    if hand_process_results.multi_handedness is not None:
        for idx, hand_handedness in enumerate(hand_process_results.multi_handedness):
            handedness_dict = MessageToDict(hand_handedness)
            class_array = handedness_dict.get('classification')
            if class_array is not None:
                for item in class_array:
                    labels_array.append(item.get('label'))
    return labels_array

def drawing_hand_landmarks(hand_process_results, right_hand_fingers, left_hand_fingers):
    if hand_process_results.multi_hand_landmarks:
        for i,hand_landmarks in enumerate(hand_process_results.multi_hand_landmarks):
            # drawing bounding box
            x_max = 0
            y_max = 0
            x_min = w
            y_min = h

            for id, lm in enumerate(hand_landmarks.landmark):
                x, y = int(lm.x * w), int(lm.y * h)
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y

                if labels[i] == 'Right':
                    right_hand_fingers.append({'id': id, 'x': x, 'y': y})
                else:
                    left_hand_fingers.append({'id': id, 'x': x, 'y': y})
                
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(frame, labels[i], (x_min,y_min-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # drawing hand landmarks
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    return right_hand_fingers, left_hand_fingers

def configure_fingers(fingers, right_hand_fingers, left_hand_fingers):
    if len(right_hand_fingers) > 0:
        # detect Thumbs coordinate whether inside palm or outside
        if right_hand_fingers[tipsId[0]]['x'] > right_hand_fingers[tipsId[0]-1]['x']:
            fingers.append(0)
        else:
            fingers.append(1)

        # other fingers
        for id in range(1,5):
            if right_hand_fingers[tipsId[id]]['y'] < right_hand_fingers[tipsId[id]-2]['y']:
                fingers.append(1)
            else:
                fingers.append(0)

    if len(left_hand_fingers) > 0:
        # detect Thumbs coordinate whether inside palm or outside
        if left_hand_fingers[tipsId[0]]['x'] < left_hand_fingers[tipsId[0]-1]['x']:
            fingers.append(0)
        else:
            fingers.append(1)
        # other fingers
        for id in range(1,5):
            if left_hand_fingers[tipsId[id]]['y'] < left_hand_fingers[tipsId[id]-2]['y']:
                fingers.append(1)
            else:
                fingers.append(0)
    return fingers

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.8)

tipsId = [4, 8, 12, 16, 20]

camera = cv2.VideoCapture(1)


while True:
    _, frame = camera.read()
    # flip frame
    frame =  cv2.flip(frame, 1)
    # getting frame width, height, center
    h, w, c = frame.shape
    # get hands
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    labels = []
    right_hand_fingers = []
    left_hand_fingers = []

    # Detect Hand Label (Right/Left)
    labels = get_hand_labels(results, labels)

    # Drawing Hand Landmarks
    right_hand_fingers, left_hand_fingers = drawing_hand_landmarks(results, right_hand_fingers, 
                                                                    left_hand_fingers)
    

    
    # Detect Fingers
    total_fingers = -1
    fingers = []

    fingers = configure_fingers(fingers, right_hand_fingers, left_hand_fingers)
        
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
    
    if total_fingers != -1:
        text = f'Number: {total_fingers}'
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
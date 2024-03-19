import cv2
import queue
import mediapipe as mp
import numpy as np

imgs = queue.Queue()

def on_image(image):
    imgs.put(image)

# Initialize VideoCapture object to capture from your camera
cap = cv2.VideoCapture(0)  # You might need to change the index if you have multiple cameras
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


# Hand landmark IDs
base = 0
thumb = [4, 3, 2, 1]    # From tip of finger to knuckle
index = [8, 7, 6, 5]
middle = [12, 11, 10, 9]
ring = [16, 15, 14, 13]
pinky = [20, 19, 18, 17]

while True:
    ret, frame = cap.read()
    if not ret:
        break

    on_image(frame)

    imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

        thumb_tip = results.multi_hand_landmarks[0].landmark[thumb[0]]
        index_tip = results.multi_hand_landmarks[0].landmark[index[0]]
        middle_tip = results.multi_hand_landmarks[0].landmark[middle[0]]
        ring_tip = results.multi_hand_landmarks[0].landmark[ring[0]]
        pinky_tip = results.multi_hand_landmarks[0].landmark[pinky[0]]

        tip_ys = np.array([thumb_tip.y, index_tip.y, middle_tip.y, ring_tip.y, pinky_tip.y])
        var = np.var(tip_ys)

        if index_tip.y < middle_tip.y - 0.1:
            print("Up")
        elif var <= 0.005:
            print("Down")
        elif np.sqrt((thumb_tip.x - index_tip.x)** 2 + (thumb_tip.y - index_tip.y)** 2) <= 0.05:
            print("Land")    
        else:
            print("Hover")


    cv2.imshow("Output", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    


cap.release()
cv2.destroyAllWindows()

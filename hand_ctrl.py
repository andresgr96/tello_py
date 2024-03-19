import time
import cv2
import keyboard
import cv2
import queue
import mediapipe as mp
import numpy as np
from threading import Thread
from djitellopy import Tello


# Start and connect to tello
tello = Tello()
tello.connect()

# Setup
keepRecording = True
command = "hover"
tello.streamon()
frame_read = tello.get_frame_read()

imgs = queue.Queue()

def on_image(image):
    imgs.put(image)

# camera and mp setup
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


def live_img():
    while keepRecording:
        imageRGB = cv2.cvtColor(frame_read.frame, cv2.COLOR_BGR2RGB)
        cv2.imshow("Tello Feed", imageRGB)
        cv2.waitKey(1)
        time.sleep(1 / 30)


def controller():
    global keepRecording

    while keepRecording:
        ret, frame = cap.read()
        if not ret:
            break
        imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(imageRGB)
        if keyboard.is_pressed('esc'):
            break
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
                tello.move_up(20)
                print("Up")
            elif var <= 0.005:
                print("Down")
                tello.move_down(20)
            elif np.sqrt((thumb_tip.x - index_tip.x)** 2 + (thumb_tip.y - index_tip.y)** 2) <= 0.05:
                print("Land")
                tello.land()
                keepRecording = False    
            else:
                print("Hover")


# Start the threads
control = Thread(target=controller)
camera = Thread(target=live_img)
control.start()
camera.start()

# Takeoff
tello.takeoff()

# Wait for the threads to finish
control.join()
camera.join()
if not keepRecording:
    tello.end()

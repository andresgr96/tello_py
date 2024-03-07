import time
import cv2
import keyboard
from threading import Thread
from djitellopy import Tello

# ... (your existing imports)

# Start and connect to tello
tello = Tello()
tello.connect()

keepRecording = True
tello.streamon()
frame_read = tello.get_frame_read()

def live_img():
    height, width, _ = frame_read.frame.shape

    while keepRecording:
        cv2.imshow("henlo", frame_read.frame)
        cv2.waitKey(1)
        time.sleep(1 / 30)

# def controller():
#     while keepRecording:
#         if keyboard.is_pressed('esc'):
#             break
#         elif keyboard.is_pressed('w'):
#             print("hhh")
#             tello.move_forward(30)
#         elif keyboard.is_pressed('s'):
#             tello.move_back(30)
#         elif keyboard.is_pressed('a'):
#             tello.move_left(30)
#         elif keyboard.is_pressed('d'):
#             tello.move_right(30)
#         elif keyboard.is_pressed('e'):
#             tello.rotate_clockwise(30)
#         elif keyboard.is_pressed('q'):
#             tello.rotate_counter_clockwise(30)
#         elif keyboard.is_pressed('r'):
#             tello.move_up(30)
#         elif keyboard.is_pressed('f'):
#             tello.move_down(30)
#         elif keyboard.is_pressed('l'):
#             tello.land()
#
# # ... (rest of your code)
#
# # Start the threads
# control = Thread(target=controller)
camera = Thread(target=live_img)
# control.start()
camera.start()

# ... (rest of your code)




tello.takeoff()

# tello.land()
keepRecording = False
# control.join()
camera.join()

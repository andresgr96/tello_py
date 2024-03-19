import cv2
import queue
import mediapipe as mp

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
        print(results.multi_hand_landmarks[0].landmark[12])
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 12:
                    cv2.circle(frame, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
                    print(lm.y)
            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    cv2.imshow("Output", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    


cap.release()
cv2.destroyAllWindows()

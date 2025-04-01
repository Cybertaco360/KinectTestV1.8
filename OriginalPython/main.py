import cv2
from cvzone.HandTrackingModule import HandDetector
import socket
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

width, height = 1920, 1080
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = HandDetector(detectionCon=0.8, maxHands=1)

communication = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_port = ("127.0.0.1", 5052)

while True:
    success, img = cap.read()
    if not success:
        continue  # Skip frame if camera fails

    img = cv2.resize(img, (width, height))  # Ensure square input
    hands, img = detector.findHands(img)

    data = []
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        for lm in lmList:
            data.extend([lm[0], height - lm[1], lm[2]])

        communication.sendto(str.encode(str(data)), server_port)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
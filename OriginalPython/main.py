import cv2
import numpy as np
import socket
import os
from cvzone.HandTrackingModule import HandDetector

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

width, height = 1920, 1080

# Initialize UDP sockets
infrared_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
infrared_socket.bind(("127.0.0.1", 5052))  # Match the C# sender's IP and port

unity_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
unity_server_port = ("127.0.0.1", 5053)  # Port for sending data to Unity

# Initialize OpenCV hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

while True:
    # Receive infrared image data
    data, _ = infrared_socket.recvfrom(640 * 480 * 2)  # 640x480 resolution, 2 bytes per pixel (Gray16)
    infrared_image = np.frombuffer(data, dtype=np.uint16).reshape((480, 640))

    # Normalize and convert to 8-bit for display
    infrared_image = cv2.normalize(infrared_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Process the infrared image for hand tracking
    hands, img = detector.findHands(infrared_image)

    hand_data = []
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        for lm in lmList:
            hand_data.extend([lm[0], height - lm[1], lm[2]])

        # Send hand tracking data to Unity
        unity_socket.sendto(str.encode(str(hand_data)), unity_server_port)

    # Display the infrared image
    cv2.imshow("Infrared Image", infrared_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
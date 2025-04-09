import cv2
import numpy as np
import socket
import os
import struct
from cvzone.HandTrackingModule import HandDetector

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

FRAME_SIZE = 640 * 480 * 2  # Expected size of full frame
TIMEOUT = 2.0  # Socket timeout

# Initialize TCP socket
infrared_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
infrared_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
infrared_socket.bind(("127.0.0.1", 5052))
infrared_socket.listen(1)

# Initialize Unity UDP socket
unity_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
unity_server_port = ("127.0.0.1", 5053)

print("Listening for incoming TCP connection...")

# Wait for a client to connect
client_socket, client_address = infrared_socket.accept()
print(f"Connection established with {client_address}")

# OpenCV Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

try:
    while True:
        received_data = b""  # Buffer to store full image data

        # Receive the full image data
        while len(received_data) < FRAME_SIZE:
            packet = client_socket.recv(8192)  # Receive in chunks
            if not packet:
                print("No data received. Connection closed.")
                break
            received_data += packet
            print(f"Received {len(packet)} bytes, total {len(received_data)}/{FRAME_SIZE}")

        # Ensure the received data is exactly FRAME_SIZE
        if len(received_data) != FRAME_SIZE:
            print("Warning: Incomplete frame received, discarding")
            continue

        # Convert raw data to infrared image
        infrared_image = np.frombuffer(received_data, dtype=np.uint16).reshape((480, 640))

        # Normalize and convert to 8-bit
        infrared_image = cv2.normalize(infrared_image, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

        # Apply a colormap for better visualization
        infrared_image_colormap = cv2.applyColorMap(infrared_image, cv2.COLORMAP_JET)

        # Convert grayscale to BGR for `cvzone`
        img_bgr = cv2.cvtColor(infrared_image, cv2.COLOR_GRAY2BGR)

        # Process image with hand tracking
        hands, img = detector.findHands(img_bgr)

        hand_data = []
        if hands:
            hand = hands[0]
            lmList = hand['lmList']
            for lm in lmList:
                hand_data.extend([lm[0], 480 - lm[1], lm[2]])  # Flip Y correctly

            # Send hand tracking data to Unity
            unity_socket.sendto(struct.pack('f' * len(hand_data), *hand_data), unity_server_port)

        # Display the infrared image with colormap
        cv2.imshow("Infrared Image", infrared_image_colormap)
        cv2.imshow("Hands", img)  # Display the image with hand landmarks

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error: {e}")

finally:
    # Ensure sockets and resources are closed properly
    cv2.destroyAllWindows()
    client_socket.close()
    infrared_socket.close()

import cv2
import serial
import serial.tools.list_ports
import time
from tensorflow.keras.models import load_model
import numpy as np
import os

# Load your trained model
model = load_model('waste_classification_model.keras')

# Function to find and connect to Arduino
def find_arduino():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "Arduino" in port.description:
            try:
                arduino_conn = serial.Serial(port.device, 9600, timeout=1)
                time.sleep(2)  # Allow Arduino time to initialize
                print(f"Connected to Arduino on {port.device}")
                return arduino_conn
            except serial.SerialException as e:
                print(f"Error connecting to Arduino: {e}")
    print("Arduino not found. Please check the connection.")
    return None

# Initialize serial communication
arduino = find_arduino()

# Open the video capture
cap = cv2.VideoCapture('http://10.10.7.162:8080/video')
if not cap.isOpened():
    print("Error: Could not open video source")
    exit()

# Define categories and angles
categories = {
    "Plastic": 0,
    "Glass": 45,
    "Metal": 90,
    "Paper": 135,
    "Cardboard": 180,
    "Trash": 180
}

# Create directories for categories if they don't already exist
for category in categories.keys():
    if not os.path.exists(category):
        os.makedirs(category)

# Function to preprocess the frame
def preprocess_frame(frame):
    img = cv2.resize(frame, (150, 150))
    img = img.astype('float32') / 255
    img = np.expand_dims(img, axis=0)
    return img

# Function to send data to Arduino
def send_to_arduino(letter, angle):
    if arduino:
        command = f"{letter},{angle}\n"
        try:
            arduino.flushOutput()  # Clear output buffer
            arduino.write(command.encode())
            print(f"Sent to Arduino: '{command.strip()}'")
            time.sleep(0.5)  # Allow Arduino to process
            response = arduino.readline().decode().strip()
            if response:
                print(f"Arduino response: {response}")
        except serial.SerialException as e:
            print(f"Serial error: {e}. Retrying...")
            time.sleep(1)
            try:
                arduino.write(command.encode())
                print(f"Retry successful: '{command.strip()}' sent to Arduino.")
            except serial.SerialException as retry_error:
                print(f"Retry failed: {retry_error}")
                print("Check Arduino connection and COM port.")
    else:
        print("Arduino is not connected. Skipping communication.")

# Main loop
image_counter = 0  # Counter for saved images
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame")
        break

    # Define the circle position (top-center of the frame)
    frame_height, frame_width = frame.shape[:2]
    circle_radius = 300  # Increased radius of the circle
    circle_center = (frame_width // 2, frame_height // 4)  # Top-center of the frame

    # Draw the circle on the frame
    cv2.circle(frame, circle_center, circle_radius, (0, 255, 0), 3)  # Green circle as a guide

    # Display the video feed with instructions
    cv2.putText(frame, "Place object inside the circle. Press 'c' to classify. Press 'q' to quit.",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.imshow('Video Feed', frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):  # Capture and classify on 'c'
        # Crop the region of interest (ROI) inside the circle
        mask = np.zeros_like(frame)
        cv2.circle(mask, circle_center, circle_radius, (255, 255, 255), -1)
        roi = cv2.bitwise_and(frame, mask)

        # Preprocess the ROI for classification
        img = preprocess_frame(roi)
        prediction = model.predict(img)
        class_index = np.argmax(prediction, axis=1)[0]
        result = list(categories.keys())[class_index]
        angle = categories[result]

        print(f"Classification result: {result}")
        send_to_arduino(result[0], angle)

        # Save the ROI to the corresponding category folder
        folder_path = os.path.join(result)  # Folder name is the classification result
        image_path = os.path.join(folder_path, f"{result}_{image_counter}.jpg")
        cv2.imwrite(image_path, roi)  # Save the cropped ROI image
        print(f"Image saved at {image_path}")

        image_counter += 1  # Increment the counter for the next image

    elif key == ord('q'):  # Quit on 'q'
        print("Exiting program.")
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()

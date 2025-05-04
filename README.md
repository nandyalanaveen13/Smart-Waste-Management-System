This project is a Smart Waste Management System that combines Deep Learning, Arduino-based hardware, and servo motors to create an intelligent, automated waste-sorting solution. The system is designed to identify and categorize waste (e.g., plastic, metal, paper, organic) using a trained machine learning model and perform sorting actions in real-time through servo-controlled bins. 

**Technologies Used:**
1. Deep Learning (TensorFlow/Keras): For image classification of waste types.
2. Arduino Uno: Microcontroller to control the hardware components.
3. Servo Motors: To automatically open/close the correct waste bin based on prediction.
4. Python: For training the deep learning model and interfacing with Arduino.
5. OpenCV: For image processing and camera feed handling.
6. Serial Communication (PySerial): To send commands from the Python server to the Arduino.
7. Wires & Sensors: Used to connect and control the physical components.

**Features**
1. Waste is classified into multiple categories using a trained CNN model.
2. Real-time camera input for detecting waste.
3. Servo motors automatically sort detected waste into the correct bins.
4. Easy to retrain or update the model with new categories.
5. Modular design for easy hardware integration.

**How to Run**
1. Clone the repo:
git clone https://github.com/nandyalanaveen13/Smart-Waste-Management-System.git
cd Smart-Waste-Management-System

2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate  # Windows

3. Install Python dependencies:
pip install -r requirements.txt

4. Upload the Arduino code:
Open arduino/sorter.ino in the Arduino IDE and upload it to your board.

5. Run the server (camera + classification):
python server/main.py

Demo video:https://drive.google.com/file/d/1OMCCgW3Zf90VtszEfsAMC3CnPSmyIqSV/view?usp=sharing

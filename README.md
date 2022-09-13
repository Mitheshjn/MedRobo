# MedRobo

**Autonomous Medicine distrbution rover with QR detection**

This was my final year project in my Under Graduate degree as a Robotics & Automation engineer.
The project was aimed to substitute the role of medical staff for medicine distribution to the patients potentially having affected by CoVid-19 virus. But the robot can be also used for general patients and can reduce human staff from coming in direct contact with the patients.

**Synopsis**

So, basically this rover has its own server where the doctor enters the patient name, disease, door no, bed no and the medicines needed to be given to the particular patient. Once the details are feeded in the database the robot starts distrbuting the medicines. The camera attached in the front is used to scan QR code which is attached on the walls of the hospital to navigate across various rooms and paths. The robot navigates its way to the patient bed and dispenses the assigned medicines to the patients. The process continues until all patients have recived their medicine and after that the rover returns back to its initial position/ start position.

**Materials required :**
* Arduino Uno (or any micro-controller)
* Raspberry Pi (3 or 4 with atlest 4GB ram or can also use any similar spec micro-processor/computer)
* 8 DC motors (4 for rover & 4 for 4 types of medicine)
* 3 motor driver (1 for rover and 2 for medicine distribution system)
* 12V DC battery
* Connecting wires
* Web cam / any compatible camera with raspberry pi
* Coil wire
* Sun Board

**Material Explaination :**

**Raspberry Pi : ** This is the main brain of the rover and it basically controls the every action of the rover. It recives input from camera and processes it and sends commands to the motor drivers via the arduino uno.

**Arduino Uno : ** The uno is used to control the all the motors in the robot. The reason behind using arduino is that the raspberry pi gets overloaded by processing the camera input and does the path planning and the server is hosted in the pi itself so, to reduce the load from the raspberry pi i am using arduino. The raspberry pi and arduino communicates via the USB cable using serial communication.


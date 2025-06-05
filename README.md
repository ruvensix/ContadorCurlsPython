# ContadorCurlsPython

Curl Counter with Pose Detection (Mediapipe and OpenCV)
This Python project uses the MediaPipe and OpenCV libraries to detect a person's pose from a video feed (webcam) and specifically count arm curl repetitions.

Features
Real-time Pose Detection: Uses MediaPipe to identify 33 body landmarks in real-time, drawing a "skeleton" over the person in the video feed.
Angle Calculation: Calculates the elbow angle to monitor arm flexion and extension.
Curl Counter:
Monitors the elbow angle to determine the "down" (arm extended) and "up" (arm flexed) stages of a curl.
Increments a counter each time a complete curl is detected.
Console Output: The number of repetitions is printed in the console.
Visual Overlay: Displays the elbow angle and the repetition counter directly on the video feed, making it an interactive tool for exercise.
Prerequisites
To run this project, you need to have Python installed, along with the mediapipe, opencv-python, and numpy libraries.

You can install them using pip:

Bash
pip install mediapipe opencv-python numpy


How to Run
Connect a webcam to your computer.

Save the code I provided you in a Python file (curl_counter.py).

Open your terminal or command prompt.

Navigate to the folder where you saved the file.

Execute the script using Python:

Bash
python curl_counter.py


An OpenCV window will open, showing your webcam feed with pose detection.

To exit, press the q key on your keyboard while the video window is active.

How the Counting Works (Curl Logic)
The curl counter works by monitoring the left elbow angle:

When the elbow angle is above 160 degrees, the arm is considered "down" (extended). The stage is set to "down".
When the elbow angle drops below 30 degrees AND the previous stage was "down", it means a curl has been completed. The stage changes to "up", and the counter is incremented.
This ensures that only complete and correct curls are counted.
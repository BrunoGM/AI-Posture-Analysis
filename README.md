# Real-time Posture Analysis Tool

## Introduction

This Python script provides a real-time posture analysis using your webcam and the power of MediaPipe. It analyzes your posture by tracking key body points (shoulders and nose) and calculating a normalized height that reflects your sitting or standing posture.

The tool provides feedback on your posture in real-time, classifying it as "Good Posture," "Medium Posture," or "Bad Posture."  If bad posture is detected for a prolonged period, it will alert you with a beep sound to remind you to correct your posture.  At the end of the session (when you press 'q' to quit), it generates a plot of your posture over time and a summary of your posture quality.

This tool is designed to help you be more mindful of your posture while working or using your computer, encouraging healthier habits.

## How to Use

Follow these steps to use the Posture Analysis Tool:

1.  **Installation:** Ensure you have Python installed on your system. Then, install the necessary libraries by running the following command in your terminal or command prompt:

    ```bash
    pip install opencv-python mediapipe numpy matplotlib winsound
    ```

2.  **Run the Script:** Save the provided Python code (at the end of this README) as a Python file (e.g., `posture_analysis.py`). Navigate to the directory where you saved the file in your terminal and run the script using:

    ```bash
    python posture_analysis.py
    ```

3.  **Calibration:** When the webcam feed appears, you will see the message "Pressione 'c' para calibrar" (Press 'c' to calibrate). **Sit or stand in your ideal posture** and press the `c` key. This will calibrate the tool to your good posture, establishing a baseline for comparison. You will see a "Calibracao Completa" (Calibration Complete) message on the screen when it's done.

4.  **Posture Analysis in Real-time:** After calibration, the tool will start analyzing your posture.
    *   Real-time feedback will be displayed on the video feed, indicating "Boa Postura" (Good Posture), "Postura Media" (Medium Posture), or "Ma Postura" (Bad Posture). The text color will also change to visually represent the posture status (Green for Good, Yellow for Medium, Red for Bad).
    *   A normalized height value is also displayed, representing the posture metric being analyzed.
    *   If "Ma Postura" is detected for a certain duration, you will hear a beep sound as a reminder to adjust your posture.

5.  **Stop and Analyze Results:** To stop the posture analysis, press the `q` key.
    *   After quitting, the script will generate a plot showing the variation of your posture over time. This plot will display the "Normalized Height" and a horizontal line representing your calibrated height.
    *   A summary of your posture analysis will also be printed in the console, including:
        *   Total recording time.
        *   Percentage of time spent in "Boa Postura," "Postura Media," and "Ma Postura."

## Installation

To run this tool, you need to install the following Python libraries. Use pip to install them:

```bash
pip install opencv-python mediapipe numpy matplotlib winsound
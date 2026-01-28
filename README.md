# Air Mouse 🖱️✋

**Air Mouse** is an AI-powered virtual mouse system that allows you to control your computer cursor and perform clicks using hand gestures captured by your webcam. Built with **Python**, **OpenCV**, and **MediaPipe**, it offers a touch-free, futuristic way to interact with your PC.

## ✨ Features

-   **Two-Handed Control**:
    -   **Right Hand (Real)**: Controls the cursor movement with smooth, jitter-free tracking.
    -   **Left Hand (Real)**: Performs click actions using pinch gestures.
-   **Gesture Recognition**:
    -   **Left Click**: Pinch **Thumb + Index Finger** (Left Hand).
    -   **Right Click**: Pinch **Thumb + Middle Finger** (Left Hand).
-   **Real-Time Performance**: Optimized for low latency and high FPS (≥ 25 FPS).
-   **Visual Feedback**: On-screen markers show hand landmarks and click status.
-   **Always-on-Top Preview**: The webcam feed stays visible so you can monitor your gestures.

## 🛠️ Tech Stack

-   **Language**: Python 3.x
-   **Computer Vision**: OpenCV (`opencv-python`)
-   **Hand Tracking**: Google MediaPipe (`mediapipe`)
-   **GUI Control**: PyAutoGUI (`pyautogui`)
-   **Math**: NumPy (`numpy`)

## ⚙️ Prerequisites

Ensure you have **Python 3.7+** installed. You will also need a working webcam.

## 🚀 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Amish-03/Air_Mouse.git
    cd Air_Mouse
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install opencv-python mediapipe pyautogui numpy
    ```
    *Note: If you encounter issues with MediaPipe, try installing version `0.10.14` specifically.*

## 🎮 Usage

1.  **Run the Application**
    ```bash
    python main.py
    ```

2.  **How to Control**
    -   **Cursor**: Show your **Real Right Hand** to the camera. Move your hand to move the mouse pointer.
    -   **Left Click**: Show your **Real Left Hand**. Pinch your **Index Finger** and **Thumb** together.
    -   **Right Click**: Show your **Real Left Hand**. Pinch your **Middle Finger** and **Thumb** together.

3.  **Exit**
    -   Press `q` while the webcam window is active to quit.

## 📝 Notes
-   Lighting conditions affect tracking accuracy. Ensure your hands are well-lit.
-   The system identifies "Right" and "Left" hands based on standard webcam mirroring. If it feels swapped, ensure you are using the correct hand for each role defined above.

## 📄 License
This project is open-source. Feel free to modify and distribute!
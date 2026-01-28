
import cv2
import numpy as np
import pyautogui
import time
from hand_tracking import HandDetector
from cursor_control import MouseController
from gesture_clicks import GestureDetector

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

def main():
    cap = cv2.VideoCapture(0)
    width, height = 640, 480
    cap.set(3, width)
    cap.set(4, height)
    
    scr_w, scr_h = pyautogui.size()
    
    # Enable tracking for 2 hands
    detector = HandDetector(maxHands=2, detectionCon=0.7)
    mouse = MouseController(scr_w, scr_h, width, height)
    gesture = GestureDetector()
    
    pTime = 0

    print("System Active. Press 'q' to exit.")
    print("RIGHT HAND: Cursor Control")
    print("LEFT HAND: Pinch Actions (Index+Thumb=Left Click, Middle+Thumb=Right Click)")

    while True:
        success, img = cap.read()
        if not success:
            break
            
        # Processing unflipped image for correct logic
        img = detector.find_hands(img)
        hands_info = detector.get_hands_info(img, draw=False)
        
        # Display image (Flipped)
        img_display = cv2.flip(img, 1)
        
        for hand in hands_info:
            hand_type = hand['type'] # 'Left' or 'Right'
            lmList = hand['lmList']
            
            # NOTE: If we do NOT flip the image input to MediaPipe:
            # - User's RIGHT Hand (facing camera) appears on LEFT side of image.
            # - MediaPipe interprets the image as it sees it.
            # - If MediaPipe assumes selfie/mirror mode (default?), it knows "Left side of image = Right Hand".
            # - CHECK: MediaPipe returns "Right" for user's Right hand usually.
            

            # Logic:
            # User reported: Real Left is interpreted as Virtual Right (and vice versa).
            # We want: Real Right -> Cursor, Real Left -> Clicks.
            # So:
            # Virtual 'Left' (Real Right) -> Mouse Control
            # Virtual 'Right' (Real Left) -> Click Control
            
            if hand_type == 'Left':
                # Cursor Control (Real Right Hand)
                if len(lmList) > 8:
                    x1, y1 = lmList[8][1], lmList[8][2]
                    try:
                        curr_x, curr_y = mouse.get_cursor_position(x1, y1)
                        pyautogui.moveTo(curr_x, curr_y)
                        
                        # Draw feedback on display image (Must flip coordinates)
                        # Coordinates x1, y1 are in original image space.
                        # Flipped x = Width - x1
                        cv2.circle(img_display, (width - x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    except:
                        pass
                        
            elif hand_type == 'Right':
                # Click Control (Real Left Hand) -> Pinch
                
                # Check Left Click Pattern (Index + Thumb)
                if gesture.check_left_click(lmList):
                    pyautogui.click()
                    cv2.putText(img_display, "Left Click", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    
                # Check Right Click Pattern (Middle + Thumb)
                elif gesture.check_right_click(lmList):
                    pyautogui.click(button='right')
                    cv2.putText(img_display, "Right Click", (200, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                
                # Draw feedback for left hand (Thumb/Index/Middle)
                # Flip x coords
                for idx in [4, 8, 12]:
                    # Draw tips
                    cx, cy = lmList[idx][1], lmList[idx][2]
                    cv2.circle(img_display, (width - cx, cy), 10, (0, 255, 0), cv2.FILLED)

        # FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img_display, f'FPS: {int(fps)}', (10, height - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        

        cv2.imshow("Hand Gesture Mouse", img_display)
        # Set Window Always on Top
        cv2.setWindowProperty("Hand Gesture Mouse", cv2.WND_PROP_TOPMOST, 1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

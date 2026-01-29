import cv2
import numpy as np
import pyautogui
import time
from hand_tracking import HandDetector
from cursor_control import MouseController

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

def main():
    cap = cv2.VideoCapture(0)
    width, height = 640, 480
    cap.set(3, width)
    cap.set(4, height)
    
    scr_w, scr_h = pyautogui.size()
    
    # Enable tracking for 1 hand (Right Hand focus)
    detector = HandDetector(maxHands=1, detectionCon=0.7)
    mouse = MouseController(scr_w, scr_h, width, height)
    
    pTime = 0
    
    # State for clicks
    left_click_active = False
    right_click_active = False

    print("System Active. Press 'q' to exit.")
    print("RIGHT HAND CONTROL MODE")
    print("- Ensure Index Finger is UP to move cursor.")
    print("- Extend Thumb for LEFT CLICK.")
    print("- Extend Middle Finger for RIGHT CLICK.")

    while True:
        success, img = cap.read()
        if not success:
            break
            
        # Find hands (Unflipped - Real Right appears as MediaPipe 'Left')
        img = detector.find_hands(img)
        hands_info = detector.get_hands_info(img, draw=False)
        
        # Display image (Flipped for Mirror View)
        img_display = cv2.flip(img, 1)
        
        for hand in hands_info:
            hand_type = hand['type']
            lmList = hand['lmList']
            
            # Real Right Hand is detected as 'Left' in unflipped mode
            if hand_type == 'Left':
                # Use 'Right' logic for thumb detection because it IS the Right hand
                fingers = detector.fingers_up(lmList, "Right")
                # fingers layout: [Thumb, Index, Middle, Ring, Pinky]
                
                # Check control condition: Index Finger must be UP (fingers[1])
                # We allow cursor movement if Index is UP, regardless of other fingers temporarily.
                if fingers[1] == 1:
                    # 1. Move Cursor
                    x1, y1 = lmList[8][1], lmList[8][2] # Index Tip
                    
                    try:
                        curr_x, curr_y = mouse.get_cursor_position(x1, y1)
                        pyautogui.moveTo(curr_x, curr_y)
                        
                        # Visual Feedback for Pointer
                        # Flip x for display: Width - x1
                        cv2.circle(img_display, (width - x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    except Exception as e:
                        pass

                    # 2. Check Left Click (Thumb Extended)
                    # Thumb is fingers[0]
                    if fingers[0] == 1:
                        if not left_click_active:
                            pyautogui.click()
                            left_click_active = True
                            print("Left Click")
                        cv2.putText(img_display, "Left Click", (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    else:
                        left_click_active = False
                        
                    # 3. Check Right Click (Middle Finger Extended)
                    # Middle is fingers[2]
                    if fingers[2] == 1:
                        if not right_click_active:
                            pyautogui.click(button='right')
                            right_click_active = True
                            print("Right Click")
                        cv2.putText(img_display, "Right Click", (200, 50), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                    else:
                        right_click_active = False

        # FPS calculation
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img_display, f'FPS: {int(fps)}', (10, height - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
        
        cv2.imshow("Hand Gesture Mouse", img_display)
        # Keep window on top
        cv2.setWindowProperty("Hand Gesture Mouse", cv2.WND_PROP_TOPMOST, 1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

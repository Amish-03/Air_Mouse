
import cv2
import mediapipe as mp
import time

class HandDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img


    def find_position(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            if handNo < len(self.results.multi_hand_landmarks):
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)
        return lmList

    def get_hands_info(self, img, draw=True):
        hands_info = []
        if self.results.multi_hand_landmarks:
            for idx, hand_lms in enumerate(self.results.multi_hand_landmarks):
                # Get Label ('Left' or 'Right')
                # Note: MediaPipe assumes mirrored input by default?
                # The label in multi_handedness refers to the specific hand classification.
                # If static_image_mode=False, it tracks.
                
                handedness = self.results.multi_handedness[idx].classification[0].label
                
                lmList = []
                for id, lm in enumerate(hand_lms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_lms, self.mpHands.HAND_CONNECTIONS)
                    
                hands_info.append({'type': handedness, 'lmList': lmList})
        
        return hands_info

    def fingers_up(self, lmList, hand_type="Right"):
        """
        Returns a list of 5 booleans [Thumb, Index, Middle, Ring, Pinky]
        True if finger is extended (up/out), False otherwise.
        """
        fingers = []
        # Tip Ids
        tip_ids = [4, 8, 12, 16, 20]

        # Thumb
        # For Right Hand: Thumb is to the Left of the hand (smaller X) when palm is facing camera?
        # WAIT: MediaPipe coordinate system: Top-Left is (0,0).
        # Right hand facing camera: Thumb is on the Left side of the hand (smaller X).
        # IF Hand is flipped (Selfie view)? 
        # Let's rely on Relative X.
        # If Right Hand: Thumb Tip x < Thumb IP x (4 < 3) => Open/Extended (if palm faces camera)
        
        # NOTE: This depends heavily on orientation.
        # Simple check: Is Thumb Tip further from MCP than IP is? (Distance based)
        # Or Just use X check assuming standard upright usage.
        
        # Assumption: "Right Hand" usually means the hand detected as Right.
        # If user holds right hand up, thumb is on the left side of the screen image?
        # Let's blindly trust the implementation that usually works for "upright" hand:
        if hand_type == "Right":
            # Inverted logic as per user request: Tip > IP means extended
            if lmList[tip_ids[0]][1] > lmList[tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else: # Left Hand
            if lmList[tip_ids[0]][1] > lmList[tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            # Check Y-axis (Tip < PIP) -> "Up"
            # Note: Y increases downwards. So Tip < PIP means Tip is higher.
            if lmList[tip_ids[id]][2] < lmList[tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lmList = detector.find_position(img)
        if len(lmList) != 0:
            print(lmList[4]) # Print Thumb tip Position

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()

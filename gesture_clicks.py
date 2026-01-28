
import math

class GestureDetector:
    def __init__(self, click_threshold=30):
        self.click_threshold = click_threshold
        # Debounce to prevent multiple clicks
        self.left_click_active = False 
        self.right_click_active = False

    def find_distance(self, p1, p2):
        x1, y1 = p1[1], p1[2]
        x2, y2 = p2[1], p2[2]
        length = math.hypot(x2 - x1, y2 - y1)
        return length

    def detect_pinch(self, lmList, finger_tip_id, thumb_tip_id=4, threshold_scale=0.1):
        """
        Detects if finger_tip is touching thumb_tip.
        Returns distance and boolean state.
        """
        if len(lmList) < 21:
            return 1000, False
            
        x1, y1 = lmList[finger_tip_id][1], lmList[finger_tip_id][2]
        x2, y2 = lmList[thumb_tip_id][1], lmList[thumb_tip_id][2]
        
        length = math.hypot(x2 - x1, y2 - y1)
        
        # Dynamic Threshold based on palm size (Wrist to Middle Finger MCP)
        scale_ref = self.find_distance(lmList[0], lmList[9])
        
        if length < scale_ref * threshold_scale:
            return length, True
        return length, False

    def check_left_click(self, lmList):
        # Index (8) and Thumb (4) Pinch
        dist, state = self.detect_pinch(lmList, 8, 4, threshold_scale=0.25)
        
        if state:
            if not self.left_click_active:
                self.left_click_active = True
                return True
        else:
            self.left_click_active = False
        return False

    def check_right_click(self, lmList):
        # Middle (12) and Thumb (4) Pinch
        dist, state = self.detect_pinch(lmList, 12, 4, threshold_scale=0.25)
        
        if state:
            if not self.right_click_active:
                self.right_click_active = True
                return True
        else:
            self.right_click_active = False
        return False

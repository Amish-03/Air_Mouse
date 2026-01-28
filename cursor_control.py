
import numpy as np
import pyautogui

class MouseController:
    def __init__(self, scr_w, scr_h, cam_w, cam_h, smoothing=5):
        self.scr_w = scr_w
        self.scr_h = scr_h
        self.cam_w = cam_w
        self.cam_h = cam_h
        self.smoothing = smoothing
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0
        self.frame_r = 100 # Frame Reduction (dead zone border)

    def get_cursor_position(self, tip_x, tip_y):
        # 1. Convert Coordinates
        # Use numpy.interp to map the range from webcam coordinates (with dead zone) to screen coordinates
        # tip_x is mapped from (frame_r, cam_w - frame_r) to (0, scr_w)
        # tip_y is mapped from (frame_r, cam_h - frame_r) to (0, scr_h)
        
        x = np.interp(tip_x, (self.frame_r, self.cam_w - self.frame_r), (0, self.scr_w))
        y = np.interp(tip_y, (self.frame_r, self.cam_h - self.frame_r), (0, self.scr_h))

        # 2. Smooth Values
        self.curr_x = self.prev_x + (x - self.prev_x) / self.smoothing
        self.curr_y = self.prev_y + (y - self.prev_y) / self.smoothing

        self.prev_x, self.prev_y = self.curr_x, self.curr_y

        return self.scr_w - self.curr_x, self.curr_y # Mirror X for natural movement

from collections import deque

class HandState:
    def __init__(self):
        self.gesture_locked = {'Left': False, 'Right': False}
        self.gesture_start_time = {'Left': 0, 'Right': 0}
        self.buffer_start_time = {'Left': 0, 'Right': 0}
        self.start_drag_time = {'Left': 0, 'Right': 0}
        self.dragging = {'Left': False, 'Right': False}
        self.drag_point = {'Left': (0, 0), 'Right': (0, 0)}
        self.buffer_duration = {'Left': 0.25, 'Right': 0.25}
        self.is_index_finger_up = {'Left': False, 'Right': False}
        self.index_finger_second = {'Left': 0, 'Right': 0}
        self.index_finger_tip = {'Left': 0, 'Right': 0}
        self.trajectory = {'Left': [], 'Right': []}
        self.square_queue = deque()
        self.wait_time = 1.5
        self.kalman_wait_time = 0.5
        self.wait_box = 2
        self.rect_draw_time = {'Left': 0, 'Right': 0}
        self.last_drawn_box = {'Left': None, 'Right': None}

    def clear_hand_states(self, detected_hand='Both'):

        hands_to_clear = {'Left', 'Right'}
        if detected_hand == 'Both':
            hands_to_clear = hands_to_clear
        else:
            hands_to_clear -= {detected_hand}

        for h in hands_to_clear:
            self.gesture_locked[h] = False
            self.gesture_start_time[h] = 0
            self.buffer_start_time[h] = 0
            self.dragging[h] = False
            self.drag_point[h] = (0, 0)
            self.buffer_duration[h] = 0.25
            self.is_index_finger_up[h] = False
            self.trajectory[h].clear()
            self.start_drag_time[h] = 0
            self.rect_draw_time[h] = 0
            self.last_drawn_box[h] = None
        # 用于记录左右手的信息 需要分开存放 否则可能会出现数据冲突

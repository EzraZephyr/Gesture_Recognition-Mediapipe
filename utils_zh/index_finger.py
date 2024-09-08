import cv2
import time
import numpy as np

class IndexFingerHandler:
    def __init__(self, hand_state, kalman_handler):
        self.hand_state = hand_state
        self.kalman_handler = kalman_handler
        self.wait_time = 1.5
        self.kalman_wait_time = 0.5
        self.wait_box = 2

    def handle_index_finger(self, image, hand_21, temp_handness, width, height):

        cz0 = hand_21.landmark[0].z
        self.hand_state.index_finger_second[temp_handness] = hand_21.landmark[7]
        self.hand_state.index_finger_tip[temp_handness] = hand_21.landmark[8]

        index_x = int(self.hand_state.index_finger_tip[temp_handness].x * width)
        index_y = int(self.hand_state.index_finger_tip[temp_handness].y * height)

        self.update_index_finger_state(hand_21, temp_handness, index_x, index_y)
        self.draw_index_finger_gesture(image, temp_handness, index_x, index_y, cz0)

        return image
        # 处理食指的状态和手势效果，并更新图像

    def update_index_finger_state(self, hand_21, temp_handness, index_x, index_y):

        if all(self.hand_state.index_finger_second[temp_handness].y < hand_21.landmark[i].y
               for i in range(21) if i not in [7, 8]) and \
                self.hand_state.index_finger_tip[temp_handness].y < self.hand_state.index_finger_second[temp_handness].y:
            self.hand_state.is_index_finger_up[temp_handness] = True
            # 如果食指指尖和第一个关节都大于其他关键点 则判定为食指抬起

        if self.hand_state.is_index_finger_up[temp_handness]:
            if not self.hand_state.gesture_locked[temp_handness]:
                if self.hand_state.gesture_start_time[temp_handness] == 0:
                    self.hand_state.gesture_start_time[temp_handness] = time.time()
                elif time.time() - self.hand_state.gesture_start_time[temp_handness] > self.wait_time:
                    self.hand_state.dragging[temp_handness] = True
                    self.hand_state.gesture_locked[temp_handness] = True
                    self.hand_state.drag_point[temp_handness] = (index_x, index_y)
                    # 如果食指指向操作已经超过了等待的时间 则设定为正式进行指向操作
                self.hand_state.buffer_start_time[temp_handness] = 0
                # 防止识别错误导致指向操作迅速中断的缓冲时间
        else:
            if self.hand_state.buffer_start_time[temp_handness] == 0:
                self.hand_state.buffer_start_time[temp_handness] = time.time()
            elif time.time() - self.hand_state.buffer_start_time[temp_handness] > self.hand_state.buffer_duration[temp_handness]:
                self.hand_state.gesture_start_time[temp_handness] = 0
                self.hand_state.gesture_locked[temp_handness] = False
                self.hand_state.dragging[temp_handness] = False
                # 如果食指指向操作的中断时间已经超过了设定的缓冲时间 则正式终断

    def draw_index_finger_gesture(self, image, temp_handness, index_x, index_y, cz0):

        if self.hand_state.dragging[temp_handness]:
            if self.hand_state.start_drag_time[temp_handness] == 0:
                self.hand_state.start_drag_time[temp_handness] = time.time()
                self.kalman_handler.reset_kalman_filter(temp_handness, index_x, index_y)
                # 如果是首次操作 则记录时间并重置kalman滤波器

            smooth_x, smooth_y = self.kalman_handler.kalman_filter_point(temp_handness, index_x, index_y)
            # 使用kalman滤波器平滑生成的轨迹 减少噪声和抖动

            self.hand_state.drag_point[temp_handness] = (index_x, index_y)
            index_finger_radius = max(int(10 * (1 + (cz0 - self.hand_state.index_finger_tip[temp_handness].z) * 5)), 0)
            cv2.circle(image, self.hand_state.drag_point[temp_handness], index_finger_radius, (0, 0, 255), -1)
            # 根据离掌根的距离同步调整圆圈大小 但是要比FingerDrawer的同比增大一些 可以看清是否锁定指向操作
            drag_point_smooth = (smooth_x, smooth_y)

            if time.time() - self.hand_state.start_drag_time[temp_handness] > self.kalman_wait_time:
                self.hand_state.trajectory[temp_handness].append(drag_point_smooth)
                # 因为滤波器初始化时需要时间稳定数据 所以等待其稳定后再将坐标点加到轨迹中
        else:
            if len(self.hand_state.trajectory[temp_handness]) > 4:
                contour = np.array(self.hand_state.trajectory[temp_handness], dtype=np.int32)
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                # 当拖拽点数大于4时则计算最小外接矩形
                self.hand_state.rect_draw_time[temp_handness] = time.time()
                self.hand_state.last_drawn_box[temp_handness] = box

            self.hand_state.start_drag_time[temp_handness] = 0
            self.hand_state.trajectory[temp_handness].clear()
            # 重置 清空

        for i in range(1, len(self.hand_state.trajectory[temp_handness])):
            pt1 = (int(self.hand_state.trajectory[temp_handness][i-1][0]), int(self.hand_state.trajectory[temp_handness][i-1][1]))
            pt2 = (int(self.hand_state.trajectory[temp_handness][i][0]), int(self.hand_state.trajectory[temp_handness][i][1]))
            cv2.line(image, pt1, pt2, (0, 0, 255), 2)
            # 绘制拖拽路径

        if self.hand_state.last_drawn_box[temp_handness] is not None:
            elapsed_time = time.time() - self.hand_state.rect_draw_time[temp_handness]
            if elapsed_time < self.wait_box:
                cv2.drawContours(image, [self.hand_state.last_drawn_box[temp_handness]], 0, (0, 255, 0), 2)
                # 为了方便观测 需要保留显示包围框一定时间
            elif elapsed_time >= self.wait_box - 0.1:
                box = self.hand_state.last_drawn_box[temp_handness]
                x_min = max(0, min(box[:, 0]))
                y_min = max(0, min(box[:, 1]))
                x_max = min(image.shape[1], max(box[:, 0]))
                y_max = min(image.shape[0], max(box[:, 1]))
                cropped_image = image[y_min:y_max, x_min:x_max]
                filename = f"../image/cropped_{temp_handness}_{int(time.time())}.jpg"
                cv2.imwrite(filename, cropped_image)
                self.hand_state.last_drawn_box[temp_handness] = None
                # 因为如果画完包围框立即剪裁 很有可能把手错误的剪裁进去
                # 所以在包围框消失的前0.1秒剪裁 这样有足够的时间让手移走

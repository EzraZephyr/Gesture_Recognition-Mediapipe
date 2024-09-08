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
        # Handle the index finger's state and gesture effect, and update the image

    def update_index_finger_state(self, hand_21, temp_handness, index_x, index_y):

        if all(self.hand_state.index_finger_second[temp_handness].y < hand_21.landmark[i].y
               for i in range(21) if i not in [7, 8]) and \
                self.hand_state.index_finger_tip[temp_handness].y < self.hand_state.index_finger_second[temp_handness].y:
            self.hand_state.is_index_finger_up[temp_handness] = True
            # If both the index fingertip and first joint are above other keypoints,
            # consider the index finger as raised.

        if self.hand_state.is_index_finger_up[temp_handness]:
            if not self.hand_state.gesture_locked[temp_handness]:
                if self.hand_state.gesture_start_time[temp_handness] == 0:
                    self.hand_state.gesture_start_time[temp_handness] = time.time()
                elif time.time() - self.hand_state.gesture_start_time[temp_handness] > self.wait_time:
                    self.hand_state.dragging[temp_handness] = True
                    self.hand_state.gesture_locked[temp_handness] = True
                    self.hand_state.drag_point[temp_handness] = (index_x, index_y)
                    # If the pointing gesture has lasted longer than the wait time, confirm the pointing action.
                self.hand_state.buffer_start_time[temp_handness] = 0
                # Buffer time to prevent immediate interruption due to recognition errors.
        else:
            if self.hand_state.buffer_start_time[temp_handness] == 0:
                self.hand_state.buffer_start_time[temp_handness] = time.time()
            elif time.time() - self.hand_state.buffer_start_time[temp_handness] > self.hand_state.buffer_duration[temp_handness]:
                self.hand_state.gesture_start_time[temp_handness] = 0
                self.hand_state.gesture_locked[temp_handness] = False
                self.hand_state.dragging[temp_handness] = False
                # If the interruption time of the pointing gesture exceeds the set buffer duration, formally terminate.

    def draw_index_finger_gesture(self, image, temp_handness, index_x, index_y, cz0):

        if self.hand_state.dragging[temp_handness]:
            if self.hand_state.start_drag_time[temp_handness] == 0:
                self.hand_state.start_drag_time[temp_handness] = time.time()
                self.kalman_handler.reset_kalman_filter(temp_handness, index_x, index_y)
                # If it's the first operation, record the time and reset the Kalman filter.

            smooth_x, smooth_y = self.kalman_handler.kalman_filter_point(temp_handness, index_x, index_y)
            # Use the Kalman filter to smooth the generated trajectory, reducing noise and jitter.

            self.hand_state.drag_point[temp_handness] = (index_x, index_y)
            index_finger_radius = max(int(10 * (1 + (cz0 - self.hand_state.index_finger_tip[temp_handness].z) * 5)), 0)
            cv2.circle(image, self.hand_state.drag_point[temp_handness], index_finger_radius, (0, 0, 255), -1)
            # Adjust the circle size based on the distance from the wrist root, slightly larger than FingerDrawer for visibility during gesture lock.
            drag_point_smooth = (smooth_x, smooth_y)

            if time.time() - self.hand_state.start_drag_time[temp_handness] > self.kalman_wait_time:
                self.hand_state.trajectory[temp_handness].append(drag_point_smooth)
                # Wait for the Kalman filter to stabilize data before adding coordinates to the trajectory.
        else:
            if len(self.hand_state.trajectory[temp_handness]) > 4:
                contour = np.array(self.hand_state.trajectory[temp_handness], dtype=np.int32)
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                # Calculate the minimum enclosing rectangle when the drag points exceed 4.
                self.hand_state.rect_draw_time[temp_handness] = time.time()
                self.hand_state.last_drawn_box[temp_handness] = box

            self.hand_state.start_drag_time[temp_handness] = 0
            self.hand_state.trajectory[temp_handness].clear()
            # Reset and clear

        for i in range(1, len(self.hand_state.trajectory[temp_handness])):
            pt1 = (int(self.hand_state.trajectory[temp_handness][i-1][0]), int(self.hand_state.trajectory[temp_handness][i-1][1]))
            pt2 = (int(self.hand_state.trajectory[temp_handness][i][0]), int(self.hand_state.trajectory[temp_handness][i][1]))
            cv2.line(image, pt1, pt2, (0, 0, 255), 2)
            # Draw the drag path

        if self.hand_state.last_drawn_box[temp_handness] is not None:
            elapsed_time = time.time() - self.hand_state.rect_draw_time[temp_handness]
            if elapsed_time < self.wait_box:
                cv2.drawContours(image, [self.hand_state.last_drawn_box[temp_handness]], 0, (0, 255, 0), 2)
                # Keep the bounding box visible for a set period for easier observation.
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
                # To avoid accidentally cropping the hand into the bounding box,
                # perform the crop in the last 0.1 seconds before the box disappears,
                # giving enough time for the hand to move away.

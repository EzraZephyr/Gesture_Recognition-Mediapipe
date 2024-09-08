import cv2
from model import HandTracker
from index_finger import IndexFingerHandler
from gesture_data import HandState
from kalman_filter import KalmanHandler
from utils_zh.finger_drawer import FingerDrawer

class HandGestureHandler:
    def __init__(self):
        self.hand_state = HandState()
        self.kalman_handler = KalmanHandler()
        self.hand_tracker = HandTracker()
        self.index_handler = IndexFingerHandler(self.hand_state, self.kalman_handler)

    def handle_hand_gestures(self, image, width, height, is_video):
        results = self.hand_tracker.process(image)

        if results.multi_hand_landmarks:
            handness_str = ''
            index_finger_tip_str = ''

            if len(results.multi_hand_landmarks) == 1:
                detected_hand = results.multi_handedness[0].classification[0].label
                self.hand_state.clear_hand_states(detected_hand)
                # If only one hand is detected, clear the information of the other hand
                # to prevent data conflicts when the second hand appears.

            for hand_idx, hand_21 in enumerate(results.multi_hand_landmarks):
                self.hand_tracker.mp_drawing.draw_landmarks(
                    image, hand_21, self.hand_tracker.mp_hands.HAND_CONNECTIONS
                )
                # Draw the connections of hand keypoints

                temp_handness = results.multi_handedness[hand_idx].classification[0].label
                handness_str += f'{hand_idx}:{temp_handness}, '
                self.hand_state.is_index_finger_up[temp_handness] = False

                image = self.index_handler.handle_index_finger(
                    image, hand_21, temp_handness, width, height
                )
                # Handle the index finger

                image, index_finger_tip_str = FingerDrawer.draw_finger_points(
                    image, hand_21, temp_handness, width, height
                )

            if is_video:
                image = cv2.flip(image, 1)
            image = cv2.putText(image, handness_str, (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 255), 2)
            image = cv2.putText(image, index_finger_tip_str, (25, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 255), 2)
        else:
            if is_video:
                image = cv2.flip(image, 1)
                # If it's input video from a rear-facing camera, flip the image before processing
                # to ensure correct left and right hand detection, and flip it back afterward
                # to prevent mirrored output errors.

            self.hand_state.clear_hand_states()
            # Clear hand states if no hands are detected

        return image

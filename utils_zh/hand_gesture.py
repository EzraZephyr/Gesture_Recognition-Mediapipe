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
                # 如果只检测到了一只手 那么就清空另一只手的信息 以免第二只手出现的时候数据冲突

            for hand_idx, hand_21 in enumerate(results.multi_hand_landmarks):
                self.hand_tracker.mp_drawing.draw_landmarks(
                    image, hand_21, self.hand_tracker.mp_hands.HAND_CONNECTIONS
                )
                # 绘制手部关键点连接

                temp_handness = results.multi_handedness[hand_idx].classification[0].label
                handness_str += f'{hand_idx}:{temp_handness}, '
                self.hand_state.is_index_finger_up[temp_handness] = False

                image = self.index_handler.handle_index_finger(
                    image, hand_21, temp_handness, width, height
                )
                # 处理食指

                image, index_finger_tip_str = FingerDrawer.draw_finger_points(image, hand_21, temp_handness, width, height)

            if is_video:
                image = cv2.flip(image, 1)
            image = cv2.putText(image, handness_str, (25, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 255), 2)
            image = cv2.putText(image, index_finger_tip_str, (25, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 255), 2)
        else:
            if is_video:
                image = cv2.flip(image, 1)
                # 如果是后置摄像头的输入视频，则需要在处理前翻转图像，确保手势检测的左右手正确；
                # 处理完毕后再翻转回来，以防止最终输出的图像出现镜像错误。
            self.hand_state.clear_hand_states()
            # 如果未检测到手 则清空手部状态

        return image

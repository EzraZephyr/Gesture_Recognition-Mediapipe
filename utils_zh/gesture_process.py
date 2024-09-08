import cv2
import time
from hand_gesture import HandGestureHandler

class HandGestureProcessor:
    def __init__(self):
        self.hand_handler = HandGestureHandler()

    def process_image(self, image):

        start_time = time.time()
        height, width = image.shape[:2]
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 获取图像尺寸 翻转并转换颜色空间

        image = self.hand_handler.handle_hand_gestures(image, width, height)

        spend_time = time.time() - start_time
        FPS = 1.0 / spend_time if spend_time > 0 else 0
        image = cv2.putText(image, f'FPS {int(FPS)}', (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (0, 0, 255), 2)
        # 计算并显示帧率

        return image

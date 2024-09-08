import cv2

class FingerDrawer:
    @staticmethod
    def draw_finger_points(image, hand_21, temp_handness, width, height):

        cz0 = hand_21.landmark[0].z
        index_finger_tip_str = ''

        for i in range(21):
            cx = int(hand_21.landmark[i].x * width)
            cy = int(hand_21.landmark[i].y * height)
            cz = hand_21.landmark[i].z
            depth_z = cz0 - cz
            radius = max(int(6 * (1 + depth_z * 5)), 0)
            # 根据深度调整圆点的半径


            if i == 0:
                image = cv2.circle(image, (cx, cy), radius, (255, 255, 0), thickness=-1)
            elif i == 8:
                image = cv2.circle(image, (cx, cy), radius, (255, 165, 0), thickness=-1)
                index_finger_tip_str += f'{temp_handness}:{depth_z:.2f}, '
            elif i in [1, 5, 9, 13, 17]:
                image = cv2.circle(image, (cx, cy), radius, (0, 0, 255), thickness=-1)
            elif i in [2, 6, 10, 14, 18]:
                image = cv2.circle(image, (cx, cy), radius, (75, 0, 130), thickness=-1)
            elif i in [3, 7, 11, 15, 19]:
                image = cv2.circle(image, (cx, cy), radius, (238, 130, 238), thickness=-1)
            elif i in [4, 12, 16, 20]:
                image = cv2.circle(image, (cx, cy), radius, (0, 255, 255), thickness=-1)
            # 根据每组关节绘制不同颜色的圆点 同时根据距离掌根的深度信息进行调整

        return image, index_finger_tip_str

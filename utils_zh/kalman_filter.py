import numpy as np
from filterpy.kalman import KalmanFilter

class KalmanHandler:
    def __init__(self):
        self.kalman_filters = {
            'Left': KalmanFilter(dim_x=4, dim_z=2),
            'Right': KalmanFilter(dim_x=4, dim_z=2)
        }
        for key in self.kalman_filters:
            self.kalman_filters[key].x = np.array([0., 0., 0., 0.])
            self.kalman_filters[key].F = np.array([[1, 0, 1, 0],
                                                   [0, 1, 0, 1],
                                                   [0, 0, 1, 0],
                                                   [0, 0, 0, 1]])
            self.kalman_filters[key].H = np.array([[1, 0, 0, 0],
                                                   [0, 1, 0, 0]])
            self.kalman_filters[key].P *= 1000.
            self.kalman_filters[key].R = 3
            self.kalman_filters[key].Q = np.eye(4) * 0.01
            # 这些参数通过多次测试得出 表现较为稳定

    def kalman_filter_point(self, hand_label, x, y):

        kf = self.kalman_filters[hand_label]
        kf.predict()
        kf.update([x, y])
        # 更新状态
        return (kf.x[0], kf.x[1])

    def reset_kalman_filter(self, hand_label, x, y):

        kf = self.kalman_filters[hand_label]
        kf.x = np.array([x, y, 0., 0.])
        kf.P *= 1000.
        # 重置

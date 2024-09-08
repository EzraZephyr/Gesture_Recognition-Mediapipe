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
            # These parameters were obtained through multiple tests and have shown stable performance.

    def kalman_filter_point(self, hand_label, x, y):

        kf = self.kalman_filters[hand_label]
        kf.predict()
        kf.update([x, y])
        # Update state
        return (kf.x[0], kf.x[1])

    def reset_kalman_filter(self, hand_label, x, y):

        kf = self.kalman_filters[hand_label]
        kf.x = np.array([x, y, 0., 0.])
        kf.P *= 1000.
        # Reset

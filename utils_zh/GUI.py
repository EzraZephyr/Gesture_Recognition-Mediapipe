import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from video_recognition import start_camera, upload_and_process_video, show_frame
from process_images import HandGestureProcessor


current_mode = None
current_cap = None
# 用于追踪当前模式和摄像头资源

def create_gui():
    root = tk.Tk()
    root.title("Gesture Recognition")
    root.geometry("800x600")

    canvas = tk.Canvas(root, width=640, height=480)
    canvas.pack()
    # 创建显示视频内容的画布

    camera_button = tk.Button(
        root,
        text="Use Camera for Real-time Recognition",
        command=lambda: switch_to_camera(canvas)
    )
    camera_button.pack(pady=10)
    # 启动摄像头实时识别的按钮

    video_button = tk.Button(
        root,
        text="Upload Video File for Processing",
        command=lambda: select_and_process_video(canvas, root)
    )
    video_button.pack(pady=10)
    # 上传并处理视频文件的按钮

    root.mainloop()

def switch_to_camera(canvas):
    global current_mode, current_cap

    stop_current_operation()
    # 停止当前操作并释放摄像头

    current_mode = "camera"
    canvas.delete("all")
    # 设置当前模式为摄像头并清空Canvas


    current_cap = cv2.VideoCapture(0)
    if not current_cap.isOpened():
        messagebox.showerror("Error", "Cannot open camera")
        current_mode = None
        return
    # 启动摄像头


    start_camera(canvas, current_cap)
    # 传入canvas和current_cap

def select_and_process_video(canvas, root):
    global current_mode, current_cap

    stop_current_operation()
    current_mode = "video"
    canvas.delete("all")

    video_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=(("MP4 files", "*.mp4"), ("AVI files", "*.avi"), ("All files", "*.*"))
    )
    # 选择视频文件

    if video_path:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot open video file")
            return
        # 获取视频的宽高并调整 Canvas 大小

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        canvas.config(width=frame_width, height=frame_height)
        root.geometry(f"{frame_width + 160}x{frame_height + 200}")  # 调整窗口大小
        # 获取视频宽高并动态调整canvas的大小

        error_message = upload_and_process_video(canvas, video_path)
        if error_message:
            messagebox.showerror("Error", error_message)
        # 上传并处理视频文件

def stop_current_operation():

    global current_cap

    if current_cap and current_cap.isOpened():
        current_cap.release()
        cv2.destroyAllWindows()
        current_cap = None
        # 停止当前操作 释放摄像头资源并关闭所有窗口

def start_camera(canvas, cap):
    if not cap.isOpened():
        return "Cannot open camera"

    gesture_processor = HandGestureProcessor()
    show_frame(canvas, cap, gesture_processor)
    # 启动摄像头进行实时手势识别

if __name__ == "__main__":
    create_gui()
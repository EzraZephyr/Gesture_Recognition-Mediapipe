import cv2
from process_images import HandGestureProcessor
from tkinter import messagebox
from PIL import Image, ImageTk

def start_camera(canvas):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Cannot open camera"

    gesture_processor = HandGestureProcessor()
    show_frame(canvas, cap, gesture_processor)

def show_frame(canvas, cap, gesture_processor):
    success, frame = cap.read()
    if success:
        processed_frame = gesture_processor.process_image(frame,False)
        img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        canvas.imgtk = imgtk
        canvas.create_image(0, 0, anchor="nw", image=imgtk)
        # 对该帧进行处理并转换为RGB显示在画布上
        canvas.after(10, show_frame, canvas, cap, gesture_processor)
        # 实现循环调用 持续处理并显示后续的每一帧
    else:
        cap.release()
        cv2.destroyAllWindows()

def upload_and_process_video(canvas, video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return "Cannot open video file"

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 获取视频的参数

    output_filename = "../video/processed_output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_filename, fourcc, fps, (frame_width, frame_height))
    # 设置输出视频文件路径和编码

    gesture_processor = HandGestureProcessor()
    process_video_frame(canvas, cap, gesture_processor, out)

def process_video_frame(canvas, cap, gesture_processor, out):
    success, frame = cap.read()
    if success:
        processed_frame = gesture_processor.process_image(frame,True)
        out.write(processed_frame)

        img = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        canvas.imgtk = imgtk
        canvas.create_image(0, 0, anchor="nw", image=imgtk)
        canvas.after(10, process_video_frame, canvas, cap, gesture_processor, out)
    else:
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        messagebox.showinfo("Info", "Processed video saved as processed_output.avi")
        print("Processed video saved as processed_output.avi")
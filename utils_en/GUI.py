import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from video_recognition import start_camera, upload_and_process_video, show_frame
from process_images import HandGestureProcessor

current_mode = None
current_cap = None
# To track the current mode and camera resources

def create_gui():
    root = tk.Tk()
    root.title("Gesture Recognition")
    root.geometry("800x600")

    canvas = tk.Canvas(root, width=640, height=480)
    canvas.pack()
    # Create a canvas to display video content

    camera_button = tk.Button(
        root,
        text="Use Camera for Real-time Recognition",
        command=lambda: switch_to_camera(canvas)
    )
    camera_button.pack(pady=10)
    # Button to start real-time recognition using the camera

    video_button = tk.Button(
        root,
        text="Upload Video File for Processing",
        command=lambda: select_and_process_video(canvas, root)
    )
    video_button.pack(pady=10)
    # Button to upload and process video files

    root.mainloop()

def switch_to_camera(canvas):
    global current_mode, current_cap

    stop_current_operation()
    # Stop the current operation and release the camera

    current_mode = "camera"
    canvas.delete("all")
    # Set the current mode to camera and clear the Canvas

    current_cap = cv2.VideoCapture(0)
    if not current_cap.isOpened():
        messagebox.showerror("Error", "Cannot open camera")
        current_mode = None
        return
    # Start the camera

    start_camera(canvas, current_cap)
    # Pass the canvas and current_cap to start the camera

def select_and_process_video(canvas, root):
    global current_mode, current_cap

    stop_current_operation()
    current_mode = "video"
    canvas.delete("all")

    video_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=(("MP4 files", "*.mp4"), ("AVI files", "*.avi"), ("All files", "*.*"))
    )
    # Select a video file

    if video_path:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot open video file")
            return
        # Get video width and height, and adjust Canvas size

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        canvas.config(width=frame_width, height=frame_height)
        root.geometry(f"{frame_width + 160}x{frame_height + 200}")  # Adjust window size
        # Get video dimensions and dynamically adjust the canvas size

        error_message = upload_and_process_video(canvas, video_path)
        if error_message:
            messagebox.showerror("Error", error_message)
        # Upload and process the video file

def stop_current_operation():
    global current_cap

    if current_cap and current_cap.isOpened():
        current_cap.release()
        cv2.destroyAllWindows()
        current_cap = None
        # Stop the current operation, release camera resources, and close all windows

def start_camera(canvas, cap):
    if not cap.isOpened():
        return "Cannot open camera"

    gesture_processor = HandGestureProcessor()
    show_frame(canvas, cap, gesture_processor)
    # Start the camera for real-time gesture recognition

if __name__ == "__main__":
    create_gui()

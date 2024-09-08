# Mediapipe 手势识别系统

[English](readme.md)  /  中文

↑ Click to switch language

## 项目简介

该项目是一个实时手势识别系统，通过摄像头捕捉手部动作，实现基本的手势绘制区域截图的功能。 其他高级手势控制功能可能根据需求在未来逐步添加。

## 演示效果

https://github.com/user-attachments/assets/489c1797-fe9a-474a-8dfa-b55c9e482a79

## 目录

- [功能特性](#功能特性)
- [多语言注释](#多语言注释)
- [安装步骤](#安装步骤)
- [注意事项](#注意事项)
- [使用方法](#使用方法)
- [文件结构](#文件结构)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 功能特性

- **实时手势识别**：通过摄像头实时捕捉手势动作。
- **手指绘制**：在图像上绘制手指关键点，提供直观的视觉反馈。
- **捕捉截图**：根据绘制的轨迹自动生成矩形，并截取矩形区域内的内容保存到image文件夹下。
- **图形用户界面**：提供易于使用的 GUI，可轻松启动摄像头、上传视频和查看手势识别结果。

## 多语言注释

为了让不同语言背景的开发者更容易理解代码 本项目的注释提供了英文和中文两种版本

## 安装步骤

1. **克隆项目**：
   ```bash
   git clone git@github.com:EzraZephyr/Gesture_Recognition-Mediapipe.git
   cd Gesture_Recognition-Mediapipe
   ```
2. **安装依赖**：
   ```bash
   pip install opencv-python mediapipe filterpy --upgrade
   ```
3. **运行项目**：
   ```bash
   python GUI.py
   ```
## 注意事项

- 本项目最初的编写和调试是在 Jupyter Notebook 上进行的，因此如果你想直接调用摄像头进行调试和测试，建议运行 `gesture_recognition.ipynb` 文件。

## 使用方法

![演示](img.png)

- **启动摄像头**：打开 GUI 后，点击 “ Use Camera for Real-time Recognition ” 按钮，系统将自动捕捉手势并在屏幕上显示。
- **上传视频**：通过 “ Upload Video File for Processing ” 按钮，可以上传预录制的视频进行手势识别。
- **手势控制**：通过 **竖起食指** 在屏幕上绘制线条，并用 **食指和中指同时竖起** 来结束绘制(或者任何使其他关节点高于食指第一个关节点的操作)，系统会根据手指的轨迹生成一个矩形，并自动截取矩形区域内的内容。

## 文件结构

项目的文件结构如下

```c++
Gesture Recognition/
│
├── image/ 
│   └── xxx.jpg
│  
├── utils(en/zh)/
│   ├── finger_drawer.py
│   ├── gesture_data.py
│   ├── gesture_process.py
│   ├── gesture_recognition.ipynb
│   ├── GUI.py
│   ├── hand_gesture.py
│   ├── index_finger.py
│   ├── kalman_filter.py
│   ├── model.py
│   ├── process_images.py
│   └── video_recognition.py
│
├── video/
│   ├── processed_output.mp4
│   └── test.mp4
└── main.py 
```

## 贡献指南

欢迎任何人参与本项目的开发。如果您想贡献代码，请遵循以下步骤：

1. **Fork 本仓库**。
2. **创建您的功能分支** (`git checkout -b feature/AmazingFeature`)。
3. **提交您的修改** (`git commit -m 'Add some AmazingFeature'`)。
4. **Push 到分支** (`git push origin feature/AmazingFeature`)。
5. **提交 Pull Request**。

## 许可证

本项目使用 MIT 许可证。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。


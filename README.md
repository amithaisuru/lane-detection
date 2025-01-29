# 🚗 Lane Detection using Computer Vision  
A Computer Vision project for detecting road lanes from dashcam footage using OpenCV Sobel edge detection and Hough Transform.

## 📌 Project Overview  
This project processes dashcam video frames to detect and highlight road lanes using edge detection and Hough Transform. It supports both **left** and **right lane detection**, saves processed images, and generates an output video showing detected lanes.

## 📂 Project Structure  

```bash
📦 Lane-Detection  
 ├── 📂 processed_images_left/      # Left lane detection output images  
 ├── 📂 processed_images_right/     # Right lane detection output images  
 ├── 📂 TestVideo_1/                # Dashcam video frames (right-side view)  
 ├── 📂 TestVideo_2/                # Dashcam video frames (left-side view)  
 ├── 📄 main.py                     # Main Python script for lane detection  
 ├── 🎥 processed_images_left.avi    # Output video for left lane detection  
 ├── 🎥 processed_images_right.avi   # Output video for right lane detection  
 └── 📄 README.md                    # Project documentation  
```


## ⚙️ How It Works  

1. **Load Video Frames**  
   - Reads 100 frames from `TestVideo_1/` (Right) and `TestVideo_2/` (Left).  

2. **Apply Image Processing**  
   - Converts frames to grayscale.  
   - Uses **Gaussian Blur** to smooth the image.  
   - Applies **Sobel Edge Detection** for feature extraction.  
   - Filters **Region of Interest (ROI)** to remove unnecessary edges.  
   - Uses **Hough Transform** to detect lane lines.  

3. **Separate Left & Right Lanes**  
   - Classifies lines based on their slope.  
   - Computes the **average lane lines** for stability.  
   - Marks lane intersections.  

4. **Generate Output**  
   - Saves detected lane images in `processed_images_left/` and `processed_images_right/`.  
   - Creates **annotated videos** (`processed_images_left.avi`, `processed_images_right.avi`).  

## ▶️ How to Run  

### **Requirements**  
Ensure you have Python installed and the required dependencies:  

```bash
pip install opencv-python numpy
python main.py
```

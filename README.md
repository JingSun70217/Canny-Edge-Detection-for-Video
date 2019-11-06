# Canny Edge Detection for Video


## Introduction

Canny edge detector is one of the most widely used edge detectors in Computer Vision. This project implemented the edge detection for video by using canny edge detector.

The program will convert the video frames to grayscale firstly. Then do a Canny Edge Detection for each frame. Play the original and processed frames in the GUI interface side by side. Finally, put processed frames together to a stream and save the stream as a video to the chosen folder.

![enter image description here](https://lh3.googleusercontent.com/kwfFtEYvq2IalLd_YowGiHUXkMk17v-DpIBDO1aMYhnuA8ABw9HzwOJZKjiuliJ45cLbCGDXGj_A "originalFrame")![enter image description here](https://lh3.googleusercontent.com/3SQSuwhf8uK-47dhuNOy23FV9CDrJKw1RRAoHBJdsQ0NNmo9b9QnKFSXZE71QVfrlNjXOI9Q9RBf "cannyFrame")


<figure class="third">
 <img src="https://lh3.googleusercontent.com/kwfFtEYvq2IalLd_YowGiHUXkMk17v-DpIBDO1aMYhnuA8ABw9HzwOJZKjiuliJ45cLbCGDXGj_A"><img src="https://lh3.googleusercontent.com/3SQSuwhf8uK-47dhuNOy23FV9CDrJKw1RRAoHBJdsQ0NNmo9b9QnKFSXZE71QVfrlNjXOI9Q9RBf">
</figure>

The left image is one of frames from original video. The right image is the related frame which being processed by canny edge detector.

## Getting Started

There are three files in this project:
 - canny_utils.py 
 - cannyEdgeDetection.py 
 - GUI.py

### Prerequisites
Python3.6
Packages:
 - numpy 
 - scipy 
 - cv2 
 - PyQt5 
 - sys 
 - time

### GUI Interface

Run GUI.py file to enter the program through GUI interface.
 - In the GUI interface, users can select a local video file through type the local video  path in the input box or click the “**select video file**” button.
 - Click "**start**" button to play the video. The program will read the original video frame by frame, play the original frame stream in the "Original Video" area of GUI interface. At the same time, each frame is processed by grayscale conversion and canny edge detector. The processed frame stream is played in the "Processed Video" area of GUI interface in real-time.
 - Click "**stop**" button to stop play.
 - Click "**save**" button to select a path and save the processed frame stream into a video. The default codec of the written video is "mp4v". Different codec types were tried. The "CVID" can make the written video be played smoother, but the size of the written video file is much larger than others. Therefore,  "mp4v" is chosen as the default codec.

### Canny Edge Detector 

There are four steps of Canny Edge Detector:
 - Noise Reduction – Gaussian Filter
 - Gradient Calculation -- Sobel Filter
 - Non-Maximum Suppression
 - Thresholding with Hysterysis

The canny_utils.py file contains these four functions, which are implemented by using Numpy and Scipy. These four functions are packaged into a function named "cannyDetector" in the cannyEdgeDetection.py file and called by GUI.py and cannyEdgeDetection.py. You can change parameters in the "cannyDetector" function. The introduction to the algorithm parameters can be found in canny_utils.py file.

There are many different ways of implementing each step, especially for the "Non-Maximum Suppression" and "Thresholding with Hysterysis". After trying different methods,  the methods which can get accurate edge detection effect as well as less processing time is chosen.


### Running Time 

The running time of the canny edge detector depends on how many edges in each frame. For a frame with few edges, the processing speed is about 12s~14s per frame. For a frame with many edges, the running time of each frame can exceed 1min sometimes. The "Non-Maximum Suppression"  function takes most of the time. Please wait patiently for the display.

### Alternative way to show 

Please run the cannyEdgeDetection.py file if GUI interface does not work as expected. This file packages the canny edge detection algorithm into the "cannyDetector" function. The original and processed video can be played at the same time in two windows. Please change the path of the input video file. If you want to stop playing, please push 'q' to break otherwise the output video cannot be open.

## Citation

Tutorial of Canny Edge Detector:
[http://www.aishack.in/tutorials/canny-edge-detector/](http://www.aishack.in/tutorials/canny-edge-detector/)


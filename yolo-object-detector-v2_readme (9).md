# 3D Point Clouds Object Detection Based on 2D Object Detection

# Introduction
Conventional object detection methods of 3D point clouds are mainly based on the 3D point clouds. But the size of 3D point cloud data is very large, which causes that processing data and training models are very time-consuming and memory-expensive. Furthermore, there is no widely used annotation tooling for 3D point clouds currently. Objects cannot be annotated like 2D images. This repository proposes a method for preprocessing 3D point clouds by combining the distance information and the region of interests (RoI) from the results of 2D image object detection. The goal of this approach is to reduce the size of processed 3D point cloud data, as well as increasing the conﬁdence of 3D object detection.

Different from 2D object detection on the normal filed of view images, our input images are 360° panorama images. At first, converting the panorama images from equirectangular projection to gnomonic projection to get small pieces flatten images. Then, annotating the 2D bounding box (bbox) on the flatten image. After that, feeding the flatten images and annotation results into the YOLOv3 models to detect objects. After getting the ROI areas of the objects from 2D detector, we project the detected 2D bbox from the flatten images back to the panorama images. Now the RoI areas in the panorama images can be obtained. With the help of corresponding distance information of the panorama images, we can extract the point clouds from the RoI areas to generate frustums for each object. The 3 dimensions, center position, rotated angle, and other 3D bbox related information of the object can be obtained through calculating the intersection space from the multi-view frustums of the same object. This information is our 3D ground truth. Finally, using the Frustum Pointnets and the baseline model to get the final 3D object detection results.

# Installation

1.	[Visual Studio Code](https://code.visualstudio.com/)
2.	Python 3.7 or Python 3.8 
If you have problems with the interpreter path in VS Code, you can set your python path in `/.vscode/settings.json`.
3.	Python packages
opencv, pyqt5, lxml, keras\==2.2.4, pillow, matplotlib, pypcd\==0.1.1, python-pcl\==0.3.0
4.	Both 2D and 3D object detection need to use Tensorflow. For 2D YOLOv3, the Tensorflow1.14.0 which works on Windows is enough. But the 3D Frustum Pointnets require Tensorflow1.4 or Tensorflow1.2 which doesn’t work on Windows. I used Tensorflow1.4 on the Ubuntu16.04 system on [WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10) (Windows Subsystem for Linux). GPUs are highly recommended. 

# Pipeline Structure

<p align="center">
 <img src=" https://faro.box.com/s/czzsbi0r9xsmmsabqsyc67hd7vaaj5cq" width="300"/>
</p>



# Usage
The following steps should be implemented in order. Please put your raw input datasets in `/datasets/0_input_data`. Other input and output paths will be generated automatically when running the main script for each step. You can modify the paths in `/.vscode/launch.json`.

## Input data

The panorama images and distance images can be downloaded manually from our [SCENE WebShare Cloud](https://arena2036.3d-enterprise.com/) website or downloaded automatically by running [ws-pano-image-downloader](https://bitbucket.org/farolabs/ws-pano-image-downloader/src/master/) repository. 
You can also download a demo dataset from this shared [link](https://faro.box.com/s/w4lts4rhbf3ahmk4nd1h933n2dzmjqc3) and save to `/datasets/0_input_data`.


## Equirectangular to gnomonic projection

Map images from equirectangular projection to gnomonic projection. Equalize each panorama images in to several small flatten images which in normal field of view. Here is the original [repository](https://github.com/NitishMutha/equirectangular-toolbox). 

Please run `/equirectangular_to_gnomonic_projection /flattenPanorama.py`

## 2D YOLOv3 Object Detection

When you run the main script of this step, the 2D annotation tooling ([Labelmg](https://github.com/tzutalin/labelImg)) will be triggered. Please annotate the flatten images. After closing the interface of Labelmg tolling, the training, testing, and prediction section will be run automatically. 
You can find more details in the [ReadMe](/2D_YOLOv3/ReadMe.md) of 2D_YOLOv3. (I will modify the ReadMe of 2D detector later)

Please run `/2D_YOLOv3/Codes/yolov3_main.py`


## 3D object detection

**Frustum proposal generation**

- Generate 9 layers tensors (RGB-distance-yaw-pitch-xyz) for each pixel from panorama images and distance images.
- Project 2D bbox back to panorama images.
- Distinguish different RoI objects in one panorama image.
- Merge the truncated objects.
- Generate frustum files for each object. (Save the VURGBDYPXYZ values for each point in the 2D bbox.)

Please run `/frustum_proposal_generation/generateFrustum.py`
You can find more details of this section in [here](https://faro.box.com/s/aib4k4z0gd49dhi0q13kglbzezax6v2u).

**Ground truth generation**

- Download transformation matrix from "https://arena2036.3d-enterprise.com/scan/".   
- Extract the intersection space from multi-view frustums of the same object.  
- Get 3-axis directions of RoI objects by using PCA.  
- Calculate 3 dimensions, heading angles, and center positions of RoI objects.  
- Get the frustum angles from the yaw of 2D bbox center.  
- Project the 3D bbox back to each frustum in the camera coordinate system.  
- Rotate the frustums toward a center view (Convert to the frustum coordinate system).  

Run`/frustum_proposal_generation/get_TransformationGlobal.py`to get the transformation matrix at first. You need to log in and update the cookies in the script to the cookies in your local browser. Please follow the steps [here](https://faro.box.com/s/u68lna4x3ivlfwjwpusmuuw2e3nr36gr) to update the login information and cookies. Then run `/frustum_proposal_generation/generate3DBbox.py`to get the annotation results.

You can find more details of this section in [here](https://faro.box.com/s/3vb4i4otfoahwd8s30ew39p5boz75bll).

**Annotation results format convertion**

- Data augmentation (Randomly shift, rotate, sdd gaussian noise, filter outliers, mirror flip along up-axis)
- Convert annotation results to Kitti format which can be used by the Frustum Pointnets. 
- Split the train, validation, and test datasets.  

Please run `/frustum_proposal_generation/prepare_fp_inputs.py`
You can find more details about data format convertion in [here](https://faro.box.com/s/d5e2aj625egwgeu8wpczvg0ky6n3gze5).

**Frustum Pointnets**

- Instance segmentation
- 3D bbox estimation (center position, heading angle, and 3 dimensions)

Please run `/3D_frsutum_pointNets/train/train.py` at first. Then run `/3D_frsutum_pointNets/train/test.py`

You can find more details in the ReadMe of Frustum Pointnets. (I will upload the ReadMe for fp later)

**3D prototype model (Baseline)**

- 3D bbox estimation (center position, heading angle, and 3 dimensions)  
- Same structure with 3D instance segmentation PointNet v1 network  
- Train & Evaluation  

Please run `/3D_prototype/3D_prototype_main.py`

# References
- [Frustum PointNets for 3D Object Detection from RGB-D Data](https://arxiv.org/abs/1711.08488) by Charles R. Qi et al. (CVPR 2018 paper). Code and data: [here](https://github.com/charlesq34/frustum-pointnets).  
- [YOLOv3: An Incremental Improvement](https://arxiv.org/abs/1804.02767) by Redmon et al. [Code](https://github.com/qqwweee/keras-yolo3)

# Todo

- Try the frustum_pointnets_v2 model in Frustum Pointnets.   
- Improve the transformation matrix getting method from the WebShareCloud. The method I used in [here](https://faro.box.com/s/u68lna4x3ivlfwjwpusmuuw2e3nr36gr) needs to do operations in the Postman and Chrome. It would be better if the matrix can be got automatically without interrupting the script. Try requests.Session, which can reference [`/ws-pano-image-downloader/wsSession.py`](https://bitbucket.org/farolabs/ws-pano-image-downloader/src/master/wsSession.py).


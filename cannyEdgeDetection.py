import numpy as np
from cv2 import *
import canny_utils

# input: original frame
# output: canny edge detection frame
def cannyDetector(frame):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rmNoise_img = canny_utils.gaussianBlur(gray_frame, 5, 1)
    G_magnitude, G_direction = canny_utils.sobelEdgeDetection(rmNoise_img)
    sup_img = canny_utils.nonMaxSuppression(G_magnitude, G_direction)
    canny_frame = canny_utils.thresholdHysteresis(sup_img, 0.05, 0.22).astype(np.uint8)
    return canny_frame


if __name__ == '__main__':
    cap = cv2.VideoCapture('../bbb_sunflower_native_60fps_normal.mp4') #input video path
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    canny_video = cv2.VideoWriter('../cannyVideo.mp4', fourcc, fps, size, False)#output video path

    while(cap.isOpened()):
        ret, ori_frame = cap.read()
        out_frame = cannyDetector(ori_frame)
        canny_video.write(out_frame)

        scale_percent = 25
        width = int(ori_frame.shape[1] * scale_percent / 100)
        height = int(ori_frame.shape[0] * scale_percent / 100)

        # show Canny_Edge Detection Video
        show_canny = np.array(out_frame).astype(np.uint8)
        canny_resized = cv2.resize(show_canny, (width, height), cv2.INTER_AREA)
        cv2.imshow('Canny Video', canny_resized)

        # show Original Video
        show_ori = np.array(ori_frame).astype(np.uint8)
        ori_resized = cv2.resize(show_ori, (width, height), cv2.INTER_AREA)
        cv2.imshow('Original Video', ori_resized)

        # Push 'q' to break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        else:
            pass

    cap.release()
    canny_video.release()
    cv2.destroyAllWindows()

import numpy as np
from scipy import ndimage, signal


# Noise Reduction
# img: grayscale images
# size: kernel size of gaussian filter
# sigma: standard deviation, determines extent of smoothing
# return: gb_img, images after gaussian blur
def gaussianBlur(img, size, sigma=1):
    x, y = np.mgrid[-size//2 + 1:size//2 + 1, -size//2 + 1:size//2 + 1]
    g = np.exp(-((x**2 + y**2)/(2.0*sigma**2)))
    g = g/g.sum()
    gb_img = ndimage.convolve(img, g, mode='constant')
    return gb_img


# Gradient Calculation -- Sobel Filter
# img: images after noise reduction
# return: G:gradient magnitudes, theta: gradient directions
def sobelEdgeDetection(img):
    Kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    Ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    sobel_img_x = signal.convolve2d(img, Kx, mode='same')
    sobel_img_y = signal.convolve2d(img, Ky, mode='same')

    G = np.hypot(sobel_img_x, sobel_img_y)
    G_max = G.max()
    G_max = 0.0001 if G_max == 0 else G_max
    G = G / G_max * 255

    theta = np.arctan2(sobel_img_y, sobel_img_x)
    theta[theta > 0.5*np.pi] -= np.pi
    theta[theta < -0.5*np.pi] += np.pi
    return G, theta


# Non-Maximum Suppression
# Gm: gradient magnitudes
# Gd: gradient directions, -pi/2 to +pi/2
# return: sup_img, gradient magnitude if local max, 0 otherwise
def nonMaxSuppression(img, direction):
    img_row, img_col = img.shape
    sup_img = np.zeros(img.shape)
    angle = direction * 180. / np.pi
    angle[angle < 0] += 180

    for i in range(1, img_row - 1):
        for j in range(1, img_col - 1):
            try:
                x = 0
                y = 0
                # angle 0
                if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                    x = 0
                    y = 1
                # angle 45
                elif (22.5 <= angle[i, j] < 67.5):
                    x = 1
                    y = 1
                # angle 90
                elif (67.5 <= angle[i, j] < 112.5):
                    x = 1
                    y = 0
                # angle 135
                elif (112.5 <= angle[i, j] < 157.5):
                    x = 1
                    y = 1
                if img[i, j] > img[i + x, j + y] and img[i, j] > img[i - x, j - y]:
                    sup_img[i, j] = img[i, j]
                else:
                    sup_img[i, j] = 0

            except IndexError as e:
                pass

    return sup_img


# Thresholding with Hysterysis
# img: images after non-maximum suppression
# thLow: ratio of low threshold to high threshold, 0 to 1
# thHigh: High threshold, 0 to 1
# return: images after double threshold and edge tracking by hysteresis
def thresholdHysteresis(img, thLow, thHigh):
    thHigh = img.max() * thHigh
    thLow = thHigh * thLow
    labels, n = ndimage.measurements.label(img > thLow, structure=np.ones((3, 3)))
    for i in range(1, n):
        upper = np.amax(img[labels == i])
        if upper < thHigh: labels[labels == i] = 0
    return 255*(labels > 0)


import cv2 as cv
import numpy as np
import ransac as rns
import read_kinect_pics as rkp


def add_ones(uvd):
    uvdo = np.ones((len(uvd), 4))
    uvdo[:, :3] = uvd
    return uvdo


def calc_coeff(uvd):
    uvdo = add_ones(uvd[:3])
    d=uvdo[:, 2]
    uvo=uvdo[:, [0, 1, 3]]
    return np.matmul(np.linalg.inv(uvo), d)


def is_inlier(m, xyz, threshold_):
    return abs(xyz[2]-(m[0]*xyz[0] + m[1]*xyz[1] + m[2])) < threshold_

n = 1
print("Choose picture[1-9]: ")
n = int(input())

path = './KinectPics/sl-0000' + str(n) +'.bmp'

rgb_image = cv.imread(path)
depth_image = rgb_image.copy()
gray = cv.cvtColor(depth_image, cv.COLOR_BGR2GRAY)


point3DArray, n3DPoints, gray = rkp.ReadKinectPic(path, gray)
rgb = cv.cvtColor(gray,cv.COLOR_GRAY2BGR)


cv.namedWindow("rgb_" + str(n), cv.WINDOW_NORMAL)
cv.resizeWindow("rgb_" + str(n), 600, 400)
cv.imshow("rgb_" + str(n), rgb_image)

cv.namedWindow("depth_image_" + str(n), cv.WINDOW_NORMAL)
cv.resizeWindow("depth_image_" + str(n), 600, 400)
cv.imshow("depth_image_" + str(n), rgb)

print("Press space to continue!")
cv.waitKey(0)

print("Calculating...(Might take a while :/ !)")


max_iterations = 1000
goal_inliers =len(point3DArray) * 0.3
threshold = 8
m, b, data_ = rns.run_ransac(point3DArray, calc_coeff, lambda x, y: is_inlier(x, y, threshold), goal_inliers,len(point3DArray), max_iterations)


cnt2 = 0

print(len(data_))
for idxv, v in enumerate(rgb):
    for idxu, u in enumerate(rgb[0]):
        if (data_[cnt2])[2] == -1:
            (rgb[idxv][idxu])[0] = 0
            (rgb[idxv][idxu])[1] = 255
            (rgb[idxv][idxu])[2] = 0
        cnt2 += 1


cv.namedWindow("dom_plane" + str(n), cv.WINDOW_NORMAL)
cv.resizeWindow("dom_plane" + str(n), 600, 400)
cv.imshow("dom_plane" + str(n),rgb)
cv.waitKey(0)

cv.destroyAllWindows()



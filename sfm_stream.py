#!/usr/bin/env python
import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
import roslib
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


frame_buffer = []
#parameters
buffer_size = 2
new_frame_idx = 1
old_frame_idx = 0


def draw_matches(img1, kp1, img2, kp2, matches, color=None): 
    # We're drawing them side by side.  Get dimensions accordingly.
    # Handle both color and grayscale images.
    ###if len(img1.shape) == 3:
    ###    new_shape = (max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1], img1.shape[2])
    ###elif len(img1.shape) == 2:
    ###    new_shape = (max(img1.shape[0], img2.shape[0]), img1.shape[1]+img2.shape[1])
    new_img = np.zeros(img1.shape, type(img1.flat[0]))  
    # Place images onto the new image.
    #new_img[0:img1.shape[0],0:img1.shape[1]] = img1
    new_img[0:img1.shape[0],0:img1.shape[1]] = img2/2 + img1/2
    
    # Draw lines between matches.  Make sure to offset kp coords in second image appropriately.
    r = 1
    thickness = 1
    if color:
        c = color
    for m in matches:
        # Generate random color for RGB/BGR and grayscale images as needed.
        if not color: 
            c = np.random.randint(255,256,3) if len(img1.shape) == 3 else np.random.randint(255,256)
        # So the keypoint locs are stored as a tuple of floats.  cv2.line(), like most other things,
        # wants locs as a tuple of ints.
        end1 = tuple(np.round(kp1[m.queryIdx].pt).astype(int))
        end2 = tuple(np.round(kp2[m.trainIdx].pt).astype(int))
        cv2.line(new_img, end1, end2, c, thickness)
        cv2.circle(new_img, end1, r, c, thickness)
        #cv2.circle(new_img, end2, r, c, thickness)
    
    return new_img


def frames_processing(new_frame, old_frame):
    '''#image = new_frame - old_frame - 100
    orb = cv2.ORB(400)
    kp1, des1 = orb.detectAndCompute(new_frame,None)
    kp2, des2 = orb.detectAndCompute(old_frame,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key = lambda x:x.distance)
    image = draw_matches(new_frame, kp1, old_frame, kp2, matches[:len(matches)*4/5])

    return image

    '''
    sift = cv2.SIFT()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(new_frame,None)
    kp2, des2 = sift.detectAndCompute(old_frame,None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1,des2,k=2)
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    image = draw_matches(new_frame, kp1, old_frame, kp2, good[:len(good)*4/5])
    return image

class feature_matching:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)
        self.image_pub = rospy.Publisher("/sfm_image", Image) #change topic later

    def callback(self, data):
        try:
            curr_frame = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        global frame_buffer
        frame_buffer.append(curr_frame)

        if len(frame_buffer)>buffer_size:
            del frame_buffer[0]
        new_frame = frame_buffer[new_frame_idx]
        old_frame = frame_buffer[old_frame_idx]
        diff = frames_processing(new_frame, old_frame)
        try:
            #print somehow fixes ROS initialization issue (not critical though)
            print("Buffer size: " + str(buffer_size) + " frames") 
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(diff, "bgr8"))
        except CvBridgeError as e:
            print(e)  


def main(args):
    fm = feature_matching()
    rospy.init_node("SfM", anonymous = True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
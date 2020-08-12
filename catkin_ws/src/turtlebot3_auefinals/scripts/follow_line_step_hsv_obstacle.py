#!/usr/bin/env python
# import rospy
# import cv2
# import numpy as np
# from cv_bridge import CvBridge, CvBridgeError
# from geometry_msgs.msg import Twist, Point
# from sensor_msgs.msg import Image
# from move_robot import MoveTurtlebot3
# from math import pow,atan2,sqrt
# from sensor_msgs.msg import LaserScan
# from turtlesim.msg import Pose

# dist_r = 0
# dist_front = 0
# dist_l = 0

# lane_confirm = False

# class LineFollower(object):

#     def __init__(self):
    
#         self.bridge_object = CvBridge()
#         self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
#         self.moveTurtlebot3_object = MoveTurtlebot3()



#     def camera_callback(self,data):
        
#         # We select bgr8 because its the OpneCV encoding by default
#         try:
#             cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
#         except CvBridgeError as e:
#             print(e)
            
#         # We get image dimensions and crop the parts of the image we dont need
#         height, width, channels = cv_image.shape
#         crop_img = cv_image[(height)/2+180:(height)/2+200][1:width]
        
#         # Convert from RGB to HSV
#         hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        
#         # Define the Yellow Colour in HSV

#         """
#         To know which color to track in HSV use ColorZilla to get the color registered by the camera in BGR and convert to HSV. 
#         """

#         # Threshold the HSV image to get only yellow colors
#         lower_yellow = np.array([20,100,100])
#         upper_yellow = np.array([50,255,255])
#         mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
#         # Calculate centroid of the blob of binary image using ImageMoments
#         m = cv2.moments(mask, False)

#         global lane_confirm

#         try:
#             cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
#             lane_finder = False
#             lane_confirm = True
#         except ZeroDivisionError:
#             cx, cy = height/2, width/2
#             lane_finder = True

#         res = cv2.bitwise_and(crop_img, crop_img, mask= mask)
#         twist_object = Twist()
#         # Draw the centroid in the resultut image
#         if not lane_finder:
#            if lane_confirm:
#             cv2.circle(res,(int(cx), int(cy)), 10,(0,0,255),-1)

#             cv2.imshow("Original", cv_image)
#             cv2.imshow("MASK", mask)
#             cv2.imshow("RES", res)
#             cv2.waitKey(1)
            
#             """
#         Enter controller here.
#             """
#             error_x = cx - width / 2
            
#             if error_x >-5 and error_x <5:
#                 error = 0
#             twist_object.angular.z = np.clip((-float(error_x/1000)), -0.2, 0.2)
#             temp = np.clip((-float(error_x/1000)), -0.2, 0.2)
#             twist_object.linear.x = np.clip(0.2*(1-abs(temp)/0.2), 0, 0.08)

#         if lane_finder:
#             if lane_confirm==False:
#                 # twist_object.linear.x = 0
#                 # twist_object.angular.z = -0.2

#             ###########################################################################################################
#                 def callback(msg):
#                     global dist_r
#                     global dist_front
#                     global dist_l
#                     distances = []
#                     distances_front = []
#                     distances_l = []
#                     head1 = msg.ranges[1:16]
#                     head2 = msg.ranges[344:359]
#                     tail = msg.ranges[280:330]
#                     left = msg.ranges[30:80]
#                     distances_front.extend(head1)
#                     distances_front.extend(head2)
#                     distances.extend(tail)
#                     distances_l.extend(left)
#                     dist_r = sum(distances)/len(distances)
#                     dist_l = sum(distances_l)/len(distances_l)
#                     dist_front = min(distances_front)

#                     if dist_front > 10:
#                         dist_front = 10

#                 pose_subscriber = rospy.Subscriber('scan', LaserScan, callback)

#                 # rate = rospy.Rate(10)
#                 front = 0.8
#                 vel = 0.25
#                 # e = 0
#                 # while e < 1:
#                     # twist_object.linear.x = 0
#                     # twist_object.angular.z = -0.2

#                 error_front = front - dist_front
#                 if error_front > 0:
#                         if dist_r > dist_l:
#                             twist_object.angular.z = -2 * (error_front)
#                             twist_object.linear.x = 0.15/(error_front + 1)
#                             # pub.publish(twist_object)
#                             # self.moveTurtlebot3_object.move_robot(twist_object)
#                         else:
#                             twist_object.angular.z = 2*(error_front)
#                             twist_object.linear.x = 0.15/(error_front + 1)
#                             # pub.publish(twist_object)
#                             # self.moveTurtlebot3_object.move_robot(twist_object)

#                 else:
#                     twist_object.linear.x = vel
#                     twist_object.angular.z = 0
#                     # pub.publish(twist_object)
#                     # self.moveTurtlebot3_object.move_robot(twist_object)

#                         ###########################################################################################
#             # if lane_confirm:
#             #     twist_object.linear.x = 0
#             #     twist_object.angular.z = 0

#         # rospy.loginfo("ANGULAR VALUE SENT===>"+str(twist_object.angular.z))
#         # Make it start turning
#         self.moveTurtlebot3_object.move_robot(twist_object)
        
#     def clean_up(self):
#         self.moveTurtlebot3_object.clean_class()
#         cv2.destroyAllWindows()
        
        

# def main():
#     rospy.init_node('line_following_node', anonymous=True)
    
    
#     line_follower_object = LineFollower()

    
#     rate = rospy.Rate(5)
#     ctrl_c = False
#     def shutdownhook():
#         # works better than the rospy.is_shut_down()
#         line_follower_object.clean_up()
#         rospy.loginfo("shutdown time!")
#         ctrl_c = True
    
#     rospy.on_shutdown(shutdownhook)
    
#     while not ctrl_c:
#         rate.sleep()

    
    
# if __name__ == '__main__':
#     main()
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist, Point
from sensor_msgs.msg import Image
from move_robot import MoveTurtlebot3
from math import pow,atan2,sqrt
from sensor_msgs.msg import LaserScan
from turtlesim.msg import Pose


dist_r = 0
dist_front = 0
dist_l = 0
kps = 1.1
kds = 0.00065
kis = 0.05
uk1s = 0.0
er_1s = 0.0
er_2s = 0.0
errors = 0.0
right = 0
left = 0

class LineFollower(object):

    def __init__(self):
    
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.moveTurtlebot3_object = MoveTurtlebot3()
                
    def camera_callback(self,data):
        
        # We select bgr8 because its the OpneCV encoding by default
        try:
            cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            print(e)
            
        # We get image dimensions and crop the parts of the image we dont need
        height, width, channels = cv_image.shape
        crop_img = cv_image[(height)/2+180:(height)/2+200][1:width]
        # velpublish = rospy.Publisher('cmd_vel',Twist,queue_size = 10)
        
        # Convert from RGB to HSV
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        
        # Define the Yellow Colour in HSV

        """
        To know which color to track in HSV use ColorZilla to get the color registered by the camera in BGR and convert to HSV. 
        """

        # Threshold the HSV image to get only yellow colors
        lower_yellow = np.array([20,100,100])
        upper_yellow = np.array([50,255,255])
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Calculate centroid of the blob of binary image using ImageMoments
        m = cv2.moments(mask, False)
        try:
            cx, cy = m['m10']/m['m00'], m['m01']/m['m00']
            lane_finder = False
            lane_confirm = True
        except ZeroDivisionError:
            cx, cy = height/2, width/2
            lane_finder = True
            lane_confirm = False

        res = cv2.bitwise_and(crop_img, crop_img, mask= mask)
        # twist_object = Twist()
        
        # Draw the centroid in the resultut image
        # if (res.any()!=0):
        #     print("True")
        #     cv2.circle(res,(int(cx), int(cy)), 10,(0,0,255),-1)

        #     cv2.imshow("Original", cv_image)
        #     cv2.imshow("MASK", mask)
        #     cv2.imshow("RES", res)
        #     cv2.waitKey(1)
            
        #     """
        # Enter controller here.
        #     """
        #     error_x = cx - (height / 2) - 89
        #     twist_object = Twist()
        #     twist_object.linear.x = 0.05
        #     twist_object.angular.z = -error_x / 2250
      
        # elif(res.any()==0):
        #     print("False")
        global kps, kds, kis, uk1s, er_1s, er_2s,errors
        def callback(msg):
            global right,left
            # global kps, kds, kis, uk1s, er_1s, er_2s
            frontleft = msg.ranges[20:80]
            frontright = msg.ranges[300:339]
            left = []
            right = []
            for i in frontleft:
                if 0 < i < 10:
                    left.append(i)
            for j in frontright:
                if 0 < j < 10:
                    right.append(j)
            return right, left

        if(res.any()==0):
            rospy.Subscriber('scan', LaserScan, callback)
            velpublish = rospy.Publisher('cmd_vel',Twist,queue_size = 10)
            twist_object = Twist()
            print("False")
            errors = np.mean(right) - np.mean(left)
            k_1s = kps + kis + kds
            k_2s = -kps - (2.0 * kds)
            k_3s = kds

            uks = uk1s + (k_1s * errors) + (k_2s * er_1s) + (k_3s * er_2s)
            uks = uks
            uk1s = uks
            er_2s = er_1s
            er_1s = errors
            twist_object.linear.x = 0.1

            if errors == 0.0:
                twist_object.angular.z = 0.0
            else:
                twist_object.angular.z = -uks
            velpublish.publish(twist_object)

        elif (res.any()!=0):
            print("True")
            cv2.circle(res,(int(cx), int(cy)), 10,(0,0,255),-1)

            cv2.imshow("Original", cv_image)
            cv2.imshow("MASK", mask)
            cv2.imshow("RES", res)
            cv2.waitKey(1)
            
            """
        Enter controller here.
            """
            velpublish = rospy.Publisher('cmd_vel',Twist,queue_size = 10)
            error_x = cx - (height / 2) - 89
            twist_object = Twist()
            twist_object.linear.x = 0.05
            twist_object.angular.z = -error_x / 2250
            velpublish.publish(twist_object)
            # pose_subscriber = rospy.Subscriber('scan', LaserScan, callback)

def main():
    rospy.init_node('line_following_node', anonymous=True)
    
    
    line_follower_object = LineFollower()

    
    rate = rospy.Rate(5)
    ctrl_c = False
    def shutdownhook():
        # works better than the rospy.is_shut_down()
        # line_follower_object.clean_up()
        rospy.loginfo("shutdown time!")
        ctrl_c = True
    
    rospy.on_shutdown(shutdownhook)
    
    while not ctrl_c:
        rate.sleep()

    
    
if __name__ == '__main__':
    main()

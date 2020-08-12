#!/usr/bin/env python
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from apriltag_ros.msg import AprilTagDetectionArray
from move_robot_BOT import MoveTurtlebot3
from people_msgs.msg import PositionMeasurementArray
from nav_msgs.msg import Odometry
# from tf import tf_conversions
import tf

x_diff = 0
z_diff = 0


class LegFollower(object):

    def __init__(self):

        self.bridge_object = CvBridge()
        self.moveTurtlebot3_object = MoveTurtlebot3()


    def callback(self,data):
        global x_diff
        global z_diff
        # extracting the relative positions of the tag in X and Z axis
        # x_diff = data.detections[0].pose.pose.pose.position.x
        # z_diff = data.detections[0].pose.pose.pose.position.z
        x = data.people[0].pos.x
        # print(type(x))
        # print(x)


    def callbackpos(self,msg):
        # cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        # cv2.imshow("Tag Scanner", cv_image)
        # cv2.waitKey(1)

        pose = Twist()

        quaternion = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
        euler = tf.transformations.euler_from_quaternion(quaternion)
        roll = euler[0]
        pitch = euler[1]
        yaw = euler[2]




        
        # roll = 0
        # pitch = 0
        # yaw = 0
        d = msg.pose.pose.orientation
        # pose.orientation = msg.Quaternion(*tf_conversions.transformations.quaternion_from_euler(roll, pitch, yaw))
        # d = msg.twist.twist.angular
        # print(type(d))
        print(euler)


if __name__ == '__main__':

    # Defining publisher and subscriber
    
    rospy.init_node('Follow_apriltag', anonymous=True)
    x = TagFollower()
    vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    tag_sub = rospy.Subscriber('/people_tracker_measurements', PositionMeasurementArray, x.callback)
    tag_sub2 = rospy.Subscriber('/odom', Odometry, x.callbackpos)

    # P-control over steering and linear forward velocity for apriltag following
    rate = rospy.Rate(10)
    vel = Twist()

    while not rospy.is_shutdown():

        # Linear velocity control
        Kp_linear = 0.25
        Kp_angular = 5
        f = 0
        if z_diff < 0.3:
            vel.linear.x = 0
        else:
            vel.linear.x = z_diff*Kp_linear

        # Steering Control
        if x_diff < 0: f = 1
        if x_diff > 0: f = -1
        vel.angular.z = f * Kp_angular * abs(x_diff)
        # publish velocity
        vel_pub.publish(vel)

        rate.sleep()
    rospy.spin()

#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time


def move(speed, distance, isForward):
    velocity_message = Twist()
    if (isForward):
        velocity_message.linear.x = abs(speed)
    else:
        velocity_message.linear.x = -abs(speed)
    velocity_message.linear.y = 0
    velocity_message.linear.z = 0

    velocity_message.angular.x = 0
    velocity_message.angular.y = 0
    velocity_message.angular.z = 0

    t0 = rospy.Time.now().to_sec()
    current_distance = 0
    loop_rate = rospy.Rate(10)

    # velocity publisher
    velocity_publisher = rospy.Publisher("/turtle1/cmd_vel", Twist,  queue_size=10)

    while True:
        velocity_publisher.publish(velocity_message)
        t1 = rospy.Time.now().to_sec()
        current_distance = speed * (t1-t0)
        loop_rate.sleep()

        if not (current_distance < distance):
            rospy.loginfo("reached")
            break



def rotate(angular_speed, relative_angle, clockwise):

    velocity_message = Twist()
    velocity_message.linear.x = 0
    velocity_message.linear.y = 0
    velocity_message.linear.z = 0

    velocity_message.angular.x = 0
    velocity_message.angular.y = 0

    if (clockwise):
        velocity_message.angular.z = -abs(angular_speed)
    else:
        velocity_message.angular.z = abs(angular_speed)

    current_angle = 0.0
    t0 = rospy.Time.now().to_sec()
    loop_rate = rospy.Rate(10)
    # velocity publisher
    velocity_publisher = rospy.Publisher(
        "/turtle1/cmd_vel", Twist,  queue_size=10)

    while True:
        velocity_publisher.publish(velocity_message)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed * (t1-t0)
        loop_rate.sleep()
        if current_angle > relative_angle:
            rospy.loginfo("reached")
            break



def degrees2radians(angle_in_degrees):
    return angle_in_degrees*(math.pi/180.0)

def square_openloop():
    global x, y, yaw
    loop = rospy.Rate(0.5)

    move(0.2, 2.0, True)
    rotate(0.2, degrees2radians(90), False)
    loop.sleep()
    move(0.2, 2.0, True)

    rotate(0.2, degrees2radians(90), False)
    loop.sleep()
    move(0.2, 2.0, True)
    rotate(0.2, degrees2radians(90), False)
    loop.sleep()
    move(0.2, 2.0, True)

    rotate(degrees2radians(11.5), degrees2radians(90), False)

if __name__ == '__main__':
    try:
        # init node
        rospy.init_node('turtlesim_motion_pose', anonymous=True)
        square_openloop()

    except rospy.ROSInterruptException:
        pass
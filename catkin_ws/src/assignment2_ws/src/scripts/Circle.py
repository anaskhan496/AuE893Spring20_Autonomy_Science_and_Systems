#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import math
import time

def circle():
    velocity_message = Twist()

    constant_speed = 4
    rk = 3.5
    loop_rate = rospy.Rate(1)

    # publisher
    cmd_vel_topic = '/turtle1/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    while True:

        rk = rk
        velocity_message.linear.x = rk
        velocity_message.linear.y = 0
        velocity_message.linear.z = 0

        velocity_message.angular.x = 0
        velocity_message.angular.y = 0
        velocity_message.angular.z = constant_speed
        print("velocity_message.x = %s" %velocity_message.linear.x)
        print("velocity_message.x = %s" %velocity_message.angular.z)

        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()

    # stop robot 
    velocity_message.linear.x = 0
    velocity_message.angular.z = 0
    velocity_publisher.publish(velocity_message)


if __name__ == '__main__':
    try:
        # init node
        rospy.init_node('turtlesim_cleaner', anonymous=True)

        circle()

    except rospy.ROSInterruptException:
        pass
#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import math

def rotate(angular_speed, angle, Clockwise):
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    #Converting from angles to radians
    relative_angle = angle*math.pi/180
    #We wont use linear components
    vel_msg.linear.x=0
    vel_msg.linear.y=0
    vel_msg.linear.z=0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0

    # Checking if our movement is CW or CCW
    if (Clockwise == True):
        vel_msg.angular.z = -abs(angular_speed)
    else:
        vel_msg.angular.z = abs(angular_speed)
    # Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_angle = 0.0
   
    while (current_angle < relative_angle):
        velocity_publisher.publish(vel_msg)
        t1 = rospy.Time.now().to_sec()
        current_angle = angular_speed*(t1-t0)

    #Forcing our robot to stop
    vel_msg.angular.z = 0
    velocity_publisher.publish(vel_msg)

def straight_line(speed, distance, isForward):
    # Starts a new node
    velocity_publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    #Checking if the movement is forward or backwards
    if(isForward == True):
        vel_msg.linear.x = abs(speed)
    else:
        vel_msg.linear.x = -abs(speed)
    #Since we are moving just in x-axis
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0
    vel_msg.angular.z = 0

    
    #Setting the current time for distance calculus
    t0 = rospy.Time.now().to_sec()
    current_distance = 0

    #Loop to move the turtle in an specified distance
    while (current_distance < distance):
        #Publish the velocity
        velocity_publisher.publish(vel_msg)
        #Takes actual time to velocity calculus
        t1=rospy.Time.now().to_sec()
        #Calculates distancePoseStamped
        current_distance= speed*(t1-t0)
    #After the loop, stops the robot
    vel_msg.linear.x = 0
    #Force the robot to stop
    velocity_publisher.publish(vel_msg)



def square_openloop():
    rospy.init_node('assignment3_turtlebot3', anonymous=True)
    straight_line(0.2,2,True)
    rotate(0.2,90,False)
    straight_line(0.2,2,True)
    rotate(0.2,90,False)
    straight_line(0.2,2,True)
    rotate(0.2,90,False)
    straight_line(0.2,2,True)
    rotate(0.2,90,False)


if __name__ == '__main__':
    
    try:    #Testing our function
        square_openloop()
    except rospy.ROSInterruptException: pass
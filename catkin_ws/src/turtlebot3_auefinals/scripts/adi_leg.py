#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from people_msgs.msg import PositionMeasurementArray
from people_msgs.msg import PositionMeasurement
from geometry_msgs.msg import Point
from geometry_msgs.msg import PoseArray
from nav_msgs.msg import Odometry
x_bot = 0
y_bot = 0
z_bot = 0

def bot_location(msg):
	global x_bot, y_bot, z_bot	
	x_bot = msg.pose.pose.position.x
	y_bot = msg.pose.pose.position.y
	z_bot = msg.pose.pose.position.z
	
	return x_bot, y_bot, z_bot

def legtracking_callback(detect):
       
	
	x = detect.poses[0].position.x
	y  = detect.poses[0].position.y
	z = detect.poses[0].position.z
	#print(x,y,z)	

	vel_msg = Twist()	
	
	x_error = x - x_bot
	y_error = y - abs(y_bot)
	print("x:",x_error,"y:", y_error)
	kp_angular = 0.01
	kp_linear = 1

	if y_error > 0 and x_error > 0 :
		vel_msg.angular.z = -kp_angular*y_error
		vel_msg.linear.x =  kp_linear*abs(x_error)
	#elif y_error < 0.2:
	#	vel_msg.angular.z = 0
	else:	
		vel_msg.angular.z = kp_angular*y_error
		vel_msg.linear.x = kp_linear*abs(x_error)

	    
	pub.publish(vel_msg)
        
    	

rospy.init_node('leg_tracking',anonymous=True)
bot_location = rospy.Subscriber("/odom",Odometry, bot_location)
leg_tracking = rospy.Subscriber("/to_pose_array/leg_detector",PoseArray, legtracking_callback)
pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
vel_msg=Twist()
rospy.spin()


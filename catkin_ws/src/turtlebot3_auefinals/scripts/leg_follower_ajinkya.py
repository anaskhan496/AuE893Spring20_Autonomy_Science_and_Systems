#!/usr/bin/env python
import rospy
from geometry_msgs.msg  import Twist, Point,PoseArray
from turtlesim.msg import Pose
from math import pow,atan2,sqrt
from sensor_msgs.msg import LaserScan

#dist_front = 0


def callback(msg):
    # global x,z
    # if not msg:
    # 	pos  = 0
    # else:
    # x = msg.detections[0].pose.pose.pose.position.x

    # print ('X is', x )
    try:
        # print('Pose leg 1x',msg.poses)
        print('----------------------------')
        # print('Pose leg 2', msg.poses[0].position.x)
        x = msg.poses[0].position.x
        y = msg.poses[0].position.y
        # x2 = msg.poses[1].position.x
        # y2 = msg.poses[1].position.y
        # print('X and Y done')
        # x = (x1 + x2)/2
        # y = (y1 + y2)/2
        print ('Position is', x )
        print('Orientation is', y)
        kp_ang = 0.25
        kp_lin = 0.1
        # move.linear.x = y/1.5
        # move.angular.z = x/2.5
        # pub.publish(move)
        if y >= 0.2:
            move.angular.z = kp_ang * y
        elif y < 0.2:
            move.angular.z = kp_ang * y

        if x >= 0.25 or x<= -0.25:
            move.linear.x = kp_lin * x
        else:
            move.linear.x = 0
            # print(move.linear.x, move.angular.z)
        pub.publish(move)

    except IndexError:
        # print('Out of index,,,yoooo')
        x = 0
        z = 0
        move.linear.x = z * 5
        move.angular.z = x * 50
        pub.publish(move)


#    	head = msg.ranges[1:50]
#    	tail = msg.ranges[300:359]
#    	distances.extend(head)
#    	distances.extend(tail)
#    	dist = max(distances)
# print("The min distance is " + str(dist))

# rate = rospy.Rate(10)
move = Twist()
rospy.init_node('vel_scan', anonymous=True)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
# rate = rospy.Rate(10)
subscriber = rospy.Subscriber('/to_pose_array/leg_detector', PoseArray, callback)
rospy.spin()
# pose = Pose()
# rate = rospy.Rate(10)
# move = Twist()
# print('X and Z are', x,z)
# move.linear.x = z*5
# move.angular.z = x*50


#    stop_dist = 0.5
# while dist > stop_dist:
# move.linear.x = 0.2
# pub.publish(move)
#	rate.sleep()

#    move.linear.x = 0
# pub.publish(move)
# rospy.spin()
# if __name__ == '__main__':
#   try:
#      x = turtlebot()
# except rospy.ROSInterruptException: pass
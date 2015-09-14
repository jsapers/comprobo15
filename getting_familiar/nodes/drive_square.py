#!/usr/bin/env python
'''Using the cmd_vel topic tells the robot to move forward turn left then
repeat 4 times then finally stops'''
import rospy
import time
from geometry_msgs.msg import Twist


if  __name__=='__main__':
	
	pub = rospy.Publisher('cmd_vel', Twist)
	rospy.init_node('drive_square')
	
	for i in range(4):

		twist = Twist()
		twist.linear.x = 1; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)


		time.sleep(2)

		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 1
		pub.publish(twist)

		time.sleep(1.65)


	twist = Twist()
	twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
	twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
	pub.publish(twist)

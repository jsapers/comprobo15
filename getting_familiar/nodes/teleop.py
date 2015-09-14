#!/usr/bin/env python
'''Publishes a cmd_vel based on the key  inputs it recieves:
	'w' goes forward
	's' geas back
	'a' goes left
	'd' goes right 
	space stops'''
import rospy
import tty
import select
import sys
import termios
from geometry_msgs.msg import Twist

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


if  __name__=='__main__':
	settings = termios.tcgetattr(sys.stdin)

	
	pub = rospy.Publisher('cmd_vel', Twist)
	rospy.init_node('teleop')
	x=0
	th=0
	key=''
	try:
		print 'use wasd and space controls to move forward, left, backwards,right and stop respectively'
		
		while 1:
			
			key = getKey()
			
			if key == 'w':
				x=1
				th=0

			if key == 's':
				x=-1
				th=0

			if key == 'a':
				th=1
				x=0

			if key == 'd':
				th=-1
				x=0	
			if key == ' ':
				th=0
				x=0	

			if key == "\x03":
				break

			twist = Twist()
			twist.linear.x = x; twist.linear.y = 0; twist.linear.z = 0
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th
			print twist
			pub.publish(twist)

	finally:

		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
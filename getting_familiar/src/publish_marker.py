#!/usr/bin/env python

""" Publishing a simple arrow marker"""

from visualization_msgs.msg import Marker
import rospy

rospy.init_node('publish_marker')



pub = rospy.Publisher("/my_marker", Marker)

r = rospy.Rate(10)
while not rospy.is_shutdown():
	my_mark=Marker()
	my_mark.header.frame_id="base_link"
	my_mark.header.stamp= rospy.Time.now()
	my_mark.type=Marker.SPHERE
	my_mark.pose.position.x = 1
	my_mark.pose.position.y = 2
	my_mark.pose.position.z = 0
	my_mark.pose.orientation.x = 0
	my_mark.pose.orientation.y = 0
	my_mark.pose.orientation.z = 0
	my_mark.pose.orientation.w = 1
	my_mark.scale.x=.5
	my_mark.scale.y=.5
	my_mark.scale.z=.1
	my_mark.color.a=1
	my_mark.color.r=1
	my_mark.color.g=0
	my_mark.color.b=0


	pub.publish(my_mark)
	r.sleep()
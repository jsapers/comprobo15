#!/usr/bin/env python
'''Using PID'''
import rospy
import time
import math

from tf import TransformListener
from geometry_msgs.msg import Twist
from neato_node.msg import Bump
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped, Point
from std_msgs.msg import Header


class Person_Follow(object):
    def __init__(self):
        rospy.init_node('person_follow')

        self.twist=Twist()
        self.twist.linear.x = 0; self.twist.linear.y = 0; self.twist.linear.z = 0
        self.twist.angular.x = 0; self.twist.angular.y = 0; self.twist.angular.z = 0

        self.dist0=0

        self.target=1
        self.p_angle=.01
        self.i_angle=.0005
        self.p_d=1
        self.i_d=.005
        self.error_angle_sum=0
        self.error_d_sum=0
        
        self.centroid=Point(x=0,y=0)
        self.header_msg=Header(stamp=rospy.Time.now(), frame_id='base_link')



    def Find_Pos(self, Data):

        d={}
        for i in range(len(Data.ranges)):
            if(Data.ranges[i]!=0):
                d[i]=Data.ranges[i]

        d_sum_x=0
        d_sum_y=0
        d_count=0
        for key in d:
            if key>345 or key<15:
                
                d_sum_x+=d[key]*math.cos(math.radians(key))
                d_sum_y+=d[key]*math.sin(math.radians(key))
                d_count+=1
                


        self.dist0=Data.ranges[0]
        d_avg_x=d_sum_x/d_count
        d_avg_y=d_sum_y/d_count

        self.centroid.x = d_avg_x
        self.centroid.y = d_avg_y

#        print self.centroid.x


    def run(self):
        
        rospy.Subscriber("/scan",LaserScan,self.Find_Pos,queue_size=10)
        self.pub = rospy.Publisher('cmd_vel',Twist,queue_size=10)
      
        self.t=TransformListener()

        self.pub_centroid = rospy.Publisher('/centroid',PointStamped,queue_size=10)
        r = rospy.Rate(30)
        while not rospy.is_shutdown():
            theta=0
            if self.centroid.x!=0:
                theta = 3*math.atan2(self.centroid.y,self.centroid.x)
                print theta
            self.twist.angular.z = theta

            print self.centroid.x
            if self.dist0 == 0:
                speed = 1
            else:
                speed = .1 *(self.dist0-.5)
            
            self.twist.linear.x=speed

            self.pub.publish(self.twist)
            #print self.t.allFramesAsString()
            try:
                point_stamped_msg = PointStamped(header=self.header_msg,
                                     point=self.t.waitForTransform('odom','base_link',target.header.stamp, rospy.Duration(0.5))Point(x=-self.centroid.x, y=-self.centroid.y))
                self.header_msg.stamp = rospy.Time.now()
                #print self.header_msg
                self.t.waitForTransform('odom','base_link',self.header_msg.stamp, rospy.Duration(0.5))
                point_stamped_msg_odom = self.t.transformPoint('/odom',point_stamped_msg)
                #print point_stamped_msg_odom
                self.pub_centroid.publish(point_stamped_msg_odom)
            except Exception as inst:
                print inst
            
            #print self.centroid.x


if  __name__=='__main__':
    
    p_f = Person_Follow()
    while not rospy.is_shutdown():
        p_f.run()
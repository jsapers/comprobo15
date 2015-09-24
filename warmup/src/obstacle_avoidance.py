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


class Obstacle_Avoidance(object):
    def __init__(self,target):

        self.twist=Twist()
        self.twist.linear.x = 0; self.twist.linear.y = 0; self.twist.linear.z = 0
        self.twist.angular.x = 0; self.twist.angular.y = 0; self.twist.angular.z = 0

        self.dist0=[]

        self.target=target

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
                


        self.dist0=Data.ranges[355:360]+Data.ranges[0:5]


    def run(self):
        
        rospy.Subscriber("/scan",LaserScan,self.Find_Pos,queue_size=10)
        self.pub = rospy.Publisher('cmd_vel',Twist,queue_size=10)
      
        r = rospy.Rate(30)
        while not rospy.is_shutdown():
            speed =1
            theta=0
            for dist in self.dist0:
                if dist!=0:
                    speed = .1 *(dist-.1)
                    theta=2


            print speed
            print theta
            self.twist.linear.x=speed
            self.twist.angular.z = theta
            self.pub.publish(self.twist)
            #print self.t.allFramesAsString()
            

if  __name__=='__main__':
    rospy.init_node('obstacle_avoidance')
    target_header = Header(stamp=rospy.Time.now(), frame_id='odom')
    target_point = Point(x=1,y=1)
    target = PointStamped(header=target_header,point=target_point)
    o_a = Obstacle_Avoidance(target)
    while not rospy.is_shutdown():
        o_a.run()
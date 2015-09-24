#!/usr/bin/env python
'''Using PID'''
import rospy
import time
from geometry_msgs.msg import Twist
from neato_node.msg import Bump
from sensor_msgs.msg import LaserScan

class Wall_Follow(object):
    def __init__(self):

        self.twist=Twist()
        self.twist.linear.x = 1; self.twist.linear.y = 0; self.twist.linear.z = 0
        self.twist.angular.x = 0; self.twist.angular.y = 0; self.twist.angular.z = 0

        self.dist0=[]

        self.target=1
        self.p_angle=.01
        self.i_angle=.0005
        self.p_d=.1
        self.i_d=.005
        self.error_angle_sum=0
        self.error_d_sum=0




    def Find_Pos(self, Data):

        d={}
        for i in range(len(Data.ranges)):
            if(Data.ranges[i]!=0):# Data.ranges[i+1]!=0 and Data.ranges[i-1]!=0):
                d[i]=Data.ranges[i]

        (min_key,min_d)=min(d.items(), key=lambda x: x[1]) 
        print min_key
        if min_key<180:
            error_angle=min_key-90
            error_d=-(min_d - self.target)
        else:
            error_angle=min_key-270
            error_d=self.target-min_d

        print "error d",error_d
        #print "error a", error_angle
        self.error_angle_sum+=error_angle

        
        self.error_d_sum+=error_d

        self.dist0=Data.ranges[355:360]+Data.ranges[0:5]

        self.PID(error_angle,error_d,self.error_angle_sum,self.error_d_sum)
        

    def PID(self,e_angle,e_d,e_angle_sum,e_d_sum):
        output_angle=self.p_angle*e_angle+self.p_d*e_d#+self.i_angle*e_angle_sum#+self.i_d*e_d_sum
        print output_angle


        self.twist.linear.x = 0.3; self.twist.linear.y = 0; self.twist.linear.z = 0
        self.twist.angular.x = 0; self.twist.angular.y = 0; self.twist.angular.z = output_angle


    def run(self):
        rospy.init_node('wall_follow')
        rospy.Subscriber("/scan",LaserScan,self.Find_Pos,queue_size=10)
        self.pub = rospy.Publisher('cmd_vel',Twist,queue_size=10)
        r = rospy.Rate(30)
        while not rospy.is_shutdown():
            self.pub.publish(self.twist)
            wall=False
            for dist in self.dist0:
                if dist<.5:
                    break
            else:
                return "Obstacle Avoidence"
                pass


class Obstacle_Avoidance(object):
    def __init__(self):

        self.twist=Twist()
        self.twist.linear.x = 0; self.twist.linear.y = 0; self.twist.linear.z = 0
        self.twist.angular.x = 0; self.twist.angular.y = 0; self.twist.angular.z = 0

        self.dist0=[]




    def Find_Pos(self, Data):


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
                    
                else:
                    print'hi2'
                    return "Wall Follow"


            print speed
            print theta
            self.twist.linear.x=speed
            self.twist.angular.z = theta
            self.pub.publish(self.twist)

if  __name__=='__main__':
    w_f = Wall_Follow()
    o_a = Obstacle_Avoidance()
    action = "Wall Follow"
    while not rospy.is_shutdown():
        if action == "Wall Follow":
            w_f.run()
        elif action == "Obstacle Avoidence":    
            o_a.run()
#!/usr/bin/env
import rospy
import math

from std_msgs.msg import String

from std_msgs.msg import Float64
from std_msgs.msg import Int32
from nav_msgs.msg import Odometry

from geometry_msgs.msg import PoseStamped 
from geometry_msgs.msg import PoseWithCovarianceStamped

# distande measure #
odom_x = 5.0
odom_y = 0.0
local_x = 0.0
local_y = 0.0
distance = 1.0

def callback_odom(msg):
    global odom_x
    global odom_y
    odom_x = msg.pose.pose.position.x
    odom_y = msg.pose.pose.position.y
    #print "received odom pose"
    #print odom_x
    
def callback_localizer(msg):
    global local_x
    global local_y
    local_x = msg.pose.position.x
    local_y = msg.pose.position.y
    #print "received localizer pose"
    #print local_y

def talk_to_me():
    # init node
    rospy.init_node('publisher_node', anonymous=True)

    # init subscribers and Publishers
    pub = rospy.Publisher('distance_odom_ndt', Float64, queue_size=10)
    sub_odom = rospy.Subscriber('/carla/ego_vehicle/odometry', Odometry, callback_odom)
    sub_localizer = rospy.Subscriber('/localizer_pose', PoseStamped, callback_localizer)

    # make ros things
    rate = rospy.Rate(20)
    rospy.loginfo("Distance Node started, now publishing distance between odom and ndt")

    while not rospy.is_shutdown():
        
        # distance #
        distance = math.sqrt((odom_x-local_x)*(odom_x-local_x)+(odom_y-local_y)*(odom_y-local_y))
        msg = distance
        pub.publish(msg)
        rospy.loginfo("Current distance %s", distance)
       
        rate.sleep()
        

if __name__ == '__main__':

    talk_to_me()



# Auswertung wie lange die Lokalisierung dauert

# rospy.wait / wait for message
# timeout
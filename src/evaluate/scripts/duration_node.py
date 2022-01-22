#!/usr/bin/env
import rospy
import math
import datetime

from std_msgs.msg import String
from std_msgs.msg import Float64
from datetime import timedelta
from enum import Enum

from geometry_msgs.msg import PoseWithCovarianceStamped

# Enumeration for state_machine #
class State(Enum):
    idle = 0
    received_initial_pose = 1
    reached_initial_pose = 2
    localisation_running = 3

# time measure #
start_localization = datetime.datetime.now()
distance = 0.0
state = State.idle

def get_time():
    return datetime.datetime.now()

def callback_distance(msg):
    global distance     
    distance = msg.data
    #rospy.loginfo("Current distance: %s", distance)    # for debugging

def callback_initial_pose(msg):
    global state
    state = State.received_initial_pose
    

if __name__ == '__main__':

    # init node
    rospy.init_node('duration_node', anonymous=True)

    # init subscribers and Publishers
    sub_distance = rospy.Subscriber('distance_odom_ndt', Float64, callback_distance)
    sub_initial_pose = rospy.Subscriber('initialpose', PoseWithCovarianceStamped, callback_initial_pose)

    # make ros things
    rate = rospy.Rate(20)
    rospy.loginfo("Duration Node started, now publishing localization times")
    
    # state variables
    localisation_running = False
    took_too_long = False
    reached_initial_pose = False

    while not rospy.is_shutdown():
        
        # rospy.loginfo(state.name)  # for debugging

        # received initial pose #
        if state == State.received_initial_pose:
            if distance > 0.5:
                state = State.reached_initial_pose
                #rospy.loginfo("received initialpose") # for debugging

        # reached initial pos #
        elif state == State.reached_initial_pose:
            start_localization = get_time()
            state = State.localisation_running
            # rospy.loginfo("reached initialpose, now localisating") # for debugging

        elif state == State.localisation_running:
            # duration #
            end_localization = get_time()
            duration = timedelta.total_seconds(end_localization - start_localization)

            # check for successful localisation
            if distance < 0.1:
                if duration < 1.0:  # successful localisation
                    rospy.loginfo("Successful localisation!")
                    rospy.loginfo("lookalisation took %s s", duration)
                else:               # successful localisation but took too long
                    rospy.loginfo("No successful localisation!")
                    rospy.loginfo("lookalisation took %s s", duration)
                
                state = State.idle
            else:
                if duration > 5.0:  # after 3s not below 0.1m distance
                    rospy.loginfo("No successful localisation!")
                    rospy.loginfo("Publish new initial Pose")
                    state = State.idle

        rate.sleep() 
#!/usr/bin/env
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
   

if __name__ == '__main__':

    # init node
    initialpose_publisher = rospy.init_node('initialpose_node', anonymous=True)

    # init subscribers and Publishers
    pub_initialpose = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=10)

    # FZG-Pos x=-50.0; y=0.0
    pose_msg = PoseWithCovarianceStamped()
    pose_msg.header.frame_id = "map"
    pose_msg.pose.pose.position.x = -52.5
    pose_msg.pose.pose.position.y = 0
    pose_msg.pose.pose.position.z = 0.0
    pose_msg.pose.pose.orientation.x = 0.0
    pose_msg.pose.pose.orientation.y = 0.0
    pose_msg.pose.pose.orientation.z = 0.0 #0.676  
    pose_msg.pose.pose.orientation.w = 1.0 #0.737

    sent_msg = False

    while not rospy.is_shutdown ():
        
        try:
            input = raw_input()
            if input == "0":
                rospy.loginfo("reset successful")
                sent_msg = False
            elif input == "1":
                if sent_msg == False:
                    rospy.loginfo("initialpose sent")
                    pub_initialpose.publish(pose_msg)
                    sent_msg = True
        except:
            rospy.sleep(0.1)
        
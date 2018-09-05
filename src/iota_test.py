#! /usr/bin/env python
import rospy
from std_msgs.msg import Header
from iota_ros_pkg.msg import send_transaction
#coding=utf-8
from iota import *
from iota.adapter.wrappers import RoutingWrapper

REC_ADDRESS='MICHIS99ROS99TEST'
SEED ='DUMMYSEED99UNCOMMENT99IN99IOTA99ROS99MAIN99FOR99PUBLISHING99999999999999999999999'
DEPTH = 3
VALUE = 0
i=0
TAG = 'TEST9TAG9999'
MSG = 'TEST99MESSAGE'

iota_send_pub = rospy.Publisher('/iota/send_transaction', send_transaction, queue_size=1)
rospy.init_node('iota_test_node', anonymous=False)
r = rospy.Rate(5)
h = Header()

def iota_info():
	i=0
	iotast = send_transaction()
	iotast.depth=DEPTH
	iotast.address=REC_ADDRESS
	iotast.sending_value=VALUE
	iotast.tag=TAG
	iotast.RDY=True
	print"READY"
	while not rospy.is_shutdown():
		h.stamp = rospy.Time.now()
		iotast.header = h
		iotast.message=str(h)
		iota_send_pub.publish(iotast)
		i=i+1
		r.sleep()
	
if __name__ == '__main__':
	try:
		iota_info()
	except rospy.ROSInterruptException: pass











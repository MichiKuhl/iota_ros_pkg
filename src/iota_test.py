#! /usr/bin/env python
import rospy
from std_msgs.msg import Header
from iota_ros_pkg.msg import iota_st
#coding=utf-8
from iota import *
from iota.adapter.wrappers import RoutingWrapper

NODE_POW='https://node.iota.org:443'	
NODE_ROUTING='https://node.node.org:443'
REC_ADDRESS='GZ9QXPNSKCQ9MH9AKPSKNVVZHZZNMLWLXMBYSQHRYGH9JYOTFCEUMBBDNQKXZVHGGJRYNBSMDOOJNJCHZGEGLLVPIC'
SEED ='DUMMYSEED99UNCOMMENT99IN99IOTA99ROS99MAIN99FOR99PUBLISHING99999999999999999999999'
DEPTH = 13
VALUE = 0
TAG = 'TEST9TAG9999'
MSG = 'TEST99MESSAGE'

iota_send_pub = rospy.Publisher('/iota/iota_send', iota_st, queue_size=10)
rospy.init_node('iota_test_node', anonymous=False)
r = rospy.Rate(5)
h = Header()

def iota_info():
	iotast = iota_st()
	iotast.node_pow= NODE_POW 
	iotast.node_routing=NODE_ROUTING
	iotast.seed=SEED			 #uncomment this part to publish the seed in a topic
	iotast.depth=DEPTH
	iotast.address=REC_ADDRESS
	iotast.sending_value=VALUE
	iotast.tag=TAG
	iotast.message=MSG
	iotast.RDY=True
	print"READY"
	while not rospy.is_shutdown():
		h.stamp = rospy.Time.now()
		iotast.header = h
		iota_send_pub.publish(iotast)
		r.sleep()
	
if __name__ == '__main__':
	try:
		iota_info()
	except rospy.ROSInterruptException: pass











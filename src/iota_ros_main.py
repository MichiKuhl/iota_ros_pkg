#! /usr/bin/env python
import rospy
from std_msgs.msg import Header
from iota_ros_pkg.msg import iota_st
#coding=utf-8
from iota import *
from iota.adapter.wrappers import RoutingWrapper

NODE_POW='https://node.iota.org:443'	#NODE for POW (don't need to be online)
NODE_ROUTING='https://node.iota.org:443'
REC_ADDRESS='GZ9QXPNSKCQ9MH9AKPSKNVVZHZZNMLWLXMBYSQHRYGH9JYOTFCEUMBBDNQKXZVHGGJRYNBSMDOOJNJCHZGEGLLVPIC'
SEED ='DUMMYSEED99UNCOMMENT99IN99IOTA99ROS99MAIN99FOR99PUBLISHING99999999999999999999999'
DEPTH = 13
VALUE = 0
TAG = 'TEST9TAG9999'
MSG = 'TESTMESSAGE'

rospy.init_node('iota_node', anonymous=False)
r = rospy.Rate(5)
h = Header()

def iota_send_cb(iotast):
	NODE_POW = iotast.node_pow
	NODE_ROUTING = iotast.node_routing
	SEED = iotast.seed 
	DEPTH = iotast.depth
	REC_ADDRESS = iotast.address
	VALUE = iotast.sending_value
	TAG = iotast.tag
	MSG = iotast.message
	api =\
		Iota(
		RoutingWrapper(NODE_ROUTING)
		.add_route('attachToTangle', NODE_POW),
		seed = SEED
 		)
	transaction = api.send_transfer(
	depth = DEPTH,
 	transfers = [
		ProposedTransaction(
  		address = Address(REC_ADDRESS),
 		value = VALUE,
  		tag = Tag(TAG),
  		message = TryteString.from_string(MSG),
		),
 	],
	)	
def iota_send():
	print"READY"
	rospy.Subscriber("/iota/iota_send", iota_st,iota_send_cb)
	rospy.spin()	

if __name__ == '__main__':
	try:
		iota_send()
	except rospy.ROSInterruptException: pass











#! /usr/bin/env python
import rospy
from iota import *
from std_msgs.msg import Header
from iota_ros_pkg.msg import main
from iota_ros_pkg.msg import send_transaction
from iota.adapter.wrappers import RoutingWrapper

NODE_POW='https://pow5.iota.community:443'	
NODE_ROUTING='https://pow5.iota.community:443'
REC_ADDRESS='MICHIS99ROS99TEST9999999999999999999999999999999999999999999999999999999999999999'
SEED ='DUMMYSEED99UNCOMMENT99IN99IOTA99ROS99MAIN99FOR99PUBLISHING99999999999999999999999'
TAG = 'TEST9TAG9999'
MSG = 'TESTMESSAGE'
VALUE = 0
DEPTH = 3

rospy.init_node('iota_send_transaction', anonymous=False)
h = Header()
print"send_transaction READY"

def get_main(msg):
	NODE_POW= msg.node_pow
	NODE_ROUTING=msg.node_routing
	SEED=msg.seed

def send(msg):
	DEPTH = msg.depth
	REC_ADDRESS = msg.address
	VALUE = msg.sending_value
	TAG = msg.tag
	MSG = msg.message
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

def sub():
	rospy.Subscriber("/iota/main", main,get_main,queue_size=1)				#enter your needed queue_size here
	rospy.Subscriber("/iota/send_transaction", send_transaction,send,queue_size=1)		#enter your needed queue_size here
	rospy.spin()	

if __name__ == '__main__':
	try:
		sub()
		
	except rospy.ROSInterruptException: pass











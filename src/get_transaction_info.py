#! /usr/bin/env python
import urllib2
import json
import rospy
from iota import TryteString
from iota import Iota
from iota_ros_pkg.msg import main
from iota_ros_pkg.msg import transaction_info
from std_msgs.msg import Header

NODE_POW="https://ENTERYOURNODEHERE"	
NODE_ROUTING="https://ENTERYOURNODEHERE"
ADDRESS='MICHIS99ROS99TEST9999999999999999999999999999999999999999999999999999999999999999'# ENTER YOUR ADDRESS HERE

def get_main(msg):
	NODE_POW= msg.node_pow
	NODE_ROUTING=msg.node_routing

def search_new_hash(new,old,single_hash):
	i=0
	t=0
	count = len(old['hashes'])
	while i<count :
		if old['hashes'][i]!=new['hashes'][i]:	
			single_hash=new['hashes'][i]
			break
		i=i+1	
	if len(single_hash)==0:
		single_hash=''
		single_hash=new['hashes'][i+1]
	return single_hash


def trytes_to_ascii(trytes):
	message = ''
	i=2
	while i < 2188:	
		message = TryteString(message + trytes[i])		
		i=i+1
	return message.decode()



new_hash=''
hashes_old=''	
i=0
transaction_info_pub = rospy.Publisher('/iota/transaction_info', transaction_info, queue_size=1)
rospy.init_node('iota_transaction_info', anonymous=False)
transaction_info = transaction_info()
h=Header()
print "get_transaction_message READY"

while not rospy.is_shutdown():
	rospy.Subscriber("/iota/main", main,get_main,queue_size=1)

	command = {
		'command': 'findTransactions',
		'addresses': [ADDRESS]
	}

	stringified = json.dumps(command)

	headers = {
	    'content-type': 'application/json',
	    'X-IOTA-API-Version': '1'
	}

	request = urllib2.Request(url=NODE_ROUTING, data=stringified, headers=headers)
	returnData = urllib2.urlopen(request).read()
	hashes_new = json.loads(returnData)
	if i==0:
		hashes_old=hashes_new
		i=i+1
	if len(hashes_new['hashes']) > len(hashes_old['hashes']): 		
		new_hash=search_new_hash(hashes_new, hashes_old,new_hash)
		hashes_old=hashes_new
		transaction_info.hash=new_hash
		command = {
    			'command': 'getTrytes',
    			'hashes':[new_hash]
		}
		stringified = json.dumps(command)
		headers = {
			'content-type': 'application/json',
			'X-IOTA-API-Version': '1'
		}
		request = urllib2.Request(url=NODE_ROUTING, data=stringified, headers=headers)
		returnData = urllib2.urlopen(request).read()

		jsonData = json.loads(returnData)
		trytes=json.dumps(jsonData['trytes'])	
		message=trytes_to_ascii(trytes)
		transaction_info.message = message
		h.stamp = rospy.Time.now()
		transaction_info.header = h
		transaction_info_pub.publish(transaction_info)
		print message


#! /usr/bin/env python

import urllib2
import json
import rospy
from iota import TryteString, int_from_trits
from iota import Iota
from iota_ros_pkg.msg import main
from iota_ros_pkg.msg import transaction_info
from iota_ros_pkg.msg import confirmed_transaction_info
from std_msgs.msg import Header

NODE_POW="https://YOURNODE"	
NODE_ROUTING="https://YOURNODE"
ADDRESS='MICHIS99ROS99TEST9999999999999999999999999999999999999999999999999999999999999999'# ENTER YOUR ADDRESS HERE
new_hash_list= []
new_hash=''
hashes_old=''	
i=0
j=0
h=Header()
confirmed_transaction_info_pub = rospy.Publisher('/iota/confirmed_transaction_info', confirmed_transaction_info, queue_size=1)
rospy.init_node('iota_confirmed_transaction_info', anonymous=False)
confirmed_transaction_info = confirmed_transaction_info()



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
	value=''
	timestamp=''
	tag=''
	for m in range(2,2188):
		message = TryteString(message + trytes[m])		
	for l in range(2270,2297):
		value = TryteString(value + trytes[l])
	for n in range(2594,2621):
		tag = TryteString(tag + trytes[n])
	for o in range(2324,2333):
		timestamp = TryteString(timestamp + trytes[o])
	return message.decode(),tag,int(int_from_trits(value.as_trits())),int(int_from_trits(timestamp.as_trits()))

def get_confirmation_status():
	
	command = {
		'command': 'getInclusionStates',
		'transactions': new_hash_list,
		'tips': [latestSolidSubtangleMilestone]
	}
	
	stringified = json.dumps(command)
	
	headers = {
		'content-type': 'application/json',
		'X-IOTA-API-Version': '1'
	}

	request = urllib2.Request(url=NODE_ROUTING, data=stringified, headers=headers)
	returnData = urllib2.urlopen(request).read()
	cstatus = json.loads(returnData)
	k=0

	while k<len(new_hash_list):

		if cstatus['states'][k]==True:

			command = {
    				'command': 'getTrytes',
    				'hashes':[new_hash_list[k]]
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
			message,tag,value,timestamp=trytes_to_ascii(trytes)
			confirmed_transaction_info.message = message
			h.stamp = rospy.Time.now()
			
			command = {
				'command': 'getBalances',
				'addresses': [ADDRESS, new_hash_list[k]],
				'threshold': 100
			}

			stringified = json.dumps(command)
			
			headers = {
			'content-type': 'application/json',
			'X-IOTA-API-Version': '1'
			}

			request = urllib2.Request(url=NODE_ROUTING, data=stringified, headers=headers)
			returnData = urllib2.urlopen(request).read()
			jsonData = json.loads(returnData)
			confirmed_transaction_info.header = h
			confirmed_transaction_info.value = value
			confirmed_transaction_info.timestamp = timestamp			
			confirmed_transaction_info.hash=new_hash_list[k]
			confirmed_transaction_info.tag = str(tag)
			confirmed_transaction_info.message = message
			confirmed_transaction_info.address_balance=jsonData['balances'][0]
			confirmed_transaction_info_pub.publish(confirmed_transaction_info)
			new_hash_list.pop(k)
		k=k+1

print "get_c_transaction_info READY"

while not rospy.is_shutdown():
	rospy.Subscriber("/iota/main", main,get_main,queue_size=1)

	if j>0:	
		get_confirmation_status()
	
	command = {
		'command': 'getNodeInfo'
	}

	stringified = json.dumps(command)

	headers = {
		'content-type': 'application/json',
		'X-IOTA-API-Version': '1'
	}

	request = urllib2.Request(url=NODE_ROUTING, data=stringified, headers=headers)
	returnData = urllib2.urlopen(request).read()
	jsonData = json.loads(returnData)
	latestSolidSubtangleMilestone=jsonData['latestSolidSubtangleMilestone']

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
		new_hash_list.append(new_hash)
		j=j+1
		hashes_old=hashes_new

		


cmake_minimum_required(VERSION 2.8.3)
project(iota_ros_pkg)
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

add_message_files(
 FILES
 confirmed_transaction_info.msg
 check_balance_address.msg
 main.msg
 send_transaction.msg
 transaction_info.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS 
   message_runtime
)

catkin_package(
 INCLUDE_DIRS include
  LIBRARIES iota_ros_pkg
  CATKIN_DEPENDS roscpp rospy std_msgs
)


include_directories(
  ${catkin_INCLUDE_DIRS}
)


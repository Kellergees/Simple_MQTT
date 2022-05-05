#!/usr/bin/env python
# -*- coding: utf-8 -*-

from warnings import catch_warnings
import paho.mqtt.client as mqtt
import rospy
import yaml
import os
import string
import time

from geometry_msgs.msg import Twist

HOST = "homedev.bit-plat.com"
PORT = 8883
POST_PATH = "v1/devices/me/attributes"
client = mqtt.Client(client_id="Unimelb_client_linux_sub")
client.tls_set('../mqtt_key/iot_mqtt.pem')
client.tls_insecure_set(True)
client.username_pw_set("PqwuPLhIwwVX0I9AaIPU")

global pub_to_ros_inst

def read_from_received_message_and_publish_to_ros(is_the_red_button_pressed, is_forced_m_mode, is_move_forwards, is_move_backwards, is_turn_left, is_turn_right, set_gear):
    target_speed = Twist()

    if(is_the_red_button_pressed == False):
        if(is_forced_m_mode == True):
            if(set_gear == 1):
                if(is_move_forwards == True):
                    target_speed.linear.x = 0.2
                elif(is_move_backwards == True):
                    target_speed.linear.x = -0.2
            
                if(is_turn_left == True):
                    target_speed.angular.z = 1.0
                elif(is_turn_right == True):
                    target_speed.angular.z = -1.0
            elif(set_gear == 2):
                if(is_move_forwards == True):
                    target_speed.linear.x = 0.4
                elif(is_move_backwards == True):
                    target_speed.linear.x = -0.4
            
                if(is_turn_left == True):
                    target_speed.angular.z = 1.0
                elif(is_turn_right == True):
                    target_speed.angular.z = -1.0
            elif(set_gear == 3):
                if(is_move_forwards == True):
                    target_speed.linear.x = 0.6
                elif(is_move_backwards == True):
                    target_speed.linear.x = -0.6
            
                if(is_turn_left == True):
                    target_speed.angular.z = 1.0
                elif(is_turn_right == True):
                    target_speed.angular.z = -1.0
    pub_to_ros_inst.publish(target_speed)
    

# Connect to the MQTT server
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(POST_PATH, 0)
    
def on_message_in(client, userdata, msg):
    print("Processing received data and sending to rostopics...")
    print("Message received-> " + msg.topic + " " + str(msg.payload))

    on_board_msg_dic = yaml.safe_load(msg.payload)
    print(on_board_msg_dic.keys())

    message_flow = on_board_msg_dic["message_direction"]
    message_flow_sub = message_flow["message_direction"]

    if(message_flow_sub == "app2ros"):
        if("emergency_inst" in on_board_msg_dic):
            rec_dic = on_board_msg_dic["emergency_inst"]
            print(rec_dic.keys())

            if("emergency_x" in rec_dic):
                emergency_x = rec_dic["emergency_x"]
            if("emergency_y" in rec_dic):
                emergency_y = rec_dic["emergency_y"]

            print("///////")
            print("///////")
            print("///////")
            print("The spillage is located at (" + str(emergency_x) + "," + str(emergency_y) + ")")
            print("///////")
            print("///////")
            print("///////")

        if("pad_inst" in on_board_msg_dic):

            rec_dic = on_board_msg_dic["pad_inst"]
            print(rec_dic.keys())

            if("red_button_status" in rec_dic.keys()):
                is_the_red_button_pressed = rec_dic["red_button_status"]
                print(str(is_the_red_button_pressed) + ", red_button_checked...")
            
            if('m_mode_inst' in rec_dic.keys()):
                is_forced_m_mode = rec_dic["m_mode_inst"]
                print(str(is_forced_m_mode) + ", m_mode_checked...")

            if('move_forwards' in rec_dic.keys()):
                is_move_forwards = rec_dic["move_forwards"]
                print(str(is_move_forwards) + ", move_forwards_checked...")

            if('move_backwards' in rec_dic.keys()):
                is_move_backwards = rec_dic["move_backwards"]
                print(str(is_move_backwards) + ", move_backwards_checked...")

            if('turn_left' in rec_dic.keys()):
                is_turn_left = rec_dic["turn_left"]
                print(str(is_turn_left) + ", turn_left_checked...")

            if('turn_right' in rec_dic.keys()):
                is_turn_right = rec_dic["turn_right"]
                print(str(is_turn_right) + ", turn_right_checked...")

            if('current_gear' in rec_dic.keys()):
                set_gear = rec_dic["current_gear"]
                print(str(set_gear) + ", gear_status_checked...")

            if('current_bucket' in rec_dic.keys()):
                set_bucket = rec_dic["current_bucket"]
                print(str(set_bucket) + ", bucket_height_checked...")

            if('instruct_down' in rec_dic.keys()):
                instruct_down = rec_dic["instruct_down"]
                print(str(instruct_down))

            read_from_received_message_and_publish_to_ros(is_the_red_button_pressed, is_forced_m_mode, is_move_forwards, is_move_backwards, is_turn_left, is_turn_right, set_gear)
            print("Data processed...")
    

def send_to_topic():
    rospy.init_node('data_from_mqtt')
    global pub_to_ros_inst
    pub_to_ros_inst = rospy.Publisher("cmd_vel", Twist, queue_size=10)

if __name__ == '__main__':
    send_to_topic()
    client.on_connect = on_connect
    client.on_message = on_message_in
    client.connect(HOST, PORT, 60)
    client.loop_forever()
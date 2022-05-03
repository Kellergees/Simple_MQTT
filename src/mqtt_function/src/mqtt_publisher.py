#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from glob import glob
import paho.mqtt.client as mqtt
import rospy
import time

from std_msgs.msg import String
from nav_msgs.msg import Odometry

HOST = "homedev.bit-plat.com"
PORT = 8883
POST_PATH = "v1/devices/me/attributes"
client = mqtt.Client(client_id="Unimelb_client_linux_pub")
client.tls_set('../mqtt_key/iot_mqtt.pem')
client.tls_insecure_set(True)
client.username_pw_set("PqwuPLhIwwVX0I9AaIPU")

global payload 

# {status_update:{cleaned_weight: 150, cleaned_area: 150, op_hours: 120, op_distance: 20, tot_cleaned_weight: 150, tot_cleaned_area: 150, tot_op_hours: 24, tot_op_distance: 25, predicted_life_span: 300, is_maintenance: false, is_replacement: false, is_OTA: false, is_activated: true, is_error: 0001}}

class message_stru:
    def __init__(self):
        self.which_update = "status_update"
        self.weight = 0.0
        self.area = 0.0
        self.hours = 0.0
        self.distance = 0.0
        self.tot_weight = 100
        self.tot_area = 100
        self.tot_hours = 100
        self.tot_distance = 100
        self.life_span = 600
        self.maintenance = False
        self.replacement = False
        self.OTA = False
        self.activated = True
        self.error = "0001"

payload = message_stru()

# Connect to the MQTT server
def on_mqtt_connect():
    client.connect(HOST, PORT, 60)
    print("Connected...")
    client.loop_start()

# Publish messages to the cloud
def on_publish(topic, load, qos):
    client.publish(topic, load, qos)

# def callback_mode(data):
#     global payload
#     payload.mode = data.data
#     #payload = '{' + '"current_mode":' + str(mode) + '}'

# def callback_odom(data):
#     global payload
#     payload.x_pose = data.pose.pose.position.x
#     payload.y_pose = data.pose.pose.position.y
#     payload.z_angular = data.twist.twist.angular.z
#     payload.x_linear = data.twist.twist.linear.x
#     #payload = '{' + '"x_pose":' + str(x_pose) + ', "y_pose":' + str(y_pose) + ', "z_angular":' + str(z_angular) + ', "x_linear":' + str(x_linear) + '}'

# def on_subscribe():
#     rospy.Subscriber("mqtt_publisher", String, callback_mode)
#     rospy.Subscriber("odom", Odometry, callback_odom)

def payload_converter():
    
    global payload

    output = "{" + payload.which_update 
    output += ":{cleaned_weight: " + str(payload.weight) 
    output += ", cleaned_area: " + str(payload.area) 
    output += ", op_hours: " + str(payload.hours) 
    output += ", op_distance: " + str(payload.distance) 
    output += ", tot_cleaned_weight: " + str(payload.tot_weight) 
    output += ", tot_cleaned_area: " + str(payload.tot_area) 
    output += ", tot_op_hours: " + str(payload.tot_hours) 
    output += ", tot_op_distance: " + str(payload.tot_distance) 
    output += ", predicted_life_span: " + str(payload.life_span) 
    output += ", is_maintenance: " + str(payload.maintenance) 
    output += ", is_replacement: " + str(payload.replacement) 
    output += ", is_OTA: " + str(payload.OTA) 
    output += ", is_activated: " + str(payload.activated) 
    output += ", is_error: " + str(payload.error) 
    output += ", instruct_down: False" + "}" + "}"

    return output

def payload_update():

    global payload

    payload.which_update = "status_update"
    payload.weight += 1.0
    payload.area += 1.0
    payload.hours += 0.1
    payload.distance += 1.0
    payload.tot_weight +=1.0
    payload.tot_area += 1.0
    payload.tot_hours += 0.1
    payload.tot_distance += 1.0
    payload.life_span -= 0.1
    payload.maintenance = False
    payload.replacement = False
    payload.OTA = False
    payload.activated = True
    payload.error = "0001"

if __name__ == '__main__':
    on_mqtt_connect()
    rospy.init_node('data_to_mqtt')
    print("mqtt node: data_to_mqtt established...")
    rate = rospy.Rate(0.25) # hz 
    while not rospy.is_shutdown():
        out_topic = payload_converter()
        print(out_topic)
        on_publish(POST_PATH, str(out_topic), 1)
        payload_update()
        rate.sleep()
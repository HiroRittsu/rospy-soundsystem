#!/usr/bin/env python
# coding: UTF-8
from time import sleep
import rospy
import subprocess
from std_msgs.msg import Bool, String

def speaker_message(message):
    result = subprocess.call("espeak '{" + message.data +"}'", shell = True)
    if result == 0:
        signal.publish(True)
    else:
        signal.publish(False)

if __name__ == '__main__':
    rospy.init_node("speaker")

    signal = rospy.Publisher('speaker_signal',Bool,queue_size=10)
    rospy.Subscriber("main_speaker_message", String, speaker_message)
    
    rospy.spin()
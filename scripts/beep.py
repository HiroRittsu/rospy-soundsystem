#!/usr/bin/env python
# coding: UTF-8
from time import sleep
import rospy
import subprocess
from std_msgs.msg import Bool, String

#PATH = "../src/sound"
PATH = "~/catkin_ws/src/soundsystem/scripts/sound/"

def sound_play(filename):
    result = subprocess.call("aplay " + PATH + filename, shell = True)
    if result == 0:
        signal.publish(True)
    else:
        signal.publish(False)

def beep_message(message):
    if message.data == "RecognitionStart":
        sound_play("RecognitionStart.wav")

    elif message.data == "RecognitionStop":
        sound_play("RecognitionStop.wav")

    elif message.data == "RecognitionErrer":
        sound_play("RecognitionErrer.wav")

    elif message.data == "SystemStart":
        sound_play("SystemStart.wav")

    elif message.data == "SystemStop":
        sound_play("SystemStop.wav")

    else:
        sound_play("SystemError.wav")

if __name__ == '__main__':
    rospy.init_node("beep")

    signal = rospy.Publisher('beep_signal',Bool,queue_size=10)
    rospy.Subscriber("main_beep_message", String, beep_message)
    
    rospy.spin()
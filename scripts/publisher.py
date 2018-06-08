#!/usr/bin/env python
# coding: UTF-8
import rospy
from std_msgs.msg import String, Bool
import time


def string_send(string, pub):
    send = String()
    send.data = string
    pub.publish(send)


def finish(message):
    print '結果: ', message.data


def result(message):
    print '結果: ', message.data


if __name__ == '__main__':
    rospy.init_node("talker")
    beep = rospy.Publisher('beep', String, queue_size=10)
    speaker = rospy.Publisher('speaker', String, queue_size=10)
    recognition_start = rospy.Publisher(
        'recognition_start', String, queue_size=10)
    recognition_stop = rospy.Publisher(
        'recognition_stop', String, queue_size=10)
    rate = rospy.Rate(10)

    rospy.Subscriber('finish', String, finish)
    rospy.Subscriber('result', String, result)

    while not rospy.is_shutdown():
        try:
            put = raw_input()
            if put == 'start':
                string_send('start', recognition_start)
            elif put == 'stop':
                string_send('stop', recognition_stop)
            elif put == 'beep':
                select = raw_input()
                string_send(select, beep)
            elif put == 'speak':
                select = raw_input()
                string_send(select, speaker)
        except Exception:
            exit

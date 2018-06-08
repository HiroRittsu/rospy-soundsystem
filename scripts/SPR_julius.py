#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Help-me-carry,音声班,publisher

import re
import socket
import sys
from time import sleep

import rospy
from std_msgs.msg import Bool, String

##################################################################################################


def connection():
    while True:
        try:
            global client
            HOST = "localhost"  # アドレス
            PORT = 10500  # ポート
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            client.send('PAUSE\n')
            break
        except IOError:
            sys.stdout.write('.')
##################################################################################################


def talker():
    global client
    pub = rospy.Publisher('result', String, queue_size=10)
    rospy.init_node('recognition')
    while not rospy.is_shutdown():
        try:
            response = client.recv(1024)  # juliusの出力をresponseと置く
            sleep(0.1)
            line_list = response.split('\n')  # juliusの出力を改行で区切りline_listと置く
            text = ''
            for line in line_list:
                if 'WORD=' in line and not '<s>' in line:
                    word = line.rsplit('"')
                    text = text + word[1]

            if text:  # リストがからではない場合
                pub.publish(text)
                print text

        except socket.error as e:
            client.close()
            sleep(3)
            connection()
            print e
##################################################################################################


def control(message):
    global client

    if message.data == True:
        client.send('RESUME\n')

    if message.data == False:
        client.send('PAUSE\n')
##################################################################################################


if __name__ == '__main__':
    try:
        connection()
        # 受け取ったメッセージに対応したシグナルをjuliusに送信する
        rospy.Subscriber('main_recognition_control', Bool, control)
        talker()

    except rospy.ROSInterruptException:
        pass

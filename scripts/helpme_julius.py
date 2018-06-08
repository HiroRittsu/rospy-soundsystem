#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Help-me-carry,音声班,publisher

import rospy
import sys
from std_msgs.msg import String
from std_msgs.msg import Bool

import socket
from time import sleep

import re

##################################################################################################

def connection():
    while True:
        try:
            global client
            HOST = "localhost"  # アドレス
            PORT = 10500  # ポート
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            #client.send('PAUSE\n')
            break
        except IOError:
            sys.stdout.write('.')

##################################################################################################

def talker() :
	global client
	pub = rospy.Publisher('result', String, queue_size=10)
	rospy.init_node('help_talker', anonymous=True)
	while not rospy.is_shutdown():
		try:
			response = client.recv(1024) # juliusの出力をresponseと置く
			#print response					
			sleep(0.1) # 全文認識させるために0.1秒時間をおく

			word_list = []
			line_list = response.split('\n') # juliusの出力を改行で区切りline_listと置く
			
			text = ''

			for line in line_list : # 必要な文字のだけ抜き出す処理
				if 'WORD' in line :
					word = re.compile('WORD="((?!").)+"').search(line)
					text = word.group().split('"')[1]
					#line_line = line.rsplit('"')
					#text = line_line[1]
					#print text
					if text != '<s>' :
						word_list.append(text) # word_listに必要な文字だけを追加する
					
					
			if word_list != [] : # word_listに文字が入っている時、処理を行う
				if len(word_list) == 1: # followme,Stopなどの時
					text = word_list[0]
				else: # かばんを置く場所の指示
					text = word_list[0] + ',' + word_list[1] + ',' + word_list[2] # 例)text = 'take,thisbag,kitchen'

				print text
				pub.publish(text) # juliusから受け取った必要な文字をpublish

				word_list = [] # word_listを初期化する

		except KeyboardInterrupt:
			#例外が発生した場合はクライアントを一旦消し，3秒後にクライアントを再作成・再接続する
				client.close()
				sleep(3)
				connection()

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
		rospy.Subscriber('main_recognition_control',Bool,control) #受け取ったメッセージに対応したシグナルをjuliusに送信する
		talker()

	except rospy.ROSInterruptException: pass

#!/usr/bin/env python
# coding: UTF-8
from time import sleep
import rospy
from std_msgs.msg import Bool, String

recognition_flag = False
beep_flag = False
speaker_flag = False
monitor_flag = False


def string_send(string, pub):
    send = String()
    send.data = string
    pub.publish(send)


def boolean_send(flag, pub):
    send = Bool()
    send.data = flag
    pub.publish(send)


def executing_start(member, monitor):
    global recognition_flag, beep_flag, speaker_flag, monitor_flag
    if member == 'beep':
        beep_flag = True
    elif member == 'speaker':
        speaker_flag = True
    elif member == 'recognition':
        recognition_flag = True

    if monitor:
        monitor_flag = True


def executing_state(status, member):
    # 自分自身すでに実行されてる場合
    if member == 'beep':
        if beep_flag:
            status = 'pass'
    if member == 'speaker':
        if speaker_flag:
            status = 'pass'
    if member == 'recognition':
        if recognition_flag:
            status = 'pass'

    if status == 'stay':
        while recognition_flag or beep_flag or speaker_flag:
            pass
        return True
    else:
        if not (recognition_flag or beep_flag or speaker_flag):
            return True
        else:
            return False


def executing_wait(member):
    global recognition_flag, beep_flag, speaker_flag
    if member == 'recognition':
        while recognition_flag:
            pass
        recognition_flag = False
    elif member == 'beep':
        while beep_flag:
            pass
        beep_flag = False
    elif member == 'speaker':
        while speaker_flag:
            pass
        speaker_flag = False


def executing_stop(member):
    global recognition_flag, beep_flag, speaker_flag, monitor_flag
    if member == 'beep':
        beep_flag = False
    elif member == 'speaker':
        speaker_flag = False
    elif member == 'recognition':
        recognition_flag = False

    if monitor_flag:
        string_send(member, main_finish_flag)
        print "モニター", member
        monitor_flag = False

##############################################################################


def recognition(send):
    global recognition_flag, beep_flag
    if send == 'start':
        if executing_state('stay', 'recognition'):
            beep('RecognitionStart')  # beep
            executing_wait('beep')  # 待機
            print "start:" ,monitor_flag
            executing_start('recognition', True)
            boolean_send(True, main_recognition_control)  # 認識開始
            print '認識開始'

    elif send == 'stop':
        boolean_send(False, main_recognition_control)  # 認識終了
        beep('RecognitionStop')  # beep
        executing_wait('beep')  # 待機
        executing_stop('recognition')
        print '認識終了'

    else:
        boolean_send(False, main_recognition_control)  # 認識終了
        beep('RecognitionError')  # beep
        executing_wait('beep')  # 待機
        executing_stop('recognition')
        print '認識エラー'


def beep(sned):
    string_send(sned, main_beep_message)  # beep音
    print "beep音開始: " + sned


def speak(send):
    string_send(send, main_speaker_message)  # 発音文
    print "発音開始: " + send

######################################################################################


def recognition_control(message):  # 音声認識
    if message.data == 'start':
        recognition(message.data)
    elif message.data == 'stop' or message.data == 'error':
        recognition(message.data)


def beep_message(message):  # beep音
    if executing_state('pass', 'none'):  # 状況確認
        executing_start('beep', True)  # 実行開始
        beep(message.data)


def speaker_message(message):  # 発音
    if executing_state('stay', 'none'):  # 状況確認
        executing_start('speaker', True)  # 実行開始
        speak(message.data)


def beep_signal(message):
    executing_stop('beep')
    print "beep音終了: ", message.data


def speaker_signal(message):
    executing_stop('speaker')
    print "発音終了: ", message.data

################################################################################################


if __name__ == '__main__':
    while not rospy.is_shutdown():
        try:
            rospy.init_node("main_node")

            main_recognition_control = rospy.Publisher(
                'main_recognition_control', Bool, queue_size=10)
            main_speaker_message = rospy.Publisher(
                'main_speaker_message', String, queue_size=10)
            main_beep_message = rospy.Publisher(
                'main_beep_message', String, queue_size=10)
            main_finish_flag = rospy.Publisher('finish', String, queue_size=10)

            rospy.Subscriber('recognition_start', String, recognition_control)
            rospy.Subscriber('recognition_stop', String, recognition_control)
            rospy.Subscriber('speaker', String, speaker_message)
            rospy.Subscriber('beep', String, beep_message)
            rospy.Subscriber('speaker_signal', Bool, speaker_signal)
            rospy.Subscriber('beep_signal', Bool, beep_signal)

            rospy.spin()

        except Exception as e:
            beep('Exception')
            print e

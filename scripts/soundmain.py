#!/usr/bin/env python
# coding: UTF-8
from time import sleep
import rospy
from std_msgs.msg import Bool, String

recognition_flag = False
recognition_subflag = False
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


def executing_start(member):
    global recognition_flag, beep_flag, speaker_flag, monitor_flag
    if member == 'beep':
        beep_flag = True
    elif member == 'speaker':
        speaker_flag = True
    elif member == 'recognition':
        recognition_flag = True


def executing_state(status):
    if status == 'stay':
        while recognition_flag or beep_flag or speaker_flag:
            pass
        return True
    else:
        if not (recognition_flag or beep_flag or speaker_flag):
            return True
        else:
            return False


def executing_stop(member):
    global recognition_flag, beep_flag, speaker_flag, monitor_flag
    if member == 'beep':
        beep_flag = False
    elif member == 'speaker':
        speaker_flag = False
    elif member == 'recognition':
        recognition_flag = False

##############################################################################
# 処理部分


def recognition(send):
    if send == 'start':
        boolean_send(True, main_recognition_control)  # 認識開始
        print '認識開始'
    else:
        boolean_send(False, main_recognition_control)  # 認識開始


def beep(sned):
    string_send(sned, main_beep_message)  # beep音
    print "beep音開始: " + sned
    executing_state('stay')  # 待機


def speak(send):
    string_send(send, main_speaker_message)  # 発音文
    print "発音開始: " + send
    executing_state('stay')  # 待機

######################################################################################
# メッセージ送受信部分 -必ずひとつだけ実行


def recognitionSTART(message):
    global recognition_subflag
    if not recognition_subflag:
        recognition_subflag = True
        beep('RecognitionStart')  # 実行からシグナル受け取りまで
        executing_start('recognition')
        recognition('start')  # 実行


def recognitionSTOP(message):
    global recognition_subflag
    recognition('stop')
    executing_stop('recognition')
    executing_start('beep')
    if message.data == 'stop':
        beep('RecognitionStop')
        print '認識終了'
    else:
        beep('RecognitionError')
        print '認識エラー'
    recognition_subflag = False
    send_singnal('recognition')  # 終了シグナル送信


def beep_message(message):  # beep音
    if executing_state('pass'):  # 状況確認
        executing_start('beep')
        beep(message.data)  # 実行からシグナル受け取りまで
        send_singnal('beep')  # 終了シグナル送信


def speaker_message(message):  # 発音
    executing_state('stay')  # 状況確認
    executing_start('speaker')
    speak(message.data)  # 実行からシグナル受け取りまで
    send_singnal('speaker')  # 終了シグナル送信
    executing_state('stay')  # 待機


def beep_signal(message):
    executing_stop('beep')
    print "beep音終了: ", message.data


def speaker_signal(message):
    executing_stop('speaker')
    print "発音終了: ", message.data


def send_singnal(send):
    string_send(send, main_finish_flag)

################################################################################################
# メイン


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

            rospy.Subscriber('recognition_start', String, recognitionSTART)
            rospy.Subscriber('recognition_stop', String, recognitionSTOP)
            rospy.Subscriber('speaker', String, speaker_message)
            rospy.Subscriber('beep', String, beep_message)
            rospy.Subscriber('speaker_signal', Bool, speaker_signal)
            rospy.Subscriber('beep_signal', Bool, beep_signal)

            rospy.spin()

        except Exception as e:
            beep('Exception')
            print e

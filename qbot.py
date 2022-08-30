# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 11:55:27 2022

@author: Administrator
"""
import socket
from receive import rev_msg
import requests
import random
import json
from tencent_nlp import nlp
from jx3pic import get_jx3_url

def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = '127.0.0.1'
    client.connect((ip, 5700))
    msg_type = resp_dict['msg_type']  # 回复类型（群聊/私聊）
    number = resp_dict['number']  # 回复账号（群号/好友号）
    msg = resp_dict['msg']  # 要回复的消息
    # 将字符中的特殊字符进行url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")
    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    elif msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(
            number) + "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("发送" + payload)
    client.send(payload.encode("utf-8"))
    client.close()
    return 0

lastrev = []

def tgrj():#舔狗日常
    r1 = requests.post("https://www.jx3api.com/transmit/random")
    r = json.loads(r1.text)
    return r['data']['text']

def sjsh():#随机骚话
    r1 = requests.post("https://www.jx3api.com/app/random")
    r = json.loads(r1.text)
    return r['data']['text']

def nlp_r(long):
    long
    short = "老黑 "
    r = long.replace(short, '')
    r1 = nlp(r)
    r1 = json.loads(r1)
    r1 = r1['Reply']
    return r1

def jx3_pic():
    url = 'https://origin.jx3box.com/emotion/'
    url = url + str(random.randint(1, 983))
    return url
while True:
    try:
        rev = rev_msg()
        #print(rev["raw_message"])
        if rev == None:
            continue
    except:
        continue
    if rev["post_type"] == "message":
        if lastrev != rev:
            #print(rev) #需要功能自己DIY
            if rev["message_type"] == "private": #私聊
                if rev['raw_message']=='在吗':
                    qq = rev['sender']['user_id']
                    send_msg({'msg_type':'private','number':qq,'msg':'我在'})
            elif rev["message_type"] == "group": #群聊
                group = rev['group_id']
                if "老黑在吗" in rev["raw_message"]:                
                    qq=rev['sender']['user_id']
                    send_msg({'msg_type':'group','number':group,'msg':'我在'})
                    lastrev = rev
                elif "老黑 舔狗日记" in rev["raw_message"]:                
                    qq=rev['sender']['user_id']
                    send_msg({'msg_type':'group','number':group,'msg':tgrj()})
                    lastrev = rev
                elif "老黑 随机骚话" in rev["raw_message"]:                
                    qq=rev['sender']['user_id']
                    send_msg({'msg_type':'group','number':group,'msg':sjsh()})
                    lastrev = rev

                elif "老黑 " in rev["raw_message"]:     #腾讯云闲聊
                    qq=rev['sender']['user_id']
                    send_msg({'msg_type':'group','number':group,'msg':nlp_r(rev["raw_message"])})
                    lastrev = rev

                elif "老黑来点图" in rev["raw_message"]:     #图片
                    qq=rev['sender']['user_id']
                    send_msg({'msg_type':'group','number':group,'msg':'[CQ:image,file='+get_jx3_url()+']'})
                    lastrev = rev

        else:
            continue
    else:  # rev["post_type"]=="meta_event":
        continue

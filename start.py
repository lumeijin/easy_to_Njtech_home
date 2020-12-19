# -*- coding: utf-8 -*-
# File  : start.py
# Author: Meijin Lu
# Date  : 2020/12/15
import requests
import json
import pywifi
from pywifi import const
import time
from tkinter import *  # 另见：import tkinter.messagebox 方法
from tkinter import messagebox
import socket


def is_net_OK(testserver):
    s = socket.socket()
    s.settimeout(3)
    try:
        status = s.connect_ex(testserver)
        if status == 0:
            s.close()
            return True
        else:
            return False
    except Exception as e:
        return False


# def ping(ping_url):
#     """
#     ping某个url,确认是否联网成功
#     """
#     # result = os.system("ping 10.65.20.245")
#     command = u"ping {}".format(ping_url)
#     result = os.system(command)
#     # print("cmd返回值为:", result)
#     if result == 0:
#         return True
#     else:
#         return False


def msgbox(title, contents):
    """
    弹窗
    :param title: 标题
    :param contents: 内容
    :return:None
    """
    root = Tk()
    root.withdraw()  # 实现主窗口隐藏
    # root.update()  		 # 也许需要update一下
    messagebox.showinfo(title, contents)


def detect(wifi_name):
    """
    检测到特定wifi信号返回True
    否则返回False
    """
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]

    iface.scan()  # 扫描附件wifi
    time.sleep(1)
    basewifi = iface.scan_results()
    for i in basewifi:
        if wifi_name == i.ssid:
            return True
    else:
        # 如果上面没有return的话就执行以下字段
        msgbox("提示", "没有检测到{}信号".format(wifi_name))
        return False


def connect(wifi_name):
    """
    连接特定wifi信号
    :return:status code
    # Define interface status.
    IFACE_DISCONNECTED = 0
    IFACE_SCANNING = 1
    IFACE_INACTIVE = 2
    IFACE_CONNECTING = 3
    IFACE_CONNECTED = 4

    """
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    profile = pywifi.Profile()
    profile.ssid = wifi_name  # wifi名称
    profile.auth = const.AUTH_ALG_OPEN  # auth - AP的认证算法
    profile.akm.append(const.AKM_TYPE_NONE)  # 选择wifi加密方式
    profile.cipher = const.CIPHER_TYPE_NONE  # cipher - AP的密码类型
    profile.key = const.CIPHER_TYPE_NONE  # wifi密钥   key （optinoal） - AP的关键。如果无密码，则应该设置此项CIPHER_TYPE_NONE
    iface.add_network_profile(profile)
    iface.connect(profile)
    return iface.status()


def browser_restraint():
    """
    抑制浏览器的启动
    不知道怎么实现,先跳过
    """
    pass


def quit_browser_resraint():
    """
    取消抑制浏览器启动
    不知道怎么实现,先跳过
    :return: bool
    """
    pass


def json_to_dict(path):
    """
    将json配置文件转化为字典
    """
    with open(path, 'rt', encoding='utf-8') as jsonFile:
        config_dict = json.load(jsonFile)
        return config_dict


def form_post():
    """
    提交表单
    :return: 状态码
    200：OK(成功)
    请求成功。成功的意义根据请求所使用的方法不同而不同。
    GET：资源已被提取，并作为响应体传回客户端。
    HEAD：实体头已作为响应头传回客户端
    POST：经过服务器处理客户端传来的数据,适合的资源作为响应体传回客户端.
    TRACE：服务器收到请求消息作为响应体传回客户端.
    PUT，DELETE和OPTIONS 方法永远不会返回 200 状态码。HTTP/0.9 可用。

    201：Created(已创建)
    请求成功，而且有一个新的资源已经依据请求的需要而建立，通常这是 PUT 方法得到的响应码。 HTTP/0.9 可用。

    202：Accepted(已接受)
    服务器已接受请求，但尚未处理。正如它可能被拒绝一样，最终该请求可能会也可能不会被执行。在异步操作的场合下，没有比发送这个状态码更方便的做法了。返回202状态码的响应的目的是允许服务器接受其他过程的请求（例如某个每天只执行一次的基于批处理的操作），而不必让客户端一直保持与服务器的连接直到批处理操作全部完成。在接受请求处理并返回202状态码的响应应当在返回的实体中包含一些指示处理当前状态的信息，以及指向处理状态监视器或状态预测的指针，以便用户能够估计操作是否已经完成。 HTTP/0.9 可用。

    203：Non-Authoritative Information(未授权信息)
    服务器已成功处理了请求，但返回的实体头部元信息不是在原始服务器上有效的确定集合，而是来自本地或者第三方的拷贝。如果不是上述情况，使用200状态码才是最合适的。HTTP/0.9 和 1.1可用。

    204：No Content(无内容)
    该响应没有响应内容，只有响应头，响应头也可能是有用的。用户代理可以根据新的响应头来更新对应资源的缓存信息。HTTP/0.9 可用。

    205：Reset Content(重置内容)
    告诉用户代理去重置发送该请求的窗口的文档视图。HTTP/1.1 可用。

    206：Partial Content(部分内容)
    当客户端通过使用range头字段进行文件分段下载时使用该状态码。 HTTP/1.1 可用。
    """
    global channel
    url = ("https://u.njtech.edu.cn/cas/login?service=https:" +
           "u.njtech.edu.cn/oauth2/authorize?client_id=Oe7wtp9CAMW0FVygUasZ&" +
           "response_type=code&state=njtech&s=f682b396da8eb53db80bb072f5745232")
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102\
                Safari/537.36',
               'referer': 'https://u.njtech.edu.cn/cas/login?'
                          'service=https://u.njtech.edu.cn/oauth2/'
                          'authorize?client_id=Oe7wtp9CAMW0FVygUasZ&'
                          'response_type=code&state=njtech&s=f682b396da8eb53db80bb072f5745232',
               'Connection': 'keep-alive'}

    info = json_to_dict("Config.json")
    # 检查配置文件是否为空
    try:
        assert (len(info['username']) != 0 and len(info['password']) != 0
                and len(info['channelshow']) != 0)
    except:
        msgbox("提示", "请检查配置文件Config.json")
        exit(0)  # 无错误退出

    if info["channelshow"] == "校园内网":
        channel = 'default'
    elif info["channelshow"] == "中国移动":
        channel = '@cmcc'
    elif info["channelshow"] == "中国电信":
        channel = '@telecom'

    data = {'username': info['username'],
            'password': info['password'],
            'channelshow': info['channelshow'],
            'channel': channel,
            # 'lt': 'LT-7384394-nWKcOVfPnclL0NskNeDfP7b0jhbFyu',
            'execution': 'e1s1',
            '_eventId': 'submit',
            'login': '登录'}
    r = requests.post(url, headers=headers, data=data)
    print(r)


if __name__ == '__main__':
    if is_net_OK(testserver=("www.baidu.com", 443)):
        msgbox("提示", "已经可以上网")
        exit(0)
    else:
        if detect("Njtech-Home"):
            if connect("Njtech-Home") in [0, 1, 2, 4]:
                form_post()
                try:
                    assert is_net_OK(testserver=("www.baidu.com", 443))
                    msgbox("提示", "认证到Njtech-Home,已经可以上网")
                    exit(0)
                except:
                    msgbox("提示", "出现错误,连接失败")
                    exit(0)
            else:
                msgbox("提示", "连接Njtech-Home失败")
                exit(0)
        else:
            exit(0)

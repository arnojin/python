#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# 设置定时执行
# crontab -e
# 0 * * * * /code/send_ip_info.py
"""
作者：金鹏
时间：2018-02-03
用途：服务器没有对外固定IP，通过python跑该程序，将对外的公网IP发给指定的邮箱，便于远程连接
"""

import logging
logging.basicConfig(filename='log.log',
                    format='[%(asctime)s -%(name)s-%(levelname)s-%(module)s]%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG)
log = logging.getLogger('simple')
sh = logging.StreamHandler()
sh.setLevel(level = logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s -%(name)s-%(levelname)s-%(module)s]%(message)s')
sh.setFormatter(formatter)
log.addHandler(sh)

# 获取外网IP地址
def get_wan_ip():
    log.info("获取外网IP地址 开始 ...")
    from urllib import request
    import re

    url     = "http://ip.chinaz.com/"
    request = request.urlopen(url).read().decode('utf-8')
    wan_ip  = re.findall(r"<p class=\"getlist pl10\"><span>您来自：</span>(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})", request)[0]
    log.info('wan_ip = ' + wan_ip)
    log.info('url = ' + url)
    log.info("获取外网IP地址 结束 。")
    return [wan_ip, url]

# 发送邮件
def send_email(sender, receivers, title, content):
    log.info("发送邮件 开始 ...")

    import smtplib
    from email.mime.text import MIMEText

    # 设置邮件服务器信息
    mail_host   = 'mail.tcl.com'        # SMTP服务器
    mail_user   = 'username@tcl.com'    # 用户名
    mail_pass   = 'password'         # 授权密码，非登录密码

    message             = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From']     = "{}".format(sender)
    message['To']       = ",".join(receivers)
    message['Subject']  = title

    try:
        # 启用SSL发信, 端口一般是465
        # smtpObj = smtplib.SMTP_SSL(mail_host, 465)

        smtpObj = smtplib.SMTP(mail_host)

        # 登录验证
        smtpObj.login(mail_user, mail_pass)

        # 发送
        smtpObj.sendmail(sender, receivers, message.as_string())

        log.info("发送邮件 结束 。")
    except smtplib.SMTPException as e:
        log.info(e)
        log.info("发送邮件 失败 ！")

def send_ip_info():
    import re
    import time
    #from datetime import datetime

    # 设置发件人、收件人
    sender      = 'username@tcl.com'    # 发件人邮箱（最好写全, 不然会失败）
    receivers   = ['username@tcl.com']  # 接收人邮件列表

    # 邮件主题
    wan_ip      = get_wan_ip()
    ip          = wan_ip[0]
    url         = wan_ip[1]
    title       = '新IP地址：' + ip

    # 读取之前保存的ip地址信息
    # ip_info.txt 文件中默认有一条记录： 2018-02-03 20:30:57 1.2.3.4
    ip_info_file    = open('ip_info.txt', 'r')
    ip_info         = ip_info_file.readlines()
    ip_info_file.close()
    last_line       = ip_info[-1]

    # 'yyyy-mm-dd hh:mm:ss nnn.nnn.nnn.nnn'
    info = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2})\s(\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3})", last_line)[0]
    last_time   = info[0]
    last_ip     = info[1]
    log.info('last_time = ' + last_time)
    log.info('last_ip = ' + last_ip)

    if (last_ip != ip) :
        # 追加新的ip地址
        ip_info_file = open('ip_info.txt', 'a')

        # 在 windows 下对换行处理不同
        #ip_info_file.write('\r' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + ip)

        # 在 linxu 下不用处理
        ip_info_file.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' ' + ip)

        ip_info_file.close()
        
        # 邮件内容
        content     = "通过 " + url + " 获取本机外网IP地址\r\n"
        content     = content + "新IP地址：" +ip
        log.info('content = ' + content)

        send_email(sender, receivers, title, content)
    else:
        log.info("IP地址没有变化。")

# 主程序
if __name__ == '__main__':
    log.info("主程序 开始 ...")
    send_ip_info()
    log.info("主程序 结束 。")
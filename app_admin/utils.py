# coding:utf-8
# @文件: utils.py
# @创建者：州的先生
# #日期：2019/11/23
# 博客地址：zmister.com

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import resolve,Resolver404
from email.mime.text import MIMEText
from email.header import Header
from app_admin.models import SysSetting
from loguru import logger
import random
import smtplib
import zipfile
import os

# 生成数字验证码
def generate_vcode(n=6):
    # 生成数字验证码
    _num = ''.join(map(str, range(3, 10)))
    vcode_str = ''.join(random.sample(_num, n))
    return vcode_str

# 发送电子邮件
def send_email(to_email,vcode_str):
    email_enable = SysSetting.objects.get(types="basic",name='enable_email')
    if email_enable.value == 'on':
        smtp_host = SysSetting.objects.get(types='email',name='smtp_host').value
        send_emailer = SysSetting.objects.get(types='email', name='send_emailer').value
        smtp_port = SysSetting.objects.get(types='email', name='smtp_port').value
        username = SysSetting.objects.get(types='email', name='username').value
        pwd = SysSetting.objects.get(types='email', name='pwd').value
        ssl = SysSetting.objects.get(types='email',name='smtp_ssl').value
        # print(smtp_host,smtp_port,send_emailer,username,pwd)

        msg_from = send_emailer  # 发件人邮箱
        passwd = dectry(pwd)  # 发件人邮箱密码
        msg_to = to_email  # 收件人邮箱
        try:
            sitename = SysSetting.objects.get(types="basic", name="site_name").value
        except:
            sitename = "MrDoc"
        subject = "{} - 重置密码验证码".format(sitename)
        content = "你的验证码为：{}，验证码30分钟内有效！".format(vcode_str)
        msg = MIMEText(content, _subtype='html', _charset='utf-8')
        msg['Subject'] = subject
        msg['From'] = Header(sitename,'utf-8').encode() + " <{}>".format(msg_from)
        msg['To'] = msg_to
        try:
            # print(smtp_host,smtp_port)
            if ssl:
                s = smtplib.SMTP_SSL(smtp_host, int(smtp_port))  # 发件箱邮件服务器及端口号
            else:
                s = smtplib.SMTP(smtp_host, int(smtp_port))
            s.login(username, passwd)
            s.sendmail(from_addr=msg_from, to_addrs=msg_to, msg=msg.as_string())
            return True
        except smtplib.SMTPException as e:
            logger.error("邮件发送异常:{}".format(repr(e)))
            return False
        except Exception as e:
            logger.error("邮件发送异常:{}".format(repr(e)))
            return False
        finally:
            s.quit()
    else:
        return False


# 加密
def enctry(s):
    k = settings.SECRET_KEY
    encry_str = ""
    for i,j in zip(s,k):
        # i为字符，j为秘钥字符
        temp = str(ord(i)+ord(j))+'_' # 加密字符 = 字符的Unicode码 + 秘钥的Unicode码
        encry_str = encry_str + temp
    return encry_str

# 解密
def dectry(p):
    k = settings.SECRET_KEY
    dec_str = ""
    for i,j in zip(p.split("_")[:-1],k):
        # i 为加密字符，j为秘钥字符
        temp = chr(int(i) - ord(j)) # 解密字符 = (加密Unicode码字符 - 秘钥字符的Unicode码)的单字节字符
        dec_str = dec_str+temp
    return dec_str

# 判断是否内部链接
def is_internal_path(path):
    try:
        resolve(path)
        return True
    except Resolver404:
        return False

def is_zip_bomb(zip_path, compression_threshold=100):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            uncompressed_size = sum(file.file_size for file in zip_file.infolist())
            compressed_size = os.path.getsize(zip_path)
            # print(f"未压缩大小：{uncompressed_size}")
            # print(f"压缩后大小：{compressed_size}")
            compression_ratio = uncompressed_size / compressed_size
            # print(f"压缩率：{compression_ratio}")
            if compression_ratio > compression_threshold:
                return True
    except zipfile.BadZipFile:
        return False
    except Exception as e:
        return False
    return False
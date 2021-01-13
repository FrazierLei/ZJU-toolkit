import os
import re
import json
import requests
from MyQR import myqr
from PIL import Image
import getpass
import sys 
sys.path.append("..") 
from zjuam import ZJUAccount


def generate_blue_horse(sess):
    """
    蓝码生成函数
    :param sess: 登录浙大通行证后的 session
    :return: 一个二维码 Image 对象
    """
    resp = sess.get('http://one.zju.edu.cn/pass_code/zx')
    horse_code = re.search(r"text: \'(.*?)\'", resp.text).group(1)
    
    myqr.run(
        words=horse_code,
        version=1,
        level='L',
        picture='./horse.png',
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=None,
        save_dir=os.getcwd()
    )

    image = Image.open('./horse_qrcode.png')
    return image

if __name__ == '__main__':
    configs = json.loads(open('../config.json', 'r').read())
    username = configs["username"]
    password = configs["password"]
    if not (username and password):
        print('未能获取用户名和密码，请手动输入！')
        username = input("👤 浙大统一认证用户名: ")
        password = getpass.getpass('🔑 浙大统一认证密码: ')

    zju = ZJUAccount(username, password)
    sess = zju.login()
    blue_horse = generate_blue_horse(sess)
    blue_horse.show()
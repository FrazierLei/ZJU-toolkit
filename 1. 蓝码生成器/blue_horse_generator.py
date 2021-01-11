import sys 
sys.path.append("..") 
from zjuam import ZJUAccount
import re
import requests
import qrcode
from PIL import Image

def generate_blue_horse(sess):
    """
    蓝码生成函数
    :param sess: 登录浙大通行证后的 session
    :return: 一个二维码 Image 对象
    """
    resp = sess.get('http://one.zju.edu.cn/pass_code/zx')
    horse_code = re.search(r"text: \'(.*?)\'", resp.text).group(1)

    # 初始化二维码对象
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=0,
        )
    qr.add_data(horse_code)
    qr.make(fit=True)

    # 生成二维码
    image = qr.make_image(fill_color="#4290F7", back_color="white")
    return image

if __name__ == '__main__':
    zju = ZJUAccount('', '')
    sess = zju.login()
    blue_horse = generate_blue_horse(sess)
    blue_horse.show()
# daka 函数改写自 https://github.com/Tishacy/ZJU-nCov-Hitcarder/blob/master/daka.py，该脚本可以实现定点打卡

import requests
import re
import json
import time
import datetime
import sys 
sys.path.append("..") 
from zjuam import ZJUAccount


def daka(sess):
    """
    获取个人信息，并完成打卡
    :param sess: 登录浙大通行证后的 session
    :return: 提交打卡表单后的响应
    """
    base_url = "https://healthreport.zju.edu.cn/ncov/wap/default/index"
    save_url = "https://healthreport.zju.edu.cn/ncov/wap/default/save"
    today = datetime.date.today()
    
    resp = sess.get(base_url)
    old_infos = re.findall(r'oldInfo: ({[^\n]+})', resp.text)
    if len(old_infos) != 0:
        old_info = json.loads(old_infos[0])
    else:
        return "未发现缓存信息，请先至少手动成功打卡一次再运行脚本。"

    new_info_tmp = json.loads(re.findall(r'def = ({[^\n]+})', resp.text)[0])
    new_id = new_info_tmp['id']
    name = re.findall(r'realname: "([^\"]+)",', resp.text)[0]
    number = re.findall(r"number: '([^\']+)',", resp.text)[0]

    info = old_info.copy()
    info['id'] = new_id
    info['name'] = name
    info['number'] = number
    info["date"] = "%4d%02d%02d" % (today.year, today.month, today.day)
    info["created"] = round(time.time())
    info['jrdqtlqk[]'] = 0
    info['jrdqjcqk[]'] = 0
    info['sfsqhzjkk'] = 1  # 是否申领杭州健康码
    info['sqhzjkkys'] = 1  # 杭州健康吗颜色，1:绿色 2:红色 3:黄色
    info['sfqrxxss'] = 1  # 是否确认信息属实
    info['jcqzrq'] = ""
    info['gwszdd'] = ""
    info['szgjcs'] = ""

    print(info['name'], end=' ')
    resp = sess.post(save_url, data=info)
    return resp.json()['m']



if __name__ == "__main__":
    zju = ZJUAccount('', '')
    sess = zju.login()
    message = daka(sess)
    print(message)
import json
import re
import getpass
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import sys 
sys.path.append("..") 
from zjuam import ZJUAccount
import colorama # 防止 windows 命令行打印带颜色字符串失败
colorama.init(autoreset=True)


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

    # 授权给软件中心
    sess.get('https://zjuam.zju.edu.cn/cas/oauth2.0/authorize?response_type=code&client_id=yRndoY4MQsFLAq0Md6&redirect_uri=http://user.ms.zju.edu.cn/login')

    software_type = input('请输入想要下载的软件类型序号\n\033[33m1. 微软应用下载\
        \033[0m\n\033[33m2. Adobe 下载\033[0m \n\033[33m3. Matlab 下载\033[0m\n')
    
    assert int(software_type) in [1, 2, 3], '请输入正确的软件类型'
    
    if software_type == '1':
        software = 'microsoft'
    elif software_type == '2':
        software = 'adobe'
    elif software_type == '3':
        software = 'matlab'

    # 初始化 list
    name_list = []
    desc_list = []
    url_list = []
    download_url = 'http://ms.zju.edu.cn/download/file'

    resp = sess.get(f'http://ms.zju.edu.cn/{software}/download.html')
    bs = BeautifulSoup(resp.text, 'html.parser')
    divs = bs.find_all('div', class_=re.compile('product.*?') if software_type == '1' else 'adobeinfo')

    # 提取数据
    if software_type == '1':
        for div in divs[2:] :
            name_list.append(div.h2.text)
            desc_list.append(div.li.text.replace('\n', ''))

            # 直接下载
            if 'http' in div.find_all('a')[-1]['href']:
                url_list.append(div.find_all('a')[-1]['href'])
            # 需要再次获取下载链接
            else:
                # 下载默认版本（通常为32位中文版）
                data = {
                    'name': re.sub('[\u4e00-\u9fa5]', '', div.h2.text)\
                    .replace(' ', '').replace('.', '_').lower(),
                    'bit': '0'
                }
                url = sess.post(download_url, data=data, allow_redirects=False).headers['Location']
                url_list.append(url if url != 'http://ms.zju.edu.cn' else '获取失败，请前往官网获取')
    else:
        for div in divs :
            name_list.append(div.h2.text + ' ' + div.a.text.replace('下载', ''))
            desc_list.append(div.p.text)
            url_list.append(sess.get(div.a['href'], allow_redirects=False).headers['Location']) 

    table = PrettyTable()
    table.add_column('\033[33m软件名称\033[0m', name_list)
    table.add_column('\033[33m软件描述\033[0m', desc_list)
    table.add_column('\033[33m下载地址\033[0m', url_list)
    print(table)
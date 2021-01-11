import os
import getpass
import json
import sys 
sys.path.append("..") 
from zjuam import ZJUAccount
from pprint import pprint


def get_ticket(sess):
    """
    获取 ticket 参数
    :param sess: 登录浙大通行证后的 session
    :return: ticket 的值
    """
    resp = sess.get('https://zjuam.zju.edu.cn/cas/oauth2.0/authorize?redirect_uri=https%3A%2F%2Fit2020.zju.edu.cn&response_type=code&client_id=PY8yOkVI3QgFerx2cK')
    # for r in resp.history:
    #     print(r.status_code, r.url)
                
    ticket = resp.history[2].url.split('ticket=')[-1]
    return ticket


if __name__ == '__main__':
    if os.path.exists('../config.json'):
        configs = json.loads(open('../config.json', 'r').read())
        username = configs["username"]
        password = configs["password"]
    else:
        username = input("👤 浙大统一认证用户名: ")
        password = getpass.getpass('🔑 浙大统一认证密码: ')

    zju = ZJUAccount(username, password)
    sess = zju.login()

    params = {
        'code': get_ticket(sess),
        'redirect_uri': 'https://it2020.zju.edu.cn',
    }
    resp = sess.post('https://it2020.zju.edu.cn/api/data', 
        headers={'X': 'X'}, 
        params=params)
    
    pprint(resp.json())

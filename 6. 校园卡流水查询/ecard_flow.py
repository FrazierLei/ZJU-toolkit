import requests
import json
import re
import getpass
from prettytable import PrettyTable
import sys 
sys.path.append("..") 
from zjuam import ZJUAccount
import colorama # 防止 windows 命令行打印带颜色字符串失败
colorama.init(autoreset=True)

def get_flow(sess, start_date, end_date):
    """
    查阅指定时间段的消费流水
    :param sess: 登录浙大通行证后的 session
    :param start_date: 开始时间，格式为2020-01-01
    :param end_date: 结束时间，格式为2020-01-01
    :return: 包含所需数据的 table 对象
    """
    # 获取 ssoticketid
    resp = sess.get('http://ecardsso.zju.edu.cn/ias/prelogin?sysid=FWDT')
    ssoticketid = re.search('id="ssoticketid" value="(.*?)"', resp.text).group(1)

    # resp 中包含了需要的cookie: hallticket
    data = {
        'errorcode': '1',
        'continueurl': 'http://ecardhall.zju.edu.cn:808/cassyno/index',
        'ssoticketid': ssoticketid
    }
    sess.post('http://ecardhall.zju.edu.cn:808/cassyno/index', data=data)

    # 查询对应的卡号
    resp = sess.post('http://ecardhall.zju.edu.cn:808/User/GetCardInfoByAccountNoParm', data={'json': 'true'})
    account = json.loads(resp.json()['Msg'])['query_card']['card'][0]['account']

    # 获取流水信息，这里只获取了第一页，可以按照需要修改
    data = {
      'sdate': start_date,
      'edate': end_date,
      'account': account,
      'page': '1',
      'rows': '100'
    }
    resp = sess.post('http://ecardhall.zju.edu.cn:808/Report/GetPersonTrjn', data=data)

    # 将重点数据储存在列表中
    time = []
    location = []
    amount = []
    balace = []

    for i in resp.json()['rows']:
        time.append(i['OCCTIME'])
        location.append(i['MERCNAME'])
        amount.append(i['TRANAMT'])
        balace.append(i['ZMONEY'])

    # 初始化 table，再按列填入数据
    table = PrettyTable()
    table.add_column('\033[33m交易时间\033[0m', time)
    table.add_column('\033[33m交易地点\033[0m', location)
    table.add_column('\033[33m交易金额\033[0m', amount)
    table.add_column('\033[33m余额\033[0m', balace)

    return table

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

    start_date = input('请输入开始时间，格式为\033[33m2020-01-01\033[0m:\n')
    end_date = input('请输入结束时间，格式为\033[33m2020-01-01\033[0m:\n')
    table = get_flow(sess, start_date=start_date, end_date=end_date)
    print(table)
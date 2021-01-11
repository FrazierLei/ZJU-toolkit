import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import sys 
sys.path.append("..") 
from zjuam import ZJUAccount

def get_cc98_info(sess):
    sess.get('https://account.cc98.org/LogOn?returnUrl=%2F')
    resp = sess.get('https://account.cc98.org/My')
    bs = BeautifulSoup(resp.text, 'html.parser')
    accounts = bs.find_all('h4')
    print(f'您共有 \033[1;31m{len(accounts)}\033[0m 个 CC98 账号，主要数据如下：')

    username_list = []
    post_count_list = []
    wealth_list = []
    register_time_list = []
    fan_count_list = []
    popularity_list = []
    like_count_list = []

    for i in accounts:
        username = i.span.text
        resp  = requests.get(f'https://api.cc98.org/user/name/{username}')
        resp_json = resp.json()
        post_count = resp_json['postCount']
        wealth = resp_json['wealth']
        register_time = resp_json['registerTime'].replace('T', ' ')
        fan_count = resp_json['fanCount']
        popularity = resp_json['popularity']
        like_count = resp_json['receivedLikeCount']

        username_list.append(username)
        post_count_list.append(post_count)
        wealth_list.append(wealth)
        register_time_list.append(register_time)
        fan_count_list.append(fan_count)
        popularity_list.append(popularity)
        like_count_list.append(like_count)

    table = PrettyTable()
    table.add_column('\033[33m用户名\033[0m', username_list)
    table.add_column('\033[33m注册时间\033[0m', register_time_list) 
    table.add_column('\033[33m发帖数\033[0m', post_count_list)
    table.add_column('\033[33m财富值\033[0m', wealth_list)
    table.add_column('\033[33m粉丝数\033[0m', fan_count_list)
    table.add_column('\033[33m收到的赞\033[0m', like_count_list)
    table.add_column('\033[33m风评\033[0m', popularity_list)

    return table


if __name__ == '__main__':
    zju = ZJUAccount('', '')
    sess = zju.login()
    table = get_cc98_info(sess)
    print(table)
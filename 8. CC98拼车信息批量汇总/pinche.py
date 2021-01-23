import os
import math
import re
import requests
import time


class CC98:
    def __init__(self, username, password):
        """
        初始化。
        :param username: 用户名
        :param password: 密码
        """
        self.sess = requests.session()
        self.username = username
        self.password = password
        self.token = ""
        self.expiretime = -1
        self.special_topic_id = 4990321
        self.start_floor = 2

    def login(self):
        """
        发起登录请求 以获取access_token 存入self.token
        并将过期时间写入self.expiretime
        """
        login_data = {
            'client_id': '9a1fd200-8687-44b1-4c20-08d50a96e5cd',
            'client_secret': '8b53f727-08e2-4509-8857-e34bf92b27f2',
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'scope': 'cc98-api openid offline_access'
        }
        x = self.sess.post("https://openid.cc98.org/connect/token",
                           data=login_data,
                           headers={"content-type": "application/x-www-form-urlencoded"})

        data = x.json()
        token = data['access_token']
        expirein = data['expires_in']
        self.token = token
        self.expiretime = int(time.time()) + expirein
        self.sess.headers.update({'authorization': 'Bearer ' + self.token})
        print(f'{self.username} 登录成功。')

    def get_topic_post(self, topic_id, from_=0):
        """
        获取指定 id 帖子中从 from_ 开始的全部回复
        :param topic_id: 帖子的 id
        :param from_: 起始楼层
        :return: 键值对为 {floor: content} 的字典
        """
        content_dict = {}
        while True:
            resp = self.sess.get(f'https://api.cc98.org/Topic/{topic_id}/post?from={from_}&size=20')
            resp_json = resp.json()
            if not resp_json:
                break
            for post in resp_json:
                content_dict.update({post['floor']: post['content']})
            from_ += 20

            # 休息一下，防止触发反爬虫系统
            time.sleep(1)

        print(f'共获取到{len(content_dict)}条回复')
        return content_dict

    @staticmethod
    def parse_content(content):
        """
        解析获取得到的文本
        :param content: 获取到的文本
        :return: 解析后的结果，如果解析成功则返回包含关键信息的 ubb 代码，如果解析失败返回 None
        """
        try:
            date = re.search("日期[：:](.*)", content).group(1)
            time_ = re.search("出发时间[：:](.*)", content).group(1)
            start = re.search("出发地点[：:](.*)", content).group(1)
            end = re.search("目的地[：:](.*)", content).group(1)
            contact = re.search("联系方式[：:](.*)", content).group(1)
            return f'[tr][th]{date}[/th][th]{time_}[/th][th]{start}[/th][th]{end}[/th][th]{contact}[/th]'
        except AttributeError:
            return None

    def make_table(self, check_last_table=True):
        """
        生成ubb语法的表格
        :param check_last_table: 是否检查上次保存的结果
        :return: ubb语法的表格
        """
        # 检查上次的获取记录
        file_path = './last_table.txt'
        if check_last_table and os.path.exists(file_path):
            with open(file_path, 'r') as f:
                text = f.read().split('\n', 1)
                start = int(re.search("当前更新到第(.*)层", text[0]).group(1))
                table = text[1]
                print(f'检测到有上次的获取记录，从第{start}层开始获取...')
        else:
            print('从头开始获取...')
            start = self.start_floor
            table = '[table]\n[tr][th]日期[/th][th]时间[/th][th]出发地[/th][th]目的地[/th][th]联系方式[/th][th]楼层[/th][/tr]\n'

        content_dict = self.get_topic_post(topic_id=self.special_topic_id, from_=start)

        # content_dict 非空，表示有新的楼层
        if content_dict:
            for floor, content in content_dict.items():
                result = self.parse_content(content)
                if result:
                    table += result + f'[th][url=/topic/{self.special_topic_id}/{math.ceil(floor/10)}#{floor%10}]>>戳我去楼层<<[/url][/th][/tr]\n'
                else:
                    print(f'第{floor}层解析失败，请手动添加。')

            table += '[/table]'

            # 在本地文件中记录本次结果
            with open(file_path, 'w') as f:
                f.write(f'当前更新到第{floor}层。\n' + table)

            return table
        else:
            print('未发现新楼层。')


if __name__ == '__main__':
    cc98 = CC98(username='', password='')
    cc98.login()
    table = cc98.make_table(check_last_table=False)
    print(table)
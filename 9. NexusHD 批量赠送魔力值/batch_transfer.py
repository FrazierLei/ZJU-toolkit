import requests


username = '' # 你的用户名
password = '' # 你的密码
login_url = 'http://www.nexushd.org/takelogin.php'
exchange_url = 'http://www.nexushd.org/mybonus.php?action=exchange'
gift = 1000 # 每个人的转账金额，大于25，小于10,000,000
users = [] # 包含待转账的用户名的list，例如['feifeizaici', 'imbitch', 'hahahaha']

sess = requests.Session()
sess.post(login_url,
       headers={'content-type': 'application/x-www-form-urlencoded'},
       data=f'username={username}&password={password}')

for user in users:
    data = {
      'option': '7',
      'username': user,
      'bonusgift': str(gift),
      'message': '有钱任性',
      'submit': '赠送'
    }
    resp = sess.post(exchange_url, data=data)
    if '不存在该用户' in resp.text:
        print(f'不存在{user}，请检查。')
    elif '你没有足够的魔力值' in resp.text:
        print('魔力值不足')
    else:
        print(f'给 {user} 转账 {gift} 成功')

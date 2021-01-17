import requests
from prettytable import PrettyTable


# 为了防止内网信息泄漏，请从 curl 的转化结果中获取 url
url = ''

data = {
  'send_by_bootstrap_table': 'true',
  'searchModel.inputType': '{"dwmc":[""]}',
  'searchModel.selectType': '{}',
  'searchModel.dateType': '{}',
  'searchModel.numberType': '{}',
  'searchModel.inputSqlType': '0',
  'bynf': '2021',
  'xydm': '1000',
  'xlccdm': '11',
  'queryModel.showCount': '15',
  'queryModel.currentPage': '1'
}

resp = requests.post(url, data=data)

company_name = []
student_num = []
page_num = resp.json()['totalPage']

# 保存数据
for page in range(1, page_num+1):
    data.update({'queryModel.currentPage': str(page)})
    resp = requests.post(url, data=data)
    for item in resp.json()['items']:
        company_name.append(item['dwmc'])
        student_num.append(item['num']) 


table = PrettyTable()
table.add_column('\033[33m单位名称\033[0m', company_name)
table.add_column('\033[33m就业人数\033[0m', student_num)

print(table)
# CC98拼车专楼自动汇总程序

## 目的

减少版主手动汇总信息的工作量。



## 格式

要求每层按照固定的格式回复：

```
日期：（如1月27日）
出发时间：（如下午3点15分）
出发地点：（如紫金港校区东2门/玉泉校区新桥门）
目的地：（如杭州东站）
联系方式：（电话、qq、微信号三选一）
备注：（选填）
```



## 环境需求

- Python 3.6 或更新版本

  因为字符串部分用到了 `f-string` 语法

- Reuqests 模块

  通过 `pip install requests` 安装



## 使用方法

###  手动调整几个参数

- 首先创建一个 CC98 对象：

  `CC98(username=, password=, special_topic_id=, start_floor=)`

  其中：

  - `username`、`password`：98用户名和密码。如果帖子是在内部板块，则需要版主以上权限的账号。如果是一般版面，则可以是普通账号。
  - `special_topic_id`：拼车专楼的 `topic_id` ，例如5026129
  - `start_floor`：拼车专楼中开始统计的楼层（如果从3楼开始，则输入2，以此类推）

- 然后生成 ubb 语法的表格代码：

  `table = cc98.make_table(check_last_table=False)` 中 `check_last_table` 表示是否检查上次保存的信息，如果为 `False` 则从头开始获取每层楼的内容，如果为 `True` 则从上一次获取的最后一层楼的下一层开始。



### 运行程序

```shell
$ python pinche.py
```

控制台中会打印出生成的表格，复制编辑到汇总楼中。

当前路径下会生成一个 `last_table.txt` 文件，包含本次程序运行时的最新楼层和表格代码。


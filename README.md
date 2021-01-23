# ZJU-toolkit

一些登录浙大通行证以后可以查看到的信息，just for fun.

## 目前实现的一些小功能

0. 登录浙大通行证

   分别实现了web端的登录和钉钉扫码登录，详见文章[【JS逆向】模拟登录浙大通行证](https://mp.weixin.qq.com/s/SOHmtLgxgpXvpbeHXhBVEQ)

1. 蓝码生成器

   文章：[生成「蓝马」背景的蓝码](https://mp.weixin.qq.com/s/O3CBi2M7o-X5a_idtHk2Hg)

2. 2020年度信息化账单

   文章：[2020浙大信息化年度数据账单中的code参数分析](https://mp.weixin.qq.com/s/8G88f8ip8PpJs3Lx-JmrvA)

3. 每日健康打卡

   参考：[ZJU-nCov-Hitcarder](https://github.com/Tishacy/ZJU-nCov-Hitcarder)

4. CC98账号管理

   查看一下同一通行证下CC98账户的基本参数。

   或许有兴趣看一下 [CC98抽卡机](https://github.com/FrazierLei/cc98-drawcard)？

   - 文章：[CC98抽卡机](https://mp.weixin.qq.com/s/WCTEPiMs-So_GRdYiheVAw)
   - 代码：[cc98-drawcard](https://github.com/FrazierLei/cc98-drawcard)

5. 就业网2021年隐藏信息查询

   详见[README](./5.%20就业网隐藏信息查询/README.md)
   
6. 校园卡流水查询

   详见[README](./6.%20校园卡流水查询/README.md)

7. 正版软件下载

   获取微软、Adobe、Matlab所有软件的实际下载链接
   
8. CC98 拼车信息批量汇总

   详见[README](./8.%20CC98拼车信息批量汇总/README.md)

## 使用方法

1. 在`config.json`中添加浙大通行证的用户名（通常为学号）和密码。

2. 在每一个文件夹中运行

   ```shell
   $ python xxx.py
   ```

   

## 欢迎关注

![](./qrcode.png)

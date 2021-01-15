# 校园卡流水查询

根据提示输入开始时间和结束时间。

![](./images/result.png)

`ssoticketid`这个参数找了我半天，一开始以为是在一个请求的响应的set-cookie里，结果比了一下发现两个的值不一样。最后发现原来藏在一个302的响应里，探索过程还挺曲折的。



![](./images/search.png)

![](./images/found.png)
## 介绍

dgut 疫情防控自动提交，每天晚上 12:30 定时提交，尝试 3 次提交失败后会延后一小时再次尝试提交

## 如何使用

在 yqfk.py 中添加你的学号和密码。

```python
username = 'your student number'
password = 'your password'
```

安装依赖

```
pip install -r requirements.txt
```

安装 chromium driver，具体安装方法看使用什么系统

前台运行

```
python yqfk.py
```

后台运行

```shell
setsid python yqfk.py 1>output.log 2>output.log
# 或者使用 nohup
nohup python yqfk.py &
```

### 可选

如果需要消息推送服务，可以到

[Server 酱](http://sc.ftqq.com/3.version)

申请一个 sckey，在下面填入你的 sckey 和想要发送的消息。

```python
# 可选
sckey = ''
# text 是消息的标题（必填）
# desp 是正文消息（可空，支持MarkDown）
payload = {'text': u'今日提交成功', 'desp': ''}
```

提交成功后会发送一条消息到微信。


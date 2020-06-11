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


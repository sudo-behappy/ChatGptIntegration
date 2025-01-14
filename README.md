# ChatGptIntegration

A chatGPT implementation GUI version via PyQt5, also my PyQt5 practice project

目前仅支持简体中文



## 构建

**要求: python >= 3.10**

在./src目录下打开终端, 运行`pip install -r requirements.txt`

然后运行`pyinstaller -F main.py -p functions.py -p main_ui.py`

可执行文件将会出现在./dist目录下

## 关于国内的访问问题

由于ChatGPT的API在国内无法访问, 请在运行时使用VPN或代理

作者不提供任何形式的VPN服务

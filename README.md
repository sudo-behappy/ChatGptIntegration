# ChatGptIntegration

A chatGPT implementation GUI version via PyQt5, also my PyQt5 practice project

目前仅支持简体中文



## 构建(Windows & Linux)

**要求: python >= 3.10**

在./src目录下打开终端, 运行`pip install -r requirements.txt`

然后运行`pyinstaller -F main.py -p functions.py -p main_ui.py`

可执行文件将会出现在./dist目录下

## 使用(MacOS)

macOS暂时不支持构建, 请请使用源码运行

安装要求之后, 在./src目录下打开终端, 运行`python main.py`

## 关于API key

作者不提供openAI代注册服务, 请自行注册

如果想要使用作者的API key, 请联系作者, 作者将酌情提供

Email: 3216539984@qq.com

## 关于国内的访问问题

由于ChatGPT的API在国内无法访问, 请在运行时使用VPN或代理

作者不提供任何形式的VPN服务

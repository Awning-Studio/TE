# 广财教务系统一键评教

## 简介
该项目由Awning Studio开发者开源，用于进行广财教务系统一键好评。Awning Studio还开源了另一个安卓软件[Afterglow](https://github.com/Awning-Studio/Afterglow)，欢迎你的使用。

## 用法
1. 请确保你有Python环境
2. 在命令行使用pip命令下载依赖库（如果没下的话）
```python
pip install requests
```
```python
pip install bs4
```
3. 将Python文件保存到本地，并填写自己的学号密码
```python
USERNAME = "你的学号"
PASSWORD = "门户密码"
```
4. 运行，会收到“输入存于当前目录下的验证码”，此时在你打开的目录下会生成一张名为“code.png”的图片，识别其中的验证码并输入即可。

## 群聊
<img src="/readme/Afterglow Group.jpg" style="width: 40%" />

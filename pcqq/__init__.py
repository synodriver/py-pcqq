"""
Created on Sat Sep 11 at 21:38 2021

用前须知:
1. py-pcqq，这是一个本萌新使用Python编写的QQBot库，基于PC版QQ协议
2. 本项目仅作个人娱乐，功能极少，有更强大的功能需求请移步onebot
3. 本项目开源于Github，萌新代码写的很烂，各位大佬请多多包涵( 给点star吧，求求惹QAQ )
4. 本萌新的博客和Github项目首页中有关于该协议库的相关说明

联系方式:
@QQ: 2224825532
@Blog: http://blog.yeli.work
@Github: https://github.com/DawnNights

使用教程:
1. 使用pip install py-pcqq来安装这个协议库，并在代码中使用import pcqq来导入
2. 创建一个pcqq.QQBot类的实例，创建完毕后通过扫码登录获取机器人对象
3. 通过编写pcqq.Plugin类的子类，并重写match和handle方法来实现对机器人功能的编写
4. 调用RunBot方法使机器人装载编写的插件并开始监听消息

注意事项: 
1. 该协议库支持账密和扫码登录，账密登录失败后自动启用扫码
2. 第一次登录后得到的token会保存于token.bin，后续的登录优先读取token.bin文件，无需再次登录
3. 该协议库能发送的消息包括(at, 文本, 表情, xml卡片)
4. 该协议库能接收的消息包括(at, 文本, 图片, 表情)
5. 该协议库目前bug贼多，坐等一个大佬带我QAQ
"""

from ._core import QQBot, Plugin

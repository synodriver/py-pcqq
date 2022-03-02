PCQQ协议的Python语言实现

本项目由纯 Python3 标准库实现，简单易懂无需第三方依赖

支持手机扫码登录与账号密码登录，在终端环境下需要安装 pillow 库打印二维码

甚至在手机上你也可以通过`qpython`或`pydroid3`的终端环境来安装运行本协议库: [在手机上玩转QQ机器人？](https://b23.tv/ZVHP0lK)

通过 Generator 和 asyncio 异步协程实现事件的处理与调度

`session.token` 是登录完成后用于下次直接重连的令牌文件

`cache.db` 是存储群信息以及成员信息的数据库文件(缺点是不会及时更新)

# 已实现功能

#### 登录
- [x] 扫码登录
- [x] 账密登录
- [x] 登录重连
- [x] 退出登录

#### 发送消息
- [x] At
- [x] 文本
- [x] 表情
- [x] 卡片
- [x] 图片(仅群聊)

#### 接收消息
- [x] At
- [x] 文本
- [x] 图片
- [x] 表情

#### 接收事件
- [x] 进群事件
- [x] 退群事件
- [x] 禁言事件

#### 开放API
- [x] 更改群名片
- [x] 群禁言
- [x] 取群信息
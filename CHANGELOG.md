# 变更记录 - CHANGELOG

## 1.0.0
2022.12.22

- [**Added**] 基于 REST API 写的 Leancloud Python 运行库(~~官方的库不会用~~)。实现如下功能，详细用法请见函数提示。

  - `create_conversation()` 创建对话
  - `search_conversations()` 查询对话，支持指定查询和所有查询
  - `update_conversation()` 更新对话名称
  - `delete_conversation()` 删除对话
  - `add_members()` 在对话中添加用户
  - `delete_members()` 从对话中移除用户
  - `search_members()` 查询一个对话中的用户
  - `send_message()` 在一个对话中发送消息
  - `search_message()` 查询一个对话的历史消息
  - `create_user()` 创建一个用户
  - `login()` 登陆，用来校验密码和用户名
  - `search_user()` 查询用户的简短信息，支持指定查询和所有查询
  - `get_user_information()` 查询用户的详细信息
  - `delete_user()` 删除用户

- [**Added**] 程序实现了聊天软件的基础功能
  - PyQt5 实现完整的 UI 界面(~~虽说很丑~~)
  - 用户注册和登陆
  - 搜索和加入聊天室
  - 发送信息
  - 实时同步信息
  - 信息提示(log 功能)


## 1.0.1
2022.12.23
- [**Added**] 加入图标支持
    - UI窗口图标
    - UI界面图标
    - 任务栏图标（仅测试Windows）

## 1.0.2
2022.12.24
- [**Fixed**] 解决了PyQt中因为限制子线程不允许修改ui部件而导致的闪退
- [**Added**] `leancloud.py` 新增函数 `change_password()`。用于修改用户密码。
- [**Change**] 使用Master key 操作暂时解决权限问题
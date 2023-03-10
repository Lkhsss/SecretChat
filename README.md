<div align="center">

# 秘密聊天室 - SecretChat

**中文 [README.md](README.md) | English [README_en.md](README_en.md)**
</div>

![仓库统计图](https://repobeats.axiom.co/api/embed/da72c82cf86ea1e24248bb0d9d95b5fe0b712f02.svg "Repobeats analytics image")

前段时间突然发现 Leancloud 的免费功能，于是想写个应用。查看了[官方文档](https://leancloud.cn/docs/)后发现能干的事挺多。之前写的东西都人模鬼样，于是这次想写一个像样一点的有点实用性的东西。于是写了这个应用。

之所以取名“秘密”其实只是因为数据可以自己在后台查看而已(~~随便想的~~)。其实没啥安全性。
这个程序利用 Leancloud 提供的免费服务，可以拥有单独的数据库和用户系统(~~白嫖党狂喜~~)。在注册了自己的 Leancloud 应用后，你们就可以使用 leancloud 提供的 API 接口使用这个应用了。

本来官方提供了 Python 库，但是功能不全(~~不会用~~)，所以自己用 rest api 写了个类(bushi

---

## 使用教程

### clone 此项目

点击下载，或者直接在命令行中 `git clone https://github.com/Lkhsss/SecretChat.git`

#### 安装依赖

在项目主目录运行 `pip install -r requirements.txt`安装依赖库

这里推荐使用虚拟环境，方便以后打包

---

### 获取 LeanCloud 的应用凭证

#### 创建 LeanCloud 账户

前往 Leancloud 控制台([华北节点](https://console.leancloud.cn/) 和 [华东节点](https://console-e1.leancloud.cn) 随便选一个，不要选**国际版**[^为啥不选国际版])，注册一个账号

#### 点击创建应用

<img title="" src="https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/点击创建应用.3tkno01z18o0.webp" alt="点击创建应用" data-align="center" width="388">
  
[^为啥不选国际版]: [国际版自 2022 年 8 月起，共享域名不再向中国大陆提供服务](https://forum.leancloud.cn/t/2022-8/25408 )
  
####  配置应用
  
  
这个可以随便填
  
<img title="配置应用" src="https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/设置应用.5yc1se677hk0.webp" alt="设置应用" width="409" data-align="center">
  
####  点击设置
  
  
<img title="点击设置" src="https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/点击设置.3gdjxx3omes.webp" alt="点击设置" data-align="center" width="420">
  
####  选择[设置]>[应用凭证]
  
  
<img src="https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/选择应用凭证.6rgsfkootks0.webp" title="选择应用凭证" alt="选择应用凭证" data-align="center" width="300">
  
####  留存待用
  
  
如果此时看到了几个小小黄框框，并且标有`AppID`, `AppKey`, `MasterKey`以及`REST API 服务器地址`，保留网页待用。
  
---
  
###  配置 REST API
  
  
打开主目录下的`leancloud.py`文件
在开头的`REST_API`, `AppID`, `AppKey`, `MasterKey`四项当中分别填入在 leancloud 控制台中获得的值
<img src="https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/像这样配置.7303zt6ihsg0.webp" title="像这样配置" alt="像这样配置" data-align="center" width="400">
  
> 注意看清楚名字，不要填错了
  
> 注意形式和上图保持一致（斜杠和 https 标头），最好使用网页自带的复制键 -> ![复制键](https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/复制键.7grz4hsq0ak0.webp )
  
---
  
###  运行
  
  
运行出来就是酱紫
![运行](https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/运行.1gxhpgprsbgg.webp )
  
#### 创建对话

~~忘了写创建对话的 UI 了，以后会加上。现在先手动调用`leancloud.py`创建吧~~
版本[1.1.3](CHANGELOG.md#113)已经加入对话管理端

#### 管理对话
版本[1.1.3](CHANGELOG.md#113 )已经加入对话管理端。

目前支持操作：
  - 添加对话
  - 删除对话
####  其他操作
  
我在`leancloud.py`中添加了详细的函数方法提示，[CHANGELOG](./CHANGELOG.md ) 中简单地也提到了用法
  
---
  
##  关于安全
  
  
因为 REST api 的许多操作需要 master key，所以直接改成使用 master key 了（懒。虽然这样密钥容易泄露，但是咱都是白嫖的 leancloud，泄露出去也没什么吧......
我争取想个办法解决这个问题。大家在打包应用时最好做好防反编译，防止 key 外泄。
如若masterkey外泄了，可以前往获取masterkey的网页重置masterkey。
  
---
  
##  变更记录
  
  
[CHANGELOG.md](./CHANGELOG.md )
  
---
  
##  TODO
  
  
- [x] 添加图标支持 --> [v1.0.1 加入图标支持](CHANGELOG.md#101 )
- [x] 写一个**管理端**以用于管理对话和用户 --> [v1.1.3 加入对话管理端](CHANGELOG.md#113 )
- [x] 更新英文版 README 和 CHANGELOG(锻炼英语(~~bushi~~)
- [ ] 解决必须使用 master key 才能使用 api 的权限问题
- [ ] 添加 github api 新版本检测
- [ ] 增加注销用户等服务
- [ ] 管理端添加重命名对话功能

---
  
##  开发环境
  
  
- 编译器
  - Python 3.9.5 64-bit
- 运行库
  - PyQt5 5.15.4
  - requests 2.28.1
  
---
  
##  开源协议
  
  
[Apache-2.0 license](LICENSE )
  
作者：[Lkhsss](https://github.com/lkhsss )
  
---
  
##  另
  
  
图床挂了记得提个 issue 踢我一下
  
**欢迎提 issues 和 pr**
  
还有
求求有没有大佬请教一下pyqt5怎么做页面美化，默认的界面太丑了。谢谢谢谢

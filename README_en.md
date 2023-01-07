#  SecretChat
  
  
Recently I find Leancloud has many free functions can be used.So wanted to write a chat program.After reading[official document](https://docs.leancloud.app/ ),I thought there was a lot of freedom here.Every program I've written before looks like crap.So I want to make this program to be useful and formally.
  
The only reason it's called "secret" is because the data can be viewed on the console.(~~no reason~~)。Actually, there's no security。
This program is by design to just use the free serves of Leancloud(~~Free is the best?~~)。Once you have registered your Leancloud app, you can use the API provided by leancloud.
  
Actually Leancloud officially provides a Python library,but I don't know how to use. So I use REST api to make a new class.
  
##  Contens
  
  
- [HOW TO USE](#how-to-use )
  - [Clone this project](#clone-this-project )
    - [Install python dependencies](#install-python-dependencies )
  - [Get any keys of LeanCloud](#get-any-keys-of-leancloud )
    - [Register a LeanCloud account](#register-a-leancloud-account )
    - [Create app](#create-app )
    - [Configuration Settings](#configuration-settings )
    - [Choose Settings](#choose-settings )
    - [Choose[Settings]>[App keys]](#choosesettingsapp-keys )
    - [Get keys](#get-keys )
  - [Configuration keys](#configuration-keys )
  - [Run](#run )
    - [Manage conversation](#manage-conversation )
    - [Other actions](#other-actions )
- [About security](#about-security )
- [CHANGELOG](#changelog )
- [TODO](#todo )
- [development environments](#development-environments )
- [LICENSE](#license )
- [PS](#ps )
  
##  HOW TO USE
  
  
###  Clone this project
  
  
Click Download or use git command `git clone https://github.com/Lkhsss/SecretChat.git`
  
####  Install python dependencies
  
  
Run commands in the project home directory: `pip install -r requirements.txt`
  
The python virtual environment is recommended here for easy packaging later
  
---
  
###  Get any keys of LeanCloud
  
  
####  Register a LeanCloud account
  
  
Go to  Leancloud console([World edition](https://console.leancloud.app/ ) or [North China](https://console.leancloud.cn/ ) | [East China](https://console-e1.leancloud.cn )), register a LeanCloud account
  
####  Create app
  
  
<img title="" src="https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/点击创建应用.3tkno01z18o0.webp" alt="Create app" data-align="center" width="388">
  
####  Configuration Settings
  
  
<img title="Configuration Settings" src="https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/设置应用.5yc1se677hk0.webp" alt="Configuration Settings" width="409" data-align="center">
  
####  Choose Settings
  
  
<img title="Choose Settings" src="https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/点击设置.3gdjxx3omes.webp" alt="Choose Settings" data-align="center" width="420">
  
####  Choose[Settings]>[App keys]
  
  
<img src="https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/选择应用凭证.6rgsfkootks0.webp" title="选择应用凭证" alt="选择应用凭证" data-align="center" width="300">
  
####  Get keys
  
  
Keek the keys of name `AppID`, `AppKey`, `MasterKey`以及`REST API Server URL`.We will use it soon.
  
---
  
###  Configuration keys
  
  
Open the file named `leancloud.py`
Fill keys `REST_API`, `AppID`, `AppKey`, `MasterKey` with the keys you get in the Leancloud console.
<img src="https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/像这样配置.7303zt6ihsg0.webp" title="Like this" alt="Like this" data-align="center" width="400">
  
> Look out the name of the key!
  
> You'd better use ![复制键](https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/复制键.7grz4hsq0ak0.webp )to copy.
  
---
  
###  Run
  
  
And it cruns like this
![运行](https://cdn.staticaly.com/gh/Lkhsss/picx@main/SecretChat/运行.1gxhpgprsbgg.webp )
  
####  Manage conversation
  
  
Use file `admin.py` to manage conversations
  
  
####  Other actions
  
  
I made a detailed function introduction in class file `leancloud.py`.
[CHANGELOG](./CHANGELOG.md ) also has a single introduction
  
---
  
##  About security
  
  
Since many operations in the REST api require the master key, I'll use the master key instead
I'll try to figure out a way to solve this problem. When you package your application, it's best to be anti-decompile-proof to prevent key leaks.
If the masterkey is leaked, you can go to the webpage where you obtained the masterkey and reset it.
  
---
  
##  CHANGELOG
  
  
[CHANGELOG.md](./CHANGELOG.md )
  
---
  
##  TODO
  
  
- [x] Add icons --> [v1.0.1](CHANGELOG.md#101 )
- [x] Made a **administration** to manage conversations --> [v1.1.3](CHANGELOG.md#113 )
- [x] Update English version README and CHANGELOG(Practice English(~~bushi~~
- [ ] Resolve the problems of api permission
- [ ] Use github api to check update
- [ ] Add the function of rename conversation to `admin.py`
---
  
##  development environments
  
  
  
- Python 3.9.5 64-bit
  - PyQt5 - 5.15.4
  - requests - 2.28.1
  
---
  
##  LICENSE
  
  
[Apache-2.0 license](LICENSE )
  
Author：[Lkhsss](https://github.com/lkhsss )
  
---
  
##  PS
  
  
**Welcome issues and pr**
  
Can someone teach me how to beautify PyQt5? The default interface is tooooooooo ugly. Thanks.
  
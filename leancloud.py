import requests
import json


AppID = "xxxxxxxxxxx" # AppID
AppKey = "xxxxxxxxxxx" #AppKey
MasterKey = "xxxxxxxxxxx" #MasterKey
REST_api = "https://xxxxxxxxxxxx.com"  # REST api 的地址 | 注意末尾不要有"/"


debug = False   #是否开启debug模式

# 构建标头
header = {
    "X-LC-Id": AppID,
    "X-LC-Key": AppKey,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36",
    }

def log(log:str): #debug模式
        if debug:
            print(log)
class leancloud():
    '''
    # Leancloud类
    使用REST API操作Leancloud
    官方文档：<https://leancloud.cn/docs/index.html#REST-API>
    '''
    def create_conversation(self, conversation_name):
        """
        ## 对话创建函数
        ### 功能：创建一个对话。如果对话名称已存在，则返回该对话的信息

        参数：`conversation_name` 将要创建的对话名称

        返回：对话信息 -> json {'unique': 是否唯一, 'updatedAt': '更新时间', 'name': '对话名称', 'objectId': '对话ID', 'm': [], 'createdAt': '对话创建时间', 'uniqueId': '独有ID'}
        
        注意：不允许存在同名对话
        """

        api_url = ("{}/1.2/rtm/conversations".format(REST_api))# 构建创建对话api

        data = {"name": conversation_name, "unique": True}
        data_json = json.dumps(data)  # 只需要传入data的json数据，不需要header的json
        response = requests.post(
                url=api_url, headers=header, data=data_json
            )  # 创建对话
        if response.status_code == 403:
            return False
        elif response.status_code == 404:
            return None
        else:
            conversation_data = response.json()
            return conversation_data  # 返回

    def search_conversations(self, conversations_name=None):
        """
        ## 查询对话函数

        ### 功能：查询对话的信息。如果传入参数`conversations_name`则返回该名称对应的对话的objectId；如果不传入该参数，则返回所有的对话信息(json)

        参数：`conversations_name` 需要查询的对话名称

        返回：有`conversations_name`参数且查询到对话时返回该对话`objectId`；未查询到时返回`None` | 无`conversations_name`参数时返回所有对话 -> json列表
        """
        api_url = "{}/1.2/rtm/conversations".format(REST_api)

        response = requests.get(url=api_url, headers=header)

        response = response.json()  # 获取所有对话的json数据
        # 如果传入对话名称，则查询所有对话，寻找匹配对话名称的对话，并返回对话ID
        if conversations_name != None:  # 如果传入了参数conversations_name
            exist = False  # 首先先设置该名称在列表中不存在
            for i in range(len(response["results"])):  # 以列表的长度为循环次数，开始循环遍历
                if (
                    response["results"][i]["name"] == conversations_name
                ):  # 如果遍历到相同的项，则说明该名称的对话存在
                    objectId = response["results"][i]["objectId"]  # 设置id为查询到的名称的id
                    feedback = "查询到名称为：[{}]的对话。objectId为：[{}]".format(
                        conversations_name, objectId
                    )
                    log(feedback)
                    exist = True  # 设置该名称在列表中存在，方便判断返回值
                    break
            if exist:  # 如果该名称存在
                return objectId  # 返回该对话的id值
            else:
                return None  # 不存在，返回None
        else:#没有传入名称
            response = response['results']
            return response  # 返回所有对话的列表

    def update_conversation(self, objectId, new_conversation_name):
        """
        ## 更新对话名称函数
        ###功能：更新对话名称
        参数：`objectId` 对话的ID | `new_conversation_name` 新的对话名称

        返回：用户数据 -> json {'updatedAt': '更新时间', 'objectId': '对话ID'}
        """
        log("update_conversation()")
        api_url = ("{}/1.2/rtm/conversations/{}".format(REST_api, objectId))  # 更新对话api
        data = {"name": new_conversation_name}
        data_json = json.dumps(data)
        response = requests.put(url=api_url, headers=header, data=data_json)

        response = response.json()

        return response

    def delete_conversation(self, objectId):
        """
        ## 删除对话函数
        ### 功能：删除一个对话

        传入：`objectId` 对话的objectId

        返回：无论成功与否都无返回值
        """
        api_url = ("{}/1.2/rtm/conversations/{}".format(REST_api, objectId))  # 删除对话api

        response = requests.delete(url=api_url, headers=header)#TODO回调函数判断是否已删除


    def add_members(self, objectId, member_name):
        """
        ## 添加用户函数
        ### 功能：给一个对话添加用户

        参数： `objectId` 要添加用户的对话 | `member_name` 要加入对话的用户的名称，可以为一个列表

        返回：对话数据 -> json {"updatedAt":"对话更新时间", "objectId":"对话id"}

        #### 注意：此函数为为一个对话添加用户，而不是向leancloud的用户系统中添加用户。此函数可以添加用户系统中不存在的用户。注册用户需用`create_user()`函数。
        """
        api_url = ("{}/1.2/rtm/conversations/{}/members").format(REST_api, objectId)

        if type(member_name) == list:  # 自动转换参数类型，不然不能处理传入的列表名称
            data = {"client_ids": member_name}
        elif type(member_name) == str:
            data = {"client_ids": [member_name]}
        else:
            return TypeError
        data_json = json.dumps(data)

        response = requests.post(url=api_url, headers=header, data=data_json)  # 加入用户

        response = response.json()#json
        return response

    def delete_members(self, objectId, member_name):
        """
        ## 移除对话用户函数
        ### 功能：移除一个对话的用户

        参数： `objectId` 要移除用户的对话 | `member_name` 要移除用户的名称，可使用列表传入多个用户

        返回：对话数据 -> json {"updatedAt":"对话更新时间", "objectId":"对话id"}

        #### 注意：此函数为从一个对话中移除用户，而不是把用户从系统中删除。删除用户需用`delete_user()`函数
        """
        api_url = "{}/1.2/rtm/conversations/{}/members".format(REST_api, objectId)
        if type(member_name) is str:
            data = {"client_ids": [member_name]}
        elif type(member_name) is list:#如果传入列表，则自带了中括号
            data = {"client_ids": member_name}
        data_json = json.dumps(data)

        response = requests.delete(url=api_url, headers=header, data=data_json)  # 调用api移除用户

        response = response.json()

        return response

    def search_members(self, objectId):
        """
        ## 查询用户函数
        ### 功能：查询objectId所在的对话的所有用户

        参数：`objectId` 对话的Id

        返回：一个包含所有用户名的列表
        """
        api_url = "{}/1.2/rtm/conversations/{}/members".format(REST_api, objectId)
        response = requests.get(url=api_url, headers=header)

        user_list = response.json()["result"]
        return user_list

    def send_message(self, objectId: str, member_name: str, message: str):
        '''
        ## 发送信息函数

        ### 功能：向指定对话发送信息

        参数：`objectId` 对话的Id | `member_name` 发送信息的用户名称 | `message` 要发送的信息
        
        返回：json {"msg-id":"信息的id", "timestamp":时间戳}
        '''
        log("send_message()")
        api_url = "{}/1.2/rtm/conversations/{}/messages".format(REST_api, objectId)
        header['X-LC-Key'] = '{},master'.format(MasterKey)#使用MasterKey

        data = {"from_client": member_name, "message": message}
        log("发送消息：{}".format(message))
        data_json = json.dumps(data)

        response = requests.post(url=api_url, headers=header, data=data_json)
        response = response.json()

        try:
            if response['code'] == '1':
                return False
        except:
            pass

        log(response)

        return response

    def search_message(self, objectId):
        """
        ##功能：查询对话的历史消息

        参数：`objectId` 对话的Id

        返回：信息列表 -> json  [
                {
                    "timestamp": 时间戳,
                    "conv-id":   "不知道是啥",
                    "data":      "聊天数据",
                    "from":      "发送人的id",
                    "msg-id":    "信息的id"
                }
                ...
                ]
        """
        api_url = "{}/1.2/rtm/conversations/{}/messages".format(REST_api, objectId)

        response = requests.get(url=api_url, headers=header)

        back_data = response.json()

        return back_data

    def create_user(self, username, password, phonenumber=None):
        """
        ## 创建用户函数

        ### 功能：创建一个用户

        参数：`username`要创建的用户的名称 | `password` 用户的密码 | `phonenumber` 电话号码 [可选]

        返回：用户数据 -> json {"sessionToken":"用户的Token","createdAt":"创建时间","objectId":"用户的id"} | 若用户已存在，则返回`False`
        """
        api_url = "{}/1.1/users".format(REST_api)
        # 判断是否传入手机号
        if phonenumber == None:
            data = {"username": username, "password": password}
        else:
            data = {
                "username": username,
                "password": password,
                "mobilePhoneNumber": phonenumber,
            }
        data_json = json.dumps(data)  # json格式化数据

        response = requests.post(url=api_url, headers=header, data=data_json)

        if response.status_code == 201:
            pass
        else:
            return False

        response = response.json()

        return response

    def login(self, username, password):
        """
        ## 登陆函数
        ### 功能：登陆，检验密码

        参数：`username` 用户名称 | `password` 密码

        返回：用户信息 -> json {"sessionToken":"用户的Token","updatedAt":"创建时间", "objectId":"用户id","username":"用户名","createdAt":"创建时间"} | 用户名或密码错误返回False
        """
        api_url = "{}/1.1/login".format(REST_api)
        data = {"username": username, "password": password}
        data_json = json.dumps(data)

        response = requests.post(url=api_url, headers=header, data=data_json)

        if response.status_code == 200:
            response = response.json()
            return response
        elif response.status_code == 400:
            return False

    def search_user(self):
        """
        ## 查询用户函数
        ### 功能：查询所有已经注册的用户
        参数：无

        返回：所有用户数据 -> list -> json {"updatedAt":"信息更新日期","phone":"电话号码","objectId":"用户id","username":"用户名","createdAt":"创建时间"}
        """
        api_url = "{}/1.1/users".format(REST_api)

        response = requests.get(url=api_url, headers=header)
        response = response.json()['results']#TODO 下个版本再构造一个直接获取用户名列表的函数
        return response
    def get_user_information(self, username):
        """
        ## 查询用户信息函数
        ### 功能：查询用户信息

        参数：`username` 用户名称

        返回：用户信息 -> json {"sessionToken":"用户的Token","updatedAt":"创建时间", "objectId":"用户id","username":"用户名","createdAt":"创建时间"} | 如果用户不存在则返回 False
        """
        log("get_user_information()")
        user_list = self.search_user() #获取所有用户
        if_exist = False #判断用户是否存在的布尔值，默认为False
        for i in range(len(user_list)):#循环遍历用户列表，判断用户是否存在
            log("{}==>{}".format(username, user_list[i]['username']))
            if username == user_list[i]['username']:#用户存在
                if_exist = True #设置布尔值为存在
                objectId = user_list[i]['objectId']#获取objectId
            #不存在则布尔值始终为设置的False
        #判断返回什么东西
        if if_exist:#如果用户存在
            log("用户存在，获取信息")
            api_url = "{}/1.1/users/{}".format(REST_api, objectId)
            response = requests.get(url=api_url, headers=header)
            response = response.json()
            return response
        else:#用户不存在
            log("用户不存在")
            return False

    def delete_user(self, username):
        """
        ## 删除用户函数
        功能：删除一个用户

        参数：`username` 用户名称

        返回：删除成功返回True
        """
        # 获取objectId和sessionToken
        user_information = self.get_user_information(username=username)#获取user信息
        objectId = user_information["objectId"]
        sessionToken = user_information["sessionToken"]
        header['X-LC-Session'] = sessionToken#加入sessionToken

        data_json = json.dumps(header)
        api_url = "{}/1.1/users/{}".format(REST_api, objectId)  # 构建api

        response = requests.delete(url=api_url, headers=header, data=data_json)

        if response.status_code == 200:
            return True

    def change_password(self, session_token:str,objectId:str,old_password:str,new_password:str):
        '''
        功能：更新用户密码
        
        参数：`session_token` 用户的session_token，注册和登陆时会返回 | `objectId` 用户的objectId，注册和登陆时会返回 | `old_password` 用户旧的密码 | `new_password` 用户新的密码
        
        返回：信息更新的时间 -> json ["updatedAt"] | 若旧密码错误，则返回`False`
        '''
        api_url = "{}/1.1/users/{}/updatePassword".format(REST_api, objectId)
        header['X-LC-Session'] = session_token#加入sessionToken

        data = {"old_password":old_password,"new_password": new_password}
        data_json = json.dumps(data)#格式化data

        response = requests.put(url=api_url, headers=header, data=data_json)#发送put请求

        if response.status_code == 200:
            response = response.json()
            return response
        elif response.status_code == 400:
            response = response.json()
            if response['code'] == 210: #210说明旧密码错误
                return False #返回False
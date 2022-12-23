from PyQt5.QtCore import QThread, QMutex
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
import sys
from leancloud import leancloud  # 引入文件类

import time

from Ui_main_windows import Ui_MainWindow # 引入ui文件

version = "1.0.0"

class Mainwindow_ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.leancloud = leancloud()

        self.pushButton_refresh.clicked.connect(self.get_chat)  # 连接刷新按钮
        self.pushButton_login.clicked.connect(self.login)  # 登陆函数
        self.pushButton_register.clicked.connect(self.register)  # 连接注册函数
        self.pushButton_join.clicked.connect(self.join)  # 连接连接函数
        self.pushButton_send.clicked.connect(self.send_message)  # 连接
        self.action_about_program.triggered.connect(self.about_program)#连接关于
        self.action_about_author.triggered.connect(self.about_author)#连接关于

        self.pushButton_send.setDisabled(True)  # 禁用发送按钮
        self.pushButton_refresh.setDisabled(True)  # 禁用刷新按钮，登陆后解开
        self.pushButton_join.setDisabled(True)  # 禁用加入按钮，登陆后解开
        self.comboBox_conversation.setDisabled(True)  # 禁用选择框
        self.plainTextEdit_inputbox.setDisabled(True)  # 禁用输入框

    def get_chat(self):
        conversations_list = self.leancloud.search_conversations()
        self.log("INFO", "查询到{}个对话".format(len(conversations_list)))

        self.comboBox_conversation.clear()  # 清除所有项
        for i in range(len(conversations_list)):
            self.comboBox_conversation.addItem(conversations_list[i]["name"])

    def disable_status_widget(self, status):
        """
        解锁部件

        `status`=login 解锁刷新按钮， 加入按钮，对话选择框

        `status`=join 解锁所有按钮
        """
        if status == "login":
            self.pushButton_refresh.setDisabled(False)  # 刷新按钮，登陆后解开
            self.pushButton_join.setDisabled(False)  # 加入按钮，登陆后解开
            self.comboBox_conversation.setDisabled(False)  # 选择框
        elif status == "join":
            self.pushButton_refresh.setDisabled(False)  # 刷新按钮，登陆后解开
            self.pushButton_join.setDisabled(False)  # 加入按钮，登陆后解开
            self.comboBox_conversation.setDisabled(False)  # 选择框
            self.plainTextEdit_inputbox.setDisabled(False)  # 解禁输入框
            self.pushButton_send.setDisabled(False)  # 加入对话后解锁发送消息按钮
            
        else:
            pass

    def login(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        if username == "":
            self.log("WARN", "未填写用户名")
        elif password == "":
            self.log("WARN", "未填写密码")
        else:
            data = self.leancloud.get_user_information(username)
            if data == False:
                self.log("ERROR", "没有找到用户：[{}]".format(username))
                self.log("WARN", "请选择注册新用户")
            else:
                self.log("INFO", "成功查询到用户[{}]".format(username))
                log_back = self.leancloud.login(username, password)
                if log_back == False:
                    self.log("ERROR", "密码错误")
                    self.lineEdit_password.clear()
                else:  # 返回了用户数据
                    self.log("INFO", "用户[{}]登陆成功".format(log_back["username"]))

                    self.user_data = log_back  # 设置用户数据为类变量
                    self.is_login = True  # 设置变量：已登陆
                    self.lineEdit_user.setText(log_back["username"])  # 设置名称
                    self.get_chat()  # 刷新对话
                    self.disable_status_widget("login")

    def register(self):
        username = self.lineEdit_username.text()
        password = self.lineEdit_password.text()

        if username == "":
            self.log("WARN", "未填写用户名")
        elif password == "":
            self.log("WARN", "未填写密码")
        else:
            back_data = self.leancloud.create_user(username, password)
            if back_data == False:
                self.log("ERROR", "用户名已存在，请重新创建")
                self.lineEdit_username.clear()  # 清除输入框
            else:
                self.log("INFO", "用户[{}]注册成功".format(back_data["username"]))
                self.lineEdit_user.setText(back_data["username"])  # 设置用户名称
                self.user_data = back_data  # 设置用户数据为类变量
                self.get_chat()  # 刷新对话
                self.disable_status_widget("login")  # 解禁加入对话部件

    def join(self):
        selection = self.comboBox_conversation.currentText()  # 获取当前值

        self.conversation_id = self.leancloud.search_conversations(selection)  # 把对话的id传入类变量
        # 获取到对话的id

        join_back = self.leancloud.add_members(self.conversation_id, self.user_data["username"])

        self.log("INFO", "用户[{}]加入对话[{}]".format(self.user_data["username"], selection))


        self.disable_status_widget("join")  # 解锁所有部件#FIXME

        # 直接开启子线程
        self.threading_show_message()


    def threading_show_message(self):#开启子线程同步消息
        self.thread_1 = mythread(self.conversation_id)
        self.thread_1.start()

    def send_message(self):
        message = self.plainTextEdit_inputbox.toPlainText()
        if message == "":
            self.log("WARN", "不能发送空消息")
        else:
            self.leancloud.send_message(self.conversation_id, self.user_data["username"], message)
            self.plainTextEdit_inputbox.clear()  # 清除内容

    def log(self, level=None, message=None):
        time_log = str(time.strftime("%H:%M:%S", time.localtime()))
        if level == None:
            message = "[{}] {}".format(time, message)
        elif level == "INFO" or level == "info":
            message = (
                """<p><span style="color: green;">【{}】</span>[{}] {}</p>""".format(
                    level, time_log, message
                )
            )
        elif level == "ERROR" or level == "error":
            message = """<p><span style="color: red;">【{}】</span>[{}] {}</p>""".format(
                level, time_log, message
            )
        elif level == "WARN" or level == "warn":
            message = """<p><span style="color: rgb(255, 170, 0);">【{}】</span>[{}] {}</p>""".format(
                level, time_log, message
            )
        else:
            message = """【{}】[{}] {}""".format(level, time_log, message)
        self.textBrowser_messsagebox.append(message)
    
    def about_program(self):
        QMessageBox.about(self, "关于本程序", "秘密聊天室(SecretChat)\n当前版本 {}".format(version))
    def about_author(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icon/space_station.ico"), QIcon.Mode.Normal, QIcon.State.Off)
        QM = QMainWindow()
        QM.setWindowIcon(icon)
        QMessageBox.about(QM, '关于我', "LKH\n一个普通的高中程序猿\n个人主页：https://lkhsss.github.io")

class mythread(QThread):
    thread_lock = QMutex()  # 创建线程锁

    def __init__(self, conversation_id):
        super().__init__()
        self.leancloud = leancloud()  # 初始化
        self.conversation_id = conversation_id

    def run(self):  # 重写run()函数，调用线程的start()方法会自动运行
        showed_message_list = []  # 创建一个将要包含所有信息的列表，开始时为空
        while True:  # 目前暂时一直运行
            new_message_list = []  # 需要发送的列表，每次循环刷新
            new_message = self.leancloud.search_message(self.conversation_id)  # 查询所有的信息
            if new_message == []:  # 如果为空
                pass
            else:
                # 如果不为空
                for i in new_message:
                    if i not in showed_message_list:  # 如果不在发送过的列表里
                        showed_message_list.append(i)  # 加入已发送的列表
                        new_message_list.append(i)  # 加入需要发送的信息的列表
                # 发送
                self.show_message(new_message_list)
            time.sleep(1)

    def show_message(self, messages):
        messages = self.sort_message(messages)
        for i in messages:
            time_stamp = str(
                time.strftime("%H:%M:%S", time.localtime(i["timestamp"] / 1000))
            )  # 时间戳转化为时间
            message = ("[{}]【{}】：{}").format(time_stamp, i["from"], i["data"])
            ui.textBrowser_messsagebox.append(str(message))

    def sort_message(self, messages):  # 数据排序
        for i in range(len(messages)):  # 冒泡排序
            for x in range(len(messages) - 1):  # 需要时间戳从小到大排序
                if messages[x]["timestamp"] > messages[x + 1]["timestamp"]:  # 如果时间戳前大于后
                    messages[x + 1], messages[x] = messages[x], messages[x + 1]  # 交换位置
        return messages


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Mainwindow_ui()
    ui.show()
    sys.exit(app.exec())

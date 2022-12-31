from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QInputDialog
import sys
import time

from Ui_admin import Ui_MainWindow
from leancloud import leancloud

version = "1.0.0" # 版本号。详见CHANGELOG


class Mainwindow_ui(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("秘密聊天室 - 对话管理")

        self.action_about_program.triggered.connect(self.about_program)#连接关于
        self.action_about_author.triggered.connect(self.about_author)#连接关于
        self.pushButton_fresh.clicked.connect(self.fresh)
        self.pushButton_delete_conversation.clicked.connect(self.delete_conversation)
        self.pushButton_create_conversation.clicked.connect(self.create_conversation)

        self.pushButton_delete_conversation.setDisabled(True)#禁用删除按钮
        self.listWidget.itemClicked.connect(self.able_pushbutton)
        self.leancloud = leancloud()

        self.fresh() # 更新对话列表
    
    def fresh(self):
        self.listWidget.clear()
        conversation_list = self.leancloud.search_conversations()
        self.pushButton_delete_conversation.setDisabled(True)#禁用删除按钮
        for i in conversation_list:
            self.listWidget.addItem(i['name'])


    def able_pushbutton(self):
        self.pushButton_delete_conversation.setDisabled(False)


    def delete_conversation(self):
        choice = self.get_choice()
        objectId = self.leancloud.search_conversations(choice)#获取对话的objectId
        self.leancloud.delete_conversation(objectId)#删除对话
        self.fresh()#刷新

    def create_conversation(self):
        name, okPressed = QInputDialog.getText(self, "创建对话", "请输入对话名称")
        if okPressed is False: #点击取消键事件
            pass
        elif okPressed is True: #点击确认
            #检查是否为空
            if name == '':#信息为空，跳过
                pass
            else:#不为空，创建
                self.leancloud.create_conversation(name)
                self.fresh()

    def get_choice(self):
        choice = self.listWidget.currentItem().text()
        if choice is None:
            self.warn("未选择对话")
        else:
            return choice
            

    def warn(self, msg):
        QMessageBox.warning(self, "警告", msg)
    def about_program(self):
        QMessageBox.about(self, "关于本程序", "秘密聊天室 - 对话管理\n当前版本 {}".format(version))
    def about_author(self):
        #icon = QIcon()
        #icon.addPixmap(QPixmap(":/icon/space_station.ico"), QIcon.Mode.Normal, QIcon.State.Off)
        QM = QMainWindow()
        #QM.setWindowIcon(icon)
        QMessageBox.about(QM, '关于作者', "LKH\n一个普通的高中程序猿\n个人主页：https://lkhsss.github.io")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Mainwindow_ui()
    ui.show()
    sys.exit(app.exec())
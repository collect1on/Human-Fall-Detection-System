import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QLabel, QLineEdit, QPlainTextEdit,QGroupBox,QCheckBox,QScrollArea
from PyQt5.uic import loadUi
import sqlite3
import tempfile
import cv2
import json
from PyQt5 import QtCore
import main
from PyQt5 import QtCore, uic
import livewebcam
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from server2 import efffe
default_style_choose = """
QPushButton{ 
    color: rgb(0, 158, 0);
    background-color: rgb(40, 40, 40);
    border: 10px;border-radius: 10px;
    border: rgb(252, 255, 255);}
QPushButton:hover { background-color: rgb(120, 120, 120);color: rgb(0, 158, 0); }
"""
default_style_notchoose = """
QPushButton{ 
    color: rgb(150, 150, 150);
    background-color: rgb(40, 40, 40);
    border: 10px;border-radius: 10px;
    border: rgb(252, 255, 255);}
QPushButton:hover { background-color: rgb(120, 120, 120);color: rgb(0, 158, 0); }
"""
qlens=0
qlens2=0
class UIUI(QWidget):
    signal_setcode = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        #loadUi("D:/b1programFile/bigprogram/ui321.ui", self)  # Load the UI file directly into the current QWidget
        # 获取当前脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(script_dir, "ui321.ui")
        # 加载UI文件
        uic.loadUi(ui_path, self)

        self.pushButton_2.clicked.connect(self.button_clicked)
        #self.pushButton_2.setStyleSheet("QPushButton:hover { background-color: rgb(120, 120, 120); }")
        #self.pushButton_2.setStyleSheet(self.pushButton_2.styleSheet() + "QPushButton:hover { background-color: rgb(120, 120, 120);color: rgb(0, 158, 0); }")
        self.pushButton_3.clicked.connect(self.button_clicked3)


        self.tableWidget1 = self.findChild(QTableWidget, 'tableWidget1')

        self.tableWidget1.setColumnWidth(0, 30)  # 第一列宽度为100像素
        self.tableWidget1.setColumnWidth(1, 150)  # 第二列宽度为200像素
        self.tableWidget1.setColumnWidth(2, 180)  # 第三列宽度为150像素
        self.plainTextEdit = self.findChild(QPlainTextEdit, 'plainTextEdit')
        #self.plainTextEdit.lower()
        self.groupBox = self.findChild(QGroupBox, 'groupBox')
        self.groupBox.setVisible(False)
        self.groupBox.setEnabled(False)
        self.plainTextEdit.setVisible(False)
        self.plainTextEdit.setEnabled(False)
        self.plainTextEdit.setReadOnly(True)
        self.checkBox = self.findChild(QCheckBox, 'checkBox')
        self.checkBox.setEnabled(False)
        self.checkBox.setVisible(False)
        self.checkBox_2 = self.findChild(QCheckBox, 'checkBox_2')
        self.checkBox_2.setEnabled(False)
        self.checkBox_2.setVisible(False)


        self.label_5 = self.findChild(QLabel, 'label_5')
        self.label_5.mousePressEvent = self.clickedlabel_5
        self.label_4 = self.findChild(QLabel, 'label_4')
        self.label_4.mousePressEvent = self.clickedlabel_4
        self.label_3 = self.findChild(QLabel, 'label_3')
        self.label_3.mousePressEvent = self.clickedlabel_3
        self.checkBox.clicked.connect(self.handle_checkbox_clicked)
        self.checkBox_2.clicked.connect(self.handle_checkbox_clicked)

        self.pushButton.setVisible(False)
        self.pushButton.setEnabled(False)
        self.pushButton_4.setVisible(False)
        self.pushButton_4.setEnabled(False)
        self.scrollArea = self.findChild(QScrollArea, 'scrollArea')
        self.pushButton.clicked.connect(self.button_clicked1)
        #self.pushButton_4.clicked.connect(self.button_clicked4)
        #self.groupBox_3= self.findChild(QGroupBox, 'groupBox_3')
        self.groupBox_3.setVisible(False)
        self.groupBox_3.setEnabled(False)
        self.pushButton_6 = self.findChild(QPushButton, 'pushButton_6')
        self.pushButton_6.clicked.connect(self.button_clicked6)
        self.pushButton_5.clicked.connect(self.button_clicked5)
        self.pushButton_7 = self.findChild(QPushButton, 'pushButton_7')
        self.pushButton_7.clicked.connect(self.button_clicked7)
        self.pushButton_8 = self.findChild(QPushButton, 'pushButton_8')
        self.pushButton_8.clicked.connect(self.button_clicked8)
        self.pushButton_8.setVisible(False)
        self.pushButton_8.setEnabled(False)
        self.groupBox_5.setVisible(False)
        self.groupBox_5.setEnabled(False)
        self.pushButton_9 = self.findChild(QPushButton, 'pushButton_9')
        self.pushButton_9.clicked.connect(self.button_clicked9)
        self.pushButton_4= self.findChild(QPushButton, 'pushButton_4')
        self.pushButton_4.clicked.connect(self.button_clicked4)
        self.groupBox_6.setVisible(False)
        self.groupBox_6.setEnabled(False)
        self.pushButton_10 = self.findChild(QPushButton, 'pushButton_10')
        self.pushButton_10.clicked.connect(self.button_clicked10)
        self.textEdit_4 = self.findChild(QTextEdit, 'textEdit_4')
        self.textEdit_5 = self.findChild(QTextEdit, 'textEdit_5')

        self.textEdit_4.setPlainText("已检测到跌倒，可至”查看分析结果”中查看")
        self.textEdit_5.setPlainText("未检测到跌倒")

        style = "QTextEdit { font-size: 12 pt; text-align: center; border-radius: none;background-color: rgb(120, 120, 120); }}"
        self.textEdit_4.setStyleSheet(style)
        self.textEdit_5.setStyleSheet(style)

        self.textEdit_4.setReadOnly(True)
        self.textEdit_5.setReadOnly(True)
        self.textBrowser = self.findChild(QTextBrowser, 'textBrowser')
        self.label_6 = self.findChild(QLabel, 'label_6')
        self.label_7 = self.findChild(QLabel, 'label_7')
        self.label_7.setVisible(False)
        self.label_7.setEnabled(False)
        self.label_6.setVisible(True)
        self.label_6.setEnabled(True)
        self.label_8 = self.findChild(QLabel, 'label_8')
        self.label_8.mousePressEvent = self.clickedlabel_8
        self.textEdit_6 = self.findChild(QTextEdit, 'textEdit_6')
        self.textEdit_6.setVisible(False)
        self.textEdit_6.setEnabled(False)
        #self.textEdit_6.setText("123")
        self.textEdit_6.setStyleSheet("color: white;font-size: 12pt;text-align: center;")
        self.textEdit_6.setAlignment(Qt.AlignCenter)
        # 設置字體大小為12pt


        # 將文字置中
        self.textEdit_6.setAlignment(Qt.AlignCenter)

        self.pushButton_7.setVisible(False)
        self.pushButton_7.setEnabled(False)

        self.label_3.setVisible(False)
        self.label_3.setEnabled(False)


        #self.pushButton

        #self.groupBox = QGroupBox("GroupBox")
        #vbox = QVBoxLayout()
        #vbox.addStretch(1)
        #self.groupBox.setLayout(vbox)

        # 设置窗口布局
        #layout = QVBoxLayout()
        #layout.addWidget(self.groupBox_3)
        #self.setLayout(layout)

        #self.setWindowTitle('Group Box Centered')
        #self.resize(400, 300)

        qlist = database()
        self.tableWidget1.setRowCount(len(qlist))
        # self.label.mousePressEvent = self.clicked_label
        for i in range(len(qlist)):
            for j in range(3):
                item = QTableWidgetItem(str(qlist[i][j]))
                self.tableWidget1.setItem(i, j, item)

        for i in range(len(qlist)):
            button = QPushButton("回放")
            button.setStyleSheet("color: rgb(200, 200, 200);")

            button.clicked.connect(self.button_clicked_vedio)
            self.tableWidget1.setCellWidget(i, 3, button)

        """
        self.setWindowTitle('Label Click Example')
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel('Click me to show textbox')
        self.label.setObjectName('label_5')
        self.label.setStyleSheet("font-size: 20px; color: blue;")
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.textbox = QLineEdit()
        self.textbox.setObjectName('textbox_1')
        self.textbox.setStyleSheet("font-size: 20px; color: black;")
        self.textbox.setFixedSize(200, 50)
        self.textbox.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.label.mousePressEvent = self.show_textbox

    def show_textbox(self, event):
        self.textbox.show()
    """


        self.signal_setcode.connect(self.setcode)

    def getdatabase(self):
        qlist = database()
        self.tableWidget1.setRowCount(len(qlist))
        # self.label.mousePressEvent = self.clicked_label
        for i in range(len(qlist)):
            for j in range(3):
                item = QTableWidgetItem(str(qlist[i][j]))
                self.tableWidget1.setItem(i, j, item)

        for i in range(len(qlist)):
            button = QPushButton("回放")
            button.setStyleSheet("color: rgb(200, 200, 200);")

            button.clicked.connect(self.button_clicked_vedio)
            self.tableWidget1.setCellWidget(i, 3, button)



    def handle_checkbox_clicked(self):
        # 确保只有一个复选框被选中
        sender = self.sender()  # 获取发送信号的复选框
        if sender == self.checkBox and sender.isChecked():
            self.checkBox_2.setChecked(False)
        elif sender == self.checkBox_2 and sender.isChecked():
            self.checkBox.setChecked(False)
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if not self.label_5.underMouse():
                print("123")
                self.groupBox.setVisible(False)
                self.groupBox.setEnabled(False)
                self.plainTextEdit.setVisible(False)
                self.plainTextEdit.setEnabled(False)
                self.checkBox.setEnabled(False)
                self.checkBox.setVisible(False)
                self.checkBox_2.setEnabled(False)
                self.checkBox_2.setVisible(False)

    def clickedlabel_5(self, a):
        self.groupBox.setVisible(True)
        self.groupBox.setEnabled(True)
        self.plainTextEdit.setVisible(True)
        self.plainTextEdit.setEnabled(True)
        self.checkBox.setEnabled(False)
        self.checkBox.setVisible(False)
        self.checkBox_2.setEnabled(False)
        self.checkBox_2.setVisible(False)
        self.textEdit_6.setVisible(False)
        self.textEdit_6.setEnabled(False)
        self.plainTextEdit.setPlainText("常见问题\n\n问题1:如何使用上传影像跌倒分析?\n点选画面左上方的人体跌倒检测按钮，点选上传影像跌倒分析，接着上传影像，即可完成检测\n\n问题2:如何开始实时录像跌倒检测?\n答:点选画面左上方的人体跌倒检测按钮，接着点选录像检测，点选停止录像以完成检测")
        print("Label clicked ")
    def clickedlabel_4(self, a):
        self.groupBox.setVisible(True)
        self.groupBox.setEnabled(True)
        self.plainTextEdit.setVisible(True)
        self.plainTextEdit.setEnabled(True)
        self.checkBox.setEnabled(False)
        self.checkBox.setVisible(False)
        self.checkBox_2.setEnabled(False)
        self.checkBox_2.setVisible(False)
        self.textEdit_6.setVisible(False)
        self.textEdit_6.setEnabled(False)
        self.plainTextEdit.setPlainText("关于我们\n\n我们是来自华南理工大学的学生，我们开发一款人体跌倒检测分析系统软件产品，此软件只需一台计算机及摄像机即可完成检测，使用AI深度学习搭配图像分析的方式完成检测，并将检测结果即刻通知到手机端应用程序。具有最灵活且价格最低廉等优势，致力于以最方便的方式完成跌倒检测，为老人小孩的家中安全保驾护航。")
        print("Label clicked ")
    def clickedlabel_3(self, a):
        self.groupBox.setVisible(True)
        self.groupBox.setEnabled(True)
        self.plainTextEdit.setVisible(True)
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit.setPlainText("设定\n\n切换语言\n\n通知音效")
        self.checkBox.setEnabled(True)
        self.checkBox.setVisible(True)
        self.checkBox_2.setEnabled(True)
        self.checkBox_2.setVisible(True)
        self.textEdit_6.setVisible(False)
        self.textEdit_6.setEnabled(False)
        print("Label clicked ")

    def clickedlabel_8(self, a):
        self.groupBox.setVisible(True)
        self.groupBox.setEnabled(True)
        self.plainTextEdit.setVisible(True)
        self.plainTextEdit.setEnabled(True)
        self.checkBox.setEnabled(False)
        self.checkBox.setVisible(False)
        self.checkBox_2.setEnabled(False)
        self.checkBox_2.setVisible(False)
        self.plainTextEdit.setPlainText("连接手机\n\n在手机端应用程序中输入以下密码进行装置配对，以获得跌倒警")
        self.textEdit_6.setVisible(True)
        self.textEdit_6.setEnabled(True)
        print("Label clicked ")




    def scrollbar_changed(self):
        print("Scroll value changed:")

    def button_clicked(self):#
        self.pushButton_2.setStyleSheet(default_style_choose)
        self.pushButton_3.setStyleSheet(default_style_notchoose)
        self.pushButton.setVisible(False)
        self.pushButton.setEnabled(False)
        self.pushButton_4.setVisible(False)
        self.pushButton_4.setEnabled(False)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setVisible(True)
        self.groupBox_3.setVisible(False)
        self.groupBox_3.setEnabled(False)
        print("Button clicked")
        self.getdatabase()

    def button_clicked3(self):

        #self.pushButton_2.setStyleSheet()
        self.pushButton_2.setStyleSheet(default_style_notchoose)
        self.pushButton_3.setStyleSheet(default_style_choose)
        self.pushButton.setVisible(True)
        self.pushButton.setEnabled(True)
        self.pushButton_4.setVisible(True)
        self.pushButton_4.setEnabled(True)
        self.scrollArea.setEnabled(False)
        self.scrollArea.setVisible(False)

    def button_clicked1(self):
        #self.groupBox_3
        self.groupBox_3.setVisible(True)
        self.groupBox_3.setEnabled(True)



        print("Button clicked1")



    def button_clicked4(self):

        # 创建文件对话框实例
        file_dialog = QFileDialog(self)
            # 设置文件对话框的背景颜色
        file_dialog.setStyleSheet("QPushButton{background-color: rgb(200, 200, 200)}")
        # file_dialog.setStyleSheet("background-color: rgb(200, 200, 200)")
        #dialog.setStyleSheet("QPushButton { background-color: red }");
        # 使用文件对话框实例来获取所选文件名
        file_name, _ = file_dialog.getOpenFileName(self, "Upload Video", "",
                                                       "Video Files (*.mp4 *.avi *.MOV *.WMV *.FLV)")
        if file_name:
                # 处理选择的文件
            print("Selected File:", file_name)

            aa=main.vedioanalyze(file_name)
            if aa>5:
                self.groupBox_6.setVisible(True)
                self.groupBox_6.setEnabled(True)
                self.textEdit_4.setVisible(True)
                self.textEdit_4.setEnabled(True)
                self.textEdit_5.setVisible(False)
                self.textEdit_5.setEnabled(False)

            else:
                self.groupBox_6.setVisible(True)
                self.groupBox_6.setEnabled(True)
                self.textEdit_5.setVisible(True)
                self.textEdit_5.setEnabled(True)
                self.textEdit_4.setVisible(False)
                self.textEdit_4.setEnabled(False)





    def button_clicked10(self):
        self.groupBox_6.setVisible(False)
        self.groupBox_6.setEnabled(False)
        aa=main.packjson()
        print("main.packjson()2")
        BB=main.get_local_ip()
        main.login1(BB, aa)


    def upload_image(self):
        openfile_name = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        #file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Image files (*.jpg *.jpeg *.png)")
        #if file_path:
            #pixmap = QPixmap(file_path)
            #pixmap = pixmap.scaled(300, 200)  # 调整图片大小以适应标签
            #self.image_label.setPixmap(pixmap)

    def button_clicked6(self):
        self.groupBox_3.setVisible(False)
        self.groupBox_3.setEnabled(False)

    def button_clicked5(self):#確定
        self.groupBox_3.setVisible(False)
        self.groupBox_3.setEnabled(False)
        self.pushButton_3.setVisible(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_8.setVisible(True)
        self.pushButton_8.setEnabled(True)
        qlist = database()
        global qlens
        qlens = len(qlist)

        main.livewebcamanalyze()
        qlist2 = database()
        qlens2 = len(qlist2)





    def button_clicked7(self):
        #main.send_iiii_message()
        #main.asyncio.run(send_database_to_server())
        #main.send_database_to_serverport()
        print("main.packjson()1")
        aa=main.packjson()
        print("main.packjson()2")
        BB=main.get_local_ip()
        main.login1(BB,aa)
        print("main.login1(aa)")
        #main.login12(aa)


    def button_clicked8(self):
        livewebcam.stop_thread_func()
        self.pushButton_8.setVisible(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_3.setVisible(True)
        self.pushButton_3.setEnabled(True)
        self.groupBox_5.setVisible(False)
        self.groupBox_5.setEnabled(False)
        qlist = database()
        global qlens
        qlens2 = len(qlist)

        if qlens2>qlens:
            self.groupBox_6.setVisible(True)
            self.groupBox_6.setEnabled(True)
            self.textEdit_4.setVisible(True)
            self.textEdit_4.setEnabled(True)
            self.textEdit_5.setVisible(False)
            self.textEdit_5.setEnabled(False)
        else:
            self.groupBox_6.setVisible(True)
            self.groupBox_6.setEnabled(True)
            self.textEdit_5.setVisible(True)
            self.textEdit_5.setEnabled(True)
            self.textEdit_4.setVisible(False)
            self.textEdit_4.setEnabled(False)



    def button_clicked9(self):
        self.groupBox_5.setVisible(False)
        self.groupBox_5.setEnabled(False)

    def upload_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file_dialog = QFileDialog(self)
        file_dialog.setStyleSheet("background-color: lightblue;")
        file_name, _ = file_dialog.getOpenFileName(self, "Upload Image", "",
                                                   "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_name:
            # 处理选择的文件
            print("Selected File:", file_name)

    def resizeEvent(self, event):
        # 在窗口大小更改时调用此函数
        self.centerGroupBox_3()
        self.centerGroupBox_5()
        self.centerGroupBox_6()
        self.centerGroupBox_7()



    def centerGroupBox_3(self):
        # 计算GroupBox的位置
        geo = self.horizontalLayout_4.geometry()
        #geo = self.formGeometry()
        x = int((geo.width() - self.groupBox_3.width()) / 2)
        y = int((geo.height() - self.groupBox_3.height()) / 2)
        self.groupBox_3.move(x, y)

    def centerGroupBox_5(self):
        # 计算GroupBox的位置
        geo = self.horizontalLayout_4.geometry()
        # geo = self.formGeometry()
        x = int((geo.width() - self.groupBox_5.width()) / 2)
        y = int((geo.height() - self.groupBox_5.height()) / 2)
        self.groupBox_5.move(x, y)

    def centerGroupBox_6(self):
        # 计算GroupBox的位置
        geo = self.horizontalLayout_4.geometry()
        # geo = self.formGeometry()
        x = int((geo.width() - self.groupBox_6.width()) / 2)
        y = int((geo.height() - self.groupBox_6.height()) / 2)
        self.groupBox_6.move(x, y)

    def centerGroupBox_7(self):
        # 计算GroupBox的位置
        geo = self.horizontalLayout_2.geometry()
        # geo = self.formGeometry()
        x = int((geo.width() - self.textBrowser.width()) / 2)
        y = int((geo.height() - self.textBrowser.height()) / 2)
        self.textBrowser.move(x, y)

        # 获取主窗口的中心位置
        #main_window_center = self.rect().center()

        # 获取GroupBox的中心位置
       # groupBox_center = self.groupBox_3.rect().center()

        # 计算GroupBox在主窗口中心位置的偏移量
        #move_x = int(main_window_center.x() - groupBox_center.x())
       # move_y = int(main_window_center.y() - groupBox_center.y())

        #
       # self.groupBox_3.move(move_x, move_y)


    
    def setwifi(self,a):
        if a==True:
            self.label_7.setVisible(True)
            self.label_7.setEnabled(True)
            self.label_6.setVisible(False)
            self.label_6.setEnabled(False)
            
        else:
            
            self.label_7.setVisible(False)
            self.label_7.setEnabled(False)
            self.label_6.setVisible(True)
            self.label_6.setEnabled(True)

    def setcode(self, code):
        self.textEdit_6.setText(code)


    def button_clicked_vedio(self):
        if self.pushButton_8.isEnabled():
            self.groupBox_5.setVisible(True)
            self.groupBox_5.setEnabled(True)

            print("stopfirst")
        else:
            button = self.sender()
            index = self.tableWidget1.indexAt(button.pos())
            if index.isValid():
                row = index.row()
                item = self.tableWidget1.item(row, 0)
                print("Button clicked in row:", row)
                conn = sqlite3.connect('databasego.db')
                cursor = conn.cursor()
                self.vedioplay(cursor, item)
                conn.close()

    def vedioplay(self, cursor, video_id):
        cursor.execute('''SELECT record FROM records WHERE id = ?''', (video_id.text(),))
        video_blob = cursor.fetchone()[0]

        temp_video_file = tempfile.NamedTemporaryFile(delete=False)
        temp_video_file.write(video_blob)
        temp_video_file.close()

        video_capture = cv2.VideoCapture(temp_video_file.name)
        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                break
            cv2.imshow('Video', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()
        temp_video_file.close()

def database():
    conn = sqlite3.connect('databasego.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id, source, time FROM records''')
    rows = cursor.fetchall()
    return rows

app = QApplication([])
uiui = UIUI()
uiui.show()

def setconn(a):
    uiui.setwifi(a)
def setcodeport(a):
    # uiui.setcode(a)
    uiui.signal_setcode.emit(a)
from main import setsetconnected
setsetconnected(setconn)

from main import setsetcode
setsetcode(setcodeport)


app.exec_()



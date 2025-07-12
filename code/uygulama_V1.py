# -*- coding: utf-8 -*-
import sys
import os
import socket
from threading import Thread
from bson import ObjectId
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QSizePolicy)
from PyQt5.QtCore import (QTimer, Qt, QObject, QThread, pyqtSignal, pyqtProperty,
                          QPropertyAnimation, QEasingCurve, QCoreApplication)
from PyQt5.QtGui import QPixmap, QPainter, QColor, QTransform, QPen
from PyQt5 import uic, QtCore, QtGui, QtWidgets
import vlc
import paramiko
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import select  # En üste ekle
#FATİH EKLEDİ
# Kullanıcı bilgileri
db_username = "ygzzngn13"
db_password = "bitirme"

uri = f"mongodb+srv://{db_username}:{db_password}@bitirme.wjg6ttl.mongodb.net/?retryWrites=true&w=majority&appName=Bitirme"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("✅ MongoDB bağlantısı başarılı!")
except Exception as e:
    print("❌ Bağlantı hatası:", e)

db = client["bitirme_veritabani"]
koleksiyon = db["kullanicilar"]

# Veri ekleme
#yeni_kullanici = {"isim": "a", "sifre": "a"}
#koleksiyon.insert_one(yeni_kullanici)

# Veri çekme
#for kullanici in koleksiyon.find():
#    print(kullanici)

class LoginWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Mongo bağlantısı
        self.client = MongoClient(
            "mongodb+srv://fatihmazlum124:bitirme@bitirme.wjg6ttl.mongodb.net/?retryWrites=true&w=majority&appName=Bitirme",
            server_api=ServerApi('1')
        )
        self.db = self.client["bitirme_veritabani"]
        self.koleksiyon = self.db["kullanicilar"]

        # Buton bağlantısı
        self.ui.pushButton.clicked.connect(self.login_control)

    def login_control(self):
        kullanici = self.ui.lineEdit.text().strip()
        sifre = self.ui.lineEdit_2.text().strip()
        user = self.koleksiyon.find_one({"isim": kullanici, "sifre": sifre})

        if user:
            self.open_main_window()
        else:
            self.ui.label_5.setText("Hatalı giriş. Tekrar deneyiniz.")

    def open_main_window(self):
        self.main_window = Arayuz(self.ui.lineEdit_3)
        self.main_window.show()
        self.close()


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(625, 565)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(30, 30, 550, 500))
        self.widget.setStyleSheet("QPushButton#pushButton{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));\n"
"    color:rgba(255, 255, 255, 210);\n"
"    border-radius:5px;\n"
"}\n"
"\n"
"QPushButton#pushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));\n"
"}\n"
"\n"
"QPushButton#pushButton:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    background-color:rgba(150, 123, 111, 255);\n"
"}\n"
"\n"
"QPushButton#pushButton_2, #pushButton_3, #pushButton_4, #pushButton_5{\n"
"    background-color: rgba(0, 0, 0, 0);\n"
"    color:rgba(85, 98, 112, 255);\n"
"}\n"
"\n"
"QPushButton#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover{\n"
"    color: rgba(131, 96, 53, 255);\n"
"}\n"
"\n"
"QPushButton#pushButton_2:pressed, #pushButton_3:pressed, #pushButton_4:pressed, #pushButton_5:pressed{\n"
"    padding-left:5px;\n"
"    padding-top:5px;\n"
"    color:rgba(91, 88, 53, 255);\n"
"}\n"
"\n"
"")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(40, 30, 280, 430))
        self.label.setStyleSheet("\n"
"background-repeat: no-repeat;\n"
"background-position: center;\n"
"background-color: rgba(0, 0, 0, 80); /* opsiyonel maske */\n"
"border-top-left-radius: 50px;\n"
"background-image: url(:/images/images/bitirme_back.jpg);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(270, 30, 240, 430))
        self.label_3.setStyleSheet("background-color:rgba(255, 255, 255, 255);\n"
"border-bottom-right-radius: 50px;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(340, 80, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:rgba(0, 0, 0, 200);")
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(295, 150, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46, 82, 101, 200);\n"
"color:rgba(0, 0, 0, 240);\n"
"padding-bottom:7px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(295, 215, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46, 82, 101, 200);\n"
"color:rgba(0, 0, 0, 240);\n"
"padding-bottom:7px;")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(295, 295, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(301, 345, 181, 16))
        self.label_5.setStyleSheet("color:rgba(0, 0, 0, 210);")
        self.label_5.setObjectName("label_5")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(318, 383, 158, 50))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_2 = QtWidgets.QWidget(self.horizontalLayoutWidget)
        self.widget_2.setStyleSheet("background-color: rgba(255, 255, 255, 0.2);\n"
"border-radius: 10px;\n"
"padding: 6px;\n"
"")
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_2.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 200, 200, 0.3);  /* Hafif gri */\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(160, 160, 160, 0.4);  /* Hover efekti */\n"
"}\n"
"")
        self.pushButton_2.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/warn.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_3.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 200, 200, 0.3);  /* Hafif gri */\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(160, 160, 160, 0.4);  /* Hover efekti */\n"
"}\n"
"")
        self.pushButton_3.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/github.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon1)
        self.pushButton_3.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_4.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 200, 200, 0.3);  /* Hafif gri */\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(160, 160, 160, 0.4);  /* Hover efekti */\n"
"}\n"
"")
        self.pushButton_4.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/google.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon2)
        self.pushButton_4.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_5.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setFamily("Social Media Circled")
        font.setPointSize(15)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 200, 200, 0.3);  /* Hafif gri */\n"
"    border: none;\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgba(160, 160, 160, 0.4);  /* Hover efekti */\n"
"}\n"
"")
        self.pushButton_5.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/appstore.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon3)
        self.pushButton_5.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.horizontalLayout.addWidget(self.widget_2)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(40, 80, 230, 130))
        self.label_6.setStyleSheet("background-color:rgba(0, 0, 0, 0);")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setGeometry(QtCore.QRect(50, 80, 201, 40))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color:rgba(255, 255, 255, 200);")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setGeometry(QtCore.QRect(50, 125, 220, 91))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color:rgba(255, 255, 255, 200);")
        self.label_8.setObjectName("label_8")
        self.widget_3 = QtWidgets.QWidget(self.widget)
        self.widget_3.setGeometry(QtCore.QRect(40, 30, 280, 430))
        self.widget_3.setStyleSheet("background-color:rgba(0, 0, 0, 80);\n"
"border-top-left-radius: 50px;")
        self.widget_3.setObjectName("widget_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setGeometry(QtCore.QRect(60, 320, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("background-color:rgba(0, 0, 0, 0);\n"
"border:none;\n"
"border-bottom:2px solid rgba(46, 82, 101, 200);\n"
"color:rgba(0, 0, 0, 240);\n"
"padding-bottom:7px;")
        self.lineEdit_3.setObjectName("lineEdit_3")
        
        self.widget_3.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.lineEdit.raise_()
        self.lineEdit_2.raise_()
        self.pushButton.raise_()
        self.label_5.raise_()
        self.horizontalLayoutWidget.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.lineEdit_3.raise_()
       

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Pi Car"))
        self.lineEdit.setPlaceholderText(_translate("Form", "  Kullanıcı Adı"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "  Şifre"))
        self.pushButton.setText(_translate("Form", "GİRİŞ  YAP"))
        self.label_5.setText(_translate("Form", "Lütfen bilgilerinizi giriniz."))
        self.label_7.setText(_translate("Form", "MERHABA!"))
        self.lineEdit_3.setPlaceholderText(_translate("Form", "SSH IP Adresi"))
        self.label_8.setText(_translate("Form", "ELE 495\n"
"BİTİRME PROJEMİZE\n"
"HOŞGELDİNİZ"))

import res_rc

# BURAYA KADAR EKLEDİ

# --- Sabitler ---
MONGO_URI = "mongodb+srv://ygzzngn13:bitirme@bitirme.wjg6ttl.mongodb.net/?retryWrites=true&w=majority&appName=Bitirme"
UI_FILE = "gelismisArayuz_yeni.ui"
STEERING_IMG = "direksiyon.png"
VIDEO_FILE = "araba_animasyon.mp4"

# === Mongo Worker ===
class MongoWorker(QObject):
    commandsUpdated = pyqtSignal(list)
    voiceUpdated = pyqtSignal(list)
    gecmisUpdated = pyqtSignal(list)
    dbError = pyqtSignal(str)

    def __init__(self, uri):
        super().__init__()
        self.uri = uri
        self.running = True
        self.client = None
        self.db = None

    def connect_db(self):
        try:
            self.client = MongoClient(self.uri, server_api=ServerApi('1'))
            self.client.admin.command('ping')
            self.db = self.client['otonom_arac']
            self.dbError.emit("MongoDB bağlantısı başarılı.")
        except Exception as e:
            self.db = None
            self.dbError.emit(f"Mongo bağlantı hatası: {e}")

    def run(self):
        self.connect_db()
        while self.running:
            if self.db is None:
                self.dbError.emit("Veritabanı bağlantısı bekleniyor...")
                if not self.breakable_sleep(5000): break
                self.connect_db()
                continue

            try:
                komutlar = list(self.db['algilanan_json'].find().sort("_id", -1).limit(10))
                sesler = list(self.db['ses_ciktisi'].find().sort("_id", -1).limit(10))
                gorev_gecmisi = list(self.db['gorev_gecmisi'].find().sort("_id", -1).limit(10))
                self.commandsUpdated.emit(komutlar)
                self.voiceUpdated.emit(sesler)
                self.gecmisUpdated.emit(gorev_gecmisi)
            except Exception as e:
                self.dbError.emit(f"Veri çekme hatası: {e}")
                self.db = None
            QCoreApplication.processEvents()
            QThread.msleep(1000)

    def update_speaker_config(self, config):
        if self.db is None:
            self.dbError.emit("Kimlik ayarları güncellenemedi: DB bağlantısı yok.")
            return

        try:
            collection = self.db["kullanici_kimliklendirme"]
            result = collection.update_one({"_id": ObjectId("683d83a5d738ad9f9bf5b225")}, {"$set": config}, upsert=True)
            if result.modified_count > 0 or result.upserted_id:
                self.dbError.emit("Kimlik verileri MongoDB'ye yazıldı.")
            else:
                self.dbError.emit("Kimlik verileri zaten güncel.")
        except Exception as e:
            self.dbError.emit(f"Güncelleme hatası: {e}")

    def stop(self):
        self.running = False
        if self.client:
            self.client.close()
    def clear_gorev_gecmisi(self):
        if self.db is None:
            self.dbError.emit("Görev geçmişi silinemedi: DB bağlantısı yok.")
            return
        try:
            result = self.db["gorev_gecmisi"].delete_many({})
            self.dbError.emit(f"Görev geçmişi koleksiyonundan {result.deleted_count} kayıt silindi.")
        except Exception as e:
            self.dbError.emit(f"Görev geçmişi silme hatası: {e}")


# === Direksiyon Widget ===
class SteeringWheelWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(150, 150)
        self._rotation = 0.0
        self.image = QPixmap(STEERING_IMG)
        if self.image.isNull():
            self.image = QPixmap(300, 300)
            self.image.fill(Qt.transparent)
        self.anim = QPropertyAnimation(self, b"rotation")
        self.anim.setDuration(400)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    @pyqtProperty(float)
    def rotation(self): return self._rotation

    @rotation.setter
    def rotation(self, angle):
        self._rotation = angle
        self.update()

    def rotate_to(self, angle):
        self.anim.stop()
        self.anim.setStartValue(self._rotation)
        self.anim.setEndValue(angle)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        s = min(self.width(), self.height())
        pix = self.image.scaled(s, s, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        painter.translate(self.width()/2, self.height()/2)
        painter.rotate(self._rotation)
        draw_x = -pix.width() / 2
        draw_y = -pix.height() / 2
        painter.drawPixmap(int(draw_x), int(draw_y), pix)
        
class ArabaWorker(QObject):
    finished = pyqtSignal(str, str)  # stdout, stderr
    #YENİ EKLENDİ
    def __init__(self, ip_adresi):
        super().__init__()
        self.ip_adresi = ip_adresi
    
    def run(self):
        #host = "10.255.36.105"
        host = self.ip_adresi
        port = 22
        username = "monster"
        password = "a"
        command = "cd /home/monster/grup10/myenv && ./bin/python main.py"

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port=port, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command)

            output = stdout.read().decode()
            error = stderr.read().decode()

            ssh.close()
            self.finished.emit(output, error)
        except Exception as e:
            self.finished.emit("", f"SSH bağlantı hatası: {e}")
            

# === Ana Arayüz ===
class Arayuz(QMainWindow):
    command_received = pyqtSignal(str)
    speaker_config_changed = pyqtSignal(dict)
    car_anim_eski = 0
    finished = pyqtSignal(str, str)  # stdout, stderr
    clear_gecmis_requested = pyqtSignal()

    def __init__(self, lineEdit_3):
        super().__init__()
        uic.loadUi(UI_FILE, self)
        self.setup_vlc()
        self.setup_direksiyon()
        self.setup_buttons()
        self.setup_tcp_server()
        self.setup_mongo_worker()
        self.command_received.connect(self.handle_command)
        self.lineEdit_3 = lineEdit_3

    def setup_vlc(self):
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
        self.media = self.vlc_instance.media_new(VIDEO_FILE)
        self.media_player.set_media(self.media)
        self.media_player.set_hwnd(int(self.widget.winId()))
        self.is_playing = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop_video)
        self.timer.start(100)
    def clear_gorev_gecmisi(self):
        self.clear_gecmis_requested.emit()
    
    def on_araba_finished(self, output, error):
        if output:
            self.textBrowser_5.append(f"<font color='green'>Çıktı:\n{output}</font>")
        if error:
            self.textBrowser_5.append(f"<font color='red'>Hata:\n{error}</font>")
            
    def start_araba(self):
        ip_adresi = self.lineEdit_3.text().strip()

        if not ip_adresi:
                print("⚠️ SSH IP adresi boş olamaz.")
                return
        self.araba_thread = QThread()
        self.araba_worker = ArabaWorker(ip_adresi)
        self.araba_worker.moveToThread(self.araba_thread)
        self.araba_thread.started.connect(self.araba_worker.run)
        self.araba_worker.finished.connect(self.on_araba_finished)
        self.araba_worker.finished.connect(self.araba_thread.quit)
        self.araba_worker.finished.connect(self.araba_worker.deleteLater)
        self.araba_thread.finished.connect(self.araba_thread.deleteLater)
        self.araba_thread.start()

    def toggle_video(self):
        if not self.is_playing:
            self.media_player.play()
            self.is_playing = True
        else:
            self.media_player.pause()
            self.is_playing = False

    def loop_video(self):
        if self.is_playing and self.media_player.get_position() > 0.90:
            self.media_player.set_position(0.1)

    def setup_direksiyon(self):
        self.direksiyon = SteeringWheelWidget()
        layout = QVBoxLayout(self.widget_2)
        layout.addWidget(self.direksiyon)

    def setup_buttons(self):
        self.pushButton_3.clicked.connect(self.textBrowser_5.clear)
        self.pushButton.clicked.connect(self.start_araba)
        self.pushButton_gecmisSil.clicked.connect(self.clear_gorev_gecmisi)
        self.radioButton_yagiz.toggled.connect(self.update_kimlik)
        self.radioButton_efe.toggled.connect(self.update_kimlik)
        self.radioButton_fatih.toggled.connect(self.update_kimlik)
        self.radioButton_alperen.toggled.connect(self.update_kimlik)
        self.radioButton_yilmaz.toggled.connect(self.update_kimlik)
        self.radioButton_acik.toggled.connect(self.update_kimlik)
        

    def setup_tcp_server(self):
        Thread(target=self.run_tcp_server, daemon=True).start()

    def setup_mongo_worker(self):
        self.mongo_thread = QThread()
        self.mongo_worker = MongoWorker(MONGO_URI)
        self.mongo_worker.moveToThread(self.mongo_thread)
        self.mongo_thread.started.connect(self.mongo_worker.run)
        self.mongo_worker.commandsUpdated.connect(self.show_komutlar)
        self.mongo_worker.voiceUpdated.connect(self.show_sesler)
        self.mongo_worker.gecmisUpdated.connect(self.show_gorev_gecmisi)
        self.mongo_worker.dbError.connect(self.textBrowser_5.append)
        self.speaker_config_changed.connect(self.mongo_worker.update_speaker_config)
        self.clear_gecmis_requested.connect(self.mongo_worker.clear_gorev_gecmisi)
        self.mongo_thread.start()

    def update_kimlik(self):
        if self.radioButton_yagiz.isChecked() or self.radioButton_efe.isChecked() or self.radioButton_fatih.isChecked() or self.radioButton_alperen.isChecked() or self.radioButton_yilmaz.isChecked():
            config = {
                "secilen_yagiz": self.radioButton_yagiz.isChecked(),
                "secilen_efe": self.radioButton_efe.isChecked(),
                "secilen_fatih": self.radioButton_fatih.isChecked(),
                "secilen_alperen": self.radioButton_alperen.isChecked(),
                "secilen_yilmaz": self.radioButton_yilmaz.isChecked(),
                "herkes" : False
            }
        else:
            config = {
                "secilen_yagiz": self.radioButton_yagiz.isChecked(),
                "secilen_efe": self.radioButton_efe.isChecked(),
                "secilen_fatih": self.radioButton_fatih.isChecked(),
                "secilen_alperen": True,
                "secilen_yilmaz": self.radioButton_yilmaz.isChecked(),
                "herkes" : False
            }
        if self.radioButton_kapali.isChecked():
            config["herkes"] = True  
            self.textBrowser_5.append("Konuşan kimliklendirme kapalı. Herkes konuşabilir.")
        else:
            self.textBrowser_5.append("Kimlik ayarı güncellendi.")
        self.speaker_config_changed.emit(config)

    def show_komutlar(self, veriler):
        #self.textBrowser_2.clear()
        #for v in veriler:
            #self.textBrowser_2.append(f"Komutlar: {v.get('json', '-')}")
        
        scrollbar_komut = self.textBrowser_2.verticalScrollBar()
        previous_value = scrollbar_komut.value()  # FATİH EKLEDİ BARI KAYDET

        self.textBrowser_2.clear()
        for v in veriler:
            self.textBrowser_2.append(f"Komutlar: {v.get('json', '-')}")

        scrollbar_komut.setValue(previous_value)  # Önceki konuma geri döndür
    
    def show_gorev_gecmisi(self, veriler):
        #self.textBrowser_3.clear()
        #for v in veriler:
            #self.textBrowser_3.append(f"{v.get('gecmis', '-')}")
        scrollbar_gorev = self.textBrowser_3.verticalScrollBar()
        previous_value = scrollbar_gorev.value()  # FATİH EKLEDİ BARI KAYDET

        self.textBrowser_3.clear()
        for v in veriler:
            self.textBrowser_3.append(f"Komutlar: {v.get('gecmis', '-')}")

        scrollbar_gorev.setValue(previous_value)  # Önceki konuma geri döndür

    def show_sesler(self, veriler):
        
        self.textBrowser.clear()
        for v in veriler:
            self.textBrowser.append(f"Ses: {v.get('ses', '-')}")

    def run_tcp_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', 5000))
            s.listen()
            while True:
                conn, addr = s.accept()
                Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_command(self, command):
        komutlar = {
            "sag": ("Araç sağa dönüyor.", 60, 1),
            "sol": ("Araç sola dönüyor.", -60, 1),
            "ileri": ("Araç ileri gidiyor.", 0, 1),
            "geri": ("Araç geri gidiyor.", 0, 1),
            "engel": ("Engel algılandı.", 0, 0),
            "dur": ("Araç durdu.", 0, 0),
            "bekle":("Araç bekliyor.", 0, 0),
            "ses":("Çalıştırmak için \"Hey Pi Car\" diyiniz.",0,0),
            "wakeword": ("Araç kullanıcıları dinliyor.",0,0)
        }
        
        msg, angle, car_anim = komutlar.get(command, (f"Bilinmeyen komut: {command}", 0,0))
        self.textBrowser_4.setPlainText(msg)
        self.direksiyon.rotate_to(angle)
        if car_anim != self.car_anim_eski :
            self.toggle_video()
        self.car_anim_eski = car_anim
        
    def handle_client(self, conn, addr):
        with conn:
            
            while True:
                
                    ready, _, _ = select.select([conn], [], [], 0.005)  # 5ms aralıkla kontrol
                    if ready:
                        data = conn.recv(1024)
                        if not data:
                            break
                        msg = data.decode('utf-8').strip()
                        if msg:
                            self.command_received.emit(msg)
                            conn.sendall(b"OK\n")
                

    def closeEvent(self, event):
        self.mongo_worker.stop()
        self.mongo_thread.quit()
        self.mongo_thread.wait()
        self.media_player.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    login.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    login.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    login.show()
    #BURAYA KADAR
    sys.exit(app.exec_())

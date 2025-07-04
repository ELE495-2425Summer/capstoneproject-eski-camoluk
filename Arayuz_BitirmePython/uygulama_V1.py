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
from PyQt5 import uic
import vlc
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# --- Sabitler ---
MONGO_URI = "mongodb+srv://ygzzngn13:bitirme@bitirme.wjg6ttl.mongodb.net/?retryWrites=true&w=majority&appName=Bitirme"
UI_FILE = "gelismisArayuz.ui"
STEERING_IMG = "direksiyon.png"
VIDEO_FILE = "araba_animasyon.mp4"

# === Mongo Worker ===
class MongoWorker(QObject):
    commandsUpdated = pyqtSignal(list)
    voiceUpdated = pyqtSignal(list)
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
                komutlar = list(self.db['algilanan_komutlar'].find().sort("_id", -1).limit(10))
                sesler = list(self.db['ses_ciktisi'].find().sort("_id", -1).limit(10))
                self.commandsUpdated.emit(komutlar)
                self.voiceUpdated.emit(sesler)
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

# === Ana Arayüz ===
class Arayuz(QMainWindow):
    command_received = pyqtSignal(str)
    speaker_config_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        uic.loadUi(UI_FILE, self)
        self.setup_vlc()
        self.setup_direksiyon()
        self.setup_buttons()
        self.setup_tcp_server()
        self.setup_mongo_worker()
        self.command_received.connect(self.handle_command)

    def setup_vlc(self):
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()
        self.media = self.vlc_instance.media_new(VIDEO_FILE)
        self.media_player.set_media(self.media)
        self.media_player.set_hwnd(int(self.widget.winId()))
        self.is_playing = False
        self.pushButton.clicked.connect(self.toggle_video)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loop_video)
        self.timer.start(100)

    def toggle_video(self):
        if not self.is_playing:
            self.media_player.play()
            self.is_playing = True
            self.pushButton.setText("Durdur")
        else:
            self.media_player.pause()
            self.is_playing = False
            self.pushButton.setText("Başlat")

    def loop_video(self):
        if self.is_playing and self.media_player.get_position() > 0.95:
            self.media_player.set_position(0.0)

    def setup_direksiyon(self):
        self.direksiyon = SteeringWheelWidget()
        layout = QVBoxLayout(self.widget_2)
        layout.addWidget(self.direksiyon)
        self.pushButton_sag.clicked.connect(lambda: self.direksiyon.rotate_to(60))
        self.pushButton_sol.clicked.connect(lambda: self.direksiyon.rotate_to(-60))
        self.pushButton_sifirla.clicked.connect(lambda: self.direksiyon.rotate_to(0))

    def setup_buttons(self):
        self.pushButton_3.clicked.connect(self.textBrowser_5.clear)
        self.pushButton_gecmisSil.clicked.connect(lambda: self.textBrowser_5.append("Geçmiş silindi."))
        self.checkBox_yagiz.stateChanged.connect(self.update_kimlik)
        self.checkBox_efe.stateChanged.connect(self.update_kimlik)
        self.checkBox_fatih.stateChanged.connect(self.update_kimlik)
        self.checkBox_alperen.stateChanged.connect(self.update_kimlik)
        self.checkBox_yilmaz.stateChanged.connect(self.update_kimlik)
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
        self.mongo_worker.dbError.connect(self.textBrowser_5.append)
        self.speaker_config_changed.connect(self.mongo_worker.update_speaker_config)
        self.mongo_thread.start()

    def update_kimlik(self):
        config = {
            "secilen_yagiz": self.checkBox_yagiz.isChecked(),
            "secilen_efe": self.checkBox_efe.isChecked(),
            "secilen_fatih": self.checkBox_fatih.isChecked(),
            "secilen_alperen": self.checkBox_alperen.isChecked(),
            "secilen_yilmaz": self.checkBox_yilmaz.isChecked()
        }
        if self.radioButton_kapali.isChecked():
            for k in config:
                config[k] = True  # Hepsi true olur
            self.textBrowser_5.append("Konuşan kimliklendirme kapalı. Hepsi açık sayıldı.")
        else:
            self.textBrowser_5.append("Kimlik ayarı güncellendi.")
        self.speaker_config_changed.emit(config)

    def show_komutlar(self, veriler):
        self.textBrowser_2.clear()
        for v in veriler:
            self.textBrowser_2.append(f"Komut: {v.get('action', '-')}, Açı: {v.get('angle', '-')}")

    def show_sesler(self, veriler):
        
        self.textBrowser.clear()
        for v in veriler:
            self.textBrowser.append(f"Ses: {v.get('ses', '-')}")

    def run_tcp_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', 5000))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    self.command_received.emit(f"{addr} bağlandı.")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        msg = data.decode('utf-8').strip()
                        self.command_received.emit(msg)
                        conn.sendall(b"OK\n")

    def handle_command(self, command):
        komutlar = {
            "sag": ("Araç sağa dönüyor", 60),
            "sol": ("Araç sola dönüyor", -60),
            "ileri": ("Araç ileri gidiyor", 0),
            "geri": ("Araç geri gidiyor", 0),
            "engel": ("Engel algılandı", 0),
            "dur": ("Durdu", 0)
        }
        msg, angle = komutlar.get(command, (f"Bilinmeyen komut: {command}", 0))
        self.textBrowser_4.setPlainText(msg)
        self.direksiyon.rotate_to(angle)

    def closeEvent(self, event):
        self.mongo_worker.stop()
        self.mongo_thread.quit()
        self.mongo_thread.wait()
        self.media_player.stop()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Arayuz()
    window.show()
    sys.exit(app.exec_())

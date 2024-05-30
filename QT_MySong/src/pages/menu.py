import sys
import os

import requests


# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from pages.buscar_page import SearchSong, SongListItem
from controller.Reproducir_cancion import ReproductorCanciones
from pages.listas_page import ListasPage
from pages.subir_cancion_page import SubirCancionPage
from pages.setting_page import SettingsWindow
from ApiServices.userService import UserService

class Menu(QMainWindow):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.setWindowTitle("MySong - HOME")
        self.setGeometry(QApplication.primaryScreen().availableGeometry())
        self.setStyleSheet("background-color:#3773DB;")
        self.reproductor = ReproductorCanciones()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        self.left_section = QWidget()
        self.left_section_layout = QVBoxLayout(self.left_section)

        logo_label = QLabel()
        pixmap = QPixmap("src/images/logo_mysong.jpeg")
        pixmap = pixmap.scaledToWidth(150, Qt.SmoothTransformation)
        rounded_pixmap = self.round_image(pixmap)
        logo_label.setPixmap(rounded_pixmap)
        logo_label.mousePressEvent = self.show_home
        self.left_section_layout.addWidget(logo_label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        self.left_section_layout.addSpacing(100)

        options = ["Buscar", "Subir canción", "Mis listas"]
        self.buttons = {}
        for option in options:
            button = QPushButton(option)
            button.setStyleSheet("background-color:#1FDBDB;color:black; font-size:19px; padding: 5px 10px; border: 1px solid #1FDBDB; border-radius: 10px;")
            button.clicked.connect(self.change_page)
            self.buttons[option] = button
            self.left_section_layout.addWidget(button, alignment=Qt.AlignCenter)

        self.left_section_layout.addSpacing(100)

        settings_button = QPushButton("Ajustes")
        settings_button.setStyleSheet("background-color:#1FDBDB;color:black; font-size:16px; padding: 0px; border: 1px solid #1FDBDB; border-radius: 10px;")
        self.left_section_layout.addWidget(settings_button, alignment=Qt.AlignBottom)

        if self.username is not None:
            settings_button.clicked.connect(self.show_settings_page)

        self.right_section = QWidget()
        self.right_section_layout = QVBoxLayout(self.right_section)

        self.stacked_widget = QStackedWidget()
        
        self.home_page = self.create_home_page()
        self.search_page = SearchSong(self.reproductor)
        self.upload_page = SubirCancionPage(self.username)
        self.lists_page = ListasPage(self.username)
        self.settings_page = SettingsWindow(self.username)

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.search_page)
        self.stacked_widget.addWidget(self.upload_page)
        self.stacked_widget.addWidget(self.lists_page)
        self.stacked_widget.addWidget(self.settings_page)

        self.right_section_layout.addWidget(self.stacked_widget)

        self.bottom_section = QWidget()
        self.bottom_section_layout = QVBoxLayout(self.bottom_section)

        self.bottom_section_layout.addWidget(self.reproductor.progress_bar)

        control_button_layout = QHBoxLayout()
        control_button_layout.addWidget(self.reproductor.pause_button)
        control_button_layout.addWidget(self.reproductor.play_button)
        control_button_layout.addWidget(self.reproductor.stop_button)
        control_button_layout.addWidget(self.reproductor.volume_slider)

        self.bottom_section_layout.addLayout(control_button_layout)

        self.bottom_section.setMinimumHeight(80)
        self.bottom_section.setMaximumHeight(80)

        self.right_section_layout.addWidget(self.bottom_section)

        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)

        self.layout.addWidget(self.left_section)
        self.layout.addWidget(separator)
        self.layout.addWidget(self.right_section)

        self.left_section.setStyleSheet("min-width: 200px; max-width: 200px;")

        # Conectar las señales a los métodos correspondientes
        self.reproductor.pause_button.clicked.connect(self.reproductor.pausar)
        self.reproductor.play_button.clicked.connect(self.reproductor.continuar)
        self.reproductor.stop_button.clicked.connect(self.reproductor.detener)
        self.reproductor.volume_slider.valueChanged.connect(self.reproductor.set_volume)
        self.reproductor.progress_changed.connect(self.reproductor.actualizar_barra_progreso)

    def change_page(self):
        sender = self.sender()
        if sender.text() == "Buscar":
            self.stacked_widget.setCurrentWidget(self.search_page)
        elif sender.text() == "Subir canción":
            self.stacked_widget.setCurrentWidget(self.upload_page)
        elif sender.text() == "Mis listas":
            self.stacked_widget.setCurrentWidget(self.lists_page)
    
    def show_home(self, event):
        self.stacked_widget.setCurrentWidget(self.home_page)

    def show_settings_page(self):
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def create_home_page(self):
        home_widget = QWidget()
        layout = QVBoxLayout(home_widget)

        self.top_section = QWidget()
        self.top_section.setStyleSheet("background-color: #1FDBDB; border: 1px solid #1FDBDB; border-radius: 15px;")
        self.top_section_layout = QHBoxLayout(self.top_section)

        novedades_button = QPushButton("Novedades")
        novedades_button.setStyleSheet("""
                                        QPushButton {
                                            background-color: #3773DB;
                                            color: white;
                                            font-size: 16px;
                                            padding: 10px;
                                            border: none;
                                            border-radius: 10px;
                                        }
                                        QPushButton:pressed {
                                            background-color: #1FDBDB;  /* Cambia el color cuando el botón está clicado */
                                        }
                                    """)

        novedades_button.clicked.connect(self.show_latest_songs_news)
        self.top_section_layout.addWidget(novedades_button)

        recomendaciones_button = QPushButton("Recomendaciones")
        recomendaciones_button.setStyleSheet("""
                                        QPushButton {
                                            background-color: #3773DB;
                                            color: white;
                                            font-size: 16px;
                                            padding: 10px;
                                            border: none;
                                            border-radius: 10px;
                                        }
                                        QPushButton:pressed {
                                            background-color: #1FDBDB;  /* Cambia el color cuando el botón está clicado */
                                        }
                                    """)
        recomendaciones_button.clicked.connect(self.show_recomendation)
        self.top_section_layout.addWidget(recomendaciones_button)

        mas_escuchadas_button = QPushButton("Más Escuchadas")
        mas_escuchadas_button.setStyleSheet("""
                                        QPushButton {
                                            background-color: #3773DB;
                                            color: white;
                                            font-size: 16px;
                                            padding: 10px;
                                            border: none;
                                            border-radius: 10px;
                                        }
                                        QPushButton:pressed {
                                            background-color: #1FDBDB;  /* Cambia el color cuando el botón está clicado */
                                        }
                                    """)
        mas_escuchadas_button.clicked.connect(self.show_mas_escuchado)
        self.top_section_layout.addWidget(mas_escuchadas_button)

        layout.addWidget(self.top_section)

        self.latest_songs_list = QListWidget()
        novedades_section = self.create_section(self.latest_songs_list)
        recomendation_section= self.create_section( self.latest_songs_list)
        mas_escuchado_section= self.create_section( self.latest_songs_list)
        layout.addWidget(novedades_section)
        layout.addWidget(recomendation_section)
        layout.addWidget(mas_escuchado_section)

        return home_widget

    def create_section(self, list_widget):
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.addWidget(list_widget)
        
        return section_widget

    def show_latest_songs_news(self):
        # Hacer la solicitud GET al endpoint para obtener las últimas 10 canciones
        url = "http://localhost:8181/canciones"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            latest_songs = data[-10:]  # Obtener las últimas 10 canciones
            self.latest_songs_list.clear()
            for song in latest_songs:
                item = QListWidgetItem()
                self.latest_songs_list.addItem(item)
                widget = SongListItem(song)
                widget.play_clicked.connect(self.reproductor.reproducir_cancion_url)
                self.latest_songs_list.setItemWidget(item, widget)
        else:
            self.latest_songs_list.clear()
            self.latest_songs_list.addItem("Error al cargar las últimas canciones")

    def show_recomendation(self):
        self.latest_songs_list.clear()
        item = QListWidgetItem()
        label = QLabel("Proximamente")
        label.setAlignment(Qt.AlignCenter)
        self.latest_songs_list.addItem(item)
        self.latest_songs_list.setItemWidget(item, label)

    def show_mas_escuchado(self):
        self.latest_songs_list.clear()
        item = QListWidgetItem()
        label = QLabel("Proximamente")
        label.setAlignment(Qt.AlignCenter)
        self.latest_songs_list.addItem(item)
        self.latest_songs_list.setItemWidget(item, label)



    def round_image(self, pixmap):
        radius = 75
        mask = QPixmap(pixmap.size())
        mask.fill(Qt.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.drawEllipse(0, 0, 2 * radius, 2 * radius)
        painter.end()
        rounded_pixmap = pixmap.copy(0, 0, 2 * radius, 2 * radius)
        rounded_pixmap.setMask(mask.mask())
        return rounded_pixmap

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window_menu = Menu()
    window_menu.show()
    sys.exit(app.exec())

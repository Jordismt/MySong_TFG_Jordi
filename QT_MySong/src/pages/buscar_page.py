import sys
import os
import requests


# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from controller.Reproducir_cancion import ReproductorCanciones

class SongListItem(QWidget):
    play_clicked = Signal(int)

    def __init__(self, song_data, parent=None):
        super().__init__(parent)
        self.song_data = song_data

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(f"{song_data['nombre']} - {song_data['nombreArchivo']}")
        layout.addWidget(label, 1)

        play_button = QPushButton("Reproducir")
        play_button.clicked.connect(self.emit_play_clicked)
        layout.addWidget(play_button)

    def emit_play_clicked(self):
        self.play_clicked.emit(self.song_data['id'])

class SearchSong(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MySong - Buscar Canciones")
        self.setStyleSheet(open("src/styles/buscar_song.css").read())

        self.reproductor = ReproductorCanciones()
        self.layout = QVBoxLayout(self)

        self.search_label = QLabel("Buscar Canciones por Nombre:")
        self.layout.addWidget(self.search_label)

        self.search_input = QLineEdit()
        self.layout.addWidget(self.search_input)

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search)
        self.layout.addWidget(self.search_button)

        self.results_list = QListWidget()
        self.results_list.setSpacing(5)  # Espaciado entre elementos
        self.layout.addWidget(self.results_list)

    def search(self):
        search_term = self.search_input.text().strip()
        if not search_term:
            return

        # Verificar si hay una canción en reproducción
        if self.reproductor.estado() == "Reproduciendo":
            QMessageBox.warning(self, "Canción en reproducción", "Ya hay una canción reproduciéndose.")
            return

        # Realizar una solicitud a la API para buscar canciones por nombre
        try:
            response = requests.get(f"http://localhost:8181/canciones/api/canciones?nombre={search_term}")
            if response.ok:
                metadata_list = response.json()
                self.display_results(metadata_list)
            else:
                print("Error al buscar canciones:", response.text)
        except Exception as e:
            print("Error al buscar canciones:", e)

    def display_results(self, songs):
        self.results_list.clear()
        if not songs:
            item = QListWidgetItem("No se encontraron canciones")
            self.results_list.addItem(item)
            return

        for song in songs:
            item = QListWidgetItem()
            self.results_list.addItem(item)
            widget = SongListItem(song)
            widget.play_clicked.connect(self.reproductor.reproducir_cancion_url)
            self.results_list.setItemWidget(item, widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SearchSong()
    window.show()
    sys.exit(app.exec())
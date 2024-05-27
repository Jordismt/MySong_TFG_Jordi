import sys
import os
import requests
# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtNetwork import *
from controller.Reproducir_cancion import ReproductorCanciones
from models.cancion import Cancion
from ApiServices.cancionService import CancionesService
from ApiServices.ListaReproduccionService import ListaReproduccionService


class SubirCancionPage(QWidget):
    BASE_URL = 'http://localhost:8181/canciones/subir-cancion'

    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("MySong - Subir Canción")
        self.setStyleSheet(open("src/styles/subir_cancion.css").read())
        self.usuario = usuario
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Crear instancia del reproductor de canciones
        self.reproductor = ReproductorCanciones()

        # Texto centrado arriba
        label = QLabel("Sube la canción que deseas añadir")
        label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(label)

        # Campo de texto para ingresar el nombre de la canción
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre de la canción")
        layout.addWidget(self.nombre_input)

        # Campo de texto para ingresar el nombre del artista
        self.artista_input = QLineEdit()
        self.artista_input.setPlaceholderText("Artista")
        layout.addWidget(self.artista_input)

        # Campo de texto para ingresar el nombre del álbum
        self.album_input = QLineEdit()
        self.album_input.setPlaceholderText("Álbum")
        layout.addWidget(self.album_input)

        # Dropdown para seleccionar la lista
        self.lista_dropdown = QComboBox()
        self.cargar_listas_usuario()
        layout.addWidget(self.lista_dropdown)

        self.file_path = None

        # Botón para seleccionar archivo
        select_button = QPushButton("Seleccionar archivo")
        select_button.setStyleSheet("background-color: #555; color: white;")
        select_button.clicked.connect(self.seleccionar_archivo)
        layout.addWidget(select_button)

        # Botón para subir la canción a la BD
        upload_button = QPushButton("Subir canción")
        upload_button.setStyleSheet("background-color: #4CAF50; color: white;")
        upload_button.clicked.connect(self.subir_cancion)
        layout.addWidget(upload_button)

        # QLabel para mostrar el nombre del archivo seleccionado
        self.file_label = QLabel("Archivo seleccionado: ")
        self.file_label.setStyleSheet("color: white;")
        layout.addWidget(self.file_label)

    def cargar_listas_usuario(self):
        listas = ListaReproduccionService.obtener_listas_usuario(self.usuario)
        if listas:
            for lista in listas:
                self.lista_dropdown.addItem(lista['nombre'], lista['id'])
        else:
            QMessageBox.warning(self, "Error", "No se pudieron cargar las listas de reproducción.")

    def seleccionar_archivo(self):
        # Abre un cuadro de diálogo para seleccionar un archivo
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Archivos de audio (*.mp3)")
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.file_path = selected_files[0]
                self.file_label.setText("Archivo seleccionado: " + os.path.basename(self.file_path))
                print(f"Archivo seleccionado: {self.file_path}")
            

    def subir_cancion(self):
        # Obtener los valores ingresados por el usuario
        nombre = self.nombre_input.text()
        artista = self.artista_input.text()
        album = self.album_input.text()
        lista_id = self.lista_dropdown.currentData()  # Obtener el ID de la lista

        # Validar que se hayan ingresado todos los campos y que se haya seleccionado un archivo
        if not all([nombre, artista, album, self.file_path]):
            QMessageBox.warning(self, "Campos incompletos", "Por favor, completa todos los campos y selecciona un archivo.")
            return

        try:
            # Leer el contenido del archivo MP3
            with open(self.file_path, 'rb') as file:
                mp3_content = file.read()

            form_data = {
                'nombre': nombre,
                'artista': artista,
                'album': album,
                'lista_id': str(lista_id),  # Convertir lista_id a cadena
                'usuario': self.usuario,
                'likes': '0',
                'nombreArchivo': self.file_path.split('/')[-1]  # Obtener el nombre del archivo MP3 desde la ruta del archivo
            }

            files = {'file': mp3_content}

            response = requests.post(self.BASE_URL, data=form_data, files=files)
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Canción subida exitosamente")
            else:
                QMessageBox.warning(self, "Error", f"Error al subir la canción: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Excepción al subir la canción: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    usuario = "usuario_de_prueba"  
    window = SubirCancionPage(usuario)
    window.show()
    sys.exit(app.exec())

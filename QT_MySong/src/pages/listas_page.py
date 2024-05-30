import sys
import os
# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from ApiServices.ListaReproduccionService import ListaReproduccionService
from models.lists import ListaReproduccion

class ListasPage(QWidget):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.setWindowTitle("Tus Listas")
        self.setStyleSheet("background-color:#3773DB;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)

        # Texto centrado arriba
        label = QLabel("Tus listas")
        label.setStyleSheet("font-size: 24px; color: white;")
        layout.addWidget(label, alignment=Qt.AlignCenter)

        # Botón para crear nueva lista
        crear_lista_button = QPushButton("Crear Nueva Lista")
        crear_lista_button.setStyleSheet("background-color:#1FDBDB; color:#FFFFFF; padding: 10px 20px; font-size: 16px;")
        crear_lista_button.clicked.connect(self.crear_nueva_lista)
        layout.addWidget(crear_lista_button, alignment=Qt.AlignRight)

        # Scroll area para las listas
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #3773DB;")
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        
        # Widget de contenido para el scroll area
        self.content_widget = QWidget()
        self.scroll_area.setWidget(self.content_widget)
        
        # Layout vertical para las listas
        self.listas_layout = QVBoxLayout(self.content_widget)
        self.listas_layout.setAlignment(Qt.AlignTop)
        self.listas_layout.setContentsMargins(10, 10, 10, 10)
        self.listas_layout.setSpacing(10)

        layout.addWidget(self.scroll_area)
        
    def showEvent(self, event):
        super().showEvent(event)
        print("Show event called")  # Agregar esta línea para verificar si se llama al método
        self.obtener_y_mostrar_listas()

    def crear_nueva_lista(self):
        if not self.username:
            QMessageBox.warning(self, "Error", "Nombre de usuario no especificado.")
            return

        nombre_lista, ok_lista = QInputDialog.getText(self, "Crear Nueva Lista", "Ingrese el nombre de la nueva lista:")
        if ok_lista and nombre_lista:
            nueva_lista = ListaReproduccion(self.username, nombre_lista, [])
            success, message = ListaReproduccionService.crear_lista_reproduccion(self.username, nueva_lista)
            if success:
                QMessageBox.information(self, "Éxito", message)
                # Actualizar la lista en la interfaz
                self.obtener_y_mostrar_listas()
            else:
                QMessageBox.warning(self, "Error", message)

    def obtener_y_mostrar_listas(self):
        # Borrar todos los widgets de lista existentes
        for i in reversed(range(self.listas_layout.count())):
            widget = self.listas_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        listas_reproduccion = ListaReproduccionService.obtener_listas_usuario(self.username)
        if listas_reproduccion:
            for lista in listas_reproduccion:
                lista_widget = self.crear_widget_lista(lista)
                self.listas_layout.addWidget(lista_widget)
        else:
            QMessageBox.warning(self, "Error", "No se pudieron obtener las listas de reproducción del usuario.")

    def crear_widget_lista(self, lista_reproduccion):
        widget = QWidget()
        widget.setStyleSheet("background-color:#1FDBDB; padding: 10px; border-radius: 5px;")
        layout = QVBoxLayout(widget)

        nombre_label = QLabel(lista_reproduccion['nombre'])
        nombre_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(nombre_label)


        return widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ListasPage(username='JordiProva')
    window.show()
    sys.exit(app.exec())

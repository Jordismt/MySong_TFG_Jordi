import sys
import os


# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout,QLabel,QPushButton,QMessageBox
from PySide6.QtGui import *
from PySide6.QtCore import *
from pages.menu import Menu
from pages.login_page import LoginRegister
from controller.Reproducir_cancion import ReproductorCanciones

class Inici(QMainWindow):
    def __init__(self):
        super().__init__()
      
        self.menu=Menu()
        self.login=LoginRegister()
        # Configurar el widget principal
        self.setWindowTitle("MySong - INICIO")
        self.setGeometry(QApplication.primaryScreen().availableGeometry())

        # Crear el widget principal y el layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)  # Usamos un layout vertical

        # Crear los widgets para las secciones
        self.top_section = QWidget()
        self.bottom_section = QWidget()

        # Establecer los colores de fondo de las secciones
        self.top_section.setStyleSheet("background-color: #1FDBDB;")  # Color top_section
        self.bottom_section.setStyleSheet("background-color: #3773DB;")  # Color bottom_section

        # Agregar los widgets de las secciones al layout
        self.layout.addWidget(self.top_section, 2.5)  # 25% de la ventana
        self.layout.addWidget(self.bottom_section, 7.5)  # Resto de la ventana (70%)

        # QLabel per a los textos (MySong, y el slogan)
        my_song_label = QLabel("MySong")
        my_song_label_slogan = QLabel("¡Música y más!")

        my_song_label.setStyleSheet("font-size: 70px; color: black;") #Estilos para el título
        my_song_label.setAlignment(Qt.AlignCenter) # Estilo para centrarlo

        my_song_label_slogan.setAlignment(Qt.AlignCenter) # Estilo para centrarlo
        my_song_label_slogan.setStyleSheet("font-size: 30px; color: black;") #Estilos para el slogan

        layout_top = QVBoxLayout(self.top_section) #Creamos layout vertical para los textos
        
        #Añadimos los textos al layout
        layout_top.addWidget(my_song_label) 
        layout_top.addWidget(my_song_label_slogan)

        # Agregar el logo centrado en la sección inferior
        logo_label = QLabel()
        pixmap = QPixmap("src/images/logo_mysong.jpeg")  # Ruta a la imagen del logo
        pixmap = pixmap.scaledToWidth(300, Qt.SmoothTransformation)  # Ajustar el tamaño de la imagen
        logo_label.setPixmap(pixmap)
        
        # Establecer la forma circular de la imagen
        radius = 150  # Radio del círculo, la mitad de lo que mide la imagen para que no se distorcione
        mask = QPixmap(radius * 2, radius * 2)
        mask.fill(Qt.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.drawEllipse(0, 0, radius * 2, radius * 2)
        painter.end()
        logo_label.setMask(mask.mask())

        layout_bottom = QVBoxLayout(self.bottom_section)
        layout_bottom.addWidget(logo_label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Agregar botones centrados verticalmente
        button_login = QPushButton("Iniciar sesion / Registrarse")
        button_invitado = QPushButton("Acceder como invitado")

        #Estilos para los botones
        button_login.setStyleSheet("padding: 10px 15px; background-color: #1FDBDB; color: black; font-size: 18px; border: 1px solid #1FDBDB; border-radius: 10px;")
        button_invitado.setStyleSheet("padding: 10px 15px; background-color: #1FDBDB; color: black; font-size: 18px; border: 1px solid #1FDBDB; border-radius: 10px; margin-bottom:250px;")

        #Añadir los botones al layout y centrarlos
        layout_bottom.addWidget(button_login, alignment=Qt.AlignCenter)
        layout_bottom.addWidget(button_invitado, alignment=Qt.AlignCenter)

        # Función para mostrar el aviso al hacer clic en el botón de invitado
        def mostrar_aviso():
            # Crear el cuadro de diálogo con el mensaje
            aviso = QMessageBox()
            aviso.setWindowTitle("Aviso")
            aviso.setText("Al acceder como invitado no podrás subir canciones ni crear listas, solo podrás escuchar música")
            aviso.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
            # Ejecutar el cuadro de diálogo y obtener el botón presionado
            result = aviso.exec()
            
            # Llamar a la función ir_a_menu con el resultado del cuadro de diálogo
            ir_a_menu(result)

        # Función para ir a la página del menú
        def ir_a_menu(result):
            # Verificar si se hizo clic en el botón Aceptar
            if result == QMessageBox.Ok:
                # Cerrar la ventana actual
                self.close()
                
                # Instanciar la ventana del menú y mostrarla
                self.menu.show()

        def page_login():
            self.close()
            self.login.show()
        # Conectar la señal clicked del botón de invitado a la función mostrar_aviso
        button_invitado.clicked.connect(mostrar_aviso)
        button_login.clicked.connect(page_login)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Inici()
    window.show()
    sys.exit(app.exec())

import sys
import os


# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from pages.buscar_page import SearchSong
from controller.Reproducir_cancion import ReproductorCanciones
from pages.listas_page import ListasPage
from pages.subir_cancion_page import SubirCancionPage
from pages.setting_page import SettingsWindow
from ApiServices.userService import UserService

class Menu(QMainWindow):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        # Configurar el widget principal
        self.setWindowTitle("MySong - HOME")
        self.setGeometry(QApplication.primaryScreen().availableGeometry())  # Establecemos que la ventana sea igual de grande que la pantalla del ordenador
        self.setStyleSheet("background-color:#3773DB;")
        self.reproductor=ReproductorCanciones()
        
        
        # Crear el widget principal y el layout horizontal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)  # Usamos un layout horizontal

        # Crear la sección izquierda con los botones
        self.left_section = QWidget()
        self.left_section_layout = QVBoxLayout(self.left_section)

        # Agregar la imagen del logo
        logo_label = QLabel()
        pixmap = QPixmap("src/images/logo_mysong.jpeg")  # Ruta a la imagen del logo
        pixmap = pixmap.scaledToWidth(150, Qt.SmoothTransformation)  # Ajustar el tamaño de la imagen
        rounded_pixmap = self.round_image(pixmap)  # Función para redondear la imagen
        logo_label.setPixmap(rounded_pixmap)
        logo_label.mousePressEvent = self.show_home  # Volver a la página de inicio al hacer clic en el logo
        self.left_section_layout.addWidget(logo_label, alignment=Qt.AlignTop | Qt.AlignHCenter)

        # Agregar espacio entre la imagen del logo y los botones
        self.left_section_layout.addSpacing(100)

        # Agregar los botones a la sección izquierda
        options = ["Buscar", "Subir canción", "Mis listas"]
        self.buttons = {}  # Diccionario para almacenar los botones
        for option in options:
            button = QPushButton(option)
            button.setStyleSheet("background-color:#1FDBDB;color:black; font-size:19px; padding: 5px 10px; border: 1px solid #1FDBDB; border-radius: 10px;")
            button.clicked.connect(self.change_page)  # Conectar la señal clicked al método change_page
            self.buttons[option] = button  # Agregar el botón al diccionario
            self.left_section_layout.addWidget(button, alignment=Qt.AlignCenter)

        # Agregar espacio entre los botones y el botón de "Ajustes"
        self.left_section_layout.addSpacing(100)

        # Agregar el botón de "Ajustes"
        settings_button = QPushButton("Ajustes")
        settings_button.setStyleSheet("background-color:#1FDBDB;color:black; font-size:16px; padding: 0px; border: 1px solid #1FDBDB; border-radius: 10px;")
        self.left_section_layout.addWidget(settings_button, alignment=Qt.AlignBottom)
        
        # Conectar la señal clicked del botón de ajustes a la función para mostrar la ventana de ajustes
        if self.username != None:
            settings_button.clicked.connect(self.show_settings_page)

        # Crear la sección derecha
        self.right_section = QWidget()
        self.right_section_layout = QVBoxLayout(self.right_section)

        # Crear el QStackedWidget para la sección superior derecha
        self.stacked_widget = QStackedWidget()
        
        # Crear las páginas para el QStackedWidget
        self.home_page = self.create_home_page()
        self.search_page = SearchSong()  # Página de búsqueda
        self.upload_page = SubirCancionPage(self.username)  # Página para subir canciones
        self.lists_page = ListasPage(self.username) # Página de listas
        self.settings_page = SettingsWindow(self.username)  # Página de ajustes

        # Agregar las páginas al QStackedWidget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.search_page)
        self.stacked_widget.addWidget(self.upload_page)
        self.stacked_widget.addWidget(self.lists_page)
        self.stacked_widget.addWidget(self.settings_page)

        # Agregar el QStackedWidget a la sección derecha
        self.right_section_layout.addWidget(self.stacked_widget)

        # Sección inferior de la sección derecha (para la barra de progreso y botones de control)
        self.bottom_section = QWidget()
        self.bottom_section_layout = QVBoxLayout(self.bottom_section)

        # Barra de progreso (QProgressBar)
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("QProgressBar {border: 2px solid grey; border-radius: 5px; background-color: white;}"
                                        "QProgressBar::chunk {background-color: blue;}")  # Cambia el color de la barra
        self.progress_bar.setRange(0, 100)

        

        self.bottom_section_layout.addWidget(self.progress_bar)

        # Botones de control de reproducción
        control_button_layout = QHBoxLayout()

        self.pause_button = QPushButton()
        self.pause_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        
            # Control de volumen
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)  # Valor inicial de volumen
        self.volume_slider.setToolTip("Control de Volumen")
        

        control_button_layout.addWidget(self.pause_button)
        control_button_layout.addWidget(self.play_button)
        control_button_layout.addWidget(self.stop_button)
        control_button_layout.addWidget(self.volume_slider)

        self.bottom_section_layout.addLayout(control_button_layout)

        # Establecer el tamaño mínimo y máximo de la sección inferior
        self.bottom_section.setMinimumHeight(80)
        self.bottom_section.setMaximumHeight(80)

        # Agregar la sección inferior a la sección derecha
        self.right_section_layout.addWidget(self.bottom_section)

        # Agregar una barra separadora entre las secciones
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)

        # Agregar las secciones al layout principal
        self.layout.addWidget(self.left_section)
        self.layout.addWidget(separator)
        self.layout.addWidget(self.right_section)

        # Establecer el ancho fijo de la sección izquierda utilizando CSS
        self.left_section.setStyleSheet("min-width: 200px; max-width: 200px;")

        
        # Conectar la señal positionChanged del reproductor al método actualizar_barra_progreso de la clase Menu
        self.reproductor.progress_changed.connect(self.reproductor.actualizar_barra_progreso)

        self.reproductor.progress_changed.connect(self.actualizar_barra_progreso_ui)

        self.volume_slider.valueChanged.connect(self.reproductor.set_volume)

        # Conectar la señal clicked de los botones de control de reproducción a los métodos correspondientes del reproductor
        self.pause_button.clicked.connect(self.reproductor.pausar)
        self.play_button.clicked.connect(self.reproductor.continuar)
        self.stop_button.clicked.connect(self.reproductor.detener)

    # Método para actualizar la barra de progreso en la interfaz de usuario
    def actualizar_barra_progreso_ui(self, position):
        
        self.progress_bar.setValue(position)
        print("actualizant barra UI")


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

        # Sección superior de la sección derecha
        self.top_section = QWidget()
        self.top_section.setStyleSheet("background-color: #1FDBDB; border 1px solid #1FDBDB; border-radius:15px;")  # Color de fondo personalizado
        self.top_section_layout = QHBoxLayout(self.top_section)

        # Función para manejar los clics en los bloques de la sección superior
        def handle_block_click(title):
            print(f"Se hizo clic en el bloque: {title}")

        # Bloque de "Me gusta"
        me_gusta_button = QPushButton("Me gusta")
        me_gusta_button.setStyleSheet("background-color: #3773DB; color: white; font-size: 16px; padding: 300px 40px; border: none; border-radius: 10px;")
        me_gusta_button.clicked.connect(lambda: handle_block_click("Me gusta"))
        self.top_section_layout.addWidget(me_gusta_button)

        # Bloque de "Recomendaciones"
        recomendaciones_button = QPushButton("Recomendaciones")
        recomendaciones_button.setStyleSheet("background-color: #3773DB; color: white; font-size: 16px; padding: 300px 40px; border: none; border-radius: 10px;")
        recomendaciones_button.clicked.connect(lambda: handle_block_click("Recomendaciones"))
        self.top_section_layout.addWidget(recomendaciones_button)

        # Bloque de "Más Escuchadas"
        mas_escuchadas_button = QPushButton("Más Escuchadas")
        mas_escuchadas_button.setStyleSheet("background-color: #3773DB; color: white; font-size: 16px; padding: 300px 40px; border: none; border-radius: 10px;")
        mas_escuchadas_button.clicked.connect(lambda: handle_block_click("Más Escuchadas"))
        self.top_section_layout.addWidget(mas_escuchadas_button)

        # Agregar la sección superior a la página de inicio
        layout.addWidget(self.top_section)

        return home_widget

    def round_image(self, pixmap):
        # Función para redondear la imagen
        radius = 75  # Radio del círculo, la mitad del ancho deseado de la imagen
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


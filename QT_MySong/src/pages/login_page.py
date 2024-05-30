import sys
import os




# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from models.user import User
from ApiServices.userService import UserService
from pages.menu import Menu
import re


class Validator:
    @staticmethod
    def validate_email(email):
        # Expresión regular para validar el formato del correo electrónico
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    @staticmethod
    def validate_password(password):
        # Expresión regular para validar la contraseña
        # Al menos 8 caracteres, 1 número, 1 mayúscula
        password_regex = r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$'
        return re.match(password_regex, password) is not None
    

class LoginForm(QWidget):

    def __init__(self):
        super().__init__()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.login_button = QPushButton("Iniciar sesión")

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.username_input.setPlaceholderText("Nombre de usuario")
        self.password_input.setPlaceholderText("Contraseña")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>INICIAR SESIÓN</h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addStretch()

        self.login_button.clicked.connect(self.login)
    
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not all([username, password]):
            QMessageBox.warning(self, "Inicio de sesión", "Por favor, complete todos los campos.")
            return

        # Llamada a la función para iniciar sesión en el servicio API
        success, message = UserService.login_user(username, password)

        if success:
            QMessageBox.information(self, "Inicio de sesión", message)
            window=LoginRegister()
            window.close()
            self.main_window = Menu(username)
            #self.principal=LoginRegister()
            
            # Abrir la ventana principal (la de menú)
            self.main_window.show()
            
        else:
            QMessageBox.warning(self, "Inicio de sesión", message)



class RegisterForm(QWidget):
    def __init__(self):
        super().__init__()

        self.username_input = QLineEdit()
        self.email_input = QLineEdit()
        self.password_input = QLineEdit()
        self.register_button = QPushButton("Registrarse")
        self.check_username_button = QPushButton("Comprobar nombre")
        self.instructions_button = QPushButton("Instrucciones para registrarse")

        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.username_input.setPlaceholderText("Nombre de usuario")
        self.email_input.setPlaceholderText("Correo electrónico")
        self.password_input.setPlaceholderText("Contraseña")

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h2>REGISTRARSE</h2>"), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.check_username_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.instructions_button)
        layout.addStretch()

        self.register_button.clicked.connect(self.register)
        self.check_username_button.clicked.connect(self.check_username)
        self.instructions_button.clicked.connect(self.show_registration_instructions)

    def clear_fields(self):
        self.username_input.clear()
        self.email_input.clear()
        self.password_input.clear()

    def register(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        tipo_usuario = "usuario"

        if not all([username, email, password]):
            QMessageBox.warning(self, "Registro de usuario", "Por favor, complete todos los campos.")
            return

        if not Validator.validate_email(email):
            QMessageBox.warning(self, "Registro de usuario", "El correo electrónico no tiene un formato válido.")
            return

        if not Validator.validate_password(password):
            QMessageBox.warning(self, "Registro de usuario", "La contraseña no cumple con los requisitos.")
            return

        # Verificar disponibilidad del nombre de usuario
        if not UserService.check_username_availability(username):
            QMessageBox.warning(self, "Registro de usuario", "El nombre de usuario ya está en uso. Por favor, elija otro.")
            return

        new_user = User(username, email, password, tipo_usuario)
        success, message = UserService.register_user(new_user)
        if success:
            self.clear_fields()
            QMessageBox.information(self, "Registro de usuario", message)
            QMessageBox.information(self, "Inicio de sesión", "Por favor, inicie sesión.")
        else:
            QMessageBox.warning(self, "Registro de usuario", message)

    def check_username(self):
        username = self.username_input.text()
        if not username:
            QMessageBox.warning(self, "Comprobar nombre de usuario", "Por favor, ingrese un nombre de usuario.")
            return

        if UserService.check_username_availability(username):
            QMessageBox.information(self, "Comprobar nombre de usuario", "El nombre de usuario está disponible.")
        else:
            QMessageBox.warning(self, "Comprobar nombre de usuario", "El nombre de usuario ya está en uso. Por favor, elija otro.")

    def show_registration_instructions(self):
        instructions = (
            "Instrucciones para registrarse correctamente:\n"
            "1. El nombre de usuario debe ser único.\n"
            "2. El correo electrónico debe tener un formato válido.\n"
            "3. La contraseña debe tener al menos 8 caracteres, incluyendo al menos una mayúscula y un número."
        )
        QMessageBox.information(self, "Instrucciones para registrarse", instructions)

class LoginRegister(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("loginForm")  # Establece el nombre del objeto para aplicar estilos
        # Aplica el estilo CSS al widget
        with open("src/styles/login_page.css", "r") as file:
            self.setStyleSheet(file.read())
        self.setWindowTitle("MySong - INICIA SESION / REGISTRATE")
        self.setGeometry(0, 0, 800, 600)
  

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)  

        self.top_section = QWidget()
        self.bottom_section = QWidget()

        #self.top_section.setStyleSheet("background-color: #1FDBDB;")  
        #self.bottom_section.setStyleSheet("background-color: #3773DB;")  

        self.layout.addWidget(self.top_section, 2.5)  
        self.layout.addWidget(self.bottom_section, 7.5)  

        self.create_top_section()
        self.create_bottom_section()

    def create_top_section(self):
        my_song_label = QLabel("MySong")
        my_song_label_slogan = QLabel("¡Música y más!")

        my_song_label.setStyleSheet("font-size: 70px; color: black;") 
        my_song_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        my_song_label_slogan.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        my_song_label_slogan.setStyleSheet("font-size: 30px; color: black;") 

        layout_top = QVBoxLayout(self.top_section) 
        layout_top.addWidget(my_song_label) 
        layout_top.addWidget(my_song_label_slogan)

    def create_bottom_section(self):
        login_form = LoginForm()
        register_form = RegisterForm()

        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine)
        separator_line.setFrameShadow(QFrame.Sunken)

        layout_bottom = QHBoxLayout(self.bottom_section)
        layout_bottom.addWidget(login_form, 1)  
        layout_bottom.addWidget(separator_line)
        layout_bottom.addWidget(register_form, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginRegister()
    window.show()
    sys.exit(app.exec())

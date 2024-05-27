import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ApiServices.userService import UserService

class SettingsWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle("MySong - AJUSTES")
        self.setObjectName("settingsWindow")
        # Aplica el estilo CSS al widget
        with open("src//styles/setting_page.css", "r") as file:
            self.setStyleSheet(file.read())
        
        self.name_label = QLabel("Nombre")
        self.name_label.setObjectName("nameLineEdit")
        self.name_value_label = QLabel(self.username if self.username != "" else "Invitado")
        self.name_value_label.setObjectName("nameLabel")
        self.change_name_button = QPushButton("Cambiar nombre")
        self.change_name_button.clicked.connect(self.change_name)
        self.logout_button=QPushButton("Cerrar Aplicacion")
        self.logout_button.clicked.connect(self.logout)
        self.delete_account_button=QPushButton("Eliminar cuenta")
        self.delete_account_button.clicked.connect(self.delete_account)
        self.make_public_checkbox = QCheckBox("Hacer todas las listas públicas")
        self.change_name_button.setObjectName("changeNameButton")
        self.make_public_checkbox.setObjectName("makePublicCheckbox")
        self.logout_button.setObjectName("logoutButton")
        self.delete_account_button.setObjectName("deleteAccountButton")

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_value_label)
        
        layout.addWidget(self.change_name_button)
        layout.addWidget(self.logout_button)
        layout.addWidget(self.delete_account_button)
        layout.addWidget(self.make_public_checkbox)
        layout.addStretch()

        self.setLayout(layout)
        
    def logout(self):
        QCoreApplication.quit()
        
    def change_name(self):
        if self.username == "":
            QMessageBox.warning(self, "Error", "No hay ningún usuario logueado.")
            return

        new_name, ok = QInputDialog.getText(self, "Cambiar nombre", "Nuevo nombre:")
        if ok and new_name:
            if new_name == self.username:
                QMessageBox.warning(self, "Error", "El nuevo nombre es igual al nombre actual.")
                return

            # Verificar la disponibilidad del nuevo nombre de usuario en el backend
            is_available = UserService.check_username_availability(new_name)
            if is_available:  # Verifica si el nombre de usuario está disponible
                # Actualizar el nombre de usuario en la base de datos
                success, message = UserService.update_user_name(self.username, new_name)
                if success:
                    QMessageBox.information(self, "Actualización de nombre", message)
                    # Actualizar el nombre en la interfaz de usuario
                    self.name_value_label.setText(new_name)
                else:
                    QMessageBox.warning(self, "Error", message)
            else:
                QMessageBox.warning(self, "Error", "El nuevo nombre de usuario no está disponible.")
                
    def delete_account(self):
        if self.username == "":
            QMessageBox.warning(self, "Error", "No hay ningún usuario logueado.")
            return
        
        confirm = QMessageBox.question(self, "Eliminar cuenta", "¿Estás seguro de que deseas eliminar tu cuenta?",
                                    QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            success, message = UserService.delete_user(self.username)
            if success:
                QMessageBox.information(self, "Eliminación de cuenta", message)
                QCoreApplication.quit()  # Salir de la aplicación después de eliminar la cuenta
            else:
                QMessageBox.warning(self, "Error", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    username = "Invitado"  
    window = SettingsWindow(username)
    window.show()
    sys.exit(app.exec())

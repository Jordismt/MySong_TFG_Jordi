
import requests
from models.user import User

class UserService:
    BASE_URL = 'http://localhost:8181/usuarios'

    @staticmethod
    def register_user(user):
        if not all([user.nombre, user.correoElectronico, user.contraseña]):
            return False, "Por favor, complete todos los campos."

        url = UserService.BASE_URL
        data = {
            "nombre": user.nombre,
            "correoElectronico": user.correoElectronico,
            "contraseña": user.contraseña,
            "tipoUsuario": user.tipoUsuario
        }

        print("Datos del usuario:", data)
        try:
            response = requests.post(url, json=data)
            print("Respuesta del servidor:", response.text)
            if response.status_code == 201:
                return True, "Usuario registrado exitosamente"
            else:
                return False, "Error al registrar usuario. Inténtelo de nuevo más tarde."
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"



    @staticmethod
    def login_user(username, password):
        # Verificar si los campos de nombre de usuario y contraseña están completos
        if not all([username, password]):
            return False, "Por favor, complete todos los campos."

        # Crear el objeto de datos para enviar al servidor
        data = {
            "username": username,
            "password": password
        }

        url = f"{UserService.BASE_URL}/login"  # Endpoint para iniciar sesión

        try:
            # Realizar la solicitud POST para iniciar sesión
            response = requests.post(url, data=data)

            if response.status_code == 200:
                return True, "Inicio de sesión exitoso"
            elif response.status_code == 401:
                return False, "Usuario o contraseña incorrectos"
            else:
                return False, f"Error al intentar iniciar sesión. Código de estado: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"


    @staticmethod
    def update_user_name(username, new_name):
        url = f"{UserService.BASE_URL}/nombre/{username}"  # URL con el nombre de usuario como parte de la ruta
        data = {"nombre": new_name}

        try:
            response = requests.put(url, json=data)

            if response.status_code == 200:
                return True, "Nombre de usuario actualizado exitosamente"
            elif response.status_code == 404:
                return False, "Usuario no encontrado"
            else:
                return False, f"Error al intentar actualizar el nombre de usuario. Código de estado: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"
        
    @staticmethod
    def check_username_availability(username):
        url = f"{UserService.BASE_URL}/check-username"
        params = {"username": username}

        try:
            response = requests.get(url, params=params)
            print("Contenido de la respuesta:", response.text)
            if response.status_code == 200:
                return response.json()
            else:
                return False  # Devuelve False si la solicitud no es exitosa
        except requests.exceptions.RequestException:
            return False  # Maneja cualquier error de conexión retornando False
        
    @staticmethod
    def delete_user(nombre_usuario):
        url = f"{UserService.BASE_URL}/{nombre_usuario}"
        try:
            response = requests.delete(url)
            if response.status_code == 204:
                return True, "Usuario eliminado exitosamente"
            elif response.status_code == 404:
                return False, "Usuario no encontrado"
            else:
                return False, "Error al eliminar usuario"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"
        

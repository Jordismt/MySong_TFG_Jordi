import requests
class ListaReproduccionService:
    BASE_URL = 'http://localhost:8181/listas-reproduccion'



    @staticmethod
    def crear_lista_reproduccion(nombre_usuario, lista_reproduccion):
        # Obtener el ID del usuario
        id_usuario = ListaReproduccionService.obtener_id_usuario_por_nombre(nombre_usuario)
        print(id_usuario)
        if id_usuario is None:
            return False, "No se pudo obtener el ID del usuario"

        url = f"{ListaReproduccionService.BASE_URL}/{nombre_usuario}"
        data = {
            "idUsuario": id_usuario,
            "nombre": lista_reproduccion.nombre,
            "canciones": [cancion.to_dict() for cancion in lista_reproduccion.canciones]
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                return True, "Lista de reproducción creada exitosamente"
            else:
                error_message = f"Error al crear lista de reproducción. Inténtelo de nuevo más tarde. \n Detalles: {response.status_code}"
                return False, error_message

        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"
        


    BASE_URL_2 = 'http://localhost:8181/usuarios'
    @staticmethod
    def obtener_id_usuario_por_nombre(nombre_usuario):
        url = f"{ListaReproduccionService.BASE_URL_2}/by-username/{nombre_usuario}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json().get('id')
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {str(e)}")
            return None
        

    @staticmethod
    def obtener_listas_usuario(username):
        url = f"http://localhost:8181/listas-reproduccion/listas/{username}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {str(e)}")
            return None
        

import requests

class CancionesService:
    BASE_URL = 'http://localhost:8181/canciones'

    @staticmethod
    def crear_cancion(cancion):
        if not all([cancion.usuario, cancion.nombre, cancion.artista, cancion.album, cancion.archivo_mp3, cancion.lista_id]):
            return False, "Por favor, complete todos los campos."

        url = f"{CancionesService.BASE_URL}/subir-cancion"
        
        # Crear un objeto FormData para enviar los datos
        form_data = {
            'nombre': cancion.nombre,
            'artista': cancion.artista,
            'album': cancion.album,
            'usuario': cancion.usuario,
            'lista_id': str(cancion.lista_id)
        }
        
        # Agregar el archivo MP3
        files = {
            'file': (cancion.archivo_mp3, open(cancion.archivo_mp3, 'rb'), 'audio/mpeg')
        }

        try:
            response = requests.post(url, data=form_data, files=files)
            if response.status_code == 201:
                return True, "Canción creada exitosamente"
            else:
                return False, f"Error al crear canción: {response.content.decode()}"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"

    @staticmethod
    def obtener_canciones():
        url = CancionesService.BASE_URL
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return False, "Error al obtener canciones"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"

    @staticmethod
    def obtener_cancion_por_id(cancion_id):
        url = f"{CancionesService.BASE_URL}/{cancion_id}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return False, "Error al obtener canción por ID"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"

    @staticmethod
    def actualizar_cancion(cancion_id, cancion):
        url = f"{CancionesService.BASE_URL}/{cancion_id}"
        data = {
            "nombre": cancion.nombre,
            "artista": cancion.artista,
            "album": cancion.album,
            "archivoMp3": cancion.archivo_mp3,
            "likes": cancion.likes
        }

        try:
            response = requests.put(url, json=data)
            if response.status_code == 200:
                return True, "Canción actualizada exitosamente"
            else:
                return False, "Error al actualizar canción"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"

    @staticmethod
    def eliminar_cancion(cancion_id):
        url = f"{CancionesService.BASE_URL}/{cancion_id}"
        try:
            response = requests.delete(url)
            if response.status_code == 204:
                return True, "Canción eliminada exitosamente"
            else:
                return False, "Error al eliminar canción"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"

    @staticmethod
    def dar_like_a_cancion(cancion_id):
        url = f"{CancionesService.BASE_URL}/{cancion_id}/like"
        try:
            response = requests.post(url)
            if response.status_code == 200:
                return True, "Like dado exitosamente"
            else:
                return False, "Error al dar like a la canción"
        except requests.exceptions.RequestException as e:
            return False, f"Error de conexión: {str(e)}"

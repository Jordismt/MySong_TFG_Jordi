# models/cancion.py
class Cancion:
    def __init__(self, nombre, artista, album, archivo_mp3, usuario, lista_id, likes=0):
        self.nombre = nombre
        self.artista = artista
        self.album = album
        self.archivo_mp3 = archivo_mp3
        self.usuario = usuario
        self.lista_id = lista_id
        self.likes = likes

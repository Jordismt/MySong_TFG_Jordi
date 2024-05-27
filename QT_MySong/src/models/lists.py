class ListaReproduccion:
    def __init__(self, nombre_usuario, nombre, canciones=None):
        self.nombre_usuario = nombre_usuario
        self.nombre = nombre
        self.canciones = canciones if canciones else []

    def to_dict(self):
        return {
            "nombre_usuario": self.nombre_usuario,
            "nombre": self.nombre,
            "canciones": [cancion.to_dict() for cancion in self.canciones]
        }

class User:
    def __init__(self, nombre, correoElectronico, contraseña, tipoUsuario="usuario"):
        self.nombre = nombre
        self.correoElectronico = correoElectronico
        self.contraseña = contraseña
        self.tipoUsuario = tipoUsuario

    @staticmethod
    def fromJson(json_data):
        nombre = json_data.get("nombre")
        if nombre is None:
            raise ValueError("El campo 'nombre' es obligatorio en el JSON")
        
        correoElectronico = json_data.get("correoElectronico")
        if correoElectronico is None:
            raise ValueError("El campo 'correoElectronico' es obligatorio en el JSON")

        contraseña = json_data.get("contraseña")
        if contraseña is None:
            raise ValueError("El campo 'contraseña' es obligatorio en el JSON")

        tipoUsuario = json_data.get("tipoUsuario", "usuario")
        
        return User(nombre, correoElectronico, contraseña, tipoUsuario)

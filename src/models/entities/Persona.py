
class Persona():
    def __init__(self, dni, nombre, apellido, contrasenia, usuario, mail=None, rol = None):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.contrasenia = contrasenia
        self.usuario = usuario
        self.mail = mail
        self.rol = rol

    def to_JSON(self):
        return {
            'dni': self.dni,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'contrasenia': self.contrasenia,
            'usuario': self.usuario,
            'mail': self.mail,
            'rol': self.rol
        }
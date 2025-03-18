
class Persona():
    def __init__(self, dni, nombre, apellido, usuario, mail=None, rol = "TUTOR", contrasenia=None):
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
            'usuario': self.usuario,
            'mail': self.mail,
            'rol': self.rol
        }
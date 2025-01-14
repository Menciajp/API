class Alumno():
    def __init__(self, nombre, apellido, dni, fechIngreso, fechNac,estado = None,idAlumno = None):
        self.idAlumno = idAlumno
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.fechIngreso = fechIngreso
        self.fechNac = fechNac
        self.estado = estado

    def to_JSON(self):
        return {
            'idAlumno': self.idAlumno,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'fechIngreso': self.fechIngreso,
            'fechNac': self.fechNac,
            'estado': self.estado
        }

   
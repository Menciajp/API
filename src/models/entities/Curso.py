class Curso():
    def __init__(self, nombre, anio):
        self.nome = nombre
        self.anio = anio

    def to_JSON(self):
        return {
            'nombre': self.nome,
            'anio': self.anio
        }
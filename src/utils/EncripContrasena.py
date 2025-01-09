import hashlib

class EncripContrasena:

    # Función para generar un hash de una contraseña
    @staticmethod
    def generar_hash(contrasena):
        if not contrasena:
            raise ValueError("La contraseña no puede estar vacía.")
        
        # Generar el hash
        hash_obj = hashlib.sha256(contrasena.encode())  # Codifica la contraseña a bytes
        
        return hash_obj.hexdigest()

    # Función para comparar una contraseña con un hash
    @staticmethod
    def comparar_contrasena(contrasena, hash_contrasena):
        if not contrasena:
            raise ValueError("La contraseña no puede estar vacía.")
        if not hash_contrasena:
            raise ValueError("El hash de la contraseña no puede estar vacío.")
        
        # Generar el hash de la contraseña
        hash_entrada = EncripContrasena.generar_hash(contrasena)
        
        # Comparar los hashes
        return hash_entrada == hash_contrasena

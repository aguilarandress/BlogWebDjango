import re


# Validar datos de registro
def validarDatosDeRegistro(usuario):
    """Valida los datos del formulario

    Entradas:
        usuario: Es un diccionario
    Precondiciones:
        usuario contiene los datos del formulario de registro
    Salidas:
        Retorna un diccionario que contiene si los datos están válidos
        y los mensajes de error
    Proceso:
        1. Se crea una variable resultado
        2. Se revisa si los están completos
        3. Se revisa el formato del correo
        4. Se comparan las contraseñas
        5. Se retorna el resultado
    """
    resultado = {"esValido": True, "mensajes": []}
    # Revisar que los datos estén completos
    for dato in usuario:
        if not usuario[dato]:
            resultado["esValido"] = False
            resultado["mensajes"].append("Por favor complete el formulario completamente")
            return resultado

    # Revisar el formato del correo
    if not validarCorreos(usuario["email"]):
        resultado["mensajes"].append("El formato del correo no es correcto")
    # Comparar contraseñas
    if not (usuario["contraseña"] == usuario["contraseña2"]):
        resultado["mensajes"].append("Ambas contraseñas deben ser iguales")

    if len(resultado["mensajes"]) > 0:
        resultado["esValido"] = False
    return resultado


# Validar formato de correo
def validarCorreos(stringEntrada):
    """Valida si el string tiene un formato de correo o no

    Entradas:
        stringEntrada: Es un string / hilera
    Precondiciones:
        No hay
    Salidas:
        Retorna True si el correo es correcto, False de lo contrario
    Proceso:
        1. Crear el patrón deseado y compilarlo
        2. Revisar con un condicional si stringEntrada es válido
        3. En caso de ser cierto se retorna True, el caso contrario False
    """
    patron = re.compile(r"\w+@((\w)+\.)+\w+")
    if patron.search(stringEntrada):
        return True
    return False
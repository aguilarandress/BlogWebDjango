import re


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




import re

REGISTERED_IDS = set()
REGISTERED_EMAILS = set()


def validate_id(id):
    if not isinstance(id, str) or not id.strip():
        return False, "El ID no puede estar vacio."
    if id in REGISTERED_IDS:
        return False, f"El ID '{id}' ya existe. No se puede duplicar"
    return True, ""


def validate_name(name):
    if not isinstance(name, str) or not name.strip():
        return False, "El nombre no puede estar vacio."
    if not re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+", name.strip()):
        return False, "El nombre solo puede contener letras y espacios."
    return True, ""


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not isinstance(email, str) or not email.strip():
        return False, "El correo no puede estar vacio."
    if not re.match(pattern, email.strip()):
        return False, f"El correo '{email}' no es valido"
    if email.strip().lower() in REGISTERED_EMAILS:
        return False, f"El correo '{email}' ya esta registrado."
    return True, ""


def validate_age(age):
    if not isinstance(age, int):
        return False, "La edad solo debe contener numeros."
    if not (0 <= age <= 120):
        return False, f"La edad '{age}' debe ser entre 0 a 120."
    return True, ""


def validate_status(status):
    options = {"soltero", "casado", "viudo", "divorciado"}
    if status.strip().lower() not in options:
        return False, f"Estatus invalido. Las opciones son: {', '.join(options)}"
    return True, ""
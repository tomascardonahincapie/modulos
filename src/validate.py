import re
from typing import Tuple

REGISTERED_IDS = set[str]()
REGISTERED_EMAILS = set[str]()


def validate_id(id: str) -> Tuple[bool, str]:
    """
    Validate the ID for a new record.

    Args:
        id (str): The ID to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not isinstance(id, str) or not id.strip():
        return False, "El ID no puede estar vacío."
    if id in REGISTERED_IDS:
        return False, f"El ID '{id}' ya existe. No se puede duplicar"
    return True, ""


def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate the name for a record.

    Args:
        name (str): The name to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not isinstance(name, str) or not name.strip():
        return False, "El nombre no puede estar vacío."
    if not re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+", name.strip()):
        return False, "El nombre solo puede contener letras y espacios."
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate the email for a record.

    Args:
        email (str): The email to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not isinstance(email, str) or not email.strip():
        return False, "El correo no puede estar vacío."
    if not re.match(pattern, email.strip()):
        return False, f"El correo '{email}' no es válido"
    if email.strip().lower() in REGISTERED_EMAILS:
        return False, f"El correo '{email}' ya está registrado."
    return True, ""


def validate_age(age: int) -> Tuple[bool, str]:
    """
    Validate the age for a record.

    Args:
        age (int): The age to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not isinstance(age, int):
        return False, "La edad solo debe contener números."
    if not (0 <= age <= 120):
        return False, f"La edad '{age}' debe ser entre 0 a 120."
    return True, ""


def validate_status(status: str) -> Tuple[bool, str]:
    """
    Validate the marital status for a record.

    Args:
        status (str): The status to validate.

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    options = {"soltero", "casado", "viudo", "divorciado"}
    if status.strip().lower() not in options:
        return False, f"Estado inválido. Las opciones son: {', '.join(sorted(options))}"
    return True, ""
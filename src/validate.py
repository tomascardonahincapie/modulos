import re

REGISTERED_IDS = set()
REGISTERED_EMAILS = set()


def validate_id(id):
    if not isinstance(id, str) or not id.strip():
        return False, "ID cannot be empty."
    if id in REGISTERED_IDS:
        return False, f"ID '{id}' already exists. Duplicates are not allowed."
    return True, ""


def validate_name(name):
    if not isinstance(name, str) or not name.strip():
        return False, "Name cannot be empty."
    if not re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+", name.strip()):
        return False, "Name can only contain letters and spaces."
    return True, ""


def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not isinstance(email, str) or not email.strip():
        return False, "Email cannot be empty."
    if not re.match(pattern, email.strip()):
        return False, f"Email '{email}' is not valid."
    if email.strip().lower() in REGISTERED_EMAILS:
        return False, f"Email '{email}' is already registered."
    return True, ""


def validate_age(age):
    if not isinstance(age, int):
        return False, "Age must be an integer."
    if not (0 <= age <= 120):
        return False, f"Age '{age}' must be between 0 and 120."
    return True, ""


def validate_status(status):
    options = {"single", "married", "widowed", "divorced"}
    if status.strip().lower() not in options:
        return False, f"Invalid status. Options: {', '.join(options)}"
    return True, ""
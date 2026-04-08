from validate import (
    validate_id,
    validate_name,
    validate_email,
    validate_age,
    validate_status,
    REGISTERED_IDS,
    REGISTERED_EMAILS,
)
from file import load_data, save_data


def _load_state():
    registers = load_data()
    for record in registers:
        REGISTERED_IDS.add(record["id"])
        REGISTERED_EMAILS.add(record["email"])
    return registers


def _save_state():
    save_data(_registers)


def _find_record_by_id(record_id):
    return next(filter(lambda record: record["id"] == record_id, _registers), None)


_registers = _load_state()


def new_register(id, name, email, age, status):
    errors = []

    ok, msg = validate_id(id)
    if not ok:
        errors.append(msg)

    ok, msg = validate_name(name)
    if not ok:
        errors.append(msg)

    ok, msg = validate_email(email)
    if not ok:
        errors.append(msg)

    ok, msg = validate_age(age)
    if not ok:
        errors.append(msg)

    ok, msg = validate_status(status)
    if not ok:
        errors.append(msg)

    if errors:
        raise ValueError("Errores de validacion:\n  - " + "\n  - ".join(errors))

    record = {
        "id": id.strip(),
        "name": name.strip(),
        "email": email.strip().lower(),
        "age": age,
        "status": status.strip().lower(),
    }

    _registers.append(record)
    REGISTERED_IDS.add(record["id"])
    REGISTERED_EMAILS.add(record["email"])
    _save_state()

    return record


def list_records(order_by="name"):
    if order_by not in {"id", "name", "email", "age", "status"}:
        raise ValueError("order_by debe ser uno de estos: id, name, email, age, status.")
    return sorted(_registers, key=lambda record: record[order_by])


def search_record(**filters):
    if not filters:
        raise ValueError("search_record necesita por lo menos un filtro.")

    invalid_fields = set(filters) - {"id", "name", "email", "age", "status"}
    if invalid_fields:
        raise ValueError(f"Campos de busca invalidos: {', '.join(sorted(invalid_fields))}.")

    normalized = {}
    for key, value in filters.items():
        if key in {"id", "name", "email", "status"}:
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"El valor de busqueda para '{key}' no puede estar vacio.")
            normalized[key] = value.strip().lower()
        else:
            normalized[key] = value

    return [
        record
        for record in _registers
        if all(
            (str(record[field]).lower() == normalized[field])
            if isinstance(record[field], str)
            else record[field] == normalized[field]
            for field in normalized
        )
    ]


def update_record(id, **changes):
    if not isinstance(id, str) or not id.strip():
        raise ValueError("El registro con el ID no puede estar vacio al actualizar.")

    record = _find_record_by_id(id)
    if record is None:
        raise ValueError(f"El Registro con el ID '{id}' no existe.")
    if "id" in changes:
        raise ValueError("Actualizar el ID no esta permitido.")

    updated = record.copy()
    errors = []

    for field, value in changes.items():
        if field == "name":
            ok, msg = validate_name(value)
            if not ok:
                errors.append(msg)
            else:
                updated["name"] = value.strip()
        elif field == "email":
            normalized_email = value.strip().lower()
            if normalized_email != record["email"]:
                REGISTERED_EMAILS.discard(record["email"])
                ok, msg = validate_email(value)
                if not ok:
                    REGISTERED_EMAILS.add(record["email"])
                    errors.append(msg)
                else:
                    updated["email"] = normalized_email
                    REGISTERED_EMAILS.add(normalized_email)
            else:
                updated["email"] = normalized_email
        elif field == "age":
            ok, msg = validate_age(value)
            if not ok:
                errors.append(msg)
            else:
                updated["age"] = value
        elif field == "status":
            ok, msg = validate_status(value)
            if not ok:
                errors.append(msg)
            else:
                updated["status"] = value.strip().lower()
        else:
            errors.append(f"El campo desconocido '{field}' no se puede actualizar.")

    if errors:
        raise ValueError("Actualizacion fallida:\n  - " + "\n  - ".join(errors))

    record.update(updated)
    _save_state()
    return record


def delete_record(id):
    if not isinstance(id, str) or not id.strip():
        raise ValueError("El ID no puede estar vacio")

    record = _find_record_by_id(id)
    if record is None:
        raise ValueError(f"Registro con ID '{id}' no existe")

    _registers.remove(record)
    REGISTERED_IDS.discard(record["id"])
    REGISTERED_EMAILS.discard(record["email"])
    _save_state()
    return record


class RegisterService:
    def __init__(self):
        self._registers = _registers
        self._ids = REGISTERED_IDS
        self._emails = REGISTERED_EMAILS

    def create_record(self, id, name, email, age, status):
        return new_register(id, name, email, age, status)

    def list_records(self):
        return list_records()
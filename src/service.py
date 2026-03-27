from validate import (
    validate_id,
    validate_name,
    validate_email,
    validate_age,
    validate_status,
    REGISTERED_IDS,
    REGISTERED_EMAILS,
)


class RegisterService:
    def __init__(self):
        self._registers = []
        self._ids = REGISTERED_IDS
        self._emails = REGISTERED_EMAILS

    def create_record(self, id, name, email, age, status):
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
            raise ValueError("Validation errors:\n  - " + "\n  - ".join(errors))

        record = {
            "id": id,
            "name": name.strip(),
            "email": email.strip().lower(),
            "age": age,
            "status": status.strip().lower(),
        }

        self._registers.append(record)
        self._ids.add(id)
        self._emails.add(email.strip().lower())

        return record

    def list_records(self):
        return list(self._registers)
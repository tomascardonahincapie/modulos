from typing import List, Dict, Any, Optional
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


class RecordService:
    """
    Service class for managing records.
    """

    def __init__(self) -> None:
        self._records: List[Dict[str, Any]] = load_data()
        for record in self._records:
            REGISTERED_IDS.add(record["id"])
            REGISTERED_EMAILS.add(record["email"])

    def _save_state(self) -> None:
        """Save the current records to file."""
        save_data(self._records)

    def _find_record_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Find a record by ID."""
        return next((r for r in self._records if r["id"] == record_id), None)

    def create_record(self, id: str, name: str, email: str, age: int, status: str) -> Dict[str, Any]:
        """
        Create a new record.

        Args:
            id (str): Unique ID.
            name (str): Name.
            email (str): Email.
            age (int): Age.
            status (str): Marital status.

        Returns:
            Dict[str, Any]: The created record.

        Raises:
            ValueError: If validation fails.
        """
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
            raise ValueError("Errores de validación:\n  - " + "\n  - ".join(errors))

        record = {
            "id": id.strip(),
            "name": name.strip(),
            "email": email.strip().lower(),
            "age": age,
            "status": status.strip().lower(),
        }

        self._records.append(record)
        REGISTERED_IDS.add(record["id"])
        REGISTERED_EMAILS.add(record["email"])
        self._save_state()

        return record

    def list_records(self, order_by: str = "name") -> List[Dict[str, Any]]:
        """
        List all records, optionally ordered.

        Args:
            order_by (str): Field to order by.

        Returns:
            List[Dict[str, Any]]: List of records.

        Raises:
            ValueError: If order_by is invalid.
        """
        if order_by not in {"id", "name", "email", "age", "status"}:
            raise ValueError("order_by debe ser uno de estos: id, name, email, age, status.")
        return sorted(self._records, key=lambda r: r[order_by])

    def search_record(self, **filters) -> List[Dict[str, Any]]:
        """
        Search records by filters.

        Args:
            **filters: Key-value pairs to filter by.

        Returns:
            List[Dict[str, Any]]: Matching records.

        Raises:
            ValueError: If filters are invalid.
        """
        if not filters:
            raise ValueError("search_record necesita por lo menos un filtro.")

        invalid_fields = set(filters) - {"id", "name", "email", "age", "status"}
        if invalid_fields:
            raise ValueError(f"Campos de búsqueda inválidos: {', '.join(sorted(invalid_fields))}.")

        normalized = {}
        for key, value in filters.items():
            if key in {"id", "name", "email", "status"}:
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"El valor de búsqueda para '{key}' no puede estar vacío.")
                normalized[key] = value.strip().lower()
            else:
                normalized[key] = value

        return [
            record
            for record in self._records
            if all(
                (str(record[field]).lower() == normalized[field])
                if isinstance(record[field], str)
                else record[field] == normalized[field]
                for field in normalized
            )
        ]

    def update_record(self, id: str, **changes) -> Dict[str, Any]:
        """
        Update a record.

        Args:
            id (str): ID of the record to update.
            **changes: Fields to update.

        Returns:
            Dict[str, Any]: The updated record.

        Raises:
            ValueError: If update fails.
        """
        if not isinstance(id, str) or not id.strip():
            raise ValueError("El ID no puede estar vacío al actualizar.")

        record = self._find_record_by_id(id)
        if record is None:
            raise ValueError(f"El registro con el ID '{id}' no existe.")
        if "id" in changes:
            raise ValueError("Actualizar el ID no está permitido.")

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
            raise ValueError("Actualización fallida:\n  - " + "\n  - ".join(errors))

        record.update(updated)
        self._save_state()
        return record

    def delete_record(self, id: str) -> Dict[str, Any]:
        """
        Delete a record.

        Args:
            id (str): ID of the record to delete.

        Returns:
            Dict[str, Any]: The deleted record.

        Raises:
            ValueError: If record not found.
        """
        if not isinstance(id, str) or not id.strip():
            raise ValueError("El ID no puede estar vacío")

        record = self._find_record_by_id(id)
        if record is None:
            raise ValueError(f"Registro con ID '{id}' no existe")

        self._records.remove(record)
        REGISTERED_IDS.discard(record["id"])
        REGISTERED_EMAILS.discard(record["email"])
        self._save_state()
        return record


# Global instance for backward compatibility
_service = RecordService()

# Backward compatibility functions
def new_register(id, name, email, age, status):
    return _service.create_record(id, name, email, age, status)

def list_records(order_by="name"):
    return _service.list_records(order_by)

def search_record(**filters):
    return _service.search_record(**filters)

def update_record(id, **changes):
    return _service.update_record(id, **changes)

def delete_record(id):
    return _service.delete_record(id)
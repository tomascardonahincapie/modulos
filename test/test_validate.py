import pytest
from src.validate import validate_id, validate_name, validate_email, validate_age, validate_status, REGISTERED_IDS, REGISTERED_EMAILS


class TestValidateId:
    def test_valid_id(self):
        REGISTERED_IDS.clear()
        assert validate_id("123") == (True, "")

    def test_empty_id(self):
        assert validate_id("") == (False, "El ID no puede estar vacío.")
        assert validate_id("   ") == (False, "El ID no puede estar vacío.")

    def test_duplicate_id(self):
        REGISTERED_IDS.clear()
        REGISTERED_IDS.add("123")
        assert validate_id("123") == (False, "El ID '123' ya existe. No se puede duplicar")


class TestValidateName:
    def test_valid_name(self):
        assert validate_name("Juan Pérez") == (True, "")
        assert validate_name("María José") == (True, "")

    def test_empty_name(self):
        assert validate_name("") == (False, "El nombre no puede estar vacío.")
        assert validate_name("   ") == (False, "El nombre no puede estar vacío.")

    def test_invalid_name(self):
        assert validate_name("Juan123") == (False, "El nombre solo puede contener letras y espacios.")
        assert validate_name("Juan@Pérez") == (False, "El nombre solo puede contener letras y espacios.")


class TestValidateEmail:
    def test_valid_email(self):
        REGISTERED_EMAILS.clear()
        assert validate_email("test@example.com") == (True, "")

    def test_empty_email(self):
        assert validate_email("") == (False, "El correo no puede estar vacío.")

    def test_invalid_email(self):
        assert validate_email("invalid") == (False, "El correo 'invalid' no es válido")
        assert validate_email("test@") == (False, "El correo 'test@' no es válido")

    def test_duplicate_email(self):
        REGISTERED_EMAILS.clear()
        REGISTERED_EMAILS.add("test@example.com")
        assert validate_email("test@example.com") == (False, "El correo 'test@example.com' ya está registrado.")


class TestValidateAge:
    def test_valid_age(self):
        assert validate_age(25) == (True, "")
        assert validate_age(0) == (True, "")
        assert validate_age(120) == (True, "")

    def test_invalid_age_type(self):
        assert validate_age("25") == (False, "La edad solo debe contener números.")

    def test_invalid_age_range(self):
        assert validate_age(-1) == (False, "La edad '-1' debe ser entre 0 a 120.")
        assert validate_age(121) == (False, "La edad '121' debe ser entre 0 a 120.")


class TestValidateStatus:
    def test_valid_status(self):
        assert validate_status("soltero") == (True, "")
        assert validate_status("casado") == (True, "")
        assert validate_status("viudo") == (True, "")
        assert validate_status("divorciado") == (True, "")

    def test_invalid_status(self):
        assert validate_status("single") == (False, "Estado inválido. Las opciones son: casado, divorciado, soltero, viudo")
        assert validate_status("") == (False, "Estado inválido. Las opciones son: casado, divorciado, soltero, viudo")

import pytest
import os
import tempfile
from src.service import RecordService
from src.validate import REGISTERED_IDS, REGISTERED_EMAILS


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_dir = os.path.join(tmpdir, "data")
        os.makedirs(data_dir)
        records_path = os.path.join(data_dir, "records.json")
        with open(records_path, "w") as f:
            f.write("[]")
        yield tmpdir


@pytest.fixture
def service(temp_data_dir):
    """Create a RecordService with temporary data."""
    # Mock the data path
    from src import file as file_module
    original_path = file_module.DATA_PATH
    file_module.DATA_PATH = os.path.join(temp_data_dir, "data", "records.json")
    # Clear global sets
    REGISTERED_IDS.clear()
    REGISTERED_EMAILS.clear()
    service = RecordService()
    yield service
    # Restore
    file_module.DATA_PATH = original_path


class TestRecordService:
    def test_create_record(self, service):
        record = service.create_record("1", "John Doe", "john@example.com", 30, "soltero")
        assert record["id"] == "1"
        assert record["name"] == "John Doe"
        assert record["email"] == "john@example.com"
        assert record["age"] == 30
        assert record["status"] == "soltero"

    def test_create_duplicate_id(self, service):
        service.create_record("1", "John Doe", "john@example.com", 30, "soltero")
        with pytest.raises(ValueError, match="El ID '1' ya existe"):
            service.create_record("1", "Jane Doe", "jane@example.com", 25, "casado")

    def test_create_duplicate_email(self, service):
        service.create_record("1", "John Doe", "john@example.com", 30, "soltero")
        with pytest.raises(ValueError, match="El correo 'john@example.com' ya está registrado"):
            service.create_record("2", "Jane Doe", "john@example.com", 25, "casado")

    def test_list_records(self, service):
        service.create_record("1", "John Doe", "john@example.com", 30, "soltero")
        service.create_record("2", "Jane Doe", "jane@example.com", 25, "casado")
        records = service.list_records()
        assert len(records) == 2
        assert records[0]["name"] == "Jane Doe"  # sorted by name
        assert records[1]["name"] == "John Doe"

    def test_search_record_by_id(self, service):
        service.create_record("1", "John Doe", "john@example.com", 30, "soltero")
        results = service.search_record(id="1")
        assert len(results) == 1
        assert results[0]["name"] == "John Doe"

    def test_search_record_by_name(self, service):
        service.create_record("1", "John Doe", "john@example.com", 30, "soltero")
        results = service.search_record(name="John Doe")
        assert len(results) == 1
        assert results[0]["id"] == "1"

    def test_update_record(self, service):
        service.create_record("1", "John Doe", "john@example.com", 30, "soltero")
        updated = service.update_record("1", name="John Smith", age=35)
        assert updated["name"] == "John Smith"
        assert updated["age"] == 35
        assert updated["email"] == "john@example.com"

    def test_update_nonexistent_record(self, service):
        with pytest.raises(ValueError, match="no existe"):
            service.update_record("999", name="Test")

    def test_delete_record(self, service):
        service.create_record("1", "John Doe", "john@example.com", 30, "soltero")
        deleted = service.delete_record("1")
        assert deleted["id"] == "1"
        assert len(service.list_records()) == 0

    def test_delete_nonexistent_record(self, service):
        with pytest.raises(ValueError, match="no existe"):
            service.delete_record("999")

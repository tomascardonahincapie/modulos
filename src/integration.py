
from typing import List, Dict, Any
from faker import Faker
from service import new_register


def generate_fake_records(count: int = 10, **kwargs) -> List[Dict[str, Any]]:
    """
    Generate fake records using the Faker library.

    Args:
        count (int): Number of records to generate (default 10).
        **kwargs: Additional options, such as 'locale' for Faker language.

    Returns:
        List[Dict[str, Any]]: List of generated records.
    """
    locale = kwargs.get('locale', 'es_ES')
    fake = Faker(locale)

    records = []
    for _ in range(count):
        record_data = {
            'id': fake.unique.uuid4()[:8].upper(),  # Unique short ID
            'name': fake.name(),
            'email': fake.email(),
            'age': fake.random_int(min=18, max=80),
            'status': fake.random_element(elements=['soltero', 'casado', 'viudo', 'divorciado'])
        }
        try:
            # Create the record using the existing function
            created_record = new_register(**record_data)
            records.append(created_record)
        except ValueError:
            # If error (e.g., duplicate ID), try with another ID
            continue

    return records

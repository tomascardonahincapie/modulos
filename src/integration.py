
from faker import Faker
from service import new_register

def generate_fake_records(count=10, **kwargs):
    """
    Genera registros falsos usando la librería Faker.

    Args:
        count (int): Número de registros a generar (por defecto 10).
        **kwargs: Opciones adicionales, como 'locale' para el idioma de Faker.

    Returns:
        list: Lista de registros generados.
    """
    locale = kwargs.get('locale', 'es_ES')
    fake = Faker(locale)

    records = []
    for _ in range(count):
        record_data = {
            'id': fake.unique.uuid4()[:8].upper(),  # ID único corto
            'name': fake.name(),
            'email': fake.email(),
            'age': fake.random_int(min=18, max=80),
            'status': fake.random_element(elements=['soltero', 'casado', 'viudo', 'divorciado'])
        }
        try:
            # Crear el registro usando la función existente
            created_record = new_register(**record_data)
            records.append(created_record)
        except ValueError as e:
            # Si hay error (ej. ID duplicado), intentar con otro ID
            continue

    return records

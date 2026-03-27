from service import RegisterService


def print_record(r, i):
    print(
        f"[{i}] ID: {r['id']:<6} | "
        f"Name: {r['name']:<20} | "
        f"Email: {r['email']:<25} | "
        f"Age: {r['age']:<4} | "
        f"Status: {r['status']}"
    )


def try_create(service, **kwargs):
    try:
        service.create_record(**kwargs)
        print(f"  ✓ Record created → ID='{kwargs.get('id')}'")
    except ValueError as e:
        print(f"  ✗ Rejected → ID='{kwargs.get('id')}'\n    {e}")

def main():
    service = RegisterService()


    print("\n──── Creating records ────────────────────────────────")
    try_create(service, id="1", name="Sofía Martínez",   email="sofiamartinez@gmail.com",  age=31, status="married")
    try_create(service, id="2", name="Andrés Herrera",  email="andresherrera@gmail.com", age=29, status="widowed")
    try_create(service, id="3", name="Valentina Ríos",   email="valerios@gmail.com",  age=24, status="single")


    print("\n──── Attempting duplicate ID ─────────────────────────")
    try_create(service, id="1", name="Camilo Vargas", email="camilov@gmail.com", age=37, status="single")

    print("\n──── Invalid fields ──────────────────────────────────")
    try_create(service, id="4", name="Isa",  email="not-an-email",  age=25,  status="single")
    try_create(service, id="5", name="Mike", email="john@gmail.com", age=200, status="married")

    print("\n──── Records in memory ───────────────────────────────")
    records = service.list_records()
    for i, r in enumerate(records, start=1):
        print_record(r, i)

    print(f"\n  Total: {len(records)} record(s)")
    print(f"  Registered IDs (set): {service._ids}")


if __name__ == "__main__":
    main()
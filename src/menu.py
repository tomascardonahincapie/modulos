from colorama import Fore, Back, Style, init
from typing import Optional
from service import RecordService
from integration import generate_fake_records

# Inicializar colorama (autoreset evita tener que resetear manualmente)
init(autoreset=True)

# ──────────────────────────────────────────────
# Helpers de presentación
# ──────────────────────────────────────────────

def _header() -> None:
    """Imprime el encabezado del sistema."""
    print(Fore.CYAN + Style.BRIGHT + "\n" + "-" * 50)
    print(Fore.CYAN + Style.BRIGHT + "   📋  SISTEMA DE GESTIÓN DE REGISTROS")
    print(Fore.CYAN + Style.BRIGHT + "-" * 50)


def _section(title: str) -> None:
    """Imprime un separador de sección."""
    print(Fore.YELLOW + Style.BRIGHT + f"\n── {title} " + "─" * (40 - len(title)))


def _ok(msg: str) -> None:
    """Mensaje de éxito."""
    print(Fore.GREEN + f"  ✔  {msg}")


def _err(msg: str) -> None:
    """Mensaje de error."""
    print(Fore.RED + f"  ✖  {msg}")


def _info(msg: str) -> None:
    """Mensaje informativo."""
    print(Fore.BLUE + f"  ℹ  {msg}")


def _ask(prompt: str) -> str:
    """Input con estilo."""
    return input(Fore.WHITE + Style.BRIGHT + f"  ▶  {prompt}: ").strip()


def _pause() -> None:
    input(Fore.MAGENTA + "\n  Presiona Enter para continuar...")


# ──────────────────────────────────────────────
# Input helpers
# ──────────────────────────────────────────────

def _get_validated_input(prompt: str, validator) -> Optional[str]:
    """Get input and validate it."""
    while True:
        value = _ask(prompt)
        if validator(value):
            return value
        _err("Entrada inválida. Inténtalo de nuevo.")


def _get_int_input(prompt: str) -> Optional[int]:
    """Get integer input."""
    while True:
        value = _ask(prompt)
        try:
            return int(value)
        except ValueError:
            _err("Debe ser un número entero.")


def _get_confirmation(prompt: str) -> bool:
    """Get yes/no confirmation."""
    while True:
        value = _ask(prompt).lower()
        if value in ['s', 'si', 'y', 'yes']:
            return True
        elif value in ['n', 'no']:
            return False
        _err("Responde 's' o 'n'.")


# ──────────────────────────────────────────────
# Opciones del menú
# ──────────────────────────────────────────────

def _show_menu() -> None:
    """Renderiza las opciones del menú principal."""
    _header()
    options = [
        ("1", "Crear registro"),
        ("2", "Listar todos los registros"),
        ("3", "Buscar registro"),
        ("4", "Actualizar registro"),
        ("5", "Eliminar registro"),
        ("6", "Generar 10 registros falsos"),
        ("0", "Salir"),
    ]
    print()
    for key, label in options:
        color = Fore.RED if key == "0" else Fore.WHITE
        print(color + f"    [{key}]  {label}")
    print()


def _read_option() -> str:
    """Lee la opción del usuario con validación básica."""
    valid = {"0", "1", "2", "3", "4", "5", "6"}
    while True:
        choice = _ask("Selecciona una opción")
        if choice in valid:
            return choice
        _err(f"Opción inválida '{choice}'. Elige entre: {', '.join(sorted(valid))}")


# ──────────────────────────────────────────────
# Flujos de cada opción
# ──────────────────────────────────────────────

def _flow_create(service: RecordService) -> None:
    _section("CREAR REGISTRO")
    try:
        id = _ask("ID")
        name = _ask("Nombre")
        email = _ask("Email")
        age = _get_int_input("Edad")
        status = _ask("Estado civil (soltero/casado/viudo/divorciado)")
        record = service.create_record(id=id, name=name, email=email, age=age, status=status)
        _ok(f"Registro creado con ID: {record['id']}")
    except ValueError as e:
        _err(str(e))
    except Exception as e:
        _err(f"Error inesperado: {e}")
    _pause()


def _flow_list(service: RecordService) -> None:
    _section("LISTADO DE REGISTROS")
    records = service.list_records()
    if not records:
        _info("No hay registros almacenados.")
    else:
        _info(f"{len(records)} registro(s) encontrado(s).\n")
        # Cabecera de tabla
        print(Fore.CYAN + Style.BRIGHT +
              f"  {'ID':<6} {'NOMBRE':<20} {'EMAIL':<28} {'EDAD':<6} {'ESTATUS':<12}")
        print(Fore.CYAN + "  " + "─" * 74)
        for r in records:
            print(Fore.WHITE +
                  f"  {r['id']:<6} {r['name']:<20} {r['email']:<28} {r['age']:<6} {r['status']:<12}")
    _pause()


def _flow_search(service: RecordService) -> None:
    _section("BUSCAR REGISTRO")
    try:
        query = _ask("ID o nombre a buscar")
        results = service.search_record(id=query)
        if not results:
            results = service.search_record(name=query)
        if not results:
            _info("No se encontraron registros con ese criterio.")
        else:
            _info(f"{len(results)} resultado(s):\n")
            for r in results:
                print(Fore.WHITE +
                      f"  ID: {r['id']} | {r['name']} | {r['email']} | {r['age']} | {r['status']}")
    except Exception as e:
        _err(f"Error al buscar: {e}")
    _pause()


def _flow_update(service: RecordService) -> None:
    _section("ACTUALIZAR REGISTRO")
    try:
        record_id = _ask("ID del registro a actualizar")
        _info("Deja en blanco los campos que no quieras cambiar.")
        name = _ask("Nuevo nombre")
        email = _ask("Nuevo email")
        age_str = _ask("Nueva edad")
        status = _ask("Nuevo estado civil")

        # Construir kwargs solo con campos no vacíos
        fields = {}
        if name:
            fields["name"] = name
        if email:
            fields["email"] = email
        if age_str:
            try:
                fields["age"] = int(age_str)
            except ValueError:
                raise ValueError("La edad debe ser un número.")
        if status:
            fields["status"] = status

        if not fields:
            _info("No se indicaron cambios.")
        else:
            service.update_record(record_id, **fields)
            _ok("Registro actualizado correctamente.")
    except (ValueError, KeyError) as e:
        _err(str(e))
    except Exception as e:
        _err(f"Error inesperado: {e}")
    _pause()


def _flow_delete(service: RecordService) -> None:
    _section("ELIMINAR REGISTRO")
    try:
        record_id = _ask("ID del registro a eliminar")
        if _get_confirmation(f"¿Confirmas eliminar el ID {record_id}? (s/n)"):
            service.delete_record(record_id)
            _ok(f"Registro {record_id} eliminado.")
        else:
            _info("Operación cancelada.")
    except (ValueError, KeyError) as e:
        _err(str(e))
    except Exception as e:
        _err(f"Error inesperado: {e}")
    _pause()


def _flow_generate_fake(service: RecordService) -> None:
    _section("GENERAR REGISTROS FALSOS")
    try:
        count_str = _ask("Número de registros a generar (por defecto 10)")
        count = int(count_str) if count_str else 10
        if count <= 0:
            raise ValueError("El número debe ser positivo.")
        records = generate_fake_records(count=count)
        _ok(f"Se generaron {len(records)} registros falsos exitosamente.")
    except ValueError as e:
        _err(str(e))
    except Exception as e:
        _err(f"Error inesperado: {e}")
    _pause()


# ──────────────────────────────────────────────
# Dispatcher
# ──────────────────────────────────────────────

_ACTIONS = {
    "1": _flow_create,
    "2": _flow_list,
    "3": _flow_search,
    "4": _flow_update,
    "5": _flow_delete,
    "6": _flow_generate_fake,
}


# ──────────────────────────────────────────────
# Punto de entrada del menú
# ──────────────────────────────────────────────

def run() -> None:
    """Bucle principal del menú. Se repite hasta que el usuario elige '0'."""
    service = RecordService()
    try:
        while True:
            _show_menu()
            option = _read_option()

            if option == "0":
                print(Fore.CYAN + Style.BRIGHT + "\n  ¡Hasta luego! 👋\n")
                break

            action = _ACTIONS.get(option)
            if action:
                action(service)
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n  ⚠  Programa interrumpido por el usuario. ¡Hasta luego! 👋\n")
        return


if __name__ == "__main__":
    run()
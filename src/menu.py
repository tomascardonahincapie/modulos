from colorama import Fore, Back, Style, init
from service import (
    new_register,
    list_records,
    search_record,
    update_record,
    delete_record,
)

# Inicializar colorama (autoreset evita tener que resetear manualmente)
init(autoreset=True)

# ──────────────────────────────────────────────
# Helpers de presentación
# ──────────────────────────────────────────────

def _header():
    """Imprime el encabezado del sistema."""
    print(Fore.CYAN + Style.BRIGHT + "\n" + "═" * 50)
    print(Fore.CYAN + Style.BRIGHT + "   📋  SISTEMA DE GESTIÓN DE REGISTROS")
    print(Fore.CYAN + Style.BRIGHT + "═" * 50)


def _section(title: str):
    """Imprime un separador de sección."""
    print(Fore.YELLOW + Style.BRIGHT + f"\n── {title} " + "─" * (40 - len(title)))


def _ok(msg: str):
    """Mensaje de éxito."""
    print(Fore.GREEN + f"  ✔  {msg}")


def _err(msg: str):
    """Mensaje de error."""
    print(Fore.RED + f"  ✖  {msg}")


def _info(msg: str):
    """Mensaje informativo."""
    print(Fore.BLUE + f"  ℹ  {msg}")


def _ask(prompt: str) -> str:
    """Input con estilo."""
    return input(Fore.WHITE + Style.BRIGHT + f"  ▶  {prompt}: ").strip()


def _pause():
    input(Fore.MAGENTA + "\n  Presiona Enter para continuar...")


# ──────────────────────────────────────────────
# Opciones del menú
# ──────────────────────────────────────────────

def _show_menu():
    """Renderiza las opciones del menú principal."""
    _header()
    options = [
        ("1", "Crear registro"),
        ("2", "Listar todos los registros"),
        ("3", "Buscar registro"),
        ("4", "Actualizar registro"),
        ("5", "Eliminar registro"),
        ("0", "Salir"),
    ]
    print()
    for key, label in options:
        color = Fore.RED if key == "0" else Fore.WHITE
        print(color + f"    [{key}]  {label}")
    print()


def _read_option() -> str:
    """Lee la opción del usuario con validación básica."""
    valid = {"0", "1", "2", "3", "4", "5"}
    while True:
        choice = _ask("Selecciona una opción")
        if choice in valid:
            return choice
        _err(f"Opción inválida '{choice}'. Elige entre: {', '.join(sorted(valid))}")


# ──────────────────────────────────────────────
# Flujos de cada opción
# ──────────────────────────────────────────────

def _flow_create():
    _section("CREAR REGISTRO")
    try:
        record_id = _ask("ID")
        name    = _ask("Nombre")
        email   = _ask("Email")
        age_str = _ask("Edad")
        if not age_str:
            raise ValueError("La edad es requerida.")
        age = int(age_str)
        status  = _ask("Estado civil (soltero/casado/viudo/divorciado)")
        if not status:
            raise ValueError("El estado civil es requerido.")
        record  = new_register(id=record_id, name=name, email=email, age=age, status=status)
        _ok(f"Registro creado con ID: {record['id']}")
    except ValueError as e:
        _err(str(e))
    except Exception as e:
        _err(f"Error inesperado: {e}")
    _pause()


def _flow_list():
    _section("LISTADO DE REGISTROS")
    records = list_records()
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


def _flow_search():
    _section("BUSCAR REGISTRO")
    try:
        query = _ask("ID o nombre a buscar")
        results = search_record(id=query)
        if not results:
            results = search_record(name=query)
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


def _flow_update():
    _section("ACTUALIZAR REGISTRO")
    try:
        record_id = _ask("ID del registro a actualizar")
        _info("Deja en blanco los campos que no quieras cambiar.")
        name  = _ask("Nuevo nombre")
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
            update_record(record_id, **fields)
            _ok("Registro actualizado correctamente.")
    except (ValueError, KeyError) as e:
        _err(str(e))
    except Exception as e:
        _err(f"Error inesperado: {e}")
    _pause()


def _flow_delete():
    _section("ELIMINAR REGISTRO")
    try:
        record_id = _ask("ID del registro a eliminar")
        confirm   = _ask(f"¿Confirmas eliminar el ID {record_id}? (s/n)").lower()
        if confirm == "s":
            delete_record(record_id)
            _ok(f"Registro {record_id} eliminado.")
        else:
            _info("Operación cancelada.")
    except (ValueError, KeyError) as e:
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
}


# ──────────────────────────────────────────────
# Punto de entrada del menú
# ──────────────────────────────────────────────

def run():
    """Bucle principal del menú. Se repite hasta que el usuario elige '0'."""
    while True:
        _show_menu()
        option = _read_option()

        if option == "0":
            print(Fore.CYAN + Style.BRIGHT + "\n  ¡Hasta luego! 👋\n")
            break

        action = _ACTIONS.get(option)
        if action:
            action()


if __name__ == "__main__":
    run()
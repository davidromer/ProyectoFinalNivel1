import os # para verificar la existencia del archivo y manejar errores de lectura/escritura
import re # para validaciones de formato (correo, teléfono, nombre)
from datetime import datetime # para registrar la fecha y hora de registro del usuario

ARCHIVO_USUARIOS = "usuarios.txt"
SEPARADOR = "|"
ENCABEZADO = "ID|NOMBRE|EDAD|CORREO|TELEFONO|REGISTRADO\n"

# ─────────────────────────────────────────
#  UTILIDADES DE ARCHIVO
# ─────────────────────────────────────────

def cargar_usuarios():
    """Carga la lista de usuarios desde el archivo TXT."""
    if not os.path.exists(ARCHIVO_USUARIOS):
        return []
    try:
        usuarios = []
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
            lineas = f.readlines()
        # Saltar encabezado y líneas vacías
        for linea in lineas[1:]:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split(SEPARADOR)
            if len(partes) != 6:
                continue  # línea malformada, se omite
            usuarios.append({
                "id"        : int(partes[0]),
                "nombre"    : partes[1],
                "edad"      : int(partes[2]),
                "correo"    : partes[3],
                "telefono"  : partes[4],
                "registrado": partes[5],
            })
        return usuarios
    except OSError as e:
        print(f"⚠️  No se pudo leer el archivo: {e}")
        return []
    except Exception:
        print("⚠️  Advertencia: el archivo de usuarios estaba corrupto. Se inicia vacío.")
        return []


def guardar_usuarios(usuarios):
    """Guarda la lista de usuarios en el archivo TXT."""
    try:
        with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as f:
            f.write(ENCABEZADO)
            for u in usuarios:
                linea = SEPARADOR.join([
                    str(u["id"]),
                    u["nombre"],
                    str(u["edad"]),
                    u["correo"],
                    u["telefono"],
                    u["registrado"],
                ])
                f.write(linea + "\n")
        print("✅  Datos guardados correctamente en 'usuarios.txt'.")
    except OSError as e:
        print(f"❌  Error al guardar los datos: {e}")


# ─────────────────────────────────────────
#  VALIDACIONES
# ─────────────────────────────────────────

def validar_nombre(nombre):
    """El nombre debe tener al menos 2 caracteres y solo letras/espacios."""
    if len(nombre.strip()) < 2:
        raise ValueError("El nombre debe tener al menos 2 caracteres.")
    if not re.match(r"^[A-Za-záéíóúÁÉÍÓÚñÑ ]+$", nombre.strip()):
        raise ValueError("El nombre solo puede contener letras y espacios.")
    return nombre.strip().title()


def validar_edad(texto):
    """La edad debe ser un entero entre 1 y 120."""
    try:
        edad = int(texto)
    except ValueError:
        raise ValueError("La edad debe ser un número entero.")
    if not (1 <= edad <= 120):
        raise ValueError("La edad debe estar entre 1 y 120 años.")
    return edad


def validar_correo(correo):
    """Verifica el formato básico de un correo electrónico."""
    patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not re.match(patron, correo.strip()):
        raise ValueError("El formato del correo no es válido. Ejemplo: usuario@dominio.com")
    return correo.strip().lower()


def validar_telefono(telefono):
    """El teléfono debe tener entre 7 y 15 dígitos (permite + al inicio)."""
    limpio = telefono.strip()
    if not re.match(r"^\+?\d{7,15}$", limpio):
        raise ValueError("El teléfono debe contener entre 7 y 15 dígitos (puede iniciar con +).")
    return limpio


# ─────────────────────────────────────────
#  ENTRADA SEGURA (loop de reintento)
# ─────────────────────────────────────────

def pedir_dato(mensaje, funcion_validacion):
    """Solicita un dato al usuario y lo reintenta si falla la validación."""
    while True:
        try:
            valor = input(mensaje)
            return funcion_validacion(valor)
        except ValueError as e:
            print(f"   ⚠️  {e}  — Intente de nuevo.")


# ─────────────────────────────────────────
#  OPERACIONES PRINCIPALES
# ─────────────────────────────────────────

def registrar_usuario(usuarios):
    """Recopila, valida y almacena un nuevo usuario."""
    print("\n" + "─" * 45)
    print("       REGISTRO DE NUEVO USUARIO")
    print("─" * 45)

    nombre   = pedir_dato("  Nombre completo : ", validar_nombre)
    edad     = pedir_dato("  Edad            : ", validar_edad)
    correo   = pedir_dato("  Correo          : ", validar_correo)
    telefono = pedir_dato("  Teléfono        : ", validar_telefono)

    # Verificar que el correo no esté duplicado
    if any(u["correo"] == correo for u in usuarios):
        print(f"\n❌  El correo '{correo}' ya está registrado. No se añadió el usuario.")
        return

    usuario = {
        "id"        : len(usuarios) + 1,
        "nombre"    : nombre,
        "edad"      : edad,
        "correo"    : correo,
        "telefono"  : telefono,
        "registrado": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    usuarios.append(usuario)
    guardar_usuarios(usuarios)
    print(f"\n🎉  ¡Usuario '{nombre}' registrado exitosamente con ID {usuario['id']}!")


def listar_usuarios(usuarios):
    """Muestra todos los usuarios registrados."""
    print("\n" + "─" * 55)
    print("          LISTA DE USUARIOS REGISTRADOS")
    print("─" * 55)

    if not usuarios:
        print("  No hay usuarios registrados aún.")
        return

    for u in usuarios:
        print(f"  ID       : {u['id']}")
        print(f"  Nombre   : {u['nombre']}")
        print(f"  Edad     : {u['edad']} años")
        print(f"  Correo   : {u['correo']}")
        print(f"  Teléfono : {u['telefono']}")
        print(f"  Registro : {u['registrado']}")
        print("  " + "·" * 45)

    print(f"\n  Total: {len(usuarios)} usuario(s).")


def buscar_usuario(usuarios):
    """Busca un usuario por nombre o correo (búsqueda parcial)."""
    print("\n" + "─" * 45)
    termino = input("  Buscar por nombre o correo: ").strip().lower()

    if not termino:
        print("  ⚠️  Ingrese un término de búsqueda.")
        return

    resultados = [
        u for u in usuarios
        if termino in u["nombre"].lower() or termino in u["correo"]
    ]

    if not resultados:
        print(f"  No se encontraron usuarios para '{termino}'.")
    else:
        print(f"\n  Se encontraron {len(resultados)} resultado(s):\n")
        for u in resultados:
            print(f"  [{u['id']}] {u['nombre']} — {u['correo']} — Tel: {u['telefono']}")


def eliminar_usuario(usuarios):
    """Elimina un usuario por su ID."""
    print("\n" + "─" * 45)
    try:
        id_buscado = int(input("  ID del usuario a eliminar: "))
    except ValueError:
        print("  ⚠️  El ID debe ser un número entero.")
        return

    indice = next((i for i, u in enumerate(usuarios) if u["id"] == id_buscado), None)

    if indice is None:
        print(f"  ❌  No existe ningún usuario con ID {id_buscado}.")
        return

    nombre = usuarios[indice]["nombre"]
    confirmacion = input(f"  ¿Seguro que desea eliminar a '{nombre}'? (s/n): ").strip().lower()

    if confirmacion == "s":
        usuarios.pop(indice)
        guardar_usuarios(usuarios)
        print(f"  🗑️   Usuario '{nombre}' eliminado correctamente.")
    else:
        print("  Operación cancelada.")


# ─────────────────────────────────────────
#  MENÚ PRINCIPAL
# ─────────────────────────────────────────

# ─────────────────────────────────────────
#  PRUEBA CON usuarios2.txt
# ─────────────────────────────────────────

def probar_usuarios2():
    """Lee usuarios2.txt y clasifica cada registro en aprobado o con error."""
    archivo = os.path.join(os.path.dirname(__file__), "usuarios2.txt")

    print("\n" + "═" * 55)
    print("   PRUEBA DE VALIDACIÓN — usuarios2.txt")
    print("═" * 55)

    if not os.path.exists(archivo):
        print(f"  ⚠️  No se encontró el archivo '{archivo}'.")
        return

    aprobados = []
    errores   = []

    with open(archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    for numero, linea in enumerate(lineas, start=1):
        linea = linea.strip()
        if not linea:
            continue

        partes = linea.split(",")
        if len(partes) < 2:
            errores.append((numero, linea, "Formato de línea inválido (se esperan al menos nombre y edad)"))
            continue

        nombre_raw = partes[0].strip()
        edad_raw   = partes[1].strip()
        errores_linea = []

        # Validar nombre
        nombre_ok = None
        try:
            nombre_ok = validar_nombre(nombre_raw)
        except ValueError as e:
            errores_linea.append(f"Nombre: {e}")

        # Validar edad
        edad_ok = None
        try:
            edad_ok = validar_edad(edad_raw)
        except ValueError as e:
            errores_linea.append(f"Edad: {e}")

        if errores_linea:
            errores.append((numero, linea, " | ".join(errores_linea)))
        else:
            aprobados.append((numero, nombre_ok, edad_ok))

    # ── Mostrar aprobados ──────────────────────
    print(f"\n  ✅  REGISTROS APROBADOS ({len(aprobados)})")
    print("  " + "─" * 50)
    if aprobados:
        for num, nombre, edad in aprobados:
            print(f"  Línea {num:>2}: {nombre:<20} | Edad: {edad} años")
    else:
        print("  (ninguno)")

    # ── Mostrar errores ────────────────────────
    print(f"\n  ❌  REGISTROS CON ERRORES ({len(errores)})")
    print("  " + "─" * 50)
    if errores:
        for num, raw, motivo in errores:
            print(f"  Línea {num:>2}: [{raw}]")
            print(f"           → {motivo}")
    else:
        print("  (ninguno)")

    print("\n" + "═" * 55)


def mostrar_menu():
    print("\n" + "═" * 45)
    print("   SISTEMA DE REGISTRO DE USUARIOS")
    print("═" * 45)
    print("  1. Registrar nuevo usuario")
    print("  2. Listar todos los usuarios")
    print("  3. Buscar usuario")
    print("  4. Eliminar usuario")
    print("  6. Probar datos de usuarios2.txt")
    print("  5. Salir")
    print("─" * 45)


def main():
    usuarios = cargar_usuarios()
    print("\n👋  Bienvenido al Sistema de Registro de Usuarios")

    opciones = {
        "1": lambda: registrar_usuario(usuarios),
        "2": lambda: listar_usuarios(usuarios),
        "3": lambda: buscar_usuario(usuarios),
        "4": lambda: eliminar_usuario(usuarios),
        "6": probar_usuarios2,
    }

    while True:
        mostrar_menu()
        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "5":
            print("\n👋  ¡Hasta luego!\n")
            break
        elif opcion in opciones:
            opciones[opcion]()
        else:
            print("  ⚠️  Opción no válida. Por favor elija entre 1 y 5.")


if __name__ == "__main__":
    main()
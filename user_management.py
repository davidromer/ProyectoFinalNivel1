from __future__ import annotations

import re
from pathlib import Path


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


class UserManagementError(Exception):
    """Base exception for user manager errors."""


class ValidationError(UserManagementError):
    """Raised when user data is invalid."""


class UserNotFoundError(UserManagementError):
    """Raised when a user does not exist."""


class UserManager:
    def __init__(self, file_path: str = "usuarios.txt") -> None:
        self.file_path = Path(file_path)
        try:
            self.file_path.touch(exist_ok=True)
        except OSError as exc:
            raise UserManagementError(f"No se pudo inicializar el archivo: {exc}") from exc

    def _validate_user(self, user_id: int, name: str, email: str, age: int) -> None:
        normalized_name = name.strip() if isinstance(name, str) else name
        normalized_email = email.strip() if isinstance(email, str) else email

        if not isinstance(user_id, int) or user_id <= 0:
            raise ValidationError("El ID debe ser un entero positivo.")

        if not isinstance(normalized_name, str) or not normalized_name or "|" in normalized_name:
            raise ValidationError("El nombre es obligatorio y no puede contener '|'.")

        if (
            not isinstance(normalized_email, str)
            or ".." in normalized_email
            or not EMAIL_PATTERN.match(normalized_email)
        ):
            raise ValidationError("El correo electrónico no es válido.")

        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValidationError("La edad debe ser un número entre 0 y 120.")

    def _read_users(self) -> list[dict[str, object]]:
        users: list[dict[str, object]] = []
        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                for line_number, raw_line in enumerate(file, start=1):
                    line = raw_line.strip()
                    if not line:
                        continue
                    parts = line.split("|")
                    if len(parts) != 4:
                        raise UserManagementError(
                            f"Formato inválido en línea {line_number}: '{line}'"
                        )
                    user_id_raw, name, email, age_raw = parts
                    users.append(
                        {
                            "id": int(user_id_raw),
                            "name": name,
                            "email": email,
                            "age": int(age_raw),
                        }
                    )
        except ValueError as exc:
            raise UserManagementError(f"Error al procesar el archivo de usuarios: {exc}") from exc
        except OSError as exc:
            raise UserManagementError(f"No se pudo leer el archivo: {exc}") from exc
        return users

    def _write_users(self, users: list[dict[str, object]]) -> None:
        try:
            with self.file_path.open("w", encoding="utf-8") as file:
                for user in users:
                    file.write(
                        f"{user['id']}|{user['name']}|{user['email']}|{user['age']}\n"
                    )
        except OSError as exc:
            raise UserManagementError(f"No se pudo escribir el archivo: {exc}") from exc

    def add_user(self, user_id: int, name: str, email: str, age: int) -> None:
        self._validate_user(user_id, name, email, age)
        users = self._read_users()

        if any(user["id"] == user_id for user in users):
            raise ValidationError("Ya existe un usuario con ese ID.")

        users.append({"id": user_id, "name": name.strip(), "email": email.strip(), "age": age})
        self._write_users(users)

    def list_users(self) -> list[dict[str, object]]:
        return self._read_users()

    def find_user(self, user_id: int) -> dict[str, object]:
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValidationError("El ID debe ser un entero positivo.")

        for user in self._read_users():
            if user["id"] == user_id:
                return user
        raise UserNotFoundError("Usuario no encontrado.")

    def delete_user(self, user_id: int) -> None:
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValidationError("El ID debe ser un entero positivo.")

        users = self._read_users()
        filtered_users = [user for user in users if user["id"] != user_id]

        if len(filtered_users) == len(users):
            raise UserNotFoundError("Usuario no encontrado.")

        self._write_users(filtered_users)


def _print_users(users: list[dict[str, object]]) -> None:
    if not users:
        print("No hay usuarios registrados.")
        return

    for user in users:
        print(
            f"ID: {user['id']}, Nombre: {user['name']}, "
            f"Email: {user['email']}, Edad: {user['age']}"
        )


def main() -> None:
    manager = UserManager()
    options = {
        "1": "Agregar usuario",
        "2": "Listar usuarios",
        "3": "Buscar usuario por ID",
        "4": "Eliminar usuario",
        "5": "Salir",
    }

    while True:
        print("\nSistema de gestión de usuarios")
        for key, value in options.items():
            print(f"{key}. {value}")

        choice = input("Selecciona una opción: ").strip()

        try:
            if choice == "1":
                user_id = int(input("ID: ").strip())
                name = input("Nombre: ").strip()
                email = input("Email: ").strip()
                age = int(input("Edad: ").strip())
                manager.add_user(user_id, name, email, age)
                print("Usuario agregado correctamente.")
            elif choice == "2":
                _print_users(manager.list_users())
            elif choice == "3":
                user_id = int(input("ID del usuario: ").strip())
                _print_users([manager.find_user(user_id)])
            elif choice == "4":
                user_id = int(input("ID del usuario: ").strip())
                manager.delete_user(user_id)
                print("Usuario eliminado correctamente.")
            elif choice == "5":
                print("Hasta luego.")
                break
            else:
                print("Opción no válida.")
        except ValueError:
            print("Error: Debes ingresar valores numéricos válidos para ID y edad.")
        except UserManagementError as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()

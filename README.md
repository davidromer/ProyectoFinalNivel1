# Sistema de Registro de Usuarios

Aplicación de consola desarrollada en **Python** para gestionar un registro de usuarios almacenado en un archivo de texto plano (`usuarios.txt`).

## Características

- Registrar nuevos usuarios con validación de datos en tiempo real
- Listar todos los usuarios registrados
- Buscar usuarios por nombre o correo (búsqueda parcial)
- Eliminar usuarios por ID
- **Prueba de validación masiva** desde un archivo externo (`usuarios2.txt`)

## Estructura del proyecto

```
ProyectoFinalNivel1/
├── Aplicacion100626.py   # Aplicación principal
├── usuarios.txt          # Base de datos de usuarios (generado automáticamente)
└── usuarios2.txt         # Archivo de prueba con datos aprobados y con errores
```

## Requisitos

- Python 3.x (sin dependencias externas)

## Ejecución

```bash
python Aplicacion100626.py
```

## Menú principal

```
═════════════════════════════════════════════
   SISTEMA DE REGISTRO DE USUARIOS
═════════════════════════════════════════════
  1. Registrar nuevo usuario
  2. Listar todos los usuarios
  3. Buscar usuario
  4. Eliminar usuario
  6. Probar datos de usuarios2.txt
  5. Salir
```

## Validaciones aplicadas

| Campo    | Regla                                                         |
|----------|---------------------------------------------------------------|
| Nombre   | Mínimo 2 caracteres, solo letras y espacios                   |
| Edad     | Número entero entre 1 y 120                                   |
| Correo   | Formato válido `usuario@dominio.com`, sin duplicados          |
| Teléfono | Entre 7 y 15 dígitos, puede iniciar con `+`                   |

## Formato del archivo `usuarios.txt`

El archivo usa `|` como separador y contiene las siguientes columnas:

```
ID|NOMBRE|EDAD|CORREO|TELEFONO|REGISTRADO
1|Carlos Pérez|25|carlos@mail.com|3001234567|2026-06-12 16:31:07
```

## Prueba con `usuarios2.txt` (opción 6)

Lee el archivo `usuarios2.txt` con el formato `nombre,edad,fecha` y clasifica cada registro:

**Ejemplo de salida:**

```
  ✅  REGISTROS APROBADOS (4)
  Línea  1: Carlos               | Edad: 25 años
  Línea  3: Miguel               | Edad: 24 años
  Línea  5: Manuela              | Edad: 19 años
  Línea  7: Valentina            | Edad: 30 años

  ❌  REGISTROS CON ERRORES (3)
  Línea  2: [Maria,-52,...]
           → Edad: La edad debe estar entre 1 y 120 años.
  Línea  4: [,23,...]
           → Nombre: El nombre debe tener al menos 2 caracteres.
  Línea  6: [Felipe,148,...]
           → Edad: La edad debe estar entre 1 y 120 años.
```

## Autor

Desarrollado como **Proyecto Final — Nivel 1** del programa DevSeniorCode · PythonSenior.

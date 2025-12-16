# Sistema de Gestión de Empleados y Contratos

## Objetivo del Proyecto

Aplicación en Python que administra un directorio de empleados y sus contratos laborales utilizando archivos JSON como almacenamiento de datos. La aplicación ofrece una interfaz CLI (Command Line Interface) para interactuar con el sistema.

### Funcionalidades

- **Gestión de Empleados:**
  - Agregar nuevos empleados
  - Buscar empleados por ID
  - Actualizar información de empleados
  - Eliminar empleados
  - Listar todos los empleados

- **Gestión de Contratos:**
  - Asociar contratos laborales a empleados
  - Ver contratos de un empleado específico
  - Consultar información de contratos

- **Consultas:**
  - Buscar empleado por ID con sus contratos
  - Listar todos los empleados
  - Ver contratos de empleados

- **Reportes:**
  - Generar reporte de contratos vencidos
  - Generar reporte de contratos activos

## Instalación

### Requisitos Previos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar o descargar el proyecto**

2. **Crear un entorno virtual (recomendado):**
   ```bash
   python -m venv .venv
   ```

3. **Activar el entorno virtual:**
   
   En Windows:
   ```bash
   .venv\Scripts\activate
   ```
   
   En Linux/Mac:
   ```bash
   source .venv/bin/activate
   ```

4. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución

1. Asegúrate de tener activado el entorno virtual.

2. Ejecuta el programa principal:
   ```bash
   python main.py
   ```

3. El sistema mostrará un menú interactivo con las siguientes opciones:
   - Gestionar Empleados
   - Gestionar Contratos
   - Consultar Información
   - Generar Reportes
   - Salir

## Ejemplo de Uso

### Ejemplo 1: Agregar un Empleado

1. Selecciona la opción `1` (Gestionar Empleados)
2. Selecciona la opción `1` (Agregar Empleado)
3. Ingresa el nombre: `Juan Pérez`
4. Ingresa el cargo: `Desarrollador Senior`
5. El sistema confirmará que el empleado ha sido agregado con un ID único

### Ejemplo 2: Asociar un Contrato

1. Selecciona la opción `2` (Gestionar Contratos)
2. Selecciona la opción `1` (Asociar Contrato a Empleado)
3. Ingresa el ID del empleado (obtenido al agregarlo)
4. Ingresa la fecha de inicio: `2024-01-15`
5. Ingresa la fecha de fin: `2024-12-31`
6. Ingresa el salario: `5000`
7. El sistema confirmará que el contrato ha sido asociado

### Ejemplo 3: Generar Reporte de Contratos Vencidos

1. Selecciona la opción `4` (Generar Reportes)
2. Selecciona la opción `1` (Contratos Vencidos)
3. El sistema mostrará todos los contratos cuya fecha de fin sea anterior a la fecha actual

## Estructura del Proyecto

```
Proyecto1/
│
├── data/                      # Carpeta con archivos de datos
│   └── empleados.json        # Archivo JSON con datos de empleados y contratos
│
├── lib/                       # Módulos del programa
│   ├── __init__.py
│   ├── gestor_empleados.py   # Gestión de empleados (CRUD)
│   └── gestor_contratos.py   # Gestión de contratos laborales
│
├── test/                      # Pruebas unitarias
│   ├── __init__.py
│   ├── test_gestor_empleados.py
│   └── test_gestor_contratos.py
│
├── main.py                    # Punto de entrada del programa (interfaz CLI)
├── requirements.txt           # Dependencias del proyecto
├── agents.md                  # Especificaciones técnicas del proyecto
├── instruccionesProyecto.md   # Instrucciones del proyecto
└── README.md                  # Este archivo
```

## Ejecución de Pruebas

Para ejecutar las pruebas unitarias, utiliza el siguiente comando:

```bash
pytest
```

Para ejecutar las pruebas con más detalles:

```bash
pytest -v
```

Para ejecutar pruebas de un módulo específico:

```bash
pytest test/test_gestor_empleados.py
pytest test/test_gestor_contratos.py
```

## Características Técnicas

- **Lenguaje:** Python 3.7+
- **Almacenamiento:** Archivos JSON
- **Interfaz:** CLI (Command Line Interface)
- **Testing:** pytest
- **Convenciones de código:**
  - camelCase para funciones y variables
  - PascalCase para clases
  - Tipado de datos en todo el proyecto

## Formato de Datos

Los datos se almacenan en formato JSON con la siguiente estructura:

```json
{
    "empleados": [
        {
            "id": 1,
            "nombre": "Carlos Pérez",
            "cargo": "Desarrollador",
            "contratos": [
                {
                    "id_contrato": 101,
                    "fecha_inicio": "2023-02-15",
                    "fecha_fin": "2024-02-15",
                    "salario": 3500
                }
            ]
        }
    ]
}
```

## Notas

- Los IDs de empleados se generan automáticamente de forma incremental
- Los IDs de contratos comienzan en 101 y se incrementan automáticamente
- Las fechas deben estar en formato YYYY-MM-DD
- El archivo de datos se crea automáticamente si no existe


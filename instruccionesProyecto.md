# Se desarrollará una aplicación en Python que administre un directorio de empleados y sus contratos laborales utilizando archivos JSON como almacenamiento de datos. La aplicación debe permitir:

-	Agregar, actualizar y eliminar empleados.
-	Registrar contratos laborales asociados a los empleados.
-	Consultar información de empleados y sus contratos.
-	Generar reportes básicos (por ejemplo, empleados con contratos vencidos).
-	Guardar y recuperar información de un archivo JSON.
-	Implementar pruebas unitarias sobre las funcionalidades clave.

Esta aplicacion usara una interfaz CLI para la interacion con el usuario.

# Pautas de elaboración

- 	Módulo gestor_empleados.py
   •	Maneja la creación, actualización, eliminación y consulta de empleados.
   •	Guarda la información en empleados.json.

- 	Módulo gestor_contratos.py
   •	Maneja la asociación de contratos laborales a empleados.
   •	Permite filtrar contratos activos y vencidos.

-	Módulo main.py
   •	Ofrece una interfaz de terminal para interactuar con el sistema.

-  El ejemplo de empleado esta en el archivo 'empleados.json' de la carpeta 'data'.

-  Implementación del gestor_empleados.py
   •	Carga y guarda los datos en empleados.json.
   •	Métodos clave:
        agregar_empleado(nombre, cargo) → dict
        eliminar_empleado(id) → bool
        buscar_empleado(id) → dict

-  Implementación del gestor_contratos.py
   •	Permite agregar y actualizar contratos de empleados.
   •	Métodos clave:
        asociar_contrato(id_empleado, fecha_inicio, fecha_fin, salario) → dict
        listar_contratos_vencidos() → list

-  Implementación del main.py
   •	Ofrece un menú interactivo por terminal con opciones para gestionar empleados y contratos.

# Pruebas del proyecto

Implementación de pruebas unitarias con la librería pytest:

-   Probar que se agrega empleado correctamente.
-   Probar que se elimina un empleado.
-   Probar la búsqueda de un empleado.
-   Probar que un empleado tiene contrato.

# Documentación del proyecto

Generar un README que incluya:

-   Objetivo del proyecto.
-   Instrucciones de instalación y ejecución.
-   Ejemplo de uso.

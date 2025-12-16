"""
main.py
Punto de inicio del programa.
Ofrece una interfaz de terminal para interactuar con el sistema.
"""

from lib.gestor_empleados import GestorEmpleados
from lib.gestor_contratos import GestorContratos
from typing import Optional, Dict


def mostrarMenu() -> None:
    """Muestra el menú principal de la aplicación."""
    print("\n" + "="*50)
    print("  SISTEMA DE GESTIÓN DE EMPLEADOS Y CONTRATOS")
    print("="*50)
    print("\n1. Gestionar Empleados")
    print("2. Gestionar Contratos")
    print("3. Consultar Información")
    print("4. Generar Reportes")
    print("5. Salir")
    print("\n" + "-"*50)


def mostrarMenuEmpleados() -> None:
    """Muestra el menú de gestión de empleados."""
    print("\n" + "-"*50)
    print("  GESTIÓN DE EMPLEADOS")
    print("-"*50)
    print("\n1. Agregar Empleado")
    print("2. Buscar Empleado")
    print("3. Actualizar Empleado")
    print("4. Eliminar Empleado")
    print("5. Listar Todos los Empleados")
    print("6. Volver al Menú Principal")
    print("\n" + "-"*50)


def mostrarMenuContratos() -> None:
    """Muestra el menú de gestión de contratos."""
    print("\n" + "-"*50)
    print("  GESTIÓN DE CONTRATOS")
    print("-"*50)
    print("\n1. Asociar Contrato a Empleado")
    print("2. Ver Contratos de un Empleado")
    print("3. Volver al Menú Principal")
    print("\n" + "-"*50)


def mostrarMenuConsultas() -> None:
    """Muestra el menú de consultas."""
    print("\n" + "-"*50)
    print("  CONSULTAS")
    print("-"*50)
    print("\n1. Buscar Empleado por ID")
    print("2. Ver Todos los Empleados")
    print("3. Ver Contratos de un Empleado")
    print("4. Volver al Menú Principal")
    print("\n" + "-"*50)


def mostrarMenuReportes() -> None:
    """Muestra el menú de reportes."""
    print("\n" + "-"*50)
    print("  REPORTES")
    print("-"*50)
    print("\n1. Contratos Vencidos")
    print("2. Contratos Activos")
    print("3. Volver al Menú Principal")
    print("\n" + "-"*50)


def procesarEmpleados(gestorEmpleados: GestorEmpleados) -> None:
    """Procesa las opciones del menú de empleados."""
    while True:
        mostrarMenuEmpleados()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n--- Agregar Empleado ---")
            nombre = input("Ingrese el nombre del empleado: ").strip()
            cargo = input("Ingrese el cargo del empleado: ").strip()
            
            if nombre and cargo:
                empleado = gestorEmpleados.agregarEmpleado(nombre, cargo)
                if empleado:
                    print(f"\n✓ Empleado agregado exitosamente!")
                    print(f"  ID: {empleado['id']}")
                    print(f"  Nombre: {empleado['nombre']}")
                    print(f"  Cargo: {empleado['cargo']}")
                else:
                    print("\n✗ Error al agregar el empleado.")
            else:
                print("\n✗ El nombre y el cargo son obligatorios.")
        
        elif opcion == "2":
            print("\n--- Buscar Empleado ---")
            try:
                idEmpleado = int(input("Ingrese el ID del empleado: ").strip())
                empleado = gestorEmpleados.buscarEmpleado(idEmpleado)
                if empleado:
                    mostrarEmpleado(empleado)
                else:
                    print(f"\n✗ No se encontró un empleado con ID {idEmpleado}.")
            except ValueError:
                print("\n✗ Por favor ingrese un ID válido (número entero).")
        
        elif opcion == "3":
            print("\n--- Actualizar Empleado ---")
            try:
                idEmpleado = int(input("Ingrese el ID del empleado: ").strip())
                empleado = gestorEmpleados.buscarEmpleado(idEmpleado)
                
                if empleado:
                    print(f"\nEmpleado actual: {empleado['nombre']} - {empleado['cargo']}")
                    nuevoNombre = input("Nuevo nombre (presione Enter para mantener): ").strip()
                    nuevoCargo = input("Nuevo cargo (presione Enter para mantener): ").strip()
                    
                    nombre = nuevoNombre if nuevoNombre else None
                    cargo = nuevoCargo if nuevoCargo else None
                    
                    empleadoActualizado = gestorEmpleados.actualizarEmpleado(
                        idEmpleado, nombre, cargo
                    )
                    if empleadoActualizado:
                        print("\n✓ Empleado actualizado exitosamente!")
                        mostrarEmpleado(empleadoActualizado)
                    else:
                        print("\n✗ Error al actualizar el empleado.")
                else:
                    print(f"\n✗ No se encontró un empleado con ID {idEmpleado}.")
            except ValueError:
                print("\n✗ Por favor ingrese un ID válido (número entero).")
        
        elif opcion == "4":
            print("\n--- Eliminar Empleado ---")
            try:
                idEmpleado = int(input("Ingrese el ID del empleado a eliminar: ").strip())
                empleado = gestorEmpleados.buscarEmpleado(idEmpleado)
                
                if empleado:
                    confirmacion = input(
                        f"\n¿Está seguro de eliminar a {empleado['nombre']}? (s/n): "
                    ).strip().lower()
                    
                    if confirmacion == 's':
                        if gestorEmpleados.eliminarEmpleado(idEmpleado):
                            print("\n✓ Empleado eliminado exitosamente!")
                        else:
                            print("\n✗ Error al eliminar el empleado.")
                    else:
                        print("\nOperación cancelada.")
                else:
                    print(f"\n✗ No se encontró un empleado con ID {idEmpleado}.")
            except ValueError:
                print("\n✗ Por favor ingrese un ID válido (número entero).")
        
        elif opcion == "5":
            print("\n--- Lista de Empleados ---")
            empleados = gestorEmpleados.listarEmpleados()
            if empleados:
                for empleado in empleados:
                    mostrarEmpleado(empleado)
                    print()
            else:
                print("\nNo hay empleados registrados.")
        
        elif opcion == "6":
            break
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción del 1 al 6.")


def procesarContratos(gestorContratos: GestorContratos) -> None:
    """Procesa las opciones del menú de contratos."""
    while True:
        mostrarMenuContratos()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n--- Asociar Contrato a Empleado ---")
            try:
                idEmpleado = int(input("Ingrese el ID del empleado: ").strip())
                
                # Validar fecha de inicio con reintento
                fechaInicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ").strip()
                if not gestorContratos.validarFormatoFecha(fechaInicio):
                    print(f"\n✗ formato de fecha invalido {fechaInicio}")
                    fechaInicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ").strip()
                    if not gestorContratos.validarFormatoFecha(fechaInicio):
                        print(f"\n✗ formato de fecha invalido {fechaInicio}")
                        continue
                
                # Validar fecha de fin con reintento
                fechaFin = input("Ingrese la fecha de fin (YYYY-MM-DD): ").strip()
                if not gestorContratos.validarFormatoFecha(fechaFin):
                    print(f"\n✗ formato de fecha invalido {fechaFin}")
                    fechaFin = input("Ingrese la fecha de fin (YYYY-MM-DD): ").strip()
                    if not gestorContratos.validarFormatoFecha(fechaFin):
                        print(f"\n✗ formato de fecha invalido {fechaFin}")
                        continue
                
                # Validar que la fecha de fin sea al menos un mes posterior a la fecha de inicio
                if not gestorContratos.validarFechasContrato(fechaInicio, fechaFin):
                    print("\n✗ La fecha de fin sea al menos un mes posterior a la fecha de inicio")
                    continue
                
                salario = float(input("Ingrese el salario: ").strip())
                
                contrato = gestorContratos.asociarContrato(
                    idEmpleado, fechaInicio, fechaFin, salario
                )
                
                if contrato:
                    print(f"\n✓ Contrato asociado exitosamente!")
                    print(f"  ID Contrato: {contrato['id_contrato']}")
                    print(f"  Fecha Inicio: {contrato['fecha_inicio']}")
                    print(f"  Fecha Fin: {contrato['fecha_fin']}")
                    print(f"  Salario: ${contrato['salario']:.2f}")
                else:
                    print("\n✗ Error al asociar el contrato.")
                    print("  Verifique que:")
                    print("  - El empleado exista")
                    print("  - Las fechas tengan el formato YYYY-MM-DD")
            except ValueError:
                print("\n✗ Por favor ingrese valores válidos.")
        
        elif opcion == "2":
            print("\n--- Ver Contratos de un Empleado ---")
            try:
                idEmpleado = int(input("Ingrese el ID del empleado: ").strip())
                contratos = gestorContratos.obtenerContratosEmpleado(idEmpleado)
                
                if contratos:
                    print(f"\nContratos del empleado ID {idEmpleado}:")
                    for contrato in contratos:
                        mostrarContrato(contrato)
                else:
                    print(f"\nEl empleado con ID {idEmpleado} no tiene contratos registrados.")
            except ValueError:
                print("\n✗ Por favor ingrese un ID válido (número entero).")
        
        elif opcion == "3":
            break
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción del 1 al 3.")


def procesarConsultas(gestorEmpleados: GestorEmpleados, 
                     gestorContratos: GestorContratos) -> None:
    """Procesa las opciones del menú de consultas."""
    while True:
        mostrarMenuConsultas()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n--- Buscar Empleado por ID ---")
            try:
                idEmpleado = int(input("Ingrese el ID del empleado: ").strip())
                empleado = gestorEmpleados.buscarEmpleado(idEmpleado)
                if empleado:
                    mostrarEmpleado(empleado)
                    contratos = gestorContratos.obtenerContratosEmpleado(idEmpleado)
                    if contratos:
                        print("\nContratos:")
                        for contrato in contratos:
                            mostrarContrato(contrato)
                else:
                    print(f"\n✗ No se encontró un empleado con ID {idEmpleado}.")
            except ValueError:
                print("\n✗ Por favor ingrese un ID válido (número entero).")
        
        elif opcion == "2":
            print("\n--- Lista Completa de Empleados ---")
            empleados = gestorEmpleados.listarEmpleados()
            if empleados:
                for empleado in empleados:
                    mostrarEmpleado(empleado)
                    print()
            else:
                print("\nNo hay empleados registrados.")
        
        elif opcion == "3":
            print("\n--- Ver Contratos de un Empleado ---")
            try:
                idEmpleado = int(input("Ingrese el ID del empleado: ").strip())
                contratos = gestorContratos.obtenerContratosEmpleado(idEmpleado)
                
                if contratos:
                    empleado = gestorEmpleados.buscarEmpleado(idEmpleado)
                    if empleado:
                        print(f"\nEmpleado: {empleado['nombre']} - {empleado['cargo']}")
                    print("\nContratos:")
                    for contrato in contratos:
                        mostrarContrato(contrato)
                else:
                    print(f"\nEl empleado con ID {idEmpleado} no tiene contratos registrados.")
            except ValueError:
                print("\n✗ Por favor ingrese un ID válido (número entero).")
        
        elif opcion == "4":
            break
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción del 1 al 4.")


def procesarReportes(gestorContratos: GestorContratos) -> None:
    """Procesa las opciones del menú de reportes."""
    while True:
        mostrarMenuReportes()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            print("\n--- Reporte: Contratos Vencidos ---")
            contratosVencidos = gestorContratos.listarContratosVencidos()
            
            if contratosVencidos:
                print(f"\nTotal de contratos vencidos: {len(contratosVencidos)}\n")
                for item in contratosVencidos:
                    empleado = item["empleado"]
                    contrato = item["contrato"]
                    print(f"Empleado: {empleado['nombre']} (ID: {empleado['id']}) - {empleado['cargo']}")
                    print(f"  Contrato ID: {contrato['id_contrato']}")
                    print(f"  Fecha Fin: {contrato['fecha_fin']}")
                    print(f"  Salario: ${contrato['salario']:.2f}")
                    print()
            else:
                print("\nNo hay contratos vencidos.")
        
        elif opcion == "2":
            print("\n--- Reporte: Contratos Activos ---")
            contratosActivos = gestorContratos.listarContratosActivos()
            
            if contratosActivos:
                print(f"\nTotal de contratos activos: {len(contratosActivos)}\n")
                for item in contratosActivos:
                    empleado = item["empleado"]
                    contrato = item["contrato"]
                    print(f"Empleado: {empleado['nombre']} (ID: {empleado['id']}) - {empleado['cargo']}")
                    print(f"  Contrato ID: {contrato['id_contrato']}")
                    print(f"  Fecha Inicio: {contrato['fecha_inicio']}")
                    print(f"  Fecha Fin: {contrato['fecha_fin']}")
                    print(f"  Salario: ${contrato['salario']:.2f}")
                    print()
            else:
                print("\nNo hay contratos activos.")
        
        elif opcion == "3":
            break
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción del 1 al 3.")


def mostrarEmpleado(empleado: Dict) -> None:
    """Muestra la información de un empleado."""
    print(f"\nID: {empleado['id']}")
    print(f"Nombre: {empleado['nombre']}")
    print(f"Cargo: {empleado['cargo']}")
    contratos = empleado.get('contratos', [])
    print(f"Número de contratos: {len(contratos)}")


def mostrarContrato(contrato: Dict) -> None:
    """Muestra la información de un contrato."""
    print(f"\n  ID Contrato: {contrato['id_contrato']}")
    print(f"  Fecha Inicio: {contrato['fecha_inicio']}")
    print(f"  Fecha Fin: {contrato['fecha_fin']}")
    print(f"  Salario: ${contrato['salario']:.2f}")


def main() -> None:
    """Función principal del programa."""
    gestorEmpleados = GestorEmpleados()
    gestorContratos = GestorContratos()
    
    print("\n¡Bienvenido al Sistema de Gestión de Empleados y Contratos!")
    
    while True:
        mostrarMenu()
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            procesarEmpleados(gestorEmpleados)
        elif opcion == "2":
            procesarContratos(gestorContratos)
        elif opcion == "3":
            procesarConsultas(gestorEmpleados, gestorContratos)
        elif opcion == "4":
            procesarReportes(gestorContratos)
        elif opcion == "5":
            print("\n¡Gracias por usar el sistema! Hasta pronto.")
            break
        else:
            print("\n✗ Opción inválida. Por favor seleccione una opción del 1 al 5.")


if __name__ == "__main__":
    main()


"""
Pruebas unitarias para el módulo gestor_empleados.py
"""

import pytest
import os
import json
import tempfile
from lib.gestor_empleados import GestorEmpleados
from lib.gestor_contratos import GestorContratos


@pytest.fixture
def gestorTemporal():
    """Fixture que crea un gestor con un archivo temporal para las pruebas."""
    # Crear un archivo temporal
    archivoTemporal = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    archivoTemporal.close()
    rutaArchivo = archivoTemporal.name
    
    gestor = GestorEmpleados(rutaArchivo=rutaArchivo)
    yield gestor
    
    # Limpiar: eliminar el archivo temporal después de las pruebas
    if os.path.exists(rutaArchivo):
        os.unlink(rutaArchivo)


def testAgregarEmpleado(gestorTemporal):
    """Prueba que se agrega un empleado correctamente."""
    empleado = gestorTemporal.agregarEmpleado("Juan Pérez", "Desarrollador")
    
    assert empleado is not None
    assert empleado["nombre"] == "Juan Pérez"
    assert empleado["cargo"] == "Desarrollador"
    assert empleado["id"] == 1
    assert empleado["contratos"] == []


def testBuscarEmpleado(gestorTemporal):
    """Prueba la búsqueda de un empleado."""
    # Agregar un empleado primero
    empleadoCreado = gestorTemporal.agregarEmpleado("María García", "Analista")
    
    # Buscar el empleado
    empleadoEncontrado = gestorTemporal.buscarEmpleado(empleadoCreado["id"])
    
    assert empleadoEncontrado is not None
    assert empleadoEncontrado["nombre"] == "María García"
    assert empleadoEncontrado["cargo"] == "Analista"
    assert empleadoEncontrado["id"] == empleadoCreado["id"]


def testBuscarEmpleadoInexistente(gestorTemporal):
    """Prueba que buscar un empleado inexistente retorna None."""
    empleado = gestorTemporal.buscarEmpleado(999)
    assert empleado is None


def testEliminarEmpleado(gestorTemporal):
    """Prueba que se elimina un empleado."""
    # Agregar un empleado
    empleado = gestorTemporal.agregarEmpleado("Carlos López", "Diseñador")
    idEmpleado = empleado["id"]
    
    # Verificar que existe
    assert gestorTemporal.buscarEmpleado(idEmpleado) is not None
    
    # Eliminar el empleado
    resultado = gestorTemporal.eliminarEmpleado(idEmpleado)
    
    assert resultado is True
    assert gestorTemporal.buscarEmpleado(idEmpleado) is None


def testEliminarEmpleadoInexistente(gestorTemporal):
    """Prueba que eliminar un empleado inexistente retorna False."""
    resultado = gestorTemporal.eliminarEmpleado(999)
    assert resultado is False


def testListarEmpleados(gestorTemporal):
    """Prueba que se listan todos los empleados."""
    # Agregar varios empleados
    gestorTemporal.agregarEmpleado("Empleado 1", "Cargo 1")
    gestorTemporal.agregarEmpleado("Empleado 2", "Cargo 2")
    gestorTemporal.agregarEmpleado("Empleado 3", "Cargo 3")
    
    empleados = gestorTemporal.listarEmpleados()
    
    assert len(empleados) == 3
    assert empleados[0]["nombre"] == "Empleado 1"
    assert empleados[1]["nombre"] == "Empleado 2"
    assert empleados[2]["nombre"] == "Empleado 3"


def testActualizarEmpleado(gestorTemporal):
    """Prueba que se actualiza un empleado correctamente."""
    # Agregar un empleado
    empleado = gestorTemporal.agregarEmpleado("Nombre Original", "Cargo Original")
    idEmpleado = empleado["id"]
    
    # Actualizar el empleado
    empleadoActualizado = gestorTemporal.actualizarEmpleado(
        idEmpleado, "Nombre Actualizado", "Cargo Actualizado"
    )
    
    assert empleadoActualizado is not None
    assert empleadoActualizado["nombre"] == "Nombre Actualizado"
    assert empleadoActualizado["cargo"] == "Cargo Actualizado"
    assert empleadoActualizado["id"] == idEmpleado


def testActualizarEmpleadoParcial(gestorTemporal):
    """Prueba que se actualiza solo el nombre del empleado."""
    empleado = gestorTemporal.agregarEmpleado("Nombre Original", "Cargo Original")
    idEmpleado = empleado["id"]
    
    # Actualizar solo el nombre
    empleadoActualizado = gestorTemporal.actualizarEmpleado(
        idEmpleado, "Nombre Actualizado", None
    )
    
    assert empleadoActualizado is not None
    assert empleadoActualizado["nombre"] == "Nombre Actualizado"
    assert empleadoActualizado["cargo"] == "Cargo Original"


def testIdsIncrementales(gestorTemporal):
    """Prueba que los IDs se generan de forma incremental."""
    empleado1 = gestorTemporal.agregarEmpleado("Empleado 1", "Cargo 1")
    empleado2 = gestorTemporal.agregarEmpleado("Empleado 2", "Cargo 2")
    empleado3 = gestorTemporal.agregarEmpleado("Empleado 3", "Cargo 3")
    
    assert empleado1["id"] == 1
    assert empleado2["id"] == 2
    assert empleado3["id"] == 3


def testEmpleadoTieneContratos(gestorTemporal):
    """Prueba que un empleado tiene la estructura de contratos."""
    empleado = gestorTemporal.agregarEmpleado("Test Empleado", "Test Cargo")
    
    assert "contratos" in empleado
    assert isinstance(empleado["contratos"], list)
    assert len(empleado["contratos"]) == 0


def testEmpleadoTieneContratoAsociado(gestorTemporal):
    """Prueba que un empleado tiene contrato después de asociarlo."""
    # Crear un empleado
    empleado = gestorTemporal.agregarEmpleado("Empleado con Contrato", "Desarrollador")
    idEmpleado = empleado["id"]
    
    # Asociar un contrato usando GestorContratos
    gestorContratos = GestorContratos(rutaArchivo=gestorTemporal.rutaArchivo)
    fechaInicio = "2024-01-01"
    fechaFin = "2024-12-31"
    salario = 5000.0
    
    contratoAsociado = gestorContratos.asociarContrato(
        idEmpleado, fechaInicio, fechaFin, salario
    )
    
    # Verificar que el contrato se asoció correctamente
    assert contratoAsociado is not None
    assert contratoAsociado["fecha_inicio"] == fechaInicio
    assert contratoAsociado["fecha_fin"] == fechaFin
    assert contratoAsociado["salario"] == salario
    assert "id_contrato" in contratoAsociado
    
    # Buscar el empleado nuevamente para verificar que tiene el contrato
    empleadoConContrato = gestorTemporal.buscarEmpleado(idEmpleado)
    
    assert empleadoConContrato is not None
    assert len(empleadoConContrato["contratos"]) == 1
    assert empleadoConContrato["contratos"][0]["id_contrato"] == contratoAsociado["id_contrato"]
    assert empleadoConContrato["contratos"][0]["fecha_inicio"] == fechaInicio
    assert empleadoConContrato["contratos"][0]["fecha_fin"] == fechaFin
    assert empleadoConContrato["contratos"][0]["salario"] == salario


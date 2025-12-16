"""
Pruebas unitarias para el módulo gestor_contratos.py
"""

import pytest
import os
import json
import tempfile
from datetime import datetime, timedelta
from lib.gestor_contratos import GestorContratos
from lib.gestor_empleados import GestorEmpleados


@pytest.fixture
def gestorEmpleadosTemporal():
    """Fixture que crea un gestor de empleados con un archivo temporal."""
    archivoTemporal = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
    archivoTemporal.close()
    rutaArchivo = archivoTemporal.name
    
    gestor = GestorEmpleados(rutaArchivo=rutaArchivo)
    yield gestor
    
    if os.path.exists(rutaArchivo):
        os.unlink(rutaArchivo)


@pytest.fixture
def gestorContratosTemporal(gestorEmpleadosTemporal):
    """Fixture que crea un gestor de contratos con el mismo archivo temporal."""
    gestor = GestorContratos(rutaArchivo=gestorEmpleadosTemporal.rutaArchivo)
    return gestor


@pytest.fixture
def empleadoDePrueba(gestorEmpleadosTemporal):
    """Fixture que crea un empleado de prueba."""
    return gestorEmpleadosTemporal.agregarEmpleado("Empleado Test", "Cargo Test")


def testAsociarContrato(gestorContratosTemporal, empleadoDePrueba):
    """Prueba que se asocia un contrato a un empleado correctamente."""
    fechaInicio = "2024-01-01"
    fechaFin = "2024-12-31"
    salario = 5000.0
    
    contrato = gestorContratosTemporal.asociarContrato(
        empleadoDePrueba["id"], fechaInicio, fechaFin, salario
    )
    
    assert contrato is not None
    assert contrato["fecha_inicio"] == fechaInicio
    assert contrato["fecha_fin"] == fechaFin
    assert contrato["salario"] == salario
    assert "id_contrato" in contrato


def testAsociarContratoEmpleadoInexistente(gestorContratosTemporal):
    """Prueba que asociar contrato a empleado inexistente retorna None."""
    fechaInicio = "2024-01-01"
    fechaFin = "2024-12-31"
    salario = 5000.0
    
    contrato = gestorContratosTemporal.asociarContrato(999, fechaInicio, fechaFin, salario)
    assert contrato is None


def testAsociarContratoFechaInvalida(gestorContratosTemporal, empleadoDePrueba):
    """Prueba que asociar contrato con fecha inválida retorna None."""
    fechaInicio = "fecha-invalida"
    fechaFin = "2024-12-31"
    salario = 5000.0
    
    contrato = gestorContratosTemporal.asociarContrato(
        empleadoDePrueba["id"], fechaInicio, fechaFin, salario
    )
    assert contrato is None


def testObtenerContratosEmpleado(gestorContratosTemporal, empleadoDePrueba):
    """Prueba que se obtienen los contratos de un empleado."""
    # Asociar varios contratos
    fecha1 = "2023-01-01"
    fecha2 = "2024-01-01"
    fecha3 = "2025-01-01"
    
    gestorContratosTemporal.asociarContrato(
        empleadoDePrueba["id"], fecha1, "2023-12-31", 4000.0
    )
    gestorContratosTemporal.asociarContrato(
        empleadoDePrueba["id"], fecha2, "2024-12-31", 5000.0
    )
    gestorContratosTemporal.asociarContrato(
        empleadoDePrueba["id"], fecha3, "2025-12-31", 6000.0
    )
    
    contratos = gestorContratosTemporal.obtenerContratosEmpleado(empleadoDePrueba["id"])
    
    assert len(contratos) == 3


def testObtenerContratosEmpleadoSinContratos(gestorContratosTemporal, empleadoDePrueba):
    """Prueba que un empleado sin contratos retorna lista vacía."""
    contratos = gestorContratosTemporal.obtenerContratosEmpleado(empleadoDePrueba["id"])
    assert contratos == []


def testListarContratosVencidos(gestorContratosTemporal, gestorEmpleadosTemporal):
    """Prueba que se listan los contratos vencidos correctamente."""
    # Crear empleado con contrato vencido
    empleado = gestorEmpleadosTemporal.agregarEmpleado("Empleado Vencido", "Cargo")
    
    # Fecha de inicio hace 60 días, fecha de fin hace 1 día (cumple con mínimo de 30 días)
    fechaPasada = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
    fechaFinPasada = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    gestorContratosTemporal.asociarContrato(
        empleado["id"], fechaPasada, fechaFinPasada, 4000.0
    )
    
    contratosVencidos = gestorContratosTemporal.listarContratosVencidos()
    
    assert len(contratosVencidos) >= 1
    assert contratosVencidos[0]["empleado"]["id"] == empleado["id"]
    assert contratosVencidos[0]["contrato"]["fecha_fin"] == fechaFinPasada


def testListarContratosActivos(gestorContratosTemporal, gestorEmpleadosTemporal):
    """Prueba que se listan los contratos activos correctamente."""
    # Crear empleado con contrato activo
    empleado = gestorEmpleadosTemporal.agregarEmpleado("Empleado Activo", "Cargo")
    
    fechaInicio = datetime.now().strftime("%Y-%m-%d")
    fechaFin = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    
    gestorContratosTemporal.asociarContrato(
        empleado["id"], fechaInicio, fechaFin, 5000.0
    )
    
    contratosActivos = gestorContratosTemporal.listarContratosActivos()
    
    assert len(contratosActivos) >= 1
    assert contratosActivos[0]["empleado"]["id"] == empleado["id"]
    assert contratosActivos[0]["contrato"]["fecha_fin"] == fechaFin


def testIdsContratosIncrementales(gestorContratosTemporal, empleadoDePrueba):
    """Prueba que los IDs de contratos se generan de forma incremental."""
    contrato1 = gestorContratosTemporal.asociarContrato(
        empleadoDePrueba["id"], "2024-01-01", "2024-12-31", 4000.0
    )
    contrato2 = gestorContratosTemporal.asociarContrato(
        empleadoDePrueba["id"], "2025-01-01", "2025-12-31", 5000.0
    )
    
    assert contrato1["id_contrato"] < contrato2["id_contrato"]


def testAsociarContratoFechaFinMenorAMes(gestorContratosTemporal, empleadoDePrueba):
    """Prueba que asociar contrato con fecha de fin menor a un mes desde inicio retorna None."""
    fechaInicio = "2024-01-01"
    fechaFin = "2024-01-15"  # Solo 14 días después, menos de un mes
    salario = 5000.0
    
    contrato = gestorContratosTemporal.asociarContrato(
        empleadoDePrueba["id"], fechaInicio, fechaFin, salario
    )
    assert contrato is None


def testAsociarContratoFechaFinExactamenteUnMes(gestorContratosTemporal, empleadoDePrueba):
    """Prueba que asociar contrato con fecha de fin exactamente un mes después es válido."""
    fechaInicio = "2024-01-01"
    fechaFin = "2024-01-31"  # Exactamente 30 días después
    salario = 5000.0
    
    contrato = gestorContratosTemporal.asociarContrato(
        empleadoDePrueba["id"], fechaInicio, fechaFin, salario
    )
    
    assert contrato is not None
    assert contrato["fecha_inicio"] == fechaInicio
    assert contrato["fecha_fin"] == fechaFin
    assert contrato["salario"] == salario


def testAsociarContratoFechaFinMayorAMes(gestorContratosTemporal, empleadoDePrueba):
    """Prueba que asociar contrato con fecha de fin mayor a un mes es válido."""
    fechaInicio = "2024-01-01"
    fechaFin = "2024-02-15"  # Más de un mes después
    salario = 5000.0
    
    contrato = gestorContratosTemporal.asociarContrato(
        empleadoDePrueba["id"], fechaInicio, fechaFin, salario
    )
    
    assert contrato is not None
    assert contrato["fecha_inicio"] == fechaInicio
    assert contrato["fecha_fin"] == fechaFin
    assert contrato["salario"] == salario


def testValidarFechasContratoValidas(gestorContratosTemporal):
    """Prueba que validarFechasContrato retorna True para fechas válidas."""
    fechaInicio = "2024-01-01"
    fechaFin = "2024-02-01"  # Más de un mes después
    
    assert gestorContratosTemporal.validarFechasContrato(fechaInicio, fechaFin) is True


def testValidarFechasContratoMenorAMes(gestorContratosTemporal):
    """Prueba que validarFechasContrato retorna False para fechas con menos de un mes de diferencia."""
    fechaInicio = "2024-01-01"
    fechaFin = "2024-01-15"  # Menos de un mes después
    
    assert gestorContratosTemporal.validarFechasContrato(fechaInicio, fechaFin) is False


def testValidarFechasContratoFechaInvalida(gestorContratosTemporal):
    """Prueba que validarFechasContrato retorna False para fechas inválidas."""
    fechaInicio = "fecha-invalida"
    fechaFin = "2024-02-01"
    
    assert gestorContratosTemporal.validarFechasContrato(fechaInicio, fechaFin) is False


def testValidarFormatoFechaValida(gestorContratosTemporal):
    """Prueba que validarFormatoFecha retorna True para formato válido."""
    fecha = "2024-01-15"
    
    assert gestorContratosTemporal.validarFormatoFecha(fecha) is True


def testValidarFormatoFechaInvalida(gestorContratosTemporal):
    """Prueba que validarFormatoFecha retorna False para formato inválido."""
    fecha = "fecha-invalida"
    
    assert gestorContratosTemporal.validarFormatoFecha(fecha) is False


def testValidarFormatoFechaFormatoIncorrecto(gestorContratosTemporal):
    """Prueba que validarFormatoFecha retorna False para formatos incorrectos."""
    fecha1 = "2024/01/15"  # Separador incorrecto
    fecha2 = "01-15-2024"  # Orden incorrecto
    fecha3 = "24-01-15"    # Año de dos dígitos
    fecha4 = "fecha-invalida"  # Texto inválido
    fecha5 = "2024-13-45"  # Mes y día fuera de rango válido
    
    assert gestorContratosTemporal.validarFormatoFecha(fecha1) is False
    assert gestorContratosTemporal.validarFormatoFecha(fecha2) is False
    assert gestorContratosTemporal.validarFormatoFecha(fecha3) is False
    assert gestorContratosTemporal.validarFormatoFecha(fecha4) is False
    assert gestorContratosTemporal.validarFormatoFecha(fecha5) is False

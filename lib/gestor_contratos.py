"""
Módulo gestor_contratos.py
Maneja la asociación de contratos laborales a empleados.
Permite filtrar contratos activos y vencidos.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class GestorContratos:
    """Clase para gestionar contratos laborales de empleados."""
    
    def __init__(self, rutaArchivo: str = "data/empleados.json"):
        """
        Inicializa el gestor de contratos.
        
        Args:
            rutaArchivo: Ruta al archivo JSON donde se almacenan los empleados.
        """
        self.rutaArchivo = rutaArchivo
    
    def _cargarDatos(self) -> Dict:
        """
        Carga los datos del archivo JSON.
        
        Returns:
            Dict con la estructura de empleados.
        """
        if not os.path.exists(self.rutaArchivo):
            return {"empleados": []}
        
        try:
            with open(self.rutaArchivo, 'r', encoding='utf-8') as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, IOError):
            return {"empleados": []}
    
    def _guardarDatos(self, datos: Dict) -> bool:
        """
        Guarda los datos en el archivo JSON.
        
        Args:
            datos: Diccionario con la estructura de empleados.
            
        Returns:
            True si se guardó correctamente, False en caso contrario.
        """
        try:
            with open(self.rutaArchivo, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def _obtenerSiguienteIdContrato(self, contratos: List[Dict]) -> int:
        """
        Obtiene el siguiente ID disponible para un contrato.
        
        Args:
            contratos: Lista de contratos existentes.
            
        Returns:
            El siguiente ID disponible.
        """
        if not contratos:
            return 101
        return max(contrato.get('id_contrato', 100) for contrato in contratos) + 1
    
    def _parsearFecha(self, fechaStr: str) -> Optional[datetime]:
        """
        Parsea una cadena de fecha en formato YYYY-MM-DD.
        
        Args:
            fechaStr: Cadena de fecha en formato YYYY-MM-DD.
            
        Returns:
            Objeto datetime o None si el formato es inválido.
        """
        try:
            return datetime.strptime(fechaStr, "%Y-%m-%d")
        except ValueError:
            return None
    
    def validarFormatoFecha(self, fechaStr: str) -> bool:
        """
        Valida que una cadena tenga el formato de fecha válido (YYYY-MM-DD).
        
        Args:
            fechaStr: Cadena de fecha a validar.
            
        Returns:
            True si el formato es válido, False en caso contrario.
        """
        return self._parsearFecha(fechaStr) is not None
    
    def validarFechasContrato(self, fechaInicio: str, fechaFin: str) -> bool:
        """
        Valida que las fechas sean válidas y que la fecha de fin sea al menos un mes posterior a la fecha de inicio.
        
        Args:
            fechaInicio: Fecha de inicio del contrato (YYYY-MM-DD).
            fechaFin: Fecha de fin del contrato (YYYY-MM-DD).
            
        Returns:
            True si las fechas son válidas y la fecha de fin es al menos un mes posterior a la fecha de inicio.
            False en caso contrario.
        """
        fechaInicioParsed = self._parsearFecha(fechaInicio)
        fechaFinParsed = self._parsearFecha(fechaFin)
        
        if not fechaInicioParsed or not fechaFinParsed:
            return False
        
        # Validar que la fecha de fin sea al menos un mes mayor que la fecha de inicio
        fechaMinimaFin = fechaInicioParsed + timedelta(days=30)
        if fechaFinParsed < fechaMinimaFin:
            return False
        
        return True
    
    def asociarContrato(self, idEmpleado: int, fechaInicio: str, 
                       fechaFin: str, salario: float) -> Optional[Dict]:
        """
        Asocia un contrato laboral a un empleado.
        
        Args:
            idEmpleado: ID del empleado.
            fechaInicio: Fecha de inicio del contrato (YYYY-MM-DD).
            fechaFin: Fecha de fin del contrato (YYYY-MM-DD). Debe ser al menos un mes posterior a la fecha de inicio.
            salario: Salario del contrato.
            
        Returns:
            Dict con la información del contrato creado o None si falló.
            Retorna None si las fechas son inválidas, la fecha de fin es menor a un mes
            desde la fecha de inicio, o el empleado no existe.
        """
        datos = self._cargarDatos()
        empleados = datos.get("empleados", [])
        
        # Validar fechas
        fechaInicioParsed = self._parsearFecha(fechaInicio)
        fechaFinParsed = self._parsearFecha(fechaFin)
        
        if not fechaInicioParsed or not fechaFinParsed:
            return None
        
        # Validar que la fecha de fin sea al menos un mes mayor que la fecha de inicio
        fechaMinimaFin = fechaInicioParsed + timedelta(days=30)
        if fechaFinParsed < fechaMinimaFin:
            return None
        
        empleadoEncontrado = None
        for empleado in empleados:
            if empleado.get("id") == idEmpleado:
                empleadoEncontrado = empleado
                break
        
        if not empleadoEncontrado:
            return None
        
        contratos = empleadoEncontrado.get("contratos", [])
        nuevoContrato = {
            "id_contrato": self._obtenerSiguienteIdContrato(contratos),
            "fecha_inicio": fechaInicio,
            "fecha_fin": fechaFin,
            "salario": salario
        }
        
        contratos.append(nuevoContrato)
        empleadoEncontrado["contratos"] = contratos
        
        datos["empleados"] = empleados
        if self._guardarDatos(datos):
            return nuevoContrato
        return None
    
    def listarContratosVencidos(self) -> List[Dict]:
        """
        Lista todos los contratos vencidos con información del empleado.
        
        Returns:
            Lista de diccionarios con información del empleado y su contrato vencido.
        """
        datos = self._cargarDatos()
        empleados = datos.get("empleados", [])
        contratosVencidos = []
        fechaActual = datetime.now()
        
        for empleado in empleados:
            contratos = empleado.get("contratos", [])
            for contrato in contratos:
                fechaFin = self._parsearFecha(contrato.get("fecha_fin", ""))
                if fechaFin and fechaFin < fechaActual:
                    contratosVencidos.append({
                        "empleado": {
                            "id": empleado.get("id"),
                            "nombre": empleado.get("nombre"),
                            "cargo": empleado.get("cargo")
                        },
                        "contrato": contrato
                    })
        
        return contratosVencidos
    
    def listarContratosActivos(self) -> List[Dict]:
        """
        Lista todos los contratos activos con información del empleado.
        
        Returns:
            Lista de diccionarios con información del empleado y su contrato activo.
        """
        datos = self._cargarDatos()
        empleados = datos.get("empleados", [])
        contratosActivos = []
        fechaActual = datetime.now()
        
        for empleado in empleados:
            contratos = empleado.get("contratos", [])
            for contrato in contratos:
                fechaFin = self._parsearFecha(contrato.get("fecha_fin", ""))
                if fechaFin and fechaFin >= fechaActual:
                    contratosActivos.append({
                        "empleado": {
                            "id": empleado.get("id"),
                            "nombre": empleado.get("nombre"),
                            "cargo": empleado.get("cargo")
                        },
                        "contrato": contrato
                    })
        
        return contratosActivos
    
    def obtenerContratosEmpleado(self, idEmpleado: int) -> List[Dict]:
        """
        Obtiene todos los contratos de un empleado.
        
        Args:
            idEmpleado: ID del empleado.
            
        Returns:
            Lista de contratos del empleado.
        """
        datos = self._cargarDatos()
        empleados = datos.get("empleados", [])
        
        for empleado in empleados:
            if empleado.get("id") == idEmpleado:
                return empleado.get("contratos", [])
        return []


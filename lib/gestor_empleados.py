"""
Módulo gestor_empleados.py
Maneja la creación, actualización, eliminación y consulta de empleados.
Guarda la información en empleados.json.
"""

import json
import os
from typing import Dict, List, Optional


class GestorEmpleados:
    """Clase para gestionar empleados y sus operaciones CRUD."""
    
    def __init__(self, rutaArchivo: str = "data/empleados.json"):
        """
        Inicializa el gestor de empleados.
        
        Args:
            rutaArchivo: Ruta al archivo JSON donde se almacenan los empleados.
        """
        self.rutaArchivo = rutaArchivo
        self._asegurarDirectorio()
    
    def _asegurarDirectorio(self) -> None:
        """Asegura que el directorio del archivo existe."""
        directorio = os.path.dirname(self.rutaArchivo)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)
    
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
    
    def _obtenerSiguienteId(self, empleados: List[Dict]) -> int:
        """
        Obtiene el siguiente ID disponible para un empleado.
        
        Args:
            empleados: Lista de empleados existentes.
            
        Returns:
            El siguiente ID disponible.
        """
        if not empleados:
            return 1
        return max(empleado.get('id', 0) for empleado in empleados) + 1
    
    def agregarEmpleado(self, nombre: str, cargo: str) -> Optional[Dict]:
        """
        Agrega un nuevo empleado al sistema.
        
        Args:
            nombre: Nombre completo del empleado.
            cargo: Cargo del empleado.
            
        Returns:
            Dict con la información del empleado creado o None si falló.
        """
        datos = self._cargarDatos()
        empleados = datos.get("empleados", [])
        
        nuevoEmpleado = {
            "id": self._obtenerSiguienteId(empleados),
            "nombre": nombre,
            "cargo": cargo,
            "contratos": []
        }
        
        empleados.append(nuevoEmpleado)
        datos["empleados"] = empleados
        
        if self._guardarDatos(datos):
            return nuevoEmpleado
        return None
    
    def eliminarEmpleado(self, idEmpleado: int) -> bool:
        """
        Elimina un empleado del sistema.
        
        Args:
            idEmpleado: ID del empleado a eliminar.
            
        Returns:
            True si se eliminó correctamente, False en caso contrario.
        """
        datos = self._cargarDatos()
        empleados = datos.get("empleados", [])
        
        empleadosOriginales = len(empleados)
        empleados = [emp for emp in empleados if emp.get("id") != idEmpleado]
        
        if len(empleados) < empleadosOriginales:
            datos["empleados"] = empleados
            return self._guardarDatos(datos)
        return False
    
    def buscarEmpleado(self, idEmpleado: int) -> Optional[Dict]:
        """
        Busca un empleado por su ID.
        
        Args:
            idEmpleado: ID del empleado a buscar.
            
        Returns:
            Dict con la información del empleado o None si no se encuentra.
        """
        datos = self._cargarDatos()
        empleados = datos.get("empleados", [])
        
        for empleado in empleados:
            if empleado.get("id") == idEmpleado:
                return empleado
        return None
    
    def listarEmpleados(self) -> List[Dict]:
        """
        Lista todos los empleados.
        
        Returns:
            Lista de diccionarios con la información de los empleados.
        """
        datos = self._cargarDatos()
        return datos.get("empleados", [])
    
    def actualizarEmpleado(self, idEmpleado: int, nombre: Optional[str] = None, 
                          cargo: Optional[str] = None) -> Optional[Dict]:
        """
        Actualiza la información de un empleado.
        
        Args:
            idEmpleado: ID del empleado a actualizar.
            nombre: Nuevo nombre (opcional).
            cargo: Nuevo cargo (opcional).
            
        Returns:
            Dict con la información actualizada del empleado o None si no se encontró.
        """
        datos = self._cargarDatos()
        empleados = datos.get("empleados", [])
        
        for empleado in empleados:
            if empleado.get("id") == idEmpleado:
                if nombre is not None:
                    empleado["nombre"] = nombre
                if cargo is not None:
                    empleado["cargo"] = cargo
                
                datos["empleados"] = empleados
                if self._guardarDatos(datos):
                    return empleado
                return None
        return None


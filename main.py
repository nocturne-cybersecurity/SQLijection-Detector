#!/usr/bin/env python3
"""
ShadowJava - Herramienta de detección de amenazas de seguridad en logs de aplicaciones Java.
"""

import logging
from typing import Optional, Dict, Any
from detectors import SQLInjectionDetector

# Configuración básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ShadowJava:
    """Clase principal de la aplicación ShadowJava."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Inicializa la aplicación con la configuración proporcionada."""
        self.config = config or {}
        self.detectors = self._initialize_detectors()
    
    def _initialize_detectors(self) -> list:
        """Inicializa los detectores de amenazas."""
        return [
            SQLInjectionDetector()
            # Agregar más detectores aquí según sea necesario
        ]
    
    def analyze_log(self, log_entry: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Analiza una entrada de log con todos los detectores configurados.
        
        Args:
            log_entry: Línea de log a analizar.
            context: Contexto adicional para el análisis.
            
        Returns:
            bool: True si se detectó alguna amenaza, False en caso contrario.
        """
        if not log_entry.strip():
            return False
            
        context = context or {}
        threat_detected = False
        
        for detector in self.detectors:
            try:
                if detector.process(log_entry, context):
                    threat_detected = True
            except Exception as e:
                logger.error(f"Error al procesar con {detector.name}: {e}", exc_info=True)
        
        return threat_detected


def main():
    """Función principal de la aplicación."""
    try:
        # Crear instancia de la aplicación
        app = ShadowJava()
        
        # Ejemplo de uso
        test_logs = [
            "SELECT * FROM users",  # Consulta SQL normal
            "SELECT * FROM users WHERE username = 'admin' OR '1'='1'"  # Posible inyección SQL
        ]
        
        for log in test_logs:
            print(f"\nAnalizando: {log}")
            if app.analyze_log(log):
                print("¡Amenaza detectada!")
            else:
                print("No se detectaron amenazas.")
                
    except Exception as e:
        logger.critical(f"Error en la aplicación: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

import re
from typing import Dict, Any, Optional, List, Pattern

from .base_detector import BaseDetector, AnomalyDetected

class SQLInjectionDetector(BaseDetector):
    """
    Detecta patrones comunes de inyección SQL en los logs.
    """
    
    # Patrones comunes de inyección SQL
    DEFAULT_PATTERNS = [
        # Patrones de consultas SQL
        r'(?i)(?:select\s.*from|insert\s+into|update\s+\w+\s+set|delete\s+from)',
        r'(?i)(?:union\s+select|union\s+all\s+select)',
        r'(?i)(?:drop\s+table|truncate\s+table|create\s+table)',
        
        # Técnicas de evasión
        r'(?:/\*.*?\*/|--|#|\/\*\*\/)',
        r'(?:\'\s*(?:--|#|\/\*|;|\|\|)',
        r'(?:\'\s*\+\s*\'\s*\+\s*\')',
        
        # Inyección basada en tiempo
        r'(?i)(?:waitfor\s+delay|sleep\s*\(|benchmark\s*\()',
        
        # Inyecciones ciegas
        r'(?i)(?:if\s*\([^)]*\)\s*[=<>]+\s*\d+\s*,\s*\w+\s*,\s*\w+\))',
        
        # Comentarios SQL
        r'(?:/\*!\d{5}.*?\*/)'
    ]
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el detector de inyección SQL.
        
        Args:
            config: Configuración del detector.
        """
        config = config or {}
        
        # Combinar patrones por defecto con los proporcionados en la configuración
        custom_patterns = config.get('patterns', [])
        config['patterns'] = self.DEFAULT_PATTERNS + custom_patterns
        
        # Inicializar la clase base primero
        super().__init__('sql_injection', config)
        
        # Configurar propiedades específicas del detector
        self.threshold = config.get('threshold', 3)
        self.match_count = 0
    
    def analyze(self, log_entry: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Analiza una entrada de log en busca de patrones de inyección SQL.
        
        Args:
            log_entry: Línea de log a analizar.
            context: Contexto adicional para el análisis.
            
        Returns:
            True si se detecta una inyección SQL, False en caso contrario.
            
        Raises:
            AnomalyDetected: Si se detecta un patrón de inyección SQL.
        """
        if not self.enabled:
            return False
            
        context = context or {}
        
        # Verificar cada patrón
        for pattern in self.patterns:
            if pattern.search(log_entry):
                self.match_count += 1
                
                # Si superamos el umbral, lanzamos la alerta
                if self.match_count >= self.threshold:
                    # Obtener información de la IP si está disponible en el contexto
                    ip_address = context.get('ip_address', 'desconocida')
                    
                    raise AnomalyDetected(
                        message=f"Posible inyección SQL detectada desde la IP {ip_address}",
                        severity='high',
                        context={
                            'detector': self.name,
                            'pattern': pattern.pattern,
                            'log_entry': log_entry,
                            'match_count': self.match_count,
                            'ip_address': ip_address,
                            'timestamp': context.get('timestamp')
                        }
                    )
                
                return True
                
        # Si no se encontraron coincidencias, reiniciamos el contador
        self.match_count = 0
        return False

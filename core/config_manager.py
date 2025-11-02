
import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:

    _instance = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        """Implementación del patrón Singleton."""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def load_config(self, config_path: str) -> None:
        """
        Carga la configuración desde un archivo YAML.
        
        Args:
            config_path: Ruta al archivo de configuración.
            
        Raises:
            FileNotFoundError: Si el archivo de configuración no existe.
            yaml.YAMLError: Si hay un error al analizar el archivo YAML.
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"El archivo de configuración no existe: {config_path}")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            self._config = yaml.safe_load(f)
        
        # Crear directorios necesarios
        self._create_required_dirs()
    
    def _create_required_dirs(self) -> None:
        """Crea los directorios necesarios especificados en la configuración."""
        # Crear directorio de logs si no existe
        log_file = self.get('system.log_file', '')
        if log_file:
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)
        
        # Crear directorio de reportes
        reports_dir = self.get('reports.output_dir', '')
        if reports_dir and not os.path.exists(reports_dir):
            os.makedirs(reports_dir, exist_ok=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de configuración usando notación de puntos.
        
        Ejemplo:
            config.get('system.log_level')
            
        Args:
            key: Clave de configuración en notación de puntos.
            default: Valor por defecto si la clave no existe.
            
        Returns:
            El valor de configuración o el valor por defecto si no existe.
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_detectors_config(self) -> Dict[str, Any]:
        """
        Obtiene la configuración de los detectores.
        
        Returns:
            Diccionario con la configuración de los detectores.
        """
        return self._config.get('detectors', {})
    
    def get_alert_config(self) -> Dict[str, Any]:
        """
        Obtiene la configuración de alertas.
        
        Returns:
            Diccionario con la configuración de alertas.
        """
        return self._config.get('alerts', {})
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """
        Obtiene la configuración de monitoreo.
        
        Returns:
            Diccionario con la configuración de monitoreo.
        """
        return self._config.get('monitoring', {})

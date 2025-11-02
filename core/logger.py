
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from colorama import Fore, Style, init as colorama_init

class ShadowGuardFormatter(logging.Formatter):
    
    # Colores para los diferentes niveles de log
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }
    
    def format(self, record):
        # Obtener el nombre del módulo sin la ruta completa
        module_parts = record.name.split('.')
        if len(module_parts) > 2:
            record.module = '.'.join(module_parts[-2:])
        else:
            record.module = record.name
            
        # Formatear el mensaje
        log_fmt = (
            f"{Fore.WHITE}{{asctime}}{Style.RESET_ALL} | "
            f"{{levelname:8}} | "
            f"{{module}}:{{lineno}} - {{message}}"
        )
        
        # Aplicar color al nivel de log
        level_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{level_color}{record.levelname}{Style.RESET_ALL}"
        
        formatter = logging.Formatter(log_fmt, style='{')
        return formatter.format(record)


def setup_logger(
    name: str = 'shadowguard',
    log_level: str = 'INFO',
    log_file: Optional[str] = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configura el logger de la aplicación.
    
    Args:
        name: Nombre del logger.
        log_level: Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Ruta al archivo de log. Si es None, solo se usa consola.
        max_bytes: Tamaño máximo del archivo de log antes de rotar.
        backup_count: Número de archivos de respaldo a mantener.
        
    Returns:
        Logger configurado.
    """
    # Inicializar colorama
    colorama_init()
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Evitar que los mensajes se propaguen al logger raíz
    logger.propagate = False
    
    # Eliminar manejadores existentes
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Configurar formateador
    formatter = ShadowGuardFormatter()
    
    # Configurar manejador de consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Configurar manejador de archivo si se especificó
    if log_file:
        # Crear directorio si no existe
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s'
        ))
        logger.addHandler(file_handler)
    
    return logger

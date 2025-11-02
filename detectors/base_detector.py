import re
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Pattern, Union, Sequence

logger = logging.getLogger(__name__)


class AnomalyDetected(Exception):
    """Excepción personalizada para representar una anomalía detectada."""

    def __init__(self, message: str, severity: str = 'medium', context: Optional[Dict[str, Any]] = None):
        """
        Args:
            message: Descripción del evento anómalo.
            severity: Nivel de severidad ('low', 'medium', 'high', 'critical').
            context: Información contextual adicional.
        """
        self.message = message
        self.severity = severity
        self.context = context or {}
        super().__init__(self.message)


class BaseDetector(ABC):
    """Clase base abstracta para detectores de anomalías."""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa el detector base.

        Args:
            name: Nombre único del detector.
            config: Configuración específica del detector.
        """
        self.name = name
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.patterns = self._compile_patterns(self.config.get('patterns', []))
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def _compile_patterns(self, patterns: Sequence[Union[str, Pattern]]) -> List[Pattern]:
        """
        Compila una lista de patrones regex.

        Args:
            patterns: Lista de patrones regex (strings o Pattern ya compilados).

        Returns:
            Lista de objetos Pattern compilados.
        """
        compiled_patterns: List[Pattern] = []
        for pattern in patterns:
            if isinstance(pattern, str):
                try:
                    compiled = re.compile(pattern, re.IGNORECASE)
                    compiled_patterns.append(compiled)
                except re.error as e:
                    self.logger.error(f"Error al compilar el patrón '{pattern}': {e}")
            elif isinstance(pattern, Pattern):
                compiled_patterns.append(pattern)
            else:
                self.logger.warning(f"Tipo de patrón no soportado: {type(pattern)}")
        return compiled_patterns

    @abstractmethod
    def analyze(self, log_entry: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Analiza una línea de log en busca de anomalías.

        Args:
            log_entry: Línea de log a analizar.
            context: Contexto adicional para el análisis.

        Returns:
            True si se detecta una anomalía, False en caso contrario.

        Raises:
            AnomalyDetected: Si se detecta una anomalía.
        """
        ...

    def process(self, log_entry: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Procesa una línea de log con manejo de excepciones.

        Args:
            log_entry: Línea de log a procesar.
            context: Contexto adicional para el procesamiento.

        Returns:
            True si se detectó una anomalía, False en caso contrario o si ocurre un error.
        """
        if not self.enabled or not log_entry:
            return False

        context = context or {}

        try:
            return self.analyze(log_entry, context)

        except AnomalyDetected as e:
            # Registra la anomalía detectada pero no la propaga
            self.logger.warning(
                f"Anomalía detectada por {self.name}: {e.message}",
                extra={
                    'detector': self.name,
                    'severity': e.severity,
                    'context': {**e.context, 'original_context': context},
                    'log_entry': log_entry[:1000]
                }
            )
            return True

        except Exception as e:
            # Registra el error y continúa
            self.logger.error(
                f"Error en el detector {self.name}: {str(e)}",
                exc_info=True,
                extra={
                    'detector': self.name,
                    'log_entry': log_entry[:1000],
                    'context': context
                }
            )
            return False

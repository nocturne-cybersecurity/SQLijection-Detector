# 🛡️ ShadowGuard

Framework de detección de anomalías en tiempo real para servidores Java y aplicaciones web.

## Características

- 🕵️ Monitoreo en tiempo real de logs
- 🔍 Detección de patrones sospechosos
- ⚙️ Configuración basada en YAML/JSON
- 🔔 Alertas por correo y webhooks
- 🧩 Arquitectura modular

## Requisitos

- Python 3.11+
- Pipenv (recomendado)

## Instalación

```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd ShadowGuard

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

1. Copia el archivo de configuración de ejemplo:
   ```bash
   cp config/config.example.yaml config/config.yaml
   ```
2. Edita el archivo `config.yaml` con tus preferencias

## Uso

```bash
python -m shadowguard --config config/config.yaml
```

## Estructura del Proyecto

```
ShadowGuard/
├── config/           # Archivos de configuración
├── core/            # Núcleo del framework
├── detectors/       # Módulos de detección
├── utils/           # Utilidades
├── output/          # Salida de logs y reportes
└── tests/           # Pruebas unitarias
```

## Licencia

MIT License

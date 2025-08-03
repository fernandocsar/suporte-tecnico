"""Configurações do Sistema de Suporte Técnico"""

import os
from typing import List, Dict

# Configurações de rede
NETWORK_CONFIG = {
    "timeout_ping": 5,
    "timeout_commands": 30,
    "timeout_gpupdate": 300,
    "test_hosts": ["8.8.8.8", "google.com", "github.com"],
    "dns_servers": ["8.8.8.8", "8.8.4.4", "1.1.1.1"],
}

# Configurações do sistema
SYSTEM_CONFIG = {
    "temp_paths": [
        os.path.expandvars("%TEMP%"),
        os.path.expandvars("%WINDIR%\\Temp"),
        os.path.expandvars("%LOCALAPPDATA%\\Temp"),
    ],
    "spooler_path": "C:\\Windows\\System32\\spool\\PRINTERS",
    "min_disk_space_gb": 5,
    "max_cpu_percent": 80,
    "max_memory_percent": 80,
}

# Configurações de interface
UI_CONFIG = {
    "menu_width": 60,
    "auto_return_delay": 3,
    "progress_delay": 2,
    "use_emojis": True,
    "clear_screen": False,  # Mantém histórico
}

# Configurações de encoding
ENCODING_CONFIG = {
    "default_encoding": "cp1252",
    "fallback_encodings": ["utf-8", "latin1"],
    "corrections": {
        "‡Æo": "ção",
        "¡": "í",
        "ˆ": "ê",
        "Pol¡tica": "Política",
        "Usu rio": "Usuário",
        "atualiza‡Æo": "atualização",
        "conclu¡da": "concluída",
        "ˆxito": "êxito",
    },
}

# Configurações de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "suporte_tecnico.log",
    "max_size_mb": 10,
    "backup_count": 5,
}

# Versão do sistema
VERSION = "1.0.0"
APP_NAME = "Sistema de Suporte Técnico"
AUTHOR = "Equipe de Desenvolvimento"

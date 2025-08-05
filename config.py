"""Configurações do Sistema de Suporte Técnico"""

import os
from typing import List, Dict

# Configurações do Sistema de Suporte Técnico

# Informações do sistema
VERSION = "1.1.0"
APP_NAME = "Sistema de Suporte Técnico"
AUTHOR = "Equipe de Desenvolvimento"

# Configurações de rede
NETWORK_CONFIG = {
    "timeout_ping": 5,
    "timeout_dns": 10,
    "timeout_gpupdate": 60,
    "servidores_teste": ["8.8.8.8", "google.com", "github.com"],
    "max_tentativas": 3
}

# Configurações de interface
UI_CONFIG = {
    "menu_width": 60,
    "auto_return_delay": 3,
    "progress_bar_width": 40
}

# Configurações de sistema
SYSTEM_CONFIG = {
    "timeout_comandos": 30,
    "max_tamanho_log": 10 * 1024 * 1024,  # 10MB
    "backup_logs": 5,
    "encoding_padrao": "utf-8"
}

# Configurações de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "arquivo": "suporte_tecnico.log",
    "max_bytes": 5 * 1024 * 1024,  # 5MB
    "backup_count": 3
}

# Configurações de programas
PROGRAMS_CONFIG = {
    "max_cpu_percent": 50,
    "max_memory_percent": 20,
    "cache_paths": [
        "%APPDATA%\\Microsoft\\Windows\\INetCache",
        "%LOCALAPPDATA%\\Microsoft\\Windows\\INetCache",
        "%TEMP%",
        "%LOCALAPPDATA%\\Temp"
    ],
    "registry_keys_to_clean": [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU",
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU"
    ]
}

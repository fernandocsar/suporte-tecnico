"""Módulo de utilitários gerais"""

import os
import subprocess
import logging
from typing import Optional, List
from config import ENCODING_CONFIG, LOGGING_CONFIG


def configurar_logging() -> None:
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG["level"]),
        format=LOGGING_CONFIG["format"],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG["file"], encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def limpar_tela() -> None:
    """Limpa a tela do terminal (desabilitado por padrão)"""
    # Função mantida para compatibilidade, mas não utilizada
    pass


def corrigir_encoding_windows(texto: str) -> str:
    """Corrige problemas de encoding do Windows para português

    Args:
        texto: Texto a ser corrigido

    Returns:
        Texto com encoding corrigido
    """
    if not texto:
        return texto

    texto_corrigido = texto
    for erro, correcao in ENCODING_CONFIG["corrections"].items():
        texto_corrigido = texto_corrigido.replace(erro, correcao)

    return texto_corrigido


def executar_comando_seguro(
    comando: str, timeout: int = 30, encoding: str = None
) -> Optional[subprocess.CompletedProcess]:
    """Executa comando de forma segura com tratamento de erros

    Args:
        comando: Comando a ser executado
        timeout: Timeout em segundos
        encoding: Encoding a ser usado

    Returns:
        Resultado do comando ou None em caso de erro
    """
    if encoding is None:
        encoding = ENCODING_CONFIG["default_encoding"]

    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Executando comando: {comando}")

        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            encoding=encoding,
            timeout=timeout,
        )

        logger.info(f"Comando executado com código: {resultado.returncode}")
        return resultado

    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout ao executar comando: {comando}")
        return None
    except UnicodeDecodeError:
        # Tenta encodings alternativos
        for alt_encoding in ENCODING_CONFIG["fallback_encodings"]:
            try:
                resultado = subprocess.run(
                    comando,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding=alt_encoding,
                    timeout=timeout,
                )
                logger.info(f"Comando executado com encoding {alt_encoding}")
                return resultado
            except:
                continue

        logger.error(f"Erro de encoding ao executar comando: {comando}")
        return None
    except Exception as e:
        logger.error(f"Erro ao executar comando {comando}: {e}")
        return None


def validar_entrada_menu(entrada: str, opcoes_validas: List[str]) -> bool:
    """Valida entrada do usuário no menu

    Args:
        entrada: Entrada do usuário
        opcoes_validas: Lista de opções válidas

    Returns:
        True se a entrada é válida, False caso contrário
    """
    return entrada.strip() in opcoes_validas


def formatar_tamanho_arquivo(tamanho_bytes: int) -> str:
    """Formata tamanho de arquivo em formato legível

    Args:
        tamanho_bytes: Tamanho em bytes

    Returns:
        Tamanho formatado (ex: "1.5 GB")
    """
    for unidade in ["B", "KB", "MB", "GB", "TB"]:
        if tamanho_bytes < 1024.0:
            return f"{tamanho_bytes:.1f} {unidade}"
        tamanho_bytes /= 1024.0
    return f"{tamanho_bytes:.1f} PB"


def verificar_privilegios_admin() -> bool:
    """Verifica se o script está sendo executado como administrador

    Returns:
        True se tem privilégios de administrador, False caso contrário
    """
    try:
        import ctypes

        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def exibir_aviso_admin() -> None:
    """Exibe aviso sobre privilégios de administrador"""
    if not verificar_privilegios_admin():
        print(
            "\n⚠️ AVISO: Algumas funcionalidades podem requerer privilégios de administrador."
        )
        print("   Para melhor resultado, execute como Administrador.\n")

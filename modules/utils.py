"""Módulo de utilitários gerais"""

import os
import subprocess
import logging
from typing import Optional, List
from config import LOGGING_CONFIG, SYSTEM_CONFIG


def configurar_logging() -> None:
    """Configura o sistema de logging"""
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG["level"]),
        format=LOGGING_CONFIG["format"],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG["arquivo"], encoding="utf-8"),
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

    # Correções básicas de encoding
    correcoes = {
        "‡Æo": "ção",
        "¡": "í",
        "ˆ": "ê",
        "Pol¡tica": "Política",
        "Usu rio": "Usuário",
        "atualiza‡Æo": "atualização",
        "conclu¡da": "concluída",
        "ˆxito": "êxito",
    }

    texto_corrigido = texto
    for erro, correcao in correcoes.items():
        texto_corrigido = texto_corrigido.replace(erro, correcao)

    return texto_corrigido


def executar_comando_seguro(
    comando: str, timeout: int = 30, encoding: str = None, input: str = None
) -> Optional[subprocess.CompletedProcess]:
    """Executa comando de forma segura com tratamento de erros

    Args:
        comando: Comando a ser executado
        timeout: Timeout em segundos
        encoding: Encoding a ser usado
        input: Input para o comando

    Returns:
        Resultado do comando ou None em caso de erro
    """
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Executando comando: {comando}")

        # Prepara o input se fornecido
        input_data = None
        if input:
            input_data = input

        # Tenta primeiro com encoding padrão do Windows
        try:
            resultado = subprocess.run(
                comando,
                shell=True,
                capture_output=True,
                text=True,
                encoding="cp1252",  # Encoding padrão do Windows
                timeout=timeout,
                input=input_data,
            )
            logger.info(f"Comando executado com código: {resultado.returncode}")
            return resultado

        except UnicodeDecodeError:
            # Se falhar, tenta com outros encodings
            encodings_alternativos = ["latin1", "utf-8", "iso-8859-1"]
            
            for alt_encoding in encodings_alternativos:
                try:
                    resultado = subprocess.run(
                        comando,
                        shell=True,
                        capture_output=True,
                        text=True,
                        encoding=alt_encoding,
                        timeout=timeout,
                        input=input_data,
                    )
                    logger.info(f"Comando executado com encoding {alt_encoding}")
                    return resultado
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    logger.warning(f"Erro com encoding {alt_encoding}: {str(e)}")
                    continue

            # Se todos os encodings falharem, tenta sem especificar encoding
            try:
                resultado = subprocess.run(
                    comando,
                    shell=True,
                    capture_output=True,
                    timeout=timeout,
                    input=input_data.encode() if input_data else None,
                )
                
                # Decodifica manualmente a saída
                try:
                    stdout = resultado.stdout.decode("cp1252", errors="replace")
                except:
                    stdout = resultado.stdout.decode("utf-8", errors="replace")
                
                try:
                    stderr = resultado.stderr.decode("cp1252", errors="replace")
                except:
                    stderr = resultado.stderr.decode("utf-8", errors="replace")
                
                # Cria um objeto similar ao CompletedProcess
                class CompletedProcessWrapper:
                    def __init__(self, returncode, stdout, stderr):
                        self.returncode = returncode
                        self.stdout = stdout
                        self.stderr = stderr
                
                logger.info(f"Comando executado com decodificação manual")
                return CompletedProcessWrapper(resultado.returncode, stdout, stderr)
                
            except Exception as e:
                logger.error(f"Erro na execução sem encoding: {str(e)}")
                return None

    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout ao executar comando: {comando}")
        return None
    except Exception as e:
        logger.error(f"Erro ao executar comando {comando}: {str(e)}")
        return None


def validar_entrada_menu(entrada: str, opcoes_validas: List[str]) -> bool:
    """Valida entrada do menu

    Args:
        entrada: Entrada do usuário
        opcoes_validas: Lista de opções válidas

    Returns:
        True se a entrada é válida, False caso contrário
    """
    return entrada.strip() in opcoes_validas


def formatar_tamanho_arquivo(tamanho_bytes: int) -> str:
    """Formata tamanho de arquivo em bytes para formato legível

    Args:
        tamanho_bytes: Tamanho em bytes

    Returns:
        String formatada (ex: "1.5 MB", "2.3 GB")
    """
    if tamanho_bytes == 0:
        return "0 B"

    unidades = ["B", "KB", "MB", "GB", "TB"]
    tamanho = float(tamanho_bytes)
    unidade_index = 0

    while tamanho >= 1024 and unidade_index < len(unidades) - 1:
        tamanho /= 1024
        unidade_index += 1

    return f"{tamanho:.1f} {unidades[unidade_index]}"


def verificar_privilegios_admin() -> bool:
    """Verifica se o programa está sendo executado como administrador

    Returns:
        True se tem privilégios de administrador, False caso contrário
    """
    try:
        # Tenta criar um arquivo no diretório do sistema
        test_file = os.path.join(
            os.environ.get("WINDIR", "C:\\Windows"), "test_admin.tmp"
        )
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        return True
    except:
        return False


def exibir_aviso_admin() -> None:
    """Exibe aviso sobre privilégios de administrador"""
    if not verificar_privilegios_admin():
        print(
            "\n⚠️  AVISO: Este programa funciona melhor com privilégios de administrador."
        )
        print("💡 Para obter os melhores resultados, execute como administrador.")
        print("   Algumas funcionalidades podem não funcionar corretamente.\n")
        input("Pressione ENTER para continuar...")
    else:
        print("\n✅ Executando com privilégios de administrador.\n")

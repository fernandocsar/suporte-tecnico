import os
import subprocess


def limpar_tela():
    """Limpa a tela do terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def corrigir_encoding_windows(texto):
    """Corrige problemas de encoding do Windows para português"""
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


def executar_comando_seguro(comando, timeout=30, encoding="cp1252"):
    """Executa comando de forma segura com tratamento de erros"""
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True,
            encoding=encoding,
            timeout=timeout,
        )
        return resultado
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"Erro ao executar comando: {e}")
        return None

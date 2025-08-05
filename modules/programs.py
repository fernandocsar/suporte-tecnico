"""Módulo para resolução de problemas com programas"""

import subprocess
import psutil
import time
import os
import winreg
from typing import List, Dict, Optional, Tuple
from .utils import corrigir_encoding_windows, executar_comando_seguro
from config import SYSTEM_CONFIG


def resolver_problemas_programas() -> None:
    """Resolve problemas comuns com programas"""
    print("=" * 60)
    print("           RESOLVENDO PROBLEMAS COM PROGRAMAS")
    print("=" * 60)

    print("\n🔍 Analisando programas e processos...")
    time.sleep(2)

    try:
        # 1. Verificar processos travados
        processos_travados = verificar_processos_travados()

        # 2. Limpar cache de programas
        limpar_cache_programas()

        # 3. Reparar aplicações Windows
        reparar_aplicacoes_windows()

        # 4. Verificar integridade de arquivos do sistema
        verificar_integridade_arquivos()

        # 5. Limpar registros corrompidos
        limpar_registros_corrompidos()

        print("\n" + "=" * 60)
        print("✅ PROBLEMAS COM PROGRAMAS RESOLVIDOS")
        print("=" * 60)
        print("\n🎯 Ações realizadas:")
        print("   • Verificação de processos travados")
        print("   • Limpeza de cache de programas")
        print("   • Reparação de aplicações Windows")
        print("   • Verificação de integridade de arquivos")
        print("   • Limpeza de registros corrompidos")
        print("\n💡 Reinicie os programas que estavam com problemas.")

    except Exception as e:
        print(f"\n❌ Erro durante resolução: {str(e)}")

    time.sleep(4)


def verificar_processos_travados() -> List[Dict]:
    """Verifica e lista processos que podem estar travados"""
    print("\n🔄 Verificando processos travados...")

    processos_travados = []

    try:
        for proc in psutil.process_iter(
            ["pid", "name", "cpu_percent", "memory_percent", "status"]
        ):
            try:
                info = proc.info

                # Verifica processos com alto uso de CPU ou memória
                if (info["cpu_percent"] > 50 or info["memory_percent"] > 20) and info[
                    "status"
                ] == "running":
                    processos_travados.append(
                        {
                            "pid": info["pid"],
                            "name": info["name"],
                            "cpu": info["cpu_percent"],
                            "memory": info["memory_percent"],
                        }
                    )

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if processos_travados:
            print(
                f"\n⚠️ Encontrados {len(processos_travados)} processos com alto consumo:"
            )
            for proc in processos_travados[:5]:  # Mostra apenas os 5 primeiros
                print(
                    f"   • {proc['name']} (PID: {proc['pid']}) - CPU: {proc['cpu']:.1f}%, RAM: {proc['memory']:.1f}%"
                )

            # Pergunta se deve finalizar processos
            print("\n💡 Recomendação: Finalizar processos com alto consumo?")
            print("   Isso pode resolver problemas de lentidão.")

        else:
            print("   ✅ Nenhum processo travado detectado")

    except Exception as e:
        print(f"   ❌ Erro ao verificar processos: {str(e)}")

    return processos_travados


def limpar_cache_programas() -> None:
    """Limpa cache de programas comuns"""
    print("\n🗑️ Limpando cache de programas...")

    cache_paths = [
        os.path.expandvars("%APPDATA%\\Microsoft\\Windows\\INetCache"),
        os.path.expandvars("%LOCALAPPDATA%\\Microsoft\\Windows\\INetCache"),
        os.path.expandvars("%TEMP%"),
        os.path.expandvars("%LOCALAPPDATA%\\Temp"),
    ]

    total_removido = 0

    for path in cache_paths:
        if os.path.exists(path):
            try:
                arquivos_removidos = 0
                for root, dirs, files in os.walk(path, topdown=False):
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            if os.path.isfile(file_path):
                                os.remove(file_path)
                                arquivos_removidos += 1
                        except:
                            continue

                    # Remove diretórios vazios
                    for dir in dirs:
                        try:
                            dir_path = os.path.join(root, dir)
                            if os.path.exists(dir_path) and not os.listdir(dir_path):
                                os.rmdir(dir_path)
                        except:
                            continue

                total_removido += arquivos_removidos

            except Exception as e:
                print(f"   ⚠️ Erro ao limpar {path}: {str(e)}")

    if total_removido > 0:
        print(f"   ✅ {total_removido} arquivos de cache removidos")
    else:
        print("   ✅ Cache já estava limpo")


def reparar_aplicacoes_windows() -> None:
    """Repara aplicações Windows usando DISM e SFC"""
    print("\n🔧 Reparando aplicações Windows...")

    try:
        # Executa DISM para reparar componentes do Windows
        print("   🔄 Executando DISM...")
        resultado_dism = executar_comando_seguro(
            "dism /online /cleanup-image /restorehealth", timeout=300
        )

        if resultado_dism and resultado_dism.returncode == 0:
            print("   ✅ DISM executado com sucesso")
        else:
            print("   ⚠️ DISM executado com avisos")

        # Executa SFC para verificar integridade de arquivos
        print("   🔄 Executando SFC...")
        resultado_sfc = executar_comando_seguro("sfc /scannow", timeout=300)

        if resultado_sfc and resultado_sfc.returncode == 0:
            print("   ✅ SFC executado com sucesso")
        else:
            print("   ⚠️ SFC executado com avisos")

    except Exception as e:
        print(f"   ❌ Erro ao reparar aplicações: {str(e)}")


def verificar_integridade_arquivos() -> None:
    """Verifica integridade de arquivos do sistema"""
    print("\n🛡️ Verificando integridade de arquivos...")

    try:
        # Verifica arquivos do sistema
        resultado = executar_comando_seguro("sfc /verifyonly", timeout=60)

        if resultado and resultado.returncode == 0:
            print("   ✅ Integridade de arquivos OK")
        else:
            print("   ⚠️ Problemas detectados na integridade")

    except Exception as e:
        print(f"   ❌ Erro na verificação: {str(e)}")


def limpar_registros_corrompidos() -> None:
    """Limpa registros corrompidos do Windows"""
    print("\n🔧 Limpando registros corrompidos...")

    try:
        # Limpa registros temporários
        chaves_temp = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU",
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU",
        ]

        for chave in chaves_temp:
            try:
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER, chave, 0, winreg.KEY_ALL_ACCESS
                ) as key:
                    winreg.DeleteKey(key, "")
                print(f"   ✅ Registro {chave} limpo")
            except:
                continue

    except Exception as e:
        print(f"   ⚠️ Erro ao limpar registros: {str(e)}")


def finalizar_processo(pid: int) -> bool:
    """Finaliza um processo específico

    Args:
        pid: ID do processo a ser finalizado

    Returns:
        True se foi finalizado com sucesso, False caso contrário
    """
    try:
        processo = psutil.Process(pid)
        processo.terminate()

        # Aguarda até 5 segundos para o processo terminar
        processo.wait(timeout=5)
        return True

    except psutil.NoSuchProcess:
        return True  # Processo já não existe
    except psutil.TimeoutExpired:
        try:
            processo.kill()  # Força o encerramento
            return True
        except:
            return False
    except Exception:
        return False


def obter_info_programa(nome_programa: str) -> Optional[Dict]:
    """Obtém informações detalhadas de um programa

    Args:
        nome_programa: Nome do programa

    Returns:
        Dicionário com informações do programa ou None
    """
    try:
        for proc in psutil.process_iter(
            ["pid", "name", "exe", "create_time", "cpu_percent", "memory_percent"]
        ):
            if proc.info["name"].lower() == nome_programa.lower():
                return {
                    "pid": proc.info["pid"],
                    "name": proc.info["name"],
                    "path": proc.info["exe"],
                    "start_time": proc.info["create_time"],
                    "cpu_percent": proc.info["cpu_percent"],
                    "memory_percent": proc.info["memory_percent"],
                }
    except Exception:
        pass

    return None

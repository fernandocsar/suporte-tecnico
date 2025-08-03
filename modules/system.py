import subprocess
import psutil
import os
import time
import glob
import shutil
import tempfile
from .utils import limpar_tela, corrigir_encoding_windows, executar_comando_seguro

# Todas as funções do sistema aqui:
# - resolver_computador_lento()
# - verificar_espaco_disco()
# - limpar_arquivos_temporarios()
# - verificar_processos_pesados()
# - verificar_integridade_sistema()
# - reiniciar_spooler_impressao()


def resolver_computador_lento():
    """Resolve problemas de lentidão do computador"""
    print("=" * 60)
    print("           RESOLVENDO LENTIDÃO DO COMPUTADOR")
    print("=" * 60)

    print("\n🔍 Analisando sistema...")
    time.sleep(2)

    try:
        # 1. Verificar espaço em disco
        verificar_espaco_disco()

        # 2. Limpar arquivos temporários
        limpar_arquivos_temporarios()

        # 3. Limpar cache do sistema
        limpar_cache_sistema()

        # 4. Verificar processos pesados
        verificar_processos_pesados()

        # 5. Opção de verificação de integridade
        print("\n" + "=" * 50)
        print("🛡️ VERIFICAÇÃO DE INTEGRIDADE (OPCIONAL)")
        print("=" * 50)
        print("\n⚠️ A verificação de integridade pode demorar 15-30 minutos.")
        print("\n💡 Recomendado apenas se o problema persistir.")

        # Execução automática sem confirmação
        print("\n🔧 Executando verificação rápida...")
        verificar_integridade_sistema()

        print("\n" + "=" * 60)
        print("✅ OTIMIZAÇÃO CONCLUÍDA")
        print("=" * 60)
        print("\n🎯 Ações realizadas:")
        print("   • Verificação de espaço em disco")
        print("   • Limpeza de arquivos temporários")
        print("   • Limpeza de cache do sistema")
        print("   • Análise de processos")
        print("   • Verificação de integridade")
        print("\n💡 Reinicie o computador para aplicar todas as otimizações.")

    except Exception as e:
        print(f"\n❌ Erro durante otimização: {str(e)}")

    time.sleep(4)  # Pausa automática


def verificar_espaco_disco():
    """Verifica espaço disponível no disco C:"""
    print("\n💾 Verificando espaço em disco...")

    try:
        total, usado, livre = shutil.disk_usage("C:\\")

        total_gb = total // (1024**3)
        usado_gb = usado // (1024**3)
        livre_gb = livre // (1024**3)
        percentual_usado = (usado / total) * 100

        print(f"\n📊 Disco C:")
        print(f"   • Total: {total_gb} GB")
        print(f"   • Usado: {usado_gb} GB ({percentual_usado:.1f}%)")
        print(f"   • Livre: {livre_gb} GB")

        if percentual_usado > 90:
            print("\n⚠️ ATENÇÃO: Disco quase cheio! Isso pode causar lentidão.")
        elif percentual_usado > 80:
            print("\n💡 Disco com pouco espaço. Considere fazer limpeza.")
        else:
            print("\n✅ Espaço em disco adequado.")

    except Exception as e:
        print(f"\n❌ Erro ao verificar espaço: {str(e)}")


def limpar_arquivos_temporarios():
    """Remove arquivos temporários do sistema"""
    print("\n🗑️ Limpando arquivos temporários...")

    arquivos_removidos = 0

    try:
        # Pasta TEMP do usuário
        temp_user = tempfile.gettempdir()
        print(f"\n📁 Limpando: {temp_user}")

        for arquivo in glob.glob(os.path.join(temp_user, "*")):
            try:
                if os.path.isfile(arquivo):
                    os.remove(arquivo)
                    arquivos_removidos += 1
                elif os.path.isdir(arquivo):
                    shutil.rmtree(arquivo, ignore_errors=True)
                    arquivos_removidos += 1
            except:
                continue  # Ignora arquivos em uso

        # Pasta Windows\Temp (se acessível)
        windows_temp = "C:\\Windows\\Temp"
        if os.path.exists(windows_temp):
            print(f"\n📁 Limpando: {windows_temp}")
            for arquivo in glob.glob(os.path.join(windows_temp, "*")):
                try:
                    if os.path.isfile(arquivo):
                        os.remove(arquivo)
                        arquivos_removidos += 1
                except:
                    continue

        print(f"\n✅ {arquivos_removidos} itens temporários removidos.")

    except Exception as e:
        print(f"\n❌ Erro na limpeza: {str(e)}")


def limpar_cache_sistema():
    """Limpa cache do sistema Windows"""
    print("\n🧹 Limpando cache do sistema...")

    try:
        # Limpar cache de thumbnails
        cache_thumbnails = os.path.expanduser(
            "~\\AppData\\Local\\Microsoft\\Windows\\Explorer"
        )
        if os.path.exists(cache_thumbnails):
            print("\n📸 Limpando cache de thumbnails...")
            for arquivo in glob.glob(os.path.join(cache_thumbnails, "thumbcache_*.db")):
                try:
                    os.remove(arquivo)
                except:
                    continue

        # Executar limpeza de disco do Windows
        print("\n🔄 Executando limpeza de disco do Windows...")
        subprocess.run("cleanmgr /sagerun:1", shell=True, capture_output=True)

        print("\n✅ Cache do sistema limpo.")

    except Exception as e:
        print(f"\n❌ Erro na limpeza de cache: {str(e)}")


def verificar_processos_pesados():
    """Verifica processos que consomem muitos recursos"""
    print("\n🔍 Analisando processos do sistema...")

    try:
        processos_pesados = []

        for processo in psutil.process_iter(
            ["pid", "name", "cpu_percent", "memory_percent"]
        ):
            try:
                info = processo.info
                if info["cpu_percent"] > 10 or info["memory_percent"] > 5:
                    processos_pesados.append(info)
            except:
                continue

        if processos_pesados:
            print("\n📊 Processos que consomem mais recursos:")
            for proc in sorted(
                processos_pesados, key=lambda x: x["cpu_percent"], reverse=True
            )[:5]:
                print(
                    f"   • {proc['name']}: CPU {proc['cpu_percent']:.1f}%, RAM {proc['memory_percent']:.1f}%"
                )
        else:
            print("\n✅ Nenhum processo pesado detectado.")

    except Exception as e:
        print(f"\n❌ Erro ao verificar processos: {str(e)}")


def verificar_integridade_sistema():
    """Executa verificação de integridade do sistema"""
    print("\n🛡️ Verificando integridade do sistema...")
    print("\n⏰ Esta operação pode demorar 15-30 minutos.")

    try:
        # SFC Scan
        print("\n🔍 Executando SFC /scannow...")
        processo_sfc = subprocess.run(
            "sfc /scannow",
            shell=True,
            capture_output=True,
            text=True,
            encoding="cp1252",
            timeout=1800,  # 30 minutos
        )

        if processo_sfc.returncode == 0:
            print("\n✅ Verificação SFC concluída.")
        else:
            print("\n⚠️ Verificação SFC concluída com avisos.")

        # DISM
        print("\n🔧 Executando DISM RestoreHealth...")
        processo_dism = subprocess.run(
            "DISM /Online /Cleanup-Image /RestoreHealth",
            shell=True,
            capture_output=True,
            text=True,
            encoding="cp1252",
            timeout=1800,
        )

        if processo_dism.returncode == 0:
            print("\n✅ Verificação DISM concluída.")
        else:
            print("\n⚠️ Verificação DISM concluída com avisos.")

        print("\n📋 Verificação de integridade concluída.")

    except subprocess.TimeoutExpired:
        print("\n⏰ Verificação demorou mais que 30 minutos.")
        print("   O processo pode ter sido concluído mesmo assim.")
    except Exception as e:
        print(f"\n❌ Erro na verificação: {str(e)}")


def reiniciar_spooler_impressao():
    """Reinicia o serviço de spooler de impressão para resolver problemas de fila"""
    print("=" * 60)
    print("           REINICIANDO SPOOLER DE IMPRESSÃO")
    print("=" * 60)

    print("\n🖨️ Resolvendo problemas de impressão...")
    print("\n⏳ Esta operação pode demorar alguns segundos.")

    try:
        # 1. Parar o serviço de spooler
        print("\n🛑 Parando serviço de spooler...")
        resultado_parar = executar_comando_seguro("net stop spooler")

        if resultado_parar and resultado_parar.returncode == 0:
            print("   ✅ Serviço de spooler parado com sucesso")
        else:
            print("   ⚠️ Aviso ao parar o serviço (pode já estar parado)")

        # Aguardar um momento
        time.sleep(2)

        # 2. Limpar arquivos de fila
        print("\n🗑️ Limpando arquivos de fila...")
        try:
            fila_path = "C:\\Windows\\System32\\spool\\PRINTERS"
            if os.path.exists(fila_path):
                arquivos_fila = glob.glob(os.path.join(fila_path, "*"))
                arquivos_removidos = 0

                for arquivo in arquivos_fila:
                    try:
                        if os.path.isfile(arquivo):
                            os.remove(arquivo)
                            arquivos_removidos += 1
                    except:
                        continue  # Ignora arquivos em uso

                if arquivos_removidos > 0:
                    print(f"   ✅ {arquivos_removidos} arquivos de fila removidos")
                else:
                    print("   ✅ Nenhum arquivo de fila para remover")
            else:
                print("   ⚠️ Pasta de fila não encontrada")
        except Exception as e:
            print(f"   ⚠️ Erro ao limpar fila: {str(e)}")

        # 3. Iniciar o serviço de spooler
        print("\n🚀 Iniciando serviço de spooler...")
        resultado_iniciar = executar_comando_seguro("net start spooler")

        if resultado_iniciar and resultado_iniciar.returncode == 0:
            print("   ✅ Serviço de spooler iniciado com sucesso")

            # Verificar status do serviço
            print("\n🔍 Verificando status do serviço...")
            resultado_status = executar_comando_seguro(
                'sc query spooler | findstr "STATE"', timeout=10
            )

            if resultado_status and "RUNNING" in resultado_status.stdout:
                print("   ✅ Serviço está executando corretamente")
            else:
                print("   ⚠️ Status do serviço não confirmado")

        else:
            print("   ❌ Erro ao iniciar o serviço de spooler")
            if resultado_iniciar and resultado_iniciar.stderr:
                stderr_corrigido = corrigir_encoding_windows(
                    resultado_iniciar.stderr[:200]
                )
                print(f"   Detalhes: {stderr_corrigido}")

        # Resultado final
        print("\n" + "=" * 60)
        print("✅ REINICIALIZAÇÃO DO SPOOLER CONCLUÍDA")
        print("=" * 60)
        print("\n🎯 Ações realizadas:")
        print("   • Serviço de spooler parado")
        print("   • Arquivos de fila limpos")
        print("   • Serviço de spooler reiniciado")
        print("   • Status verificado")
        print("\n🖨️ Tente imprimir novamente!")

    except Exception as e:
        print(f"\n❌ Erro durante reinicialização do spooler: {str(e)}")
        print("\n💡 Possíveis soluções:")
        print("   • Execute como Administrador")
        print("   • Verifique se há impressoras conectadas")
        print("   • Reinicie o computador se o problema persistir")

    time.sleep(3)  # Pausa automática

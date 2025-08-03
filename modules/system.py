import subprocess
import psutil
import os
import time
import glob
from .utils import limpar_tela, corrigir_encoding_windows, executar_comando_seguro

# Todas as funções do sistema aqui:
# - resolver_computador_lento()
# - verificar_espaco_disco()
# - limpar_arquivos_temporarios()
# - verificar_processos_pesados()
# - verificar_integridade_sistema()
# - reiniciar_spooler_impressao()


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

"""Módulo de funções relacionadas à rede"""

import subprocess
import psutil
import time
from typing import List, Tuple, Optional
from .utils import corrigir_encoding_windows, executar_comando_seguro
from config import NETWORK_CONFIG


def verificar_tipo_conexao() -> Tuple[List[Tuple[str, str]], bool]:
    """Verifica se o computador está usando WiFi ou cabo de rede

    Returns:
        Tuple contendo lista de conexões ativas e status da internet
    """
    try:
        interfaces = psutil.net_if_stats()
        conexoes_ativas = []

        for interface, stats in interfaces.items():
            if stats.isup:
                interface_lower = interface.lower()

                if any(
                    wifi_term in interface_lower
                    for wifi_term in ["wifi", "wireless", "wlan", "wi-fi"]
                ):
                    conexoes_ativas.append(("wifi", interface))
                elif any(
                    eth_term in interface_lower
                    for eth_term in ["ethernet", "eth", "local", "cable"]
                ):
                    conexoes_ativas.append(("cabo", interface))

        # Verifica conectividade
        tem_internet = testar_conectividade_basica()
        return conexoes_ativas, tem_internet

    except Exception as e:
        print(f"Erro ao verificar conexões: {e}")
        return [], False


def testar_conectividade_basica() -> bool:
    """Testa conectividade básica com a internet

    Returns:
        True se há conectividade, False caso contrário
    """
    try:
        resultado_ping = subprocess.run(
            "ping -n 1 8.8.8.8",
            shell=True,
            capture_output=True,
            text=True,
            timeout=NETWORK_CONFIG["timeout_ping"],
        )
        return resultado_ping.returncode == 0
    except:
        return False


def resolver_erro_rede() -> None:
    """Resolve problemas de rede verificando tipo de conexão"""
    print("=" * 60)
    print("           RESOLVENDO PROBLEMAS DE REDE")
    print("=" * 60)

    print("\n🔍 Verificando tipo de conexão...")
    time.sleep(2)

    conexoes, tem_internet = verificar_tipo_conexao()

    if not conexoes:
        print("\n❌ Nenhuma conexão de rede detectada!")
        print("\n💡 Verifique se:")
        print("   • Os cabos estão conectados")
        print("   • O WiFi está ligado")
        print("   • Os drivers de rede estão instalados")
        time.sleep(3)
        return

    tem_wifi = any(tipo == "wifi" for tipo, _ in conexoes)
    tem_cabo = any(tipo == "cabo" for tipo, _ in conexoes)

    print(f"\n📡 Status da conexão:")
    for tipo, interface in conexoes:
        emoji = "📶" if tipo == "wifi" else "🔌"
        print(f"   {emoji} {tipo.upper()}: {interface}")

    internet_status = "✅ Conectado" if tem_internet else "❌ Sem internet"
    print(f"\n🌐 Internet: {internet_status}")

    if tem_wifi and not tem_cabo:
        print("\n⚠️ ATENÇÃO: Você está usando WiFi!")
        print("\n📋 Para resolver problemas de rede corporativa:")
        print("   • Conecte um cabo de rede")
        print("   • Desconecte do WiFi")
        print("   • Execute este script novamente")
        print("\n💡 Problemas de rede corporativa precisam de conexão cabeada")
        print("   para aplicar as políticas de grupo corretamente.")
    elif tem_cabo:
        if tem_wifi:
            print("\n💡 Detectado WiFi e cabo conectados.")
            print("   Recomendamos desconectar o WiFi para melhor resultado.")

        print("\n🔌 Conexão cabeada detectada!")
        print("\n🚀 Executando correção de políticas de rede...")
        executar_gpupdate()
    else:
        print("\n❓ Tipo de conexão não identificado claramente.")
        print("\n💡 Para problemas de rede corporativa:")
        print("   • Use conexão cabeada sempre que possível")
        print("   • Verifique com o suporte de TI")

    time.sleep(3)


def executar_gpupdate() -> None:
    """Executa o comando gpupdate /force e aguarda conclusão"""
    print("\n" + "=" * 50)
    print("    ATUALIZANDO POLÍTICAS DE GRUPO")
    print("=" * 50)

    print("\n🔄 Executando: gpupdate /force")
    print("\n⏳ Esta operação pode demorar alguns minutos...")
    print("   Por favor, aguarde até a conclusão.")

    try:
        print("\n🖥️ Processando...")

        resultado = executar_comando_seguro(
            "gpupdate /force", timeout=NETWORK_CONFIG["timeout_gpupdate"]
        )

        if resultado and resultado.returncode == 0:
            print("\n✅ Comando gpupdate executado com sucesso!")
        else:
            print("\n⚠️ Comando gpupdate executado com avisos.")
            if resultado and resultado.stderr:
                stderr_corrigido = corrigir_encoding_windows(resultado.stderr[:200])
                print(f"   Detalhes: {stderr_corrigido}...")

        if resultado and resultado.stdout:
            linhas_saida = resultado.stdout.strip().split("\n")
            if linhas_saida:
                print("\n📋 Resultado:")
                for linha in linhas_saida[-3:]:
                    if linha.strip():
                        linha_corrigida = corrigir_encoding_windows(linha.strip())
                        print(f"   {linha_corrigida}")

        print("\n" + "=" * 50)
        print("✅ ATUALIZAÇÃO DE POLÍTICAS CONCLUÍDA")
        print("=" * 50)
        print("\n🎯 Ações realizadas:")
        print("   • Políticas de usuário atualizadas")
        print("   • Políticas de computador atualizadas")
        print("   • Configurações de rede aplicadas")
        print("\n🌐 Teste sua conexão novamente!")

    except Exception as e:
        print(f"\n❌ Erro durante atualização de políticas: {str(e)}")
        print("\n💡 Possíveis soluções:")
        print("   • Execute como Administrador")
        print("   • Verifique a conexão com o domínio")
        print("   • Tente executar manualmente: gpupdate /force")

    time.sleep(3)


def executar_flush_dns() -> None:
    """Executa limpeza completa do cache DNS"""
    print("=" * 60)
    print("           LIMPANDO CACHE DNS")
    print("=" * 60)

    print("\n🔄 Executando limpeza do cache DNS...")
    print("\n⏳ Esta operação pode demorar alguns segundos.")

    comandos = [
        "ipconfig /flushdns",
        "ipconfig /registerdns",
        "ipconfig /release",
        "ipconfig /renew",
    ]

    try:
        for i, comando in enumerate(comandos, 1):
            print(f"\n🔧 Executando comando {i}/4: {comando}")

            resultado = executar_comando_seguro(
                comando, timeout=NETWORK_CONFIG["timeout_commands"]
            )

            if resultado and resultado.returncode == 0:
                print(f"   ✅ Comando {i} executado com sucesso")
            else:
                print(f"   ⚠️ Aviso no comando {i}")
                if resultado and resultado.stderr:
                    stderr_corrigido = corrigir_encoding_windows(resultado.stderr[:100])
                    print(f"   Detalhes: {stderr_corrigido}")

            time.sleep(1)

        print("\n" + "=" * 60)
        print("✅ LIMPEZA DO CACHE DNS CONCLUÍDA")
        print("=" * 60)
        print("\n🎯 Comandos executados:")
        print("   • ipconfig /flushdns")
        print("   • ipconfig /registerdns")
        print("   • ipconfig /release")
        print("   • ipconfig /renew")
        print("\n🌐 Teste sua conexão novamente!")

    except Exception as e:
        print(f"\n❌ Erro ao executar comandos DNS: {str(e)}")
        print("\n💡 Possíveis soluções:")
        print("   • Execute como Administrador")
        print("   • Verifique se o serviço DNS Client está ativo")

    time.sleep(3)

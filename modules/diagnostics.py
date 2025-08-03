"""Módulo de diagnósticos de rede e sistema"""

import subprocess
import psutil
import socket
import time
from typing import List, Dict, Optional
from .utils import corrigir_encoding_windows, executar_comando_seguro
from config import NETWORK_CONFIG


def verificar_informacoes_rede() -> None:
    """Exibe informações completas da rede para diagnóstico"""
    print("=" * 60)
    print("           INFORMAÇÕES COMPLETAS DA REDE")
    print("=" * 60)

    print("\n🔍 Coletando informações da rede...")
    time.sleep(2)

    try:
        exibir_ip_computador()
        exibir_configuracao_ip()
        exibir_interfaces_rede()
        testar_conectividade()
        exibir_conectividade_basica()

    except Exception as e:
        print(f"\n❌ Erro ao coletar informações: {str(e)}")

    time.sleep(3)


def exibir_ip_computador() -> None:
    """Exibe o IP do computador"""
    print("\n" + "=" * 50)
    print("🖥️ IP DO COMPUTADOR")
    print("=" * 50)

    try:
        resultado = executar_comando_seguro('ipconfig | findstr "IPv4"')

        if resultado and resultado.stdout:
            linhas = resultado.stdout.split("\n")
            ips_encontrados = []

            for linha in linhas:
                if "IPv4" in linha and linha.strip():
                    linha_corrigida = corrigir_encoding_windows(linha.strip())
                    ip = linha_corrigida.split(":")[-1].strip()
                    if ip and ip != "127.0.0.1":
                        ips_encontrados.append(ip)

            if ips_encontrados:
                for ip in ips_encontrados:
                    print(f"   🌐 {ip}")
            else:
                print("   ⚠️ Nenhum IP válido encontrado")
        else:
            print("   ❌ Não foi possível obter o IP")

    except Exception as e:
        print(f"   ❌ Erro ao obter IP: {str(e)}")


def exibir_configuracao_ip() -> None:
    """Exibe configuração completa de IP"""
    print("\n" + "=" * 50)
    print("⚙️ CONFIGURAÇÃO DE IP")
    print("=" * 50)

    try:
        resultado = executar_comando_seguro("ipconfig /all")

        if resultado and resultado.stdout:
            linhas = resultado.stdout.split("\n")
            info_relevante = []

            for linha in linhas:
                linha_limpa = linha.strip()
                if any(
                    termo in linha_limpa
                    for termo in ["Adaptador", "IPv4", "Gateway", "DNS", "DHCP"]
                ):
                    if linha_limpa:
                        linha_corrigida = corrigir_encoding_windows(linha_limpa)
                        info_relevante.append(linha_corrigida)

            if info_relevante:
                for info in info_relevante[:10]:  # Limita a 10 linhas
                    print(f"   {info}")
            else:
                print("   ⚠️ Informações de configuração não disponíveis")
        else:
            print("   ❌ Não foi possível obter configurações")

    except Exception as e:
        print(f"   ❌ Erro ao obter configurações: {str(e)}")


def exibir_interfaces_rede() -> None:
    """Exibe informações das interfaces de rede"""
    print("\n" + "=" * 50)
    print("🔌 INTERFACES DE REDE")
    print("=" * 50)

    try:
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        for interface, enderecos in interfaces.items():
            if interface in stats:
                status = "🟢 Ativa" if stats[interface].isup else "🔴 Inativa"
                print(f"\n   📡 {interface} - {status}")

                for endereco in enderecos:
                    if endereco.family == socket.AF_INET:  # IPv4
                        print(f"      IPv4: {endereco.address}")
                    elif endereco.family == socket.AF_INET6:  # IPv6
                        print(f"      IPv6: {endereco.address}")

    except Exception as e:
        print(f"   ❌ Erro ao listar interfaces: {str(e)}")


def testar_conectividade() -> None:
    """Testa conectividade com sites importantes"""
    print("\n" + "=" * 50)
    print("🌐 TESTE DE CONECTIVIDADE")
    print("=" * 50)

    sites = NETWORK_CONFIG["test_hosts"]

    for site in sites:
        try:
            print(f"\n   🔍 Testando {site}...")

            resultado = executar_comando_seguro(
                f"ping -n 1 {site}", timeout=NETWORK_CONFIG["timeout_ping"]
            )

            if resultado and resultado.returncode == 0:
                print(f"   ✅ {site} - Conectado")
            else:
                print(f"   ❌ {site} - Falha na conexão")

        except Exception as e:
            print(f"   ❌ {site} - Erro: {str(e)}")


def exibir_conectividade_basica() -> None:
    """Exibe informações básicas de conectividade"""
    print("\n" + "=" * 50)
    print("📊 RESUMO DA CONECTIVIDADE")
    print("=" * 50)

    try:
        # Testa DNS
        resultado_dns = executar_comando_seguro("nslookup google.com")
        dns_ok = resultado_dns and resultado_dns.returncode == 0

        # Testa gateway
        resultado_gateway = executar_comando_seguro('ipconfig | findstr "Gateway"')
        gateway_ok = resultado_gateway and resultado_gateway.stdout.strip()

        # Testa internet
        internet_ok = False
        try:
            resultado_ping = executar_comando_seguro(
                "ping -n 1 8.8.8.8", timeout=NETWORK_CONFIG["timeout_ping"]
            )
            internet_ok = resultado_ping and resultado_ping.returncode == 0
        except:
            pass

        print(f"\n   🌐 Internet: {'✅ OK' if internet_ok else '❌ Falha'}")
        print(f"   🔍 DNS: {'✅ OK' if dns_ok else '❌ Falha'}")
        print(f"   🚪 Gateway: {'✅ OK' if gateway_ok else '❌ Falha'}")

        if not internet_ok:
            print("\n   💡 Sugestões:")
            if not gateway_ok:
                print("      • Verifique a conexão com o roteador")
            if not dns_ok:
                print("      • Verifique as configurações de DNS")
            print("      • Reinicie o roteador/modem")
            print("      • Execute flush DNS")

    except Exception as e:
        print(f"   ❌ Erro no diagnóstico: {str(e)}")

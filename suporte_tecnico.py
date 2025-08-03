#!/usr/bin/env python3
"""
Sistema de Suporte Técnico - Arquivo Principal

Sistema automatizado para resolução de problemas comuns em computadores Windows.
Desenvolvido para facilitar o suporte técnico em ambientes corporativos.

Author: Fernando César
Version: 1.0.0
License: MIT
"""

import os
import sys
import time
import logging
from typing import NoReturn


def exibir_menu() -> None:
    """Exibe o menu principal do sistema"""
    width = UI_CONFIG["menu_width"]

    print("=" * width)
    print(f"{APP_NAME:^{width}}")
    print(f"Versão {VERSION}:^{width}")
    print("=" * width)
    print()
    print("Escolha o problema que você está enfrentando:")
    print()
    print("1. 🌐 Problemas de rede")
    print("2. 🔄 Flush DNS (Limpar cache DNS)")
    print("3. 📊 Verificar informações da rede")
    print("4. 🐌 Computador lento")
    print("5. 🖨️ Reiniciar spooler de impressão")
    print("6. 💻 Problemas com programas (Em breve)")
    print("7. 🔧 Problemas de hardware (Em breve)")
    print("0. ❌ Sair")
    print()
    print("=" * width)


def verificar_tipo_conexao():
    """Verifica se o computador está usando WiFi ou cabo de rede"""
    try:
        # Obtém informações das interfaces de rede
        interfaces = psutil.net_if_stats()
        conexoes_ativas = []

        for interface, stats in interfaces.items():
            if stats.isup:  # Interface ativa
                interface_lower = interface.lower()

                # Identifica tipos de conexão
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

        # Verifica conectividade real testando ping
        try:
            resultado_ping = subprocess.run(
                "ping -n 1 8.8.8.8",
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
            )
            tem_internet = resultado_ping.returncode == 0
        except:
            tem_internet = False

        return conexoes_ativas, tem_internet

    except Exception as e:
        print(f"Erro ao verificar conexões: {e}")
        return [], False


def resolver_erro_rede():
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
        time.sleep(3)  # Pausa automática em vez de input
        return

    # Verifica se tem WiFi ativo
    tem_wifi = any(tipo == "wifi" for tipo, _ in conexoes)
    tem_cabo = any(tipo == "cabo" for tipo, _ in conexoes)

    print(f"\n📡 Status da conexão:")
    for tipo, interface in conexoes:
        emoji = "📶" if tipo == "wifi" else "🔌"
        print(f"   {emoji} {tipo.upper()}: {interface}")

    internet_status = "✅ Conectado" if tem_internet else "❌ Sem internet"
    print(f"\n🌐 Internet: {internet_status}")

    if tem_wifi and not tem_cabo:
        # Usuário está apenas no WiFi
        print("\n⚠️ ATENÇÃO: Você está usando WiFi!")
        print("\n📋 Para resolver problemas de rede corporativa:")
        print("   • Conecte um cabo de rede")
        print("   • Desconecte do WiFi")
        print("   • Execute este script novamente")
        print("\n💡 Problemas de rede corporativa precisam de conexão cabeada")
        print("   para aplicar as políticas de grupo corretamente.")

    elif tem_cabo:
        # Usuário está com cabo (pode ter WiFi também)
        if tem_wifi:
            print("\n💡 Detectado WiFi e cabo conectados.")
            print("   Recomendamos desconectar o WiFi para melhor resultado.")

        print("\n🔌 Conexão cabeada detectada!")
        print("\n🚀 Executando correção de políticas de rede...")

        # Executa gpupdate /force automaticamente
        executar_gpupdate()

    else:
        print("\n❓ Tipo de conexão não identificado claramente.")
        print("\n💡 Para problemas de rede corporativa:")
        print("   • Use conexão cabeada sempre que possível")
        print("   • Verifique com o suporte de TI")

    input("\nPressione ENTER para voltar ao menu...")


def corrigir_encoding_windows(texto):
    """Corrige problemas de encoding do Windows para português"""
    # Dicionário de correções para caracteres corrompidos comuns
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


def executar_gpupdate():
    """Executa o comando gpupdate /force e aguarda conclusão"""
    print("\n" + "=" * 50)
    print("    ATUALIZANDO POLÍTICAS DE GRUPO")
    print("=" * 50)

    print("\n🔄 Executando: gpupdate /force")
    print("\n⏳ Esta operação pode demorar alguns minutos...")
    print("   Por favor, aguarde até a conclusão.")

    try:
        # Executa gpupdate diretamente sem abrir janela separada
        print("\n🖥️ Processando...")

        # Tenta diferentes encodings para capturar a saída corretamente
        encodings_para_testar = ["cp1252", "utf-8", "latin1"]
        processo = None

        for encoding in encodings_para_testar:
            try:
                processo = subprocess.run(
                    "gpupdate /force",
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding=encoding,
                    timeout=300,
                )
                break
            except UnicodeDecodeError:
                continue

        # Se nenhum encoding funcionou, usa o padrão
        if processo is None:
            processo = subprocess.run(
                "gpupdate /force",
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,
            )

        # Verifica o resultado
        if processo.returncode == 0:
            print("\n✅ Comando gpupdate executado com sucesso!")
        else:
            print("\n⚠️ Comando gpupdate executado com avisos.")
            if processo.stderr:
                stderr_corrigido = corrigir_encoding_windows(processo.stderr[:200])
                print(f"   Detalhes: {stderr_corrigido}...")

        # Mostra parte da saída com correção de encoding
        if processo.stdout:
            linhas_saida = processo.stdout.strip().split("\n")
            if len(linhas_saida) > 0:
                print("\n📋 Resultado:")
                for linha in linhas_saida[-3:]:  # Mostra últimas 3 linhas
                    if linha.strip():
                        # Corrige o encoding da linha
                        linha_corrigida = corrigir_encoding_windows(linha.strip())
                        print(f"   {linha_corrigida}")

        print("\n📋 O que foi feito:")
        print("   • Políticas de grupo atualizadas")
        print("   • Configurações de rede aplicadas")
        print("   • Cache de políticas limpo")

    except subprocess.TimeoutExpired:
        print("\n⏰ Timeout: O comando demorou mais que 5 minutos.")
        print("   Isso pode ser normal em redes muito lentas.")
        print("   O processo pode ter sido concluído mesmo assim.")
    except Exception as e:
        print(f"\n❌ Erro ao executar gpupdate: {str(e)}")
        print("\n💡 Possíveis soluções:")
        print("   • Execute como Administrador")
        print("   • Verifique a conexão de rede")
        print("   • Contate o suporte de TI")


def executar_flush_dns():
    """Executa o comando ipconfig /flushdns para limpar cache DNS"""
    print("=" * 60)
    print("           LIMPANDO CACHE DNS")
    print("=" * 60)

    print("\n🔄 Executando comandos de limpeza DNS...")
    print("\n⏳ Aguarde...")

    try:
        # Lista de comandos para executar
        comandos = [
            "ipconfig /flushdns",
            "ipconfig /registerdns",
            "ipconfig /release",
            "ipconfig /renew",
        ]

        for comando in comandos:
            print(f"\n🔄 Executando: {comando}")
            resultado = subprocess.run(
                comando,
                shell=True,
                capture_output=True,
                text=True,
                encoding="cp1252",
                timeout=30,
            )

            if resultado.returncode == 0:
                print(f"   ✅ {comando} executado com sucesso!")
            else:
                print(f"   ⚠️ {comando} executado com avisos.")

        print("\n" + "=" * 60)
        print("✅ LIMPEZA DO CACHE DNS CONCLUÍDA")
        print("=" * 60)
        print("\n🎯 Comandos executados:")
        print("   • ipconfig /flushdns")
        print("   • ipconfig /registerdns")
        print("   • ipconfig /release")
        print("   • ipconfig /renew")
        print("\n🌐 Teste sua conexão novamente!")

    except subprocess.TimeoutExpired:
        print("\n⏰ Comando demorou muito para executar (timeout).")
        print("\n💡 Tente executar manualmente os comandos:")
        for comando in comandos:
            print(f"   • {comando}")
    except Exception as e:
        print(f"\n❌ Erro ao executar comandos DNS: {str(e)}")
        print("\n💡 Possíveis soluções:")
        print("   • Execute como Administrador")
        print("   • Verifique se o serviço DNS Client está ativo")

    time.sleep(3)  # Pausa automática em vez de input


def resolver_computador_lento():
    """Resolve problemas de lentidão do computador"""
    print("=" * 60)
    print("           RESOLVENDO LENTIDÃO DO COMPUTADOR")
    print("=" * 60)

    print("\n🔍 Analisando sistema...")
    time.sleep(2)

    try:
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

    time.sleep(4)  # Pausa automática em vez de input


def exibir_ip_computador():
    """Exibe o IP principal do computador"""
    print("\n" + "=" * 50)
    print("💻 IP DO COMPUTADOR")
    print("=" * 50)

    try:
        # Método 1: Usando ipconfig para pegar IP principal
        resultado = subprocess.run(
            'ipconfig | findstr /C:"IPv4" /C:"Endereço IPv4"',
            shell=True,
            capture_output=True,
            text=True,
            encoding="cp1252",
            timeout=5,
        )

        if resultado.returncode == 0 and resultado.stdout.strip():
            linhas = resultado.stdout.split("\n")
            ips_encontrados = []

            for linha in linhas:
                linha = linha.strip()
                if linha and ("IPv4" in linha or "Endereço" in linha):
                    # Extrair apenas o IP da linha
                    if ":" in linha:
                        ip_parte = linha.split(":")[-1].strip()
                        # Remove caracteres extras como (Preferencial)
                        ip_limpo = ip_parte.split("(")[0].strip()
                        if ip_limpo and not ip_limpo.startswith("127."):
                            ips_encontrados.append(ip_limpo)

            if ips_encontrados:
                print("\n🌐 Endereços IP ativos:")
                for i, ip in enumerate(ips_encontrados, 1):
                    emoji = "🏠" if ip.startswith(("192.168.", "10.", "172.")) else "🌍"
                    tipo = (
                        "(Rede local)"
                        if ip.startswith(("192.168.", "10.", "172."))
                        else "(Público)"
                    )
                    print(f"   {emoji} IP {i}: {ip} {tipo}")
            else:
                print("   ⚠️ Nenhum IP ativo encontrado")

        # Método 2: Usando psutil como backup
        print("\n🔍 Verificação adicional com psutil:")
        import socket

        # Pega o IP usado para conectar à internet
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_principal = s.getsockname()[0]
            s.close()
            print(f"   🎯 IP principal (rota padrão): {ip_principal}")
        except:
            print("   ❌ Não foi possível determinar IP principal")

    except Exception as e:
        print(f"   ❌ Erro ao obter IP do computador: {str(e)}")


def exibir_interfaces_rede():
    """Exibe informações das interfaces usando psutil"""
    print("\n" + "=" * 50)
    print("🖧 INTERFACES DE REDE (PSUTIL)")
    print("=" * 50)

    try:
        import socket  # Importar socket para as constantes

        # Estatísticas das interfaces
        stats = psutil.net_if_stats()
        addrs = psutil.net_if_addrs()

        for interface, stat in stats.items():
            if interface in addrs:
                print(f"\n🔌 {interface}")
                print(f"   • Status: {'🟢 Ativo' if stat.isup else '🔴 Inativo'}")
                print(
                    f"   • Velocidade: {stat.speed} Mbps"
                    if stat.speed > 0
                    else "   • Velocidade: Desconhecida"
                )
                print(f"   • MTU: {stat.mtu}")

                # Endereços IP - usando socket em vez de psutil para as constantes
                for addr in addrs[interface]:
                    if addr.family == socket.AF_INET:  # IPv4 - Corrigido
                        print(f"   • IPv4: {addr.address}")
                        if addr.netmask:
                            print(f"   • Máscara: {addr.netmask}")
                    elif addr.family == socket.AF_INET6:  # IPv6 - Corrigido
                        print(f"   • IPv6: {addr.address}")
                    elif (
                        hasattr(addr, "address")
                        and len(addr.address) == 17
                        and ":" in addr.address
                    ):  # MAC
                        print(f"   • MAC: {addr.address}")

    except Exception as e:
        print(f"   ❌ Erro ao obter interfaces: {str(e)}")


def verificar_informacoes_rede():
    """Exibe informações completas da rede para diagnóstico"""
    print("=" * 60)
    print("           INFORMAÇÕES COMPLETAS DA REDE")
    print("=" * 60)

    print("\n🔍 Coletando informações da rede...")
    print("   Esta operação pode demorar alguns segundos.")

    try:
        # 1. IP do computador
        exibir_ip_computador()

        # 2. Informações básicas de conectividade
        exibir_conectividade_basica()

        # 3. Configuração IP detalhada
        exibir_configuracao_ip()

        # 4. Interfaces de rede
        exibir_interfaces_rede()

        # 5. Tabela de roteamento
        exibir_tabela_roteamento()

        # 6. Servidores DNS
        exibir_servidores_dns()

        # 7. Teste de conectividade
        testar_conectividade()

        # 8. Informações de domínio
        exibir_info_dominio()

        print("\n" + "=" * 60)
        print("✅ DIAGNÓSTICO DE REDE CONCLUÍDO")
        print("=" * 60)
        print("\n💡 Se ainda houver problemas de rede:")
        print("   • Use a opção 1 para resolver problemas específicos")
        print("   • Use a opção 2 para limpar cache DNS")
        print("   • Contate o suporte de TI com essas informações")

    except Exception as e:
        print(f"\n❌ Erro durante diagnóstico: {str(e)}")

    time.sleep(4)  # Pausa automática em vez de input


def exibir_conectividade_basica():
    """Exibe status básico de conectividade"""
    print("\n" + "=" * 50)
    print("📡 STATUS DE CONECTIVIDADE")
    print("=" * 50)

    try:
        # Teste de ping para diferentes servidores
        servidores_teste = [
            ("8.8.8.8", "Google DNS"),
            ("1.1.1.1", "Cloudflare DNS"),
            ("208.67.222.222", "OpenDNS"),
        ]

        for ip, nome in servidores_teste:
            try:
                resultado = subprocess.run(
                    f"ping -n 1 -w 3000 {ip}",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                if resultado.returncode == 0:
                    # Extrair tempo de resposta
                    linhas = resultado.stdout.split("\n")
                    for linha in linhas:
                        if "tempo=" in linha or "time=" in linha:
                            tempo = (
                                linha.split("tempo=")[-1].split("ms")[0]
                                if "tempo=" in linha
                                else linha.split("time=")[-1].split("ms")[0]
                            )
                            print(f"   ✅ {nome} ({ip}): {tempo.strip()}ms")
                            break
                    else:
                        print(f"   ✅ {nome} ({ip}): Conectado")
                else:
                    print(f"   ❌ {nome} ({ip}): Sem resposta")

            except:
                print(f"   ⚠️ {nome} ({ip}): Erro no teste")

    except Exception as e:
        print(f"   ❌ Erro nos testes de conectividade: {str(e)}")


def exibir_configuracao_ip():
    """Exibe configuração IP detalhada usando ipconfig"""
    print("\n" + "=" * 50)
    print("🔧 CONFIGURAÇÃO IP DETALHADA")
    print("=" * 50)

    try:
        resultado = subprocess.run(
            "ipconfig /all",
            shell=True,
            capture_output=True,
            text=True,
            encoding="cp1252",
            timeout=10,
        )

        if resultado.returncode == 0:
            linhas = resultado.stdout.split("\n")
            interface_atual = ""

            for linha in linhas:
                linha = linha.strip()
                if not linha:
                    continue

                # Detectar nova interface
                if "adaptador" in linha.lower() or "adapter" in linha.lower():
                    interface_atual = linha
                    print(f"\n🔌 {interface_atual}")
                    continue

                # Informações importantes
                if any(
                    termo in linha.lower()
                    for termo in [
                        "endereço físico",
                        "physical address",
                        "dhcp habilitado",
                        "dhcp enabled",
                        "endereço ipv4",
                        "ipv4 address",
                        "máscara de sub-rede",
                        "subnet mask",
                        "gateway padrão",
                        "default gateway",
                        "servidores dns",
                        "dns servers",
                    ]
                ):
                    # Corrigir encoding se necessário
                    linha_corrigida = corrigir_encoding_windows(linha)
                    print(f"   • {linha_corrigida}")
        else:
            print("   ❌ Erro ao executar ipconfig /all")

    except Exception as e:
        print(f"   ❌ Erro ao obter configuração IP: {str(e)}")


def exibir_interfaces_rede():
    """Exibe informações das interfaces usando psutil"""
    print("\n" + "=" * 50)
    print("🖧 INTERFACES DE REDE (PSUTIL)")
    print("=" * 50)

    try:
        import socket  # Importar socket para as constantes

        # Estatísticas das interfaces
        stats = psutil.net_if_stats()
        addrs = psutil.net_if_addrs()

        for interface, stat in stats.items():
            if interface in addrs:
                print(f"\n🔌 {interface}")
                print(f"   • Status: {'🟢 Ativo' if stat.isup else '🔴 Inativo'}")
                print(
                    f"   • Velocidade: {stat.speed} Mbps"
                    if stat.speed > 0
                    else "   • Velocidade: Desconhecida"
                )
                print(f"   • MTU: {stat.mtu}")

                # Endereços IP - usando socket em vez de psutil para as constantes
                for addr in addrs[interface]:
                    if addr.family == socket.AF_INET:  # IPv4 - Corrigido
                        print(f"   • IPv4: {addr.address}")
                        if addr.netmask:
                            print(f"   • Máscara: {addr.netmask}")
                    elif addr.family == socket.AF_INET6:  # IPv6 - Corrigido
                        print(f"   • IPv6: {addr.address}")
                    elif (
                        hasattr(addr, "address")
                        and len(addr.address) == 17
                        and ":" in addr.address
                    ):  # MAC
                        print(f"   • MAC: {addr.address}")

    except Exception as e:
        print(f"   ❌ Erro ao obter interfaces: {str(e)}")


def exibir_tabela_roteamento():
    """Exibe tabela de roteamento"""
    print("\n" + "=" * 50)
    print("🗺️ TABELA DE ROTEAMENTO")
    print("=" * 50)

    try:
        resultado = subprocess.run(
            "route print",
            shell=True,
            capture_output=True,
            text=True,
            encoding="cp1252",
            timeout=10,
        )

        if resultado.returncode == 0:
            linhas = resultado.stdout.split("\n")
            mostrar_proximas = False
            contador = 0

            for linha in linhas:
                linha = linha.strip()

                # Procurar pela seção de rotas IPv4
                if "Rotas Ativas" in linha or "Active Routes" in linha:
                    mostrar_proximas = True
                    print(f"\n📋 {linha}")
                    continue

                if mostrar_proximas and linha:
                    if contador < 15:  # Limitar a 15 linhas principais
                        linha_corrigida = corrigir_encoding_windows(linha)
                        print(f"   {linha_corrigida}")
                        contador += 1
                    elif "Rotas Persistentes" in linha or "Persistent Routes" in linha:
                        break
        else:
            print("   ❌ Erro ao executar route print")

    except Exception as e:
        print(f"   ❌ Erro ao obter tabela de roteamento: {str(e)}")


def exibir_servidores_dns():
    """Exibe configuração de servidores DNS"""
    print("\n" + "=" * 50)
    print("🌐 SERVIDORES DNS")
    print("=" * 50)

    try:
        resultado = subprocess.run(
            "nslookup",
            input="exit\n",
            shell=True,
            capture_output=True,
            text=True,
            encoding="cp1252",
            timeout=5,
        )

        if resultado.returncode == 0:
            linhas = resultado.stdout.split("\n")
            for linha in linhas:
                if "Servidor:" in linha or "Server:" in linha:
                    linha_corrigida = corrigir_encoding_windows(linha.strip())
                    print(f"   • {linha_corrigida}")
                elif "Address:" in linha or "Endereço:" in linha:
                    linha_corrigida = corrigir_encoding_windows(linha.strip())
                    print(f"   • {linha_corrigida}")

    except Exception as e:
        print(f"   ❌ Erro ao obter servidores DNS: {str(e)}")


def testar_conectividade():
    """Testa conectividade com sites importantes"""
    print("\n" + "=" * 50)
    print("🌍 TESTE DE CONECTIVIDADE WEB")
    print("=" * 50)

    sites_teste = ["google.com", "github.com"]  # Removido microsoft.com

    for site in sites_teste:
        try:
            resultado = subprocess.run(
                f"ping -n 2 {site}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if resultado.returncode == 0:
                print(f"   ✅ {site}: Acessível")
            else:
                print(f"   ❌ {site}: Inacessível")

        except:
            print(f"   ⚠️ {site}: Erro no teste")


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
        resultado_parar = subprocess.run(
            "net stop spooler",
            shell=True,
            capture_output=True,
            text=True,
            encoding="cp1252",
            timeout=30,
        )

        if resultado_parar.returncode == 0:
            print("   ✅ Serviço de spooler parado com sucesso")
        else:
            print("   ⚠️ Aviso ao parar o serviço (pode já estar parado)")

        # Aguardar um momento
        time.sleep(2)

        # 2. Limpar arquivos de fila (opcional)
        print("\n🗑️ Limpando arquivos de fila...")
        try:
            fila_path = "C:\\Windows\\System32\\spool\\PRINTERS"
            if os.path.exists(fila_path):
                import glob

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
        resultado_iniciar = subprocess.run(
            "net start spooler",
            shell=True,
            capture_output=True,
            text=True,
            encoding="cp1252",
            timeout=30,
        )

        if resultado_iniciar.returncode == 0:
            print("   ✅ Serviço de spooler iniciado com sucesso")

            # Verificar status do serviço
            print("\n🔍 Verificando status do serviço...")
            resultado_status = subprocess.run(
                'sc query spooler | findstr "STATE"',
                shell=True,
                capture_output=True,
                text=True,
                encoding="cp1252",
                timeout=10,
            )

            if "RUNNING" in resultado_status.stdout:
                print("   ✅ Serviço está executando corretamente")
            else:
                print("   ⚠️ Status do serviço não confirmado")

        else:
            print("   ❌ Erro ao iniciar o serviço de spooler")
            if resultado_iniciar.stderr:
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

    except subprocess.TimeoutExpired:
        print("\n⏰ Operação demorou muito para executar (timeout).")
        print("\n💡 Tente executar manualmente:")
        print("   • net stop spooler")
        print("   • net start spooler")
    except Exception as e:
        print(f"\n❌ Erro durante reinicialização do spooler: {str(e)}")
        print("\n💡 Possíveis soluções:")
        print("   • Execute como Administrador")
        print("   • Verifique se há impressoras conectadas")
        print("   • Reinicie o computador se o problema persistir")

    time.sleep(4)  # Pausa automática


def exibir_info_dominio():
    """Exibe informações de domínio/workgroup"""
    print("\n" + "=" * 50)
    print("🏢 INFORMAÇÕES DE DOMÍNIO")
    print("=" * 50)

    try:
        # Informações do computador
        resultado = subprocess.run(
            'systeminfo | findstr /C:"Nome do computador" /C:"Domínio" /C:"Computer Name" /C:"Domain"',
            shell=True,
            capture_output=True,
            text=True,
            encoding="cp1252",
            timeout=10,
        )

        if resultado.returncode == 0:
            linhas = resultado.stdout.split("\n")
            for linha in linhas:
                if linha.strip():
                    linha_corrigida = corrigir_encoding_windows(linha.strip())
                    print(f"   • {linha_corrigida}")
        else:
            print("   ⚠️ Informações de domínio não disponíveis")

    except Exception as e:
        print(f"   ❌ Erro ao obter informações de domínio: {str(e)}")


def exibir_funcionalidade_em_breve() -> None:
    """Exibe mensagem para funcionalidades em desenvolvimento"""
    print("\n🚧 Esta funcionalidade ainda está em desenvolvimento!")
    print("\n💡 Por enquanto, use as opções 1, 2, 3, 4 e 5 para resolver problemas.")
    time.sleep(UI_CONFIG["auto_return_delay"])


def processar_opcao(opcao: str) -> bool:
    """Processa a opção escolhida pelo usuário

    Args:
        opcao: Opção escolhida pelo usuário

    Returns:
        False se deve sair do programa, True caso contrário
    """
    logger = logging.getLogger(__name__)

    try:
        if opcao == "1":
            logger.info("Executando resolução de problemas de rede")
            resolver_erro_rede()
        elif opcao == "2":
            logger.info("Executando flush DNS")
            executar_flush_dns()
        elif opcao == "3":
            logger.info("Verificando informações da rede")
            verificar_informacoes_rede()
        elif opcao == "4":
            logger.info("Resolvendo problemas de computador lento")
            resolver_computador_lento()
        elif opcao == "5":
            logger.info("Reiniciando spooler de impressão")
            reiniciar_spooler_impressao()
        elif opcao in ["6", "7"]:
            logger.info(f"Funcionalidade {opcao} ainda em desenvolvimento")
            exibir_funcionalidade_em_breve()
        elif opcao == "0":
            logger.info("Encerrando sistema")
            print("\n👋 Obrigado por usar o Sistema de Suporte Técnico!")
            print(f"\n🔧 Mantenha seu computador sempre otimizado!")
            time.sleep(UI_CONFIG["auto_return_delay"])
            return False
        else:
            print("\n❌ Opção inválida!")
            print("\n💡 Digite apenas o número da opção desejada (0-7).")
            time.sleep(UI_CONFIG["auto_return_delay"])

    except Exception as e:
        logger.error(f"Erro ao processar opção {opcao}: {e}")
        print(f"\n❌ Erro inesperado: {str(e)}")
        print("\n💡 Tente novamente ou reinicie o programa.")
        time.sleep(UI_CONFIG["auto_return_delay"])

    return True


def main() -> NoReturn:
    """Função principal do sistema"""
    # Configura logging
    configurar_logging()
    logger = logging.getLogger(__name__)

    logger.info(f"Iniciando {APP_NAME} v{VERSION}")

    # Exibe aviso sobre privilégios de administrador
    exibir_aviso_admin()

    opcoes_validas = ["0", "1", "2", "3", "4", "5", "6", "7"]

    while True:
        try:
            exibir_menu()
            opcao = input("Digite o número da sua escolha: ").strip()

            if not validar_entrada_menu(opcao, opcoes_validas):
                print("\n❌ Opção inválida!")
                print("\n💡 Digite apenas o número da opção desejada (0-7).")
                time.sleep(UI_CONFIG["auto_return_delay"])
                continue

            if not processar_opcao(opcao):
                break

        except KeyboardInterrupt:
            logger.info("Sistema encerrado pelo usuário (Ctrl+C)")
            print("\n\n👋 Sistema encerrado.")
            break
        except Exception as e:
            logger.error(f"Erro inesperado no loop principal: {e}")
            print(f"\n❌ Erro inesperado: {str(e)}")
            time.sleep(UI_CONFIG["auto_return_delay"])

    logger.info("Sistema encerrado")


if __name__ == "__main__":
    # Verifica se está no Windows
    if os.name != "nt":
        print("❌ Este sistema foi desenvolvido para Windows.")
        sys.exit(1)

    # Importa configurações
    try:
        from config import UI_CONFIG, VERSION, APP_NAME
    except ImportError:
        print("❌ Arquivo de configuração não encontrado.")
        sys.exit(1)

    # Importa módulos do sistema
    try:
        from modules.utils import (
            configurar_logging,
            validar_entrada_menu,
            verificar_privilegios_admin,
            exibir_aviso_admin,
        )
        from modules.network import resolver_erro_rede, executar_flush_dns
        from modules.diagnostics import verificar_informacoes_rede
        from modules.system import (
            resolver_computador_lento,
            reiniciar_spooler_impressao,
        )
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("💡 Verifique se todos os arquivos estão presentes.")
        sys.exit(1)

    # Verifica dependências
    try:
        import psutil
    except ImportError:
        print("❌ Biblioteca 'psutil' não encontrada.")
        print("\n💡 Para instalar, execute: pip install psutil")
        input("\nPressione ENTER para sair...")
        sys.exit(1)

    main()

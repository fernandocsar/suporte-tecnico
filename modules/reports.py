"""Módulo para geração de relatórios de diagnóstico"""

import os
import json
import time
import datetime
import platform
import psutil
from typing import Dict, List, Optional, Any
from pathlib import Path
from .utils import corrigir_encoding_windows, executar_comando_seguro
from config import VERSION, APP_NAME, LOGGING_CONFIG


class RelatorioDiagnostico:
    """Classe para geração de relatórios de diagnóstico"""

    def __init__(self):
        self.dados = {
            "metadata": {
                "sistema": APP_NAME,
                "versao": VERSION,
                "data_geracao": datetime.datetime.now().isoformat(),
                "plataforma": platform.system(),
                "arquitetura": platform.architecture()[0],
                "hostname": platform.node(),
            },
            "sistema": {},
            "rede": {},
            "programas": {},
            "problemas": [],
            "acoes_realizadas": [],
        }
        # Cria a pasta de relatórios se não existir
        self.pasta_relatorios = Path("reports")
        self.pasta_relatorios.mkdir(exist_ok=True)

    def coletar_dados_sistema(self) -> None:
        """Coleta dados básicos do sistema"""
        try:
            # Informações do sistema operacional
            self.dados["sistema"] = {
                "os": platform.system(),
                "versao": platform.version(),
                "release": platform.release(),
                "arquitetura": platform.architecture()[0],
                "processador": platform.processor(),
                "hostname": platform.node(),
                "uptime": self._obter_uptime(),
                "usuarios_ativos": len(psutil.users()),
            }

            # Informações de memória
            memoria = psutil.virtual_memory()
            self.dados["sistema"]["memoria"] = {
                "total_gb": memoria.total // (1024**3),
                "disponivel_gb": memoria.available // (1024**3),
                "usado_gb": memoria.used // (1024**3),
                "percentual_uso": memoria.percent,
            }

            # Informações de disco
            disco = psutil.disk_usage("C:\\")
            self.dados["sistema"]["disco"] = {
                "total_gb": disco.total // (1024**3),
                "usado_gb": disco.used // (1024**3),
                "livre_gb": disco.free // (1024**3),
                "percentual_uso": (disco.used / disco.total) * 100,
            }

            # Informações de CPU
            self.dados["sistema"]["cpu"] = {
                "cores_fisicos": psutil.cpu_count(),
                "cores_logicos": psutil.cpu_count(logical=True),
                "uso_atual": psutil.cpu_percent(interval=1),
            }

        except Exception as e:
            self._adicionar_problema(
                "sistema", "Erro ao coletar dados do sistema", str(e)
            )

    def coletar_dados_rede(self) -> None:
        """Coleta dados de rede"""
        try:
            self.dados["rede"] = {
                "conectividade": self._testar_conectividade(),
                "configuracao_ip": self._obter_configuracao_ip(),
                "servidores_dns": self._obter_servidores_dns(),
                "interfaces_ativas": self._obter_interfaces_ativas(),
            }
        except Exception as e:
            self._adicionar_problema("rede", "Erro ao coletar dados de rede", str(e))

    def coletar_dados_programas(self) -> None:
        """Coleta dados de programas e processos"""
        try:
            self.dados["programas"] = {
                "processos_ativos": len(list(psutil.process_iter())),
                "processos_alto_consumo": self._obter_processos_alto_consumo(),
                "servicos_sistema": self._obter_servicos_sistema(),
                "aplicacoes_instaladas": self._obter_aplicacoes_instaladas(),
            }
        except Exception as e:
            self._adicionar_problema(
                "programas", "Erro ao coletar dados de programas", str(e)
            )

    def _obter_uptime(self) -> str:
        """Obtém o tempo de atividade do sistema"""
        try:
            uptime_seconds = time.time() - psutil.boot_time()
            uptime_hours = uptime_seconds // 3600
            uptime_days = uptime_hours // 24
            return f"{int(uptime_days)} dias, {int(uptime_hours % 24)} horas"
        except:
            return "Desconhecido"

    def _testar_conectividade(self) -> Dict:
        """Testa conectividade com servidores externos"""
        servidores = ["8.8.8.8", "google.com", "github.com"]
        resultados = {}

        for servidor in servidores:
            try:
                resultado = executar_comando_seguro(f"ping -n 1 {servidor}", timeout=5)
                resultados[servidor] = resultado.returncode == 0 if resultado else False
            except:
                resultados[servidor] = False

        return resultados

    def _obter_configuracao_ip(self) -> Dict:
        """Obtém configuração IP atual"""
        try:
            resultado = executar_comando_seguro("ipconfig", timeout=10)
            if resultado and resultado.returncode == 0:
                return {"status": "Disponível", "configuracao": resultado.stdout[:500]}
            else:
                return {"status": "Erro ao obter"}
        except:
            return {"status": "Não disponível"}

    def _obter_servidores_dns(self) -> List[str]:
        """Obtém servidores DNS configurados"""
        try:
            resultado = executar_comando_seguro("nslookup", input="exit\n", timeout=5)
            if resultado and resultado.returncode == 0:
                linhas = resultado.stdout.split("\n")
                dns_servers = []
                for linha in linhas:
                    if "Server:" in linha or "Servidor:" in linha:
                        dns_servers.append(linha.strip())
                return dns_servers
        except:
            pass
        return []

    def _obter_interfaces_ativas(self) -> List[str]:
        """Obtém interfaces de rede ativas"""
        try:
            stats = psutil.net_if_stats()
            return [interface for interface, stat in stats.items() if stat.isup]
        except:
            return []

    def _obter_processos_alto_consumo(self) -> List[Dict]:
        """Obtém processos com alto consumo de recursos"""
        processos = []
        try:
            for proc in psutil.process_iter(
                ["pid", "name", "cpu_percent", "memory_percent"]
            ):
                try:
                    info = proc.info
                    if info["cpu_percent"] > 10 or info["memory_percent"] > 5:
                        processos.append(
                            {
                                "pid": info["pid"],
                                "nome": info["name"],
                                "cpu_percent": info["cpu_percent"],
                                "memory_percent": info["memory_percent"],
                            }
                        )
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except:
            pass
        return processos[:10]  # Limita a 10 processos

    def _obter_servicos_sistema(self) -> Dict:
        """Obtém informações de serviços do sistema"""
        try:
            resultado = executar_comando_seguro("sc query", timeout=30)
            if resultado and resultado.returncode == 0:
                servicos = resultado.stdout.split("\n")
                servicos_ativos = len([s for s in servicos if "RUNNING" in s])
                return {
                    "total_servicos": len(servicos) // 4,  # Aproximação
                    "servicos_ativos": servicos_ativos,
                }
        except:
            pass
        return {"total_servicos": 0, "servicos_ativos": 0}

    def _obter_aplicacoes_instaladas(self) -> int:
        """Obtém número de aplicações instaladas"""
        try:
            resultado = executar_comando_seguro(
                "wmic product get name /format:list", timeout=60
            )
            if resultado and resultado.returncode == 0:
                return len([l for l in resultado.stdout.split("\n") if "Name=" in l])
        except:
            pass
        return 0

    def _adicionar_problema(
        self, categoria: str, descricao: str, detalhes: str = ""
    ) -> None:
        """Adiciona um problema detectado ao relatório"""
        self.dados["problemas"].append(
            {
                "categoria": categoria,
                "descricao": descricao,
                "detalhes": detalhes,
                "timestamp": datetime.datetime.now().isoformat(),
            }
        )

    def adicionar_acao_realizada(self, acao: str, resultado: str = "") -> None:
        """Adiciona uma ação realizada ao relatório"""
        self.dados["acoes_realizadas"].append(
            {
                "acao": acao,
                "resultado": resultado,
                "timestamp": datetime.datetime.now().isoformat(),
            }
        )

    def gerar_relatorio_json(self, caminho_arquivo: str = None) -> str:
        """Gera relatório em formato JSON"""
        if not caminho_arquivo:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_arquivo = (
                self.pasta_relatorios / f"relatorio_diagnostico_{timestamp}.json"
            )

        try:
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, indent=2, ensure_ascii=False)
            return str(caminho_arquivo)
        except Exception as e:
            self._adicionar_problema(
                "relatorio", "Erro ao gerar relatório JSON", str(e)
            )
            return ""

    def gerar_relatorio_texto(self, caminho_arquivo: str = None) -> str:
        """Gera relatório em formato texto"""
        if not caminho_arquivo:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_arquivo = (
                self.pasta_relatorios / f"relatorio_diagnostico_{timestamp}.txt"
            )

        try:
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(self._formatar_relatorio_texto())
            return str(caminho_arquivo)
        except Exception as e:
            self._adicionar_problema(
                "relatorio", "Erro ao gerar relatório texto", str(e)
            )
            return ""

    def _formatar_relatorio_texto(self) -> str:
        """Formata relatório para texto"""
        relatorio = []
        relatorio.append("=" * 80)
        relatorio.append(f"{APP_NAME} - Relatório de Diagnóstico")
        relatorio.append(f"Versão: {VERSION}")
        relatorio.append(
            f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )
        relatorio.append("=" * 80)
        relatorio.append("")

        # Informações do sistema
        relatorio.append("📊 INFORMAÇÕES DO SISTEMA")
        relatorio.append("-" * 40)
        if "sistema" in self.dados:
            sys_info = self.dados["sistema"]
            relatorio.append(
                f"Sistema Operacional: {sys_info.get('os', 'N/A')} {sys_info.get('release', '')}"
            )
            relatorio.append(f"Arquitetura: {sys_info.get('arquitetura', 'N/A')}")
            relatorio.append(f"Processador: {sys_info.get('processador', 'N/A')}")
            relatorio.append(f"Hostname: {sys_info.get('hostname', 'N/A')}")
            relatorio.append(f"Uptime: {sys_info.get('uptime', 'N/A')}")
            relatorio.append("")

        # Informações de rede
        relatorio.append("🌐 INFORMAÇÕES DE REDE")
        relatorio.append("-" * 40)
        if "rede" in self.dados:
            net_info = self.dados["rede"]
            conectividade = net_info.get("conectividade", {})
            for servidor, status in conectividade.items():
                status_texto = "✅ Conectado" if status else "❌ Desconectado"
                relatorio.append(f"{servidor}: {status_texto}")
            relatorio.append("")

        # Problemas detectados
        if self.dados["problemas"]:
            relatorio.append("⚠️ PROBLEMAS DETECTADOS")
            relatorio.append("-" * 40)
            for problema in self.dados["problemas"]:
                relatorio.append(f"Categoria: {problema['categoria']}")
                relatorio.append(f"Descrição: {problema['descricao']}")
                if problema["detalhes"]:
                    relatorio.append(f"Detalhes: {problema['detalhes']}")
                relatorio.append("")

        # Ações realizadas
        if self.dados["acoes_realizadas"]:
            relatorio.append("🎯 AÇÕES REALIZADAS")
            relatorio.append("-" * 40)
            for acao in self.dados["acoes_realizadas"]:
                relatorio.append(f"• {acao['acao']}")
                if acao["resultado"]:
                    relatorio.append(f"  Resultado: {acao['resultado']}")
            relatorio.append("")

        relatorio.append("=" * 80)
        relatorio.append(
            "Relatório gerado automaticamente pelo Sistema de Suporte Técnico"
        )
        relatorio.append("=" * 80)

        return "\n".join(relatorio)

    def gerar_relatorio_html(self, caminho_arquivo: str = None) -> str:
        """Gera relatório em formato HTML"""
        if not caminho_arquivo:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_arquivo = (
                self.pasta_relatorios / f"relatorio_diagnostico_{timestamp}.html"
            )

        try:
            html_content = self._formatar_relatorio_html()
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(html_content)
            return str(caminho_arquivo)
        except Exception as e:
            self._adicionar_problema(
                "relatorio", "Erro ao gerar relatório HTML", str(e)
            )
            return ""

    def _formatar_relatorio_html(self) -> str:
        """Formata relatório para HTML"""
        html = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Diagnóstico - {APP_NAME}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; border-bottom: 2px solid #007acc; padding-bottom: 20px; margin-bottom: 30px; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{ color: #007acc; border-bottom: 1px solid #ddd; padding-bottom: 10px; }}
        .info-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .info-card {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #007acc; }}
        .problem {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .success {{ background-color: #d4edda; border-left: 4px solid #28a745; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔧 {APP_NAME}</h1>
            <h2>Relatório de Diagnóstico</h2>
            <p class="timestamp">Gerado em: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
            <p>Versão: {VERSION}</p>
        </div>
        
        <div class="section">
            <h2>📊 Informações do Sistema</h2>
            <div class="info-grid">
"""

        # Adiciona informações do sistema
        if "sistema" in self.dados:
            sys_info = self.dados["sistema"]
            html += f"""
                <div class="info-card">
                    <h3>Sistema Operacional</h3>
                    <p><strong>OS:</strong> {sys_info.get('os', 'N/A')} {sys_info.get('release', '')}</p>
                    <p><strong>Arquitetura:</strong> {sys_info.get('arquitetura', 'N/A')}</p>
                    <p><strong>Processador:</strong> {sys_info.get('processador', 'N/A')}</p>
                    <p><strong>Hostname:</strong> {sys_info.get('hostname', 'N/A')}</p>
                </div>
                <div class="info-card">
                    <h3>Recursos</h3>
                    <p><strong>Memória Total:</strong> {sys_info.get('memoria', {}).get('total_gb', 0)} GB</p>
                    <p><strong>Memória Usada:</strong> {sys_info.get('memoria', {}).get('percentual_uso', 0):.1f}%</p>
                    <p><strong>Disco Total:</strong> {sys_info.get('disco', {}).get('total_gb', 0)} GB</p>
                    <p><strong>Disco Usado:</strong> {sys_info.get('disco', {}).get('percentual_uso', 0):.1f}%</p>
                </div>
            """

        html += """
            </div>
        </div>
        """

        # Adiciona problemas detectados
        if self.dados["problemas"]:
            html += """
        <div class="section">
            <h2>⚠️ Problemas Detectados</h2>
            """
            for problema in self.dados["problemas"]:
                html += f"""
            <div class="problem">
                <h4>{problema['categoria'].title()}</h4>
                <p><strong>Descrição:</strong> {problema['descricao']}</p>
                {f"<p><strong>Detalhes:</strong> {problema['detalhes']}</p>" if problema['detalhes'] else ""}
                <p class="timestamp">{problema['timestamp']}</p>
            </div>
                """
            html += """
        </div>
        """

        # Adiciona ações realizadas
        if self.dados["acoes_realizadas"]:
            html += """
        <div class="section">
            <h2>🎯 Ações Realizadas</h2>
            """
            for acao in self.dados["acoes_realizadas"]:
                html += f"""
            <div class="success">
                <h4>{acao['acao']}</h4>
                {f"<p><strong>Resultado:</strong> {acao['resultado']}</p>" if acao['resultado'] else ""}
                <p class="timestamp">{acao['timestamp']}</p>
            </div>
                """
            html += """
        </div>
        """

        html += """
    </div>
</body>
</html>
        """

        return html


def gerar_relatorio_completo(formato: str = "texto") -> str:
    """Gera um relatório completo de diagnóstico

    Args:
        formato: Formato do relatório ('texto', 'json', 'html')

    Returns:
        Caminho do arquivo gerado
    """
    relatorio = RelatorioDiagnostico()

    print("🔍 Coletando dados do sistema...")
    relatorio.coletar_dados_sistema()

    print("🌐 Coletando dados de rede...")
    relatorio.coletar_dados_rede()

    print("💻 Coletando dados de programas...")
    relatorio.coletar_dados_programas()

    # Gera relatório no formato solicitado
    if formato.lower() == "json":
        caminho = relatorio.gerar_relatorio_json()
    elif formato.lower() == "html":
        caminho = relatorio.gerar_relatorio_html()
    else:
        caminho = relatorio.gerar_relatorio_texto()

    if caminho:
        print(f"✅ Relatório gerado com sucesso: {caminho}")
        return caminho
    else:
        print("❌ Erro ao gerar relatório")
        return ""


def gerar_relatorio_rapido() -> str:
    """Gera um relatório rápido com informações essenciais"""
    relatorio = RelatorioDiagnostico()

    print("🔍 Coletando informações essenciais...")
    relatorio.coletar_dados_sistema()
    relatorio.coletar_dados_rede()

    caminho = relatorio.gerar_relatorio_texto()

    if caminho:
        print(f"✅ Relatório rápido gerado: {caminho}")
        return caminho
    else:
        print("❌ Erro ao gerar relatório rápido")
        return ""

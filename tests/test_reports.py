"""Testes para o módulo reports"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import tempfile
import json

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.reports import (
    RelatorioDiagnostico,
    gerar_relatorio_completo,
    gerar_relatorio_rapido,
)


class TestRelatorioDiagnostico(unittest.TestCase):
    """Testes para a classe RelatorioDiagnostico"""

    def setUp(self):
        """Configuração inicial para cada teste"""
        self.relatorio = RelatorioDiagnostico()

    def test_inicializacao(self):
        """Testa inicialização da classe"""
        self.assertIsNotNone(self.relatorio.dados)
        self.assertIn("metadata", self.relatorio.dados)
        self.assertIn("sistema", self.relatorio.dados)
        self.assertIn("hardware", self.relatorio.dados)
        self.assertIn("rede", self.relatorio.dados)
        self.assertIn("programas", self.relatorio.dados)
        self.assertIn("problemas", self.relatorio.dados)
        self.assertIn("acoes_realizadas", self.relatorio.dados)

    def test_adicionar_problema(self):
        """Testa adição de problemas ao relatório"""
        self.relatorio._adicionar_problema(
            "teste", "Problema de teste", "Detalhes do problema"
        )

        self.assertEqual(len(self.relatorio.dados["problemas"]), 1)
        problema = self.relatorio.dados["problemas"][0]
        self.assertEqual(problema["categoria"], "teste")
        self.assertEqual(problema["descricao"], "Problema de teste")
        self.assertEqual(problema["detalhes"], "Detalhes do problema")

    def test_adicionar_acao_realizada(self):
        """Testa adição de ações realizadas ao relatório"""
        self.relatorio.adicionar_acao_realizada("Teste de ação", "Sucesso")

        self.assertEqual(len(self.relatorio.dados["acoes_realizadas"]), 1)
        acao = self.relatorio.dados["acoes_realizadas"][0]
        self.assertEqual(acao["acao"], "Teste de ação")
        self.assertEqual(acao["resultado"], "Sucesso")

    @patch("modules.reports.executar_comando_seguro")
    def test_obter_uptime(self, mock_executar_comando):
        """Testa obtenção de uptime"""
        uptime = self.relatorio._obter_uptime()
        self.assertIsInstance(uptime, str)
        self.assertIn("dias", uptime or "horas", uptime)

    def test_gerar_relatorio_json(self):
        """Testa geração de relatório JSON"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            caminho_temp = f.name

        try:
            caminho = self.relatorio.gerar_relatorio_json(caminho_temp)
            self.assertEqual(caminho, caminho_temp)

            # Verifica se o arquivo foi criado e contém JSON válido
            with open(caminho_temp, "r", encoding="utf-8") as f:
                dados = json.load(f)

            self.assertIn("metadata", dados)
            self.assertIn("sistema", dados)

        finally:
            if os.path.exists(caminho_temp):
                os.unlink(caminho_temp)

    def test_gerar_relatorio_texto(self):
        """Testa geração de relatório texto"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            caminho_temp = f.name

        try:
            caminho = self.relatorio.gerar_relatorio_texto(caminho_temp)
            self.assertEqual(caminho, caminho_temp)

            # Verifica se o arquivo foi criado
            with open(caminho_temp, "r", encoding="utf-8") as f:
                conteudo = f.read()

            self.assertIn("Relatório de Diagnóstico", conteudo)
            self.assertIn("INFORMAÇÕES DO SISTEMA", conteudo)

        finally:
            if os.path.exists(caminho_temp):
                os.unlink(caminho_temp)

    def test_gerar_relatorio_html(self):
        """Testa geração de relatório HTML"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as f:
            caminho_temp = f.name

        try:
            caminho = self.relatorio.gerar_relatorio_html(caminho_temp)
            self.assertEqual(caminho, caminho_temp)

            # Verifica se o arquivo foi criado
            with open(caminho_temp, "r", encoding="utf-8") as f:
                conteudo = f.read()

            self.assertIn("<!DOCTYPE html>", conteudo)
            self.assertIn("Relatório de Diagnóstico", conteudo)

        finally:
            if os.path.exists(caminho_temp):
                os.unlink(caminho_temp)

    @patch("modules.reports.psutil")
    def test_coletar_dados_sistema(self, mock_psutil):
        """Testa coleta de dados do sistema"""
        # Mock para psutil
        mock_psutil.virtual_memory.return_value = MagicMock(
            total=8589934592,  # 8GB
            available=4294967296,  # 4GB
            used=4294967296,  # 4GB
            percent=50.0,
        )
        mock_psutil.disk_usage.return_value = MagicMock(
            total=107374182400,  # 100GB
            used=53687091200,  # 50GB
            free=53687091200,  # 50GB
        )
        mock_psutil.cpu_count.return_value = 4
        mock_psutil.cpu_percent.return_value = 25.0
        mock_psutil.users.return_value = [MagicMock()]

        self.relatorio.coletar_dados_sistema()

        self.assertIn("sistema", self.relatorio.dados)
        self.assertIn("memoria", self.relatorio.dados["sistema"])
        self.assertIn("disco", self.relatorio.dados["sistema"])
        self.assertIn("cpu", self.relatorio.dados["sistema"])

    @patch("modules.reports.executar_comando_seguro")
    def test_coletar_dados_rede(self, mock_executar_comando):
        """Testa coleta de dados de rede"""
        # Mock para comandos de rede
        mock_executar_comando.return_value = MagicMock(
            returncode=0, stdout="ping response"
        )

        self.relatorio.coletar_dados_rede()

        self.assertIn("rede", self.relatorio.dados)
        self.assertIn("conectividade", self.relatorio.dados["rede"])


class TestFuncoesRelatorio(unittest.TestCase):
    """Testes para funções de relatório"""

    @patch("modules.reports.RelatorioDiagnostico")
    def test_gerar_relatorio_completo(self, mock_relatorio_class):
        """Testa geração de relatório completo"""
        # Mock da classe RelatorioDiagnostico
        mock_relatorio = MagicMock()
        mock_relatorio_class.return_value = mock_relatorio
        mock_relatorio.gerar_relatorio_texto.return_value = "relatorio.txt"

        caminho = gerar_relatorio_completo("texto")

        self.assertEqual(caminho, "relatorio.txt")
        mock_relatorio.coletar_dados_sistema.assert_called_once()
        mock_relatorio.coletar_dados_hardware.assert_called_once()
        mock_relatorio.coletar_dados_rede.assert_called_once()
        mock_relatorio.coletar_dados_programas.assert_called_once()

    @patch("modules.reports.RelatorioDiagnostico")
    def test_gerar_relatorio_rapido(self, mock_relatorio_class):
        """Testa geração de relatório rápido"""
        # Mock da classe RelatorioDiagnostico
        mock_relatorio = MagicMock()
        mock_relatorio_class.return_value = mock_relatorio
        mock_relatorio.gerar_relatorio_texto.return_value = "relatorio_rapido.txt"

        caminho = gerar_relatorio_rapido()

        self.assertEqual(caminho, "relatorio_rapido.txt")
        mock_relatorio.coletar_dados_sistema.assert_called_once()
        mock_relatorio.coletar_dados_rede.assert_called_once()


if __name__ == "__main__":
    unittest.main()

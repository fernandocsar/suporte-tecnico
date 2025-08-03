"""Testes para o módulo network"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.network import testar_conectividade_basica, verificar_tipo_conexao


class TestNetwork(unittest.TestCase):
    """Testes para funções de rede"""

    @patch("subprocess.run")
    def test_testar_conectividade_basica(self, mock_run):
        """Testa conectividade básica"""
        # Mock de ping bem-sucedido
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        resultado = testar_conectividade_basica()
        self.assertTrue(resultado)

        # Mock de ping falhado
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        resultado = testar_conectividade_basica()
        self.assertFalse(resultado)

    @patch("psutil.net_if_stats")
    @patch("modules.network.testar_conectividade_basica")
    def test_verificar_tipo_conexao(self, mock_conectividade, mock_interfaces):
        """Testa verificação de tipo de conexão"""
        # Mock de interfaces
        mock_stats = MagicMock()
        mock_stats.isup = True

        mock_interfaces.return_value = {"Ethernet": mock_stats, "WiFi": mock_stats}

        mock_conectividade.return_value = True

        conexoes, tem_internet = verificar_tipo_conexao()

        self.assertTrue(tem_internet)
        self.assertEqual(len(conexoes), 2)

        # Verifica se detectou cabo e wifi
        tipos = [conexao[0] for conexao in conexoes]
        self.assertIn("cabo", tipos)
        self.assertIn("wifi", tipos)


if __name__ == "__main__":
    unittest.main()

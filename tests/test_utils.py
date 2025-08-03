"""Testes para o módulo utils"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.utils import (
    corrigir_encoding_windows,
    executar_comando_seguro,
    validar_entrada_menu,
    formatar_tamanho_arquivo,
    verificar_privilegios_admin,
)


class TestUtils(unittest.TestCase):
    """Testes para funções utilitárias"""

    def test_corrigir_encoding_windows(self):
        """Testa correção de encoding"""
        # Testa correções conhecidas
        self.assertEqual(corrigir_encoding_windows("‡Æo"), "ção")
        self.assertEqual(corrigir_encoding_windows("Pol¡tica"), "Política")
        self.assertEqual(corrigir_encoding_windows("ˆxito"), "êxito")

        # Testa texto sem problemas
        self.assertEqual(corrigir_encoding_windows("texto normal"), "texto normal")

        # Testa texto vazio
        self.assertEqual(corrigir_encoding_windows(""), "")
        self.assertEqual(corrigir_encoding_windows(None), None)

    def test_validar_entrada_menu(self):
        """Testa validação de entrada do menu"""
        opcoes = ["1", "2", "3", "0"]

        # Testa entradas válidas
        self.assertTrue(validar_entrada_menu("1", opcoes))
        self.assertTrue(validar_entrada_menu("0", opcoes))
        self.assertTrue(validar_entrada_menu(" 2 ", opcoes))  # Com espaços

        # Testa entradas inválidas
        self.assertFalse(validar_entrada_menu("4", opcoes))
        self.assertFalse(validar_entrada_menu("a", opcoes))
        self.assertFalse(validar_entrada_menu("", opcoes))

    def test_formatar_tamanho_arquivo(self):
        """Testa formatação de tamanho de arquivo"""
        self.assertEqual(formatar_tamanho_arquivo(512), "512.0 B")
        self.assertEqual(formatar_tamanho_arquivo(1024), "1.0 KB")
        self.assertEqual(formatar_tamanho_arquivo(1048576), "1.0 MB")
        self.assertEqual(formatar_tamanho_arquivo(1073741824), "1.0 GB")

    @patch("subprocess.run")
    def test_executar_comando_seguro(self, mock_run):
        """Testa execução segura de comandos"""
        # Mock de resultado bem-sucedido
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "sucesso"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        resultado = executar_comando_seguro("echo teste")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.returncode, 0)
        self.assertEqual(resultado.stdout, "sucesso")

        # Verifica se o comando foi chamado corretamente
        mock_run.assert_called_once()


if __name__ == "__main__":
    unittest.main()

import subprocess
import psutil
import socket
from .utils import limpar_tela, corrigir_encoding_windows, executar_comando_seguro

# Todas as funções de diagnóstico aqui:
# - verificar_informacoes_rede()
# - exibir_ip_computador()
# - exibir_conectividade_basica()
# - exibir_configuracao_ip()
# - exibir_interfaces_rede()
# - testar_conectividade()

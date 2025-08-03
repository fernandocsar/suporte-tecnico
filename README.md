# 🔧 Sistema de Suporte Técnico

Sistema automatizado para resolução de problemas comuns em computadores Windows, desenvolvido para facilitar o suporte técnico em ambientes corporativos.

## 📋 Funcionalidades

### 1. 🌐 Problemas de Rede
- Detecção automática do tipo de conexão (WiFi/Cabo)
- Aplicação de políticas de grupo com `gpupdate /force`
- Orientações específicas para conexões corporativas
- Verificação de conectividade com a internet

### 2. 🔄 Flush DNS (Limpar Cache DNS)
- Execução automática de comandos DNS:
  - `ipconfig /flushdns`
  - `ipconfig /registerdns`
  - `ipconfig /release`
  - `ipconfig /renew`
- Resolução de problemas de resolução de nomes

### 3. 📊 Verificar Informações da Rede
- Exibição completa das configurações de rede
- Informações de IP, gateway e DNS
- Status das interfaces de rede
- Teste de conectividade com sites essenciais

### 4. 🐌 Computador Lento
- Verificação de espaço em disco
- Limpeza de arquivos temporários
- Limpeza de cache do sistema
- Análise de processos com alto consumo de recursos
- Verificação de integridade do sistema

### 5. 🖨️ Reiniciar Spooler de Impressão
- Parada segura do serviço de spooler
- Limpeza de arquivos de fila de impressão
- Reinicialização do serviço
- Verificação de status do serviço

### 6. 💻 Problemas com Programas (Em Desenvolvimento)
- Funcionalidade planejada para gerenciamento de processos
- Correção de aplicações travadas
- Limpeza de cache de programas

### 7. 🔧 Problemas de Hardware (Em Desenvolvimento)
- Funcionalidade planejada para diagnósticos de hardware

## 🚀 Como Usar

### Pré-requisitos
- Windows 10 ou superior
- Python 3.6+
- Biblioteca `psutil`

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/fernandocsar/suporte-tecnico
cd suporte-tecnico
```

2. Instale as dependências:
```bash
pip install psutil
```

3. Execute o sistema:
```bash
python suporte_tecnico.py
```

### Execução como Administrador

Para funcionalidades que requerem privilégios administrativos (como políticas de grupo e serviços), execute o prompt de comando como Administrador antes de rodar o script.
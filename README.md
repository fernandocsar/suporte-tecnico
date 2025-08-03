# 🔧 Sistema de Suporte Técnico

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)]()

Sistema automatizado para resolução de problemas comuns em computadores Windows, desenvolvido para facilitar o suporte técnico em ambientes corporativos.

## 🚀 Características

- **Interface Intuitiva**: Menu simples com emojis e descrições claras
- **Execução Segura**: Timeouts configurados e tratamento robusto de erros
- **Logging Completo**: Sistema de logs para auditoria e debugging
- **Modular**: Arquitetura organizada em módulos especializados
- **Configurável**: Arquivo de configuração centralizado
- **Testado**: Suite de testes unitários incluída

## 📋 Funcionalidades

### 🌐 1. Problemas de Rede
- Detecção automática do tipo de conexão (WiFi/Cabo)
- Aplicação de políticas de grupo com `gpupdate /force`
- Orientações específicas para conexões corporativas
- Verificação de conectividade com a internet

### 🔄 2. Flush DNS (Limpar Cache DNS)
- Execução automática de comandos DNS:
  - `ipconfig /flushdns`
  - `ipconfig /registerdns`
  - `ipconfig /release`
  - `ipconfig /renew`
- Resolução de problemas de resolução de nomes

### 📊 3. Verificar Informações da Rede
- Exibição completa das configurações de rede
- Informações de IP, gateway e DNS
- Status das interfaces de rede
- Teste de conectividade com sites essenciais
- Diagnóstico automático de problemas

### 🐌 4. Computador Lento
- Verificação de espaço em disco
- Limpeza de arquivos temporários
- Limpeza de cache do sistema
- Análise de processos com alto consumo de recursos
- Verificação de integridade do sistema

### 🖨️ 5. Reiniciar Spooler de Impressão
- Parada segura do serviço de spooler
- Limpeza de arquivos de fila de impressão
- Reinicialização do serviço
- Verificação de status do serviço

### 💻 6. Problemas com Programas (Em Desenvolvimento)
- Gerenciamento de processos travados
- Correção de aplicações não responsivas
- Limpeza de cache de programas

### 🔧 7. Problemas de Hardware (Em Desenvolvimento)
- Diagnósticos de hardware
- Verificação de drivers

## 🛠️ Instalação

### Pré-requisitos
- Windows 7 ou superior
- Python 3.6+
- Privilégios de administrador (recomendado)

### Instalação Rápida

1. **Clone o repositório**:
```bash
git clone https://github.com/fernandocsar/suporte-tecnico
cd suporte-tecnico
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Execute o sistema**:
```bash
python suporte_tecnico.py
```

### Instalação como Pacote

```bash
pip install -e .
```

Após a instalação, execute:
```bash
suporte-tecnico
```
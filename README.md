# 🔧 Sistema de Suporte Técnico

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)]()
[![Version](https://img.shields.io/badge/version-1.1.0-orange.svg)]()

Sistema automatizado para resolução de problemas comuns em computadores Windows, desenvolvido para facilitar o suporte técnico em ambientes corporativos.

## 🚀 Características

- **Interface Intuitiva**: Menu simples com emojis e descrições claras
- **Execução Segura**: Timeouts configurados e tratamento robusto de erros
- **Logging Completo**: Sistema de logs para auditoria e debugging
- **Modular**: Arquitetura organizada em módulos especializados
- **Configurável**: Arquivo de configuração centralizado
- **Testado**: Suite de testes unitários incluída
- **Relatórios**: Sistema completo de geração de relatórios de diagnóstico

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

### 💻 6. Problemas com Programas
- **Gerenciamento de processos travados**
  - Detecção de processos com alto consumo de CPU/memória
  - Finalização segura de processos problemáticos
  - Análise de processos em tempo real

- **Limpeza de cache de programas**
  - Limpeza de cache do Windows
  - Limpeza de arquivos temporários
  - Limpeza de cache de navegadores

- **Reparação de aplicações Windows**
  - Execução de DISM para reparar componentes
  - Execução de SFC para verificar integridade
  - Reparação automática de aplicações

- **Verificação de integridade**
  - Verificação de arquivos do sistema
  - Limpeza de registros corrompidos
  - Análise de integridade

### 📋 7. Gerar Relatório de Diagnóstico
- **Relatório rápido (texto)**
  - Informações essenciais do sistema
  - Status de conectividade
  - Problemas detectados

- **Relatório completo (texto)**
  - Análise completa do sistema
  - Informações detalhadas de hardware
  - Status de rede e programas
  - Histórico de ações realizadas

- **Relatório completo (HTML)**
  - Interface visual moderna
  - Gráficos e indicadores
  - Relatório interativo
  - Fácil compartilhamento

- **Relatório completo (JSON)**
  - Dados estruturados
  - Integração com outros sistemas
  - Análise programática
  - Exportação de dados

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
python technical_support.py
```

### Instalação como Pacote

```bash
pip install -e .
```

Após a instalação, execute:
```bash
technical-support
```

## 📊 Estrutura do Projeto

```
suporte-tecnico/
├── technical_support.py      # Arquivo principal
├── config.py                 # Configurações centralizadas
├── requirements.txt          # Dependências
├── setup.py                 # Configuração do pacote
├── README.md                # Documentação
├── reports/                 # 📁 Pasta para relatórios gerados
├── modules/                 # Módulos especializados
│   ├── __init__.py
│   ├── utils.py            # Utilitários gerais
│   ├── network.py          # Funcionalidades de rede
│   ├── system.py           # Funcionalidades do sistema
│   ├── diagnostics.py      # Diagnósticos
│   ├── programs.py         # Problemas com programas
│   └── reports.py          # Sistema de relatórios
└── tests/                  # Testes unitários
    ├── __init__.py
    ├── test_utils.py
    ├── test_network.py
    └── test_reports.py
```

## 🎯 Uso

### Execução Básica
```bash
python technical_support.py
```

### Geração de Relatórios
```python
from modules.reports import gerar_relatorio_completo, gerar_relatorio_rapido

# Relatório rápido
caminho = gerar_relatorio_rapido()

# Relatório completo em diferentes formatos
caminho_texto = gerar_relatorio_completo("texto")
caminho_html = gerar_relatorio_completo("html")
caminho_json = gerar_relatorio_completo("json")
```

### Uso Programático
```python
from modules.reports import RelatorioDiagnostico

# Criar relatório personalizado
relatorio = RelatorioDiagnostico()
relatorio.coletar_dados_sistema()
relatorio.coletar_dados_rede()

# Adicionar problemas detectados
relatorio._adicionar_problema("rede", "Problema de conectividade", "Detalhes...")

# Adicionar ações realizadas
relatorio.adicionar_acao_realizada("Limpeza de cache", "Sucesso")

# Gerar relatório
caminho = relatorio.gerar_relatorio_html()
```

## 📁 Relatórios

Todos os relatórios gerados são automaticamente salvos na pasta `reports/` com os seguintes formatos:

- **Relatórios de texto**: `relatorio_diagnostico_YYYYMMDD_HHMMSS.txt`
- **Relatórios HTML**: `relatorio_diagnostico_YYYYMMDD_HHMMSS.html`
- **Relatórios JSON**: `relatorio_diagnostico_YYYYMMDD_HHMMSS.json`

### Exemplo de Estrutura de Relatórios
```
reports/
├── relatorio_diagnostico_20241219_143022.txt
├── relatorio_diagnostico_20241219_143045.html
├── relatorio_diagnostico_20241219_143112.json
└── ...
```

## 🧪 Testes

### Executar Todos os Testes
```bash
python -m unittest discover tests
```

### Executar Testes Específicos
```bash
python -m unittest tests.test_reports
python -m unittest tests.test_utils
python -m unittest tests.test_network
```

## 📈 Melhorias na Versão 1.1.0

### ✨ Novas Funcionalidades
- **Módulo de Programas**: Resolução completa de problemas com aplicações
- **Sistema de Relatórios**: Geração de relatórios em múltiplos formatos
- **Interface Melhorada**: Menu expandido com novas opções

### 🔧 Melhorias Técnicas
- **Arquitetura Modular**: Novos módulos especializados
- **Sistema de Relatórios**: Classe `RelatorioDiagnostico` completa
- **Testes Expandidos**: Cobertura de testes para novos módulos
- **Configurações**: Novas configurações para programas

### 📊 Relatórios Disponíveis
- **Formato Texto**: Relatórios legíveis e organizados
- **Formato HTML**: Interface visual moderna e responsiva
- **Formato JSON**: Dados estruturados para integração
- **Relatórios Rápidos**: Informações essenciais em segundos

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **Fernando César** - *Desenvolvimento inicial* - [fernandocsar](https://github.com/fernandocsar)

## 🙏 Agradecimentos

- Comunidade de usuários
- Contribuidores do projeto
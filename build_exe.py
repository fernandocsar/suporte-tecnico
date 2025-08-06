#!/usr/bin/env python3
"""
Script para gerar executável do Sistema de Suporte Técnico

Este script usa PyInstaller para criar um executável standalone
que não requer Python instalado no sistema.

Uso:
    python build_exe.py

Requisitos:
    pip install pyinstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def verificar_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller

        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller não encontrado")
        print("\n💡 Para instalar, execute:")
        print("   pip install pyinstaller")
        return False


def limpar_builds_anteriores():
    """Remove builds anteriores"""
    diretorios = ["build", "dist", "__pycache__"]
    arquivos = ["technical_support.spec"]

    print("🧹 Limpando builds anteriores...")

    for diretorio in diretorios:
        if os.path.exists(diretorio):
            shutil.rmtree(diretorio)
            print(f"   ✅ Removido: {diretorio}")

    for arquivo in arquivos:
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print(f"   ✅ Removido: {arquivo}")


def gerar_executavel():
    """Gera o executável usando PyInstaller"""
    print("\n🔨 Gerando executável...")

    # Comando PyInstaller
    comando = [
        "pyinstaller",
        "--onefile",  # Arquivo único
        "--name=TechnicalSupport",  # Nome do executável
        "--icon=icon.ico",  # Ícone (se existir)
        "--add-data=modules;modules",  # Incluir módulos
        "--add-data=config.py;.",  # Incluir configuração
        "--add-data=reports;reports",  # Incluir pasta de relatórios
        "--hidden-import=modules.compat",  # Importar módulo de compatibilidade
        "--hidden-import=modules.utils",
        "--hidden-import=modules.network",
        "--hidden-import=modules.system",
        "--hidden-import=modules.diagnostics",
        "--hidden-import=modules.programs",
        "--hidden-import=modules.reports",
        "technical_support.py",
    ]

    # Remove opções que podem não existir
    if not os.path.exists("icon.ico"):
        comando.remove("--icon=icon.ico")

    try:
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        print("✅ Executável gerado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao gerar executável: {e}")
        print(f"Stderr: {e.stderr}")
        return False


def verificar_executavel():
    """Verifica se o executável foi criado"""
    executavel = "dist/TechnicalSupport.exe"

    if os.path.exists(executavel):
        tamanho = os.path.getsize(executavel) / (1024 * 1024)  # MB
        print(f"\n✅ Executável criado: {executavel}")
        print(f"📊 Tamanho: {tamanho:.1f} MB")
        return True
    else:
        print(f"\n❌ Executável não encontrado: {executavel}")
        return False


def criar_instalador():
    """Cria um instalador simples (opcional)"""
    print("\n📦 Criando instalador...")

    # Cria pasta de distribuição
    dist_dir = "dist/TechnicalSupport"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

    os.makedirs(dist_dir)

    # Copia arquivos necessários
    arquivos = ["dist/TechnicalSupport.exe", "README.md", "LICENSE"]

    for arquivo in arquivos:
        if os.path.exists(arquivo):
            shutil.copy2(arquivo, dist_dir)
            print(f"   ✅ Copiado: {arquivo}")

    # Cria pasta de relatórios
    reports_dir = os.path.join(dist_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    print(f"✅ Instalador criado em: {dist_dir}")


def main():
    """Função principal"""
    print("=" * 60)
    print("           GERADOR DE EXECUTÁVEL")
    print("=" * 60)

    # Verifica PyInstaller
    if not verificar_pyinstaller():
        return False

    # Limpa builds anteriores
    limpar_builds_anteriores()

    # Gera executável
    if not gerar_executavel():
        return False

    # Verifica se foi criado
    if not verificar_executavel():
        return False

    # Cria instalador (opcional)
    try:
        criar_instalador()
    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível criar instalador: {e}")

    print("\n" + "=" * 60)
    print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print("\n🎯 Próximos passos:")
    print("   1. Teste o executável: dist/TechnicalSupport.exe")
    print("   2. Distribua o arquivo executável")
    print("   3. O executável funciona em qualquer Windows sem Python")

    return True


if __name__ == "__main__":
    sucesso = main()
    if not sucesso:
        sys.exit(1)

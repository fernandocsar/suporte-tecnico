from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="sistema-suporte-tecnico",
    version="1.0.0",
    author="Seu Nome",
    author_email="seu.email@exemplo.com",
    description="Sistema automatizado para resolução de problemas comuns em computadores Windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seu-usuario/suporte-tecnico",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "suporte-tecnico=suporte_tecnico:main",
        ],
    },
    keywords="suporte tecnico windows automacao ti sistema",
    project_urls={
        "Bug Reports": "https://github.com/seu-usuario/suporte-tecnico/issues",
        "Source": "https://github.com/seu-usuario/suporte-tecnico",
        "Documentation": "https://github.com/seu-usuario/suporte-tecnico#readme",
    },
)

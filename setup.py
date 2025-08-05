from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]

setup(
    name="technical-support-system",
    version="1.1.0",
    author="Fernando César",
    author_email="fernando.cesar@exemplo.com",
    description="Sistema automatizado para resolução de problemas comuns em computadores Windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fernandocsar/suporte-tecnico",
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
            "technical-support=technical_support:main",
        ],
    },
    keywords="technical support windows automation it system",
    project_urls={
        "Bug Reports": "https://github.com/fernandocsar/suporte-tecnico/issues",
        "Source": "https://github.com/fernandocsar/suporte-tecnico",
        "Documentation": "https://github.com/fernandocsar/suporte-tecnico#readme",
    },
)

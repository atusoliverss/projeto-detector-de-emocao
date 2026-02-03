#!/bin/bash

echo "=========================================="
echo "   INSTALADOR DO DETECTOR (LINUX/MAC)     "
echo "=========================================="
echo ""

# 1. Verifica se o Python 3 está instalado
if ! command -v python3 &> /dev/null
then
    echo "[ERRO] Python 3 não encontrado. Instale-o (sudo apt install python3)."
    exit
fi

# 2. Cria o ambiente virtual (.venv) se não existir
# Nota: Usamos .venv para bater com seu .gitignore
if [ ! -d ".venv" ]; then
    echo "[1/3] Criando ambiente virtual (.venv)..."
    python3 -m venv .venv
fi

# 3. Ativa o ambiente e instala bibliotecas
echo "[2/3] Verificando bibliotecas..."
source .venv/bin/activate

# Atualiza o pip para evitar erros
pip install --upgrade pip > /dev/null 2>&1

# Instala os requisitos
pip install -r requirements.txt

# 4. Verifica se o Tkinter está instalado (comum faltar no Linux)
python3 -c "import tkinter" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo ""
    echo "[AVISO] O Tkinter parece não estar instalado no sistema."
    echo "Se der erro, rode: sudo apt-get install python3-tk"
    echo ""
fi

# 5. Roda o projeto
echo ""
echo "[3/3] Iniciando o Detector de Emoções..."
echo ""
python app_emocoes.py
@echo off
echo ==========================================
echo   INSTALADOR DO PROJETO DE EMOCOES
echo ==========================================
echo.

REM Verifica se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado! Instale o Python 3.10 ou superior.
    pause
    exit
)

REM Cria o ambiente virtual se não existir
if not exist "venv" (
    echo [1/3] Criando ambiente virtual (venv)...
    python -m venv venv
)

REM Ativa o ambiente e instala bibliotecas
echo [2/3] Verificando bibliotecas...
call venv\Scripts\activate
pip install -r requirements.txt

REM Roda o projeto
echo.
echo [3/3] Iniciando o Detector de Emocoes...
echo.
python app_emocoes.py

pause
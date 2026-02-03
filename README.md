# 🎭 Detector de Emoções com IA Generativa (Multimodal)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![Interface](https://img.shields.io/badge/UI-CustomTkinter-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **Projeto Acadêmico:** Sistema inteligente capaz de detectar emoções complexas (ironia, contexto, sentimento) através de texto e voz, utilizando a API do Google Gemini.

---

## 📸 Demonstração

*(Adicione aqui um print da tela do seu projeto funcionando, se tiver. Ex: fundo amarelo para felicidade, vermelho para raiva)*

---

## 🚀 Funcionalidades

* **🎙️ Entrada Multimodal:** Aceita digitação de texto ou entrada de voz via microfone.
* **🧠 Inteligência Artificial Avançada:** Utiliza o modelo **Google Gemini (Flash)** para interpretar nuances, gírias e sarcasmo que métodos tradicionais não captam.
* **🎨 Feedback Visual Dinâmico:** A interface muda de cor instantaneamente para refletir a emoção detectada (ex: Vermelho para Raiva, Azul Escuro para Tristeza, Amarelo para Alegria).
* **👁️ Acessibilidade:** Ajuste automático de contraste da fonte (Texto preto em fundos claros, Texto branco em fundos escuros).
* **🔐 Segurança:** A API Key é salva localmente no computador do usuário e nunca é enviada para o repositório.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** [Python 3](https://www.python.org/)
* **Interface Gráfica:** [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) (Visual moderno e Dark Mode)
* **IA Generativa:** [Google GenAI SDK](https://pypi.org/project/google-genai/) (Integração com Gemini 1.5/2.0)
* **Áudio:** [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) (Conversão de Voz para Texto)

---

## ⚙️ Pré-requisitos

Antes de começar, você precisará de:

1.  **Python 3.10 ou superior** instalado.
2.  Uma **API Key do Google (Grátis)**.
    * Gere a sua aqui: [Google AI Studio](https://aistudio.google.com/app/apikey)

---

## 📦 Como Instalar e Rodar

Facilitamos o processo com scripts automáticos para Windows e Linux.

### 🪟 No Windows

1.  Clone este repositório ou baixe o ZIP.
2.  Na pasta do projeto, dê um **duplo clique** no arquivo:
    ```
    instalar_e_rodar.bat
    ```
3.  O script criará o ambiente virtual, instalará as bibliotecas e abrirá o programa.
4.  Na primeira execução, cole sua **API Key** quando solicitado.

### 🐧 No Linux / Mac

1.  Abra o terminal na pasta do projeto.
2.  Dê permissão de execução ao script:
    ```bash
    chmod +x instalar_e_rodar.sh
    ```
3.  Execute o script:
    ```bash
    ./instalar_e_rodar.sh
    ```
    *(Nota: Se der erro de Tkinter, instale com `sudo apt-get install python3-tk`)*

---

## 🔧 Instalação Manual (Para Desenvolvedores)

Se preferir configurar manualmente via terminal:

```bash
# 1. Crie o ambiente virtual
python -m venv .venv

# 2. Ative o ambiente
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Rode o projeto
python app_emocoes.py
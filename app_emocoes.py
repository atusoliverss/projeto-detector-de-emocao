import customtkinter as ctk
import speech_recognition as sr
import threading
import os
from google import genai

# --- FUNÇÕES DE CONFIGURAÇÃO (API KEY) ---
ARQUIVO_CHAVE = "api_key.txt"

def carregar_api_key():
    """Tenta ler a chave do arquivo. Se não existir, retorna None."""
    if os.path.exists(ARQUIVO_CHAVE):
        with open(ARQUIVO_CHAVE, "r") as f:
            return f.read().strip()
    return None

def salvar_api_key(chave):
    """Salva a chave para usar depois"""
    with open(ARQUIVO_CHAVE, "w") as f:
        f.write(chave)

# --- TENTA CARREGAR A CHAVE AUTOMATICAMENTE ---
CHAVE_API = carregar_api_key()
client = None

if CHAVE_API:
    try:
        client = genai.Client(api_key=CHAVE_API)
    except:
        pass

# --- INTERFACE GRÁFICA ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppEmocoes(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Detector de Emoções - Facul")
        self.geometry("650x600")
        self.resizable(False, False)

        # Se não tiver chave, bloqueia o app e pede
        if not CHAVE_API:
            self.dialogo_chave()
        else:
            self.iniciar_interface_principal()

    def dialogo_chave(self):
        self.geometry("400x200")
        ctk.CTkLabel(self, text="Bem-vindo! Para começar,\ncole sua Google API Key:", font=("Arial", 14)).pack(pady=20)
        self.entrada_key = ctk.CTkEntry(self, width=300, placeholder_text="Cole a chave AIza...")
        self.entrada_key.pack(pady=10)
        ctk.CTkButton(self, text="Salvar e Iniciar", command=self.salvar_e_iniciar).pack(pady=10)

    def salvar_e_iniciar(self):
        chave = self.entrada_key.get().strip()
        if chave:
            salvar_api_key(chave)
            global CHAVE_API, client
            CHAVE_API = chave
            client = genai.Client(api_key=CHAVE_API)
            
            # Limpa a tela e inicia o app real
            for widget in self.winfo_children():
                widget.destroy()
            self.geometry("650x600")
            self.iniciar_interface_principal()

    def iniciar_interface_principal(self):
        # Título
        ctk.CTkLabel(self, text="Detector de Emoções (Gemini)", font=("Roboto", 24, "bold")).pack(pady=20)

        # Área de Resultado
        self.frame_resultado = ctk.CTkFrame(self, fg_color="#333333", corner_radius=15)
        self.frame_resultado.pack(pady=10, padx=20, fill="x")

        self.label_emoji = ctk.CTkLabel(self.frame_resultado, text="🤖", font=("Arial", 70))
        self.label_emoji.pack(pady=(15, 0))

        self.label_status = ctk.CTkLabel(self.frame_resultado, text="Aguardando...", font=("Roboto", 18), wraplength=550)
        self.label_status.pack(pady=(5, 15))

        # Input
        self.entry_texto = ctk.CTkEntry(self, placeholder_text="Digite ou fale algo...", width=450, height=40)
        self.entry_texto.pack(pady=20)

        # Botões
        frame_btn = ctk.CTkFrame(self, fg_color="transparent")
        frame_btn.pack(pady=10)

        ctk.CTkButton(frame_btn, text="Analisar Texto", command=self.acao_texto, width=150, height=40).grid(row=0, column=0, padx=10)
        
        self.btn_mic = ctk.CTkButton(frame_btn, text="🎤 Gravar Áudio", fg_color="#eb4034", hover_color="#b02c23", command=self.acao_audio, width=150, height=40)
        self.btn_mic.grid(row=0, column=1, padx=10)

        self.rec = sr.Recognizer()

    # --- LÓGICA DA IA ---
    def consultar_gemini(self, texto_usuario):
        if not texto_usuario: return "NEUTRO", "#333333", "😐", "Texto vazio."
        
        prompt = f"""
        Analise a frase: "{texto_usuario}"
        Responda APENAS neste formato: EMOÇÃO|COR_HEX|EMOJI|EXPLICAÇÃO
        Emoções: FELIZ, TRISTE, RAIVA, MEDO, SURPRESA, NOJO, ANSIEDADE, APAIXONADO, NEUTRO.
        Exemplo: TRISTE|#1a3b5c|😢|Expressa solidão.
        """
        
        try:
            # Tenta usar o modelo genérico mais recente
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt
            )
            partes = response.text.strip().split('|')
            if len(partes) >= 4:
                return partes[0], partes[1], partes[2], partes[3]
            else:
                return "DESCONHECIDO", "#333333", "🤔", "IA respondeu fora do padrão."
        except Exception as e:
            print(e)
            return "ERRO", "#333333", "❌", "Erro de API (Verifique cota ou chave)."

    # --- INTERFACE UPDATE ---
    def atualizar_tela(self, texto, emocao, cor, emoji, explicacao):
        self.label_emoji.configure(text=emoji)
        self.label_status.configure(text=f"{emocao}: {explicacao}")
        self.frame_resultado.configure(fg_color=cor)

        # CORREÇÃO DE CONTRASTE (Se for amarelo/claro, texto preto)
        emocao_upper = emocao.upper()
        if any(x in emocao_upper for x in ["FELIZ", "ALEGRIA", "SURPRESA", "APAIXONADO", "POSITIVO"]):
            self.label_status.configure(text_color="#000000")
            self.label_emoji.configure(text_color="#000000")
        else:
            self.label_status.configure(text_color="#FFFFFF")
            self.label_emoji.configure(text_color="#FFFFFF")

        self.entry_texto.delete(0, 'end')
        self.entry_texto.insert(0, texto)
        self.btn_mic.configure(state="normal", text="🎤 Gravar Áudio")

    # --- AÇÕES ---
    def acao_texto(self):
        texto = self.entry_texto.get()
        threading.Thread(target=self.thread_proc, args=(texto,)).start()

    def acao_audio(self):
        self.btn_mic.configure(state="disabled", text="Ouvindo...")
        self.label_status.configure(text="Escutando...", text_color="#FFFFFF")
        threading.Thread(target=self.thread_audio).start()

    def thread_audio(self):
        with sr.Microphone() as source:
            try:
                self.rec.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.rec.listen(source, timeout=5)
                texto = self.rec.recognize_google(audio, language="pt-BR")
                self.thread_proc(texto)
            except:
                self.label_status.configure(text="Não entendi.")
                self.btn_mic.configure(state="normal", text="🎤 Gravar Áudio")

    def thread_proc(self, texto):
        e, c, em, exp = self.consultar_gemini(texto)
        self.after(0, lambda: self.atualizar_tela(texto, e, c, em, exp))

if __name__ == "__main__":
    app = AppEmocoes()
    app.mainloop()
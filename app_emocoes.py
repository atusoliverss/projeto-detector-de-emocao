import customtkinter as ctk
import speech_recognition as sr
import threading
from google import genai # <--- ESTA é a biblioteca nova

# --- CONFIGURAÇÃO DA IA ---
# COLE SUA NOVA CHAVE AQUI (E NÃO TIRE PRINT DESTA PARTE!):
CHAVE_API = "AIzaSyDnm3UEXfnmAmCNkQrHTA9mNpdMpyUpdmI" 

# Configura o cliente moderno
client = genai.Client(api_key=CHAVE_API)

# Configurações Visuais
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppEmocoes(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Detector de Emoções - IA Gemini")
        self.geometry("650x550")
        self.resizable(False, False)

        # Título
        ctk.CTkLabel(self, text="Detector de Emoções (Gemini 1.5)", font=("Roboto", 24, "bold")).pack(pady=20)

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

    # --- CÉREBRO DA IA (Lógica Atualizada) ---
    def consultar_gemini(self, texto_usuario):
        if not texto_usuario: return "NEUTRO", "#333333", "😐", "Texto vazio."
        
        prompt = f"""
        Analise a frase: "{texto_usuario}"
        Responda APENAS neste formato: EMOÇÃO|COR_HEX|EMOJI|EXPLICAÇÃO
        Emoções: FELIZ, TRISTE, RAIVA, MEDO, SURPRESA, NOJO, ANSIEDADE, APAIXONADO, NEUTRO.
        Exemplo: TRISTE|#1a3b5c|😢|Expressa solidão.
        """
        
        try:
            # USANDO O MODELO QUE APARECEU NA SUA LISTA (GEMINI 2.0)
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
            print(f"Erro Detalhado: {e}")
            return "ERRO", "#333333", "❌", "Verifique a Chave API."

    # --- Lógica de Interface ---
    def atualizar_tela(self, texto, emocao, cor, emoji, explicacao):
        # 1. Atualiza os textos e a cor do fundo
        self.label_emoji.configure(text=emoji)
        self.label_status.configure(text=f"{emocao}: {explicacao}")
        self.frame_resultado.configure(fg_color=cor)

        # 2. CORREÇÃO DE VISIBILIDADE (O Pulo do Gato 😸)
        # Se a emoção for FELIZ ou SURPRESA (cores claras), muda o texto para PRETO.
        # Caso contrário (Triste, Raiva, etc), mantém o texto BRANCO.
        emocao_upper = emocao.upper()
        if "FELIZ" in emocao_upper or "ALEGRIA" in emocao_upper or "SURPRESA" in emocao_upper or "APAIXONADO" in emocao_upper:
            self.label_status.configure(text_color="#000000") # Texto Preto
            self.label_emoji.configure(text_color="#000000") # Emoji Preto (se o sistema suportar)
        else:
            self.label_status.configure(text_color="#FFFFFF") # Texto Branco
            self.label_emoji.configure(text_color="#FFFFFF")

        # 3. Limpa a caixa de texto e reativa o botão
        self.entry_texto.delete(0, 'end')
        self.entry_texto.insert(0, texto)
        self.btn_mic.configure(state="normal", text="🎤 Gravar Áudio")

    def acao_texto(self):
        texto = self.entry_texto.get()
        threading.Thread(target=self.thread_proc, args=(texto,)).start()

    def acao_audio(self):
        self.btn_mic.configure(state="disabled", text="Ouvindo...")
        self.label_status.configure(text="Escutando...")
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
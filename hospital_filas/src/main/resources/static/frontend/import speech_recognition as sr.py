import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import time
import psutil
from groq import Groq
import threading
import pyautogui

# =========================
# IA
# =========================
client = Groq(api_key="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")

# =========================
# VOZ
# =========================
engine = pyttsx3.init()

voices = engine.getProperty('voices')
for v in voices:
    if "portuguese" in v.name.lower() or "maria" in v.name.lower():
        engine.setProperty('voice', v.id)
        break

engine.setProperty('rate', 165)
engine.setProperty('volume', 1.0)

voz_lock = threading.Lock()

def falar(texto):
    with voz_lock:
        print("\nIA:", texto)
        engine.stop()
        engine.say(texto)
        engine.runAndWait()

# =========================
# MICROFONE
# =========================
recognizer = sr.Recognizer()
recognizer.energy_threshold = 350
recognizer.pause_threshold = 0.8

ultimo_comando = ""

# =========================
# FECHAR PROCESSO
# =========================
def fechar_processo(nome):
    for p in psutil.process_iter(['name']):
        try:
            n = p.info['name']
            if n and nome.lower() in n.lower():
                p.kill()
                return True
        except:
            pass
    return False

# =========================
# IA FALLBACK
# =========================
def ia_responder(texto):
    try:
        r = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Responde MUITO curto em português de Moçambique."},
                {"role": "user", "content": texto}
            ],
            temperature=0.4,
            max_tokens=120
        )
        return r.choices[0].message.content
    except:
        return "IA indisponível"

# =========================
# YOUTUBE
# =========================
def abrir_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    falar(f"A abrir YouTube sobre {query}")

# =========================
# WORD - NOVO SISTEMA
# =========================
def abrir_word():
    os.system("start winword")
    time.sleep(3)

def escrever_word(texto):
    pyautogui.write(texto, interval=0.05)

# =========================
# EXECUTAR COMANDOS
# =========================
def executar(texto):
    global ultimo_comando

    texto = texto.lower().strip()

    if texto == ultimo_comando:
        return
    ultimo_comando = texto

    if len(texto) < 2:
        return

    # ================= YOUTUBE =================
    if "youtube" in texto and "abrir" in texto:
        if "gustavo guanabara" in texto:
            abrir_youtube("Gustavo Guanabara Java")
        else:
            abrir_youtube(texto.replace("abrir youtube", "").strip())
        return

    # ================= CHROME =================
    if "chrome" in texto and "abrir" in texto:
        os.system("start chrome")
        falar("Chrome aberto")
        return

    if "chrome" in texto and "fechar" in texto:
        fechar_processo("chrome.exe")
        falar("Chrome fechado")
        return

    # ================= WORD ABRIR =================
    if "abrir word" in texto:
        abrir_word()
        falar("Word aberto")
        return

    # ================= WORD ESCREVER SIMPLES =================
    if "escrever no word" in texto:
        abrir_word()
        falar("Diz o texto")
        
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)
            texto_escrito = recognizer.recognize_google(audio, language="pt-PT")

        escrever_word(texto_escrito)
        falar("Texto escrito no Word")
        return

    # ================= WORD ESCREVER DIRETO =================
    if "word escreve" in texto:
        abrir_word()
        texto_escrito = texto.replace("word escreve", "").strip()
        escrever_word(texto_escrito)
        falar("Escrito no Word")
        return

    # ================= FECHAR WORD =================
    if "word" in texto and "fechar" in texto:
        if fechar_processo("WINWORD.EXE"):
            falar("Word fechado")
        else:
            falar("Word já está fechado")
        return

    # ================= MÚSICA =================
    if "musica" in texto:
        caminho = r"C:\Users\Enoque Manecas\Desktop\musica.mp3"
        if os.path.exists(caminho):
            os.startfile(caminho)
            falar("A tocar música")
        else:
            falar("Música não encontrada")
        return

    # ================= VÍDEO =================
    if "video" in texto:
        caminho = r"C:\Users\Enoque Manecas\Desktop\video.mp4"
        if os.path.exists(caminho):
            os.startfile(caminho)
            falar("A reproduzir vídeo")
        else:
            falar("Vídeo não encontrado")
        return

    # ================= CALCULADORA =================
    if "calculadora" in texto:
        os.system("calc")
        falar("Calculadora aberta")
        return

    # ================= HORA =================
    if "hora" in texto:
        falar(time.strftime("%H:%M"))
        return

    # ================= IA =================
    falar("A pensar")
    falar(ia_responder(texto))

# =========================
# LOOP
# =========================
falar("Assistente iniciado")

while True:
    try:
        with sr.Microphone() as source:
            print("\n🎤 A ouvir comando...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=7)

        texto = recognizer.recognize_google(audio, language="pt-PT")
        print("Tu disseste:", texto)

        executar(texto)

    except sr.UnknownValueError:
        continue

    except Exception as e:
        print("Erro:", e)
        falar("Erro no sistema")
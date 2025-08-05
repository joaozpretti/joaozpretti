import streamlit as st
import requests
from gtts import gTTS
import tempfile
import base64

DEEPAI_API_KEY = st.secrets["deepai_api_key"] if "deepai_api_key" in st.secrets else "SUA_DEEPAI_API_KEY"

def deepai_generate(prompt):
    r = requests.post(
        "https://api.deepai.org/api/text-generator",
        data={'text': prompt},
        headers={'api-key': '838caf3d-a0f8-4629-938b-4e4e0a182d1d'}
    )
    try:
        return r.json()["output"]
    except Exception as e:
        return f"[ERRO DeepAI]: {r.text}"

def gerar_frase_associativa(expressao):
    prompt = (
        f"Crie uma frase curta e natural em inglês começando com '{expressao}', "
        f"e depois, em português, explique o contexto ou finalize a ideia. "
        f"Formato: [frase em inglês] + [continuação em português]."
    )
    return deepai_generate(prompt)

def traduzir_para(texto, destino="pt"):
    if destino == "pt":
        prompt = f"Traduza para português brasileiro de forma natural: {texto}"
    else:
        prompt = f"Traduza para inglês natural: {texto}"
    return deepai_generate(prompt)

def gerar_contexto(frase_en):
    prompt = (
        f"Crie um mini-diálogo curto (em inglês) usando a frase '{frase_en}'."
    )
    return deepai_generate(prompt)

def tts_audio(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        audio_file = open(fp.name, "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        audio_file.close()

st.title("English Acquisition LAB (DeepAI)")

expressao = st.text_input("Digite a palavra, frase ou expressão em inglês:")

if expressao:
    resultado = gerar_frase_associativa(expressao)
    st.markdown(f"**▶ ASSOCIATIVO EN+PT:**")
    st.success(resultado)

    frase_pt = traduzir_para(resultado, destino="pt")
    frase_en = traduzir_para(resultado, destino="en")

    st.markdown(f"**★ TOTALMENTE EM PORTUGUÊS:**\n{frase_pt}")
    st.markdown(f"**★ TOTALMENTE EM INGLÊS:**\n{frase_en}")

    st.markdown("**▶ MINI-DIÁLOGO/CONTEXTO:**")
    contexto = gerar_contexto(frase_en)
    st.info(contexto)

    if st.button("Ouvir frase em inglês"):
        tts_audio(frase_en, lang="en")

    # Você pode adicionar os outros módulos (quiz, explicação, feedback, etc) da mesma forma usando deepai_generate(prompt)

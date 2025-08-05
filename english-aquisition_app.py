import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import tempfile
import os

st.set_page_config(page_title="Aquisicao de Inglês AI", layout="wide")
st.title("🧠 English Acquisition LAB - Online")

# Funções
def gerar_frase_associativa_g4f(expressao):
    prompt = (
        f"Você é um gerador de frases para aquisição de inglês. "
        f"Sempre crie uma frase curta e natural em inglês usando ou começando com '{expressao}', "
        f"e logo depois concatene com uma ideia relevante para o final da frase em português, no formato: "
        f"[frase completa em inglês] + [continuação em português associada ao contexto]. "
        f"Exemplo: What's that sound + que acordei no meio da noite ouvindo.\n"
        f"Agora gere uma frase para '{expressao}' no mesmo formato:"
    )
    response = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response.strip()

def traduzir_tudo_para_pt_gpt(frase_completa):
    prompt = (
        f"Traduza a frase abaixo para o português natural e fluente, juntando todas as partes em uma frase só:\n\n{frase_completa}"
    )
    response = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response.strip()

def traduzir_tudo_para_en(frase_completa):
    prompt = (
        f"Traduza a frase abaixo para o inglês natural, juntando todas as partes num texto único e fluente, mantendo o sentido e contexto:\n\n{frase_completa}"
    )
    response = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response.strip()

def quiz(frase_en, frase_pt):
    prompt = (
        f"Crie uma pergunta de múltipla escolha (quiz) com 4 alternativas, sobre a frase inglesa abaixo e sua tradução. Pergunte algo relevante sobre vocabulário, gramática ou significado. Responda no formato:\nPergunta:\nA)\nB)\nC)\nD)\nResposta correta: (letra)\n\nFrase em inglês: {frase_en}\nTradução: {frase_pt}"
    )
    response = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response.strip()

def gerar_contexto(frase_en):
    prompt = (
        f"Crie um mini-diálogo ou exemplo de uso real para esta frase em inglês, com contexto natural e curto. Mostre só o diálogo/situação, sem tradução.\n\nFrase: {frase_en}"
    )
    response = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response.strip()

# Interface
with st.form("frase_form"):
    expressao = st.text_input("Digite a palavra, frase ou expressão em inglês", "")
    submitted = st.form_submit_button("Gerar Frase")

if expressao and submitted:
    st.info("Gerando frase e contexto... aguarde ⏳")
    resultado = gerar_frase_associativa_g4f(expressao)
    frase_pt = traduzir_tudo_para_pt_gpt(resultado)
    frase_en = traduzir_tudo_para_en(resultado)
    contexto = gerar_contexto(frase_en)
    st.markdown(f"### Associativo EN+PT:\n> **{resultado}**")
    st.success(f"**Português:** {frase_pt}")
    st.info(f"**Inglês:** {frase_en}")
    st.markdown(f"---\n#### Mini-Diálogo/Contexto:\n{contexto}")

    st.markdown("---")
    st.subheader("Quiz Rápido")
    st.caption("Teste sua compreensão:")
    quiz_ = quiz(frase_en, frase_pt)
    st.code(quiz_, language="markdown")

    # TTS para escutar (só funciona local, não web)
    # try:
    #     tts = gTTS(frase_en, lang="en")
    #     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
    #         tts.save(f.name)
    #         audio_file = open(f.name, "rb")
    #         st.audio(audio_file.read(), format="audio/mp3")
    # except Exception as e:
    #     st.warning("Erro ao gerar áudio TTS.")
else:
    st.warning("Digite uma expressão/frase e clique em Gerar Frase.")

st.markdown("---\n_Criado para aquisição de inglês via IA. Deploy gratuito: [Streamlit Cloud](https://streamlit.io/cloud)_")


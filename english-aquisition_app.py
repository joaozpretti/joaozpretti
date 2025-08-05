import streamlit as st
import g4f
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Aquisicao de Inglês AI", layout="wide")
st.title("🧠 English Acquisition LAB - Web App (Smart & Full)")

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

def traduzir_para(texto, destino="pt"):
    prompt = (
        f"Traduza de forma natural e fluente para {'português' if destino == 'pt' else 'inglês'}:\n\n{texto}"
    )
    resposta = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return resposta.strip()

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

def variacoes_vocabulário(frase_en):
    prompt = (
        f"Liste, em formato de tópicos:\n- Sinônimos\n- Antônimos\n- Outras variações comuns\npara as principais palavras da frase inglesa abaixo. Liste só as mais relevantes.\n\nFrase: {frase_en}"
    )
    resposta_en = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    ).strip()
    resposta_pt = traduzir_para(resposta_en, destino="pt")
    return resposta_pt, resposta_en

def dicionario_visual(frase_en):
    prompt = (
        f"Para a frase ou ideia abaixo, diga UMA imagem simples que poderia ilustrar (em inglês):\n\n{frase_en}"
    )
    resposta_en = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    ).strip()
    busca = resposta_en.replace(" ", "+")
    url = f"https://source.unsplash.com/400x250/?{busca}"
    return resposta_en, url

def conversacao_simulada(frase_en):
    prompt = (
        f"Imagine um bate-papo curto, estilo WhatsApp, usando como ponto de partida a frase abaixo. Você será meu amigo virtual, me responda no papel de alguém que conversa de forma natural.\n\nFrase: {frase_en}"
    )
    resposta_en = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    ).strip()
    resposta_pt = traduzir_para(resposta_en, destino="pt")
    return resposta_pt, resposta_en

def feedback_nativo(frase_en, frase_pt):
    prompt = (
        f"Explique como um nativo de inglês sentiria ou interpretaria a frase abaixo. Dê feedback sobre nuances, informalidade, contexto, e dicas para soar mais natural. Frase: {frase_en}\nTradução: {frase_pt}"
    )
    resposta_en = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    ).strip()
    resposta_pt = traduzir_para(resposta_en, destino="pt")
    return resposta_pt, resposta_en

def quiz(frase_en, frase_pt):
    prompt = (
        f"Crie uma pergunta de múltipla escolha (quiz) com 4 alternativas, sobre a frase inglesa abaixo e sua tradução. Pergunte algo relevante sobre vocabulário, gramática ou significado. Responda no formato:\nPergunta:\nA)\nB)\nC)\nD)\nResposta correta: (letra)\n\nFrase em inglês: {frase_en}\nTradução: {frase_pt}"
    )
    resposta_en = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    ).strip()
    resposta_pt = traduzir_para(resposta_en, destino="pt")
    return resposta_pt, resposta_en

def teste_reverso(frase_pt, frase_en):
    st.subheader("Traduza para inglês:")
    user_input = st.text_input("Sua resposta:", "")
    if st.button("Ver Sugestão"):
        st.info(f"Sugestão correta: {frase_en}")
        # Poderia ter correção automática aqui com LLM também
    return ""

def gerar_ipa(frase_en):
    prompt = (
        f"Mostre a transcrição fonética IPA da frase em inglês:\n\n{frase_en}"
    )
    resposta_en = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    ).strip()
    resposta_pt = traduzir_para(resposta_en, destino="pt")
    return resposta_pt, resposta_en

def explicacao_gramatical(frase_en):
    prompt = (
        f"Explique brevemente a estrutura gramatical usada nesta frase em inglês. Mostre o tempo verbal, estrutura e por quê ela é assim:\n\n{frase_en}"
    )
    resposta_en = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    ).strip()
    resposta_pt = traduzir_para(resposta_en, destino="pt")
    return resposta_pt, resposta_en

def palavras_chave(frase_en):
    prompt = (
        f"Liste as principais palavras-chave da frase em inglês abaixo e mostre a tradução de cada uma. Liste até 5 palavras. No formato:\nword: tradução\n\nFrase: {frase_en}"
    )
    resposta_en = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    ).strip()
    resposta_pt = traduzir_para(resposta_en, destino="pt")
    return resposta_pt, resposta_en

def frequencia_ingles(frase_en):
    prompt = (
        f"Analise se as palavras/frase abaixo são comuns, formais ou informais no inglês atual. Explique brevemente:\n\n{frase_en}"
    )
    resposta_en = g4f.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "user", "content": prompt}],
        stream=False
    ).strip()
    resposta_pt = traduzir_para(resposta_en, destino="pt")
    return resposta_pt, resposta_en

def gerar_tts(frase_en):
    tts = gTTS(text=frase_en, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        tts.save(f.name)
        return f.name

# --- INTERFACE PRINCIPAL ---
with st.form("frase_form"):
    expressao = st.text_input("Digite a palavra, frase ou expressão em inglês:", "")
    submitted = st.form_submit_button("Gerar frase")

if expressao and submitted:
    st.info("Gerando frase e contexto...")
    resultado = gerar_frase_associativa_g4f(expressao)
    frase_pt = traduzir_para(resultado, destino="pt")
    frase_en = traduzir_para(resultado, destino="en")
    contexto_en = gerar_contexto(frase_en)
    contexto_pt = traduzir_para(contexto_en, destino="pt")
    st.markdown(f"### Associativo EN+PT:\n> **{resultado}**")
    st.success(f"**Português:** {frase_pt}")
    st.info(f"**Inglês:** {frase_en}")
    st.markdown(f"---\n#### Mini-Diálogo/Contexto:\n{contexto_en}\n\n**PT:** {contexto_pt}")

    st.markdown("---")
    tabs = st.tabs([
        "Vocabulário Ativo",
        "Dicionário Visual",
        "Conversação Simulada",
        "Feedback Nativo",
        "Quiz",
        "Teste Reverso",
        "IPA / Pronúncia",
        "Gramática",
        "Palavras-chave",
        "Frequência de Uso",
        "Modo Só Escuta (TTS)"
    ])

    with tabs[0]:
        st.subheader("Vocabulário Ativo")
        pt, en = variacoes_vocabulário(frase_en)
        st.write("PT:", pt)
        st.write("EN:", en)

    with tabs[1]:
        st.subheader("Dicionário Visual (Imagem Sugerida)")
        imagem_en, url = dicionario_visual(frase_en)
        st.write("EN:", imagem_en)
        st.image(url, caption=imagem_en)
        st.caption("Fonte: Unsplash (imagem gerada via palavra-chave)")

    with tabs[2]:
        st.subheader("Conversação Simulada")
        pt, en = conversacao_simulada(frase_en)
        st.write("PT:", pt)
        st.write("EN:", en)

    with tabs[3]:
        st.subheader("Feedback Nativo")
        pt, en = feedback_nativo(frase_en, frase_pt)
        st.write("PT:", pt)
        st.write("EN:", en)

    with tabs[4]:
        st.subheader("Quiz")
        pt, en = quiz(frase_en, frase_pt)
        st.write("PT:", pt)
        st.code(en)

    with tabs[5]:
        st.subheader("Teste Reverso")
        teste_reverso(frase_pt, frase_en)

    with tabs[6]:
        st.subheader("Pronúncia IPA")
        pt, en = gerar_ipa(frase_en)
        st.write("PT:", pt)
        st.write("EN:", en)

    with tabs[7]:
        st.subheader("Explicação Gramatical")
        pt, en = explicacao_gramatical(frase_en)
        st.write("PT:", pt)
        st.write("EN:", en)

    with tabs[8]:
        st.subheader("Palavras-chave")
        pt, en = palavras_chave(frase_en)
        st.write("PT:", pt)
        st.write("EN:", en)

    with tabs[9]:
        st.subheader("Frequência de Uso no Inglês")
        pt, en = frequencia_ingles(frase_en)
        st.write("PT:", pt)
        st.write("EN:", en)

    with tabs[10]:
        st.subheader("Modo Só Escuta (TTS)")
        st.write("Escute a frase em inglês quantas vezes quiser (áudio mp3):")
        audio_file = gerar_tts(frase_en)
        st.audio(audio_file, format="audio/mp3")

        st.caption("O áudio será reproduzido no navegador.")

    st.markdown("---\n_Criado para aquisição de inglês via IA. Deploy gratuito: [Streamlit Cloud](https://streamlit.io/cloud)_")

else:
    st.warning("Digite uma expressão/frase e clique em Gerar frase.")


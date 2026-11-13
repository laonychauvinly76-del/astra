"""Astra • Assistant Souverain — assistant personnel propulsé par Mistral AI."""

import os

import streamlit as st
from dotenv import load_dotenv

try:
    from mistralai import Mistral
except ImportError:
    from mistralai.client import Mistral

load_dotenv()

st.set_page_config(
    page_title="Astra • Assistant Souverain",
    page_icon="✦",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Identité visuelle — dérivée du logo : dégradé violet → cyan, fond sombre,
# lignes fines blanches, esprit minimaliste et premium.
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;500&display=swap');

        :root {
            --astra-violet: #6A0DAD;
            --astra-cyan: #00D4FF;
            --astra-bg: #0B0B14;
            --astra-surface: #12121F;
            --astra-border: rgba(255, 255, 255, 0.08);
            --astra-text: #EDEDF2;
            --astra-muted: #9A9AB0;
        }

        html, body, [class*="css"], .stApp {
            font-family: 'Outfit', 'Segoe UI', sans-serif;
            font-weight: 300;
            letter-spacing: 0.01em;
        }

        .stApp {
            background:
                radial-gradient(ellipse 80% 55% at 15% -10%, rgba(106, 13, 173, 0.28), transparent 60%),
                radial-gradient(ellipse 70% 50% at 90% 110%, rgba(0, 212, 255, 0.16), transparent 60%),
                var(--astra-bg);
            color: var(--astra-text);
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        h1, h2, h3, .stMarkdown {
            color: var(--astra-text);
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(106, 13, 173, 0.14), rgba(0, 212, 255, 0.06));
            border-right: 1px solid var(--astra-border);
        }

        [data-testid="stSidebar"] * {
            color: var(--astra-text);
        }

        .astra-brand {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            padding: 0.4rem 0 1.2rem 0;
        }

        .astra-mark {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.3rem;
            color: #FFFFFF;
            background: linear-gradient(135deg, var(--astra-violet), var(--astra-cyan));
            box-shadow: 0 0 24px rgba(0, 212, 255, 0.25);
        }

        .astra-title {
            font-size: 1.45rem;
            font-weight: 400;
            line-height: 1.1;
        }

        .astra-subtitle {
            font-size: 0.78rem;
            font-weight: 200;
            color: var(--astra-muted);
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }

        .astra-hero {
            text-align: center;
            padding: 2.2rem 1rem 1.6rem 1rem;
        }

        .astra-hero h1 {
            font-size: 2.4rem;
            font-weight: 200;
            margin-bottom: 0.2rem;
        }

        .astra-hero p {
            color: var(--astra-muted);
            font-weight: 200;
            font-size: 0.95rem;
        }

        .astra-gradient-text {
            background: linear-gradient(90deg, var(--astra-violet), var(--astra-cyan));
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        [data-testid="stChatMessage"] {
            background: var(--astra-surface);
            border: 1px solid var(--astra-border);
            border-radius: 14px;
            padding: 0.9rem 1.1rem;
        }

        [data-testid="stChatMessage"][aria-label="Chat message from user"] {
            border-left: 2px solid var(--astra-cyan);
        }

        [data-testid="stChatMessage"][aria-label="Chat message from assistant"] {
            border-left: 2px solid var(--astra-violet);
        }

        [data-testid="stChatInput"] {
            border: 1px solid var(--astra-border);
            border-radius: 12px;
            background: var(--astra-surface);
        }

        [data-testid="stChatInput"] textarea {
            color: var(--astra-text);
        }

        [data-testid="stChatInput"] button {
            background: linear-gradient(135deg, var(--astra-violet), var(--astra-cyan));
            border-radius: 10px;
            color: #FFFFFF;
        }

        .stButton > button {
            width: 100%;
            border: 1px solid var(--astra-border);
            border-radius: 10px;
            background: transparent;
            color: var(--astra-text);
            font-weight: 300;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            border-color: var(--astra-cyan);
            box-shadow: 0 0 16px rgba(0, 212, 255, 0.18);
        }

        [data-testid="stSelectbox"] > div > div,
        [data-testid="stTextInput"] > div > div,
        [data-testid="stPasswordInput"] > div > div {
            background: var(--astra-surface);
            border: 1px solid var(--astra-border);
            border-radius: 10px;
            color: var(--astra-text);
        }

        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--astra-border), transparent);
        }

        .astra-footer {
            text-align: center;
            color: var(--astra-muted);
            font-size: 0.75rem;
            font-weight: 200;
            letter-spacing: 0.08em;
            padding-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Rôles / modes d'Astra
# ---------------------------------------------------------------------------
ROLES = {
    "Assistant Général": (
        "Tu es Astra, un assistant personnel souverain, bienveillant et précis. "
        "Tu réponds en français par défaut, de façon claire, structurée et élégante. "
        "Tu vas droit au but tout en restant chaleureux."
    ),
    "Expert Code": (
        "Tu es Astra en mode Expert Code. Tu es un ingénieur logiciel senior. "
        "Tu fournis du code propre, idiomatique et commenté uniquement lorsque nécessaire. "
        "Tu expliques brièvement tes choix techniques et tu signales les pièges potentiels. "
        "Réponds en français, avec des blocs de code correctement balisés."
    ),
    "Correcteur": (
        "Tu es Astra en mode Correcteur. Tu corriges l'orthographe, la grammaire, "
        "la syntaxe et le style du texte fourni. Tu proposes une version corrigée, "
        "puis une courte liste des modifications importantes. Tu conserves le ton "
        "et l'intention de l'auteur."
    ),
}

MODELS = ["mistral-small-latest", "mistral-large-latest", "codestral-latest"]


# ---------------------------------------------------------------------------
# État de session
# ---------------------------------------------------------------------------
def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []


def reset_conversation() -> None:
    st.session_state.messages = []


# ---------------------------------------------------------------------------
# Barre latérale
# ---------------------------------------------------------------------------
def render_sidebar() -> tuple[str, str, str]:
    with st.sidebar:
        st.markdown(
            """
            <div class="astra-brand">
                <div class="astra-mark">✦</div>
                <div>
                    <div class="astra-title">Astra</div>
                    <div class="astra-subtitle">Assistant Souverain</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("##### Configuration")

        env_key = os.getenv("MISTRAL_API_KEY", "")
        api_key = st.text_input(
            "Clé API Mistral",
            value=env_key,
            type="password",
            placeholder="Collez votre clé ici…",
            help="Pré-remplie depuis le fichier .env si présent.",
        )

        model = st.selectbox("Modèle Mistral", MODELS, index=0)

        role = st.selectbox("Rôle / Mode", list(ROLES.keys()), index=0)

        st.markdown("")
        if st.button("✦  Réinitialiser la conversation", use_container_width=True):
            reset_conversation()
            st.rerun()

        st.markdown("---")
        st.markdown(
            '<div class="astra-footer">Propulsé par Mistral AI</div>',
            unsafe_allow_html=True,
        )

    return api_key.strip(), model, role


# ---------------------------------------------------------------------------
# Appel à l'API Mistral en streaming
# ---------------------------------------------------------------------------
def stream_response(api_key: str, model: str, system_prompt: str, prompt: str):
    client = Mistral(api_key=api_key)
    history = [
        {"role": "system", "content": system_prompt},
        *[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        {"role": "user", "content": prompt},
    ]
    stream = client.chat.stream(model=model, messages=history)
    for chunk in stream:
        delta = chunk.data.choices[0].delta.content
        if delta:
            yield delta


# ---------------------------------------------------------------------------
# Interface principale
# ---------------------------------------------------------------------------
def main() -> None:
    init_state()
    api_key, model, role = render_sidebar()
    system_prompt = ROLES[role]

    st.markdown(
        """
        <div class="astra-hero">
            <h1>✦ <span class="astra-gradient-text">Astra</span></h1>
            <p>Votre assistant personnel souverain — vos conversations restent entre vous et les étoiles.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not api_key:
        st.warning(
            "Aucune clé API détectée. Renseignez `MISTRAL_API_KEY` dans le fichier "
            "`.env` ou collez-la dans la barre latérale pour éveiller Astra."
        )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Écrivez à Astra…", disabled=not api_key):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(
                stream_response(api_key, model, system_prompt, prompt)
            )

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 — barrière d'erreur globale propre
        st.error(f"Astra a rencontré une erreur : {exc}")

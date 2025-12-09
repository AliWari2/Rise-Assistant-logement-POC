import os
import json
from datetime import datetime

import streamlit as st
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# ---------- CONFIG GÉNÉRALE ----------
st.set_page_config(
    page_title="Assistant Logement - PoC Rise",
    page_icon="🏠",
    layout="wide"
)

# ---------- STYLES PERSONNALISÉS (TES COULEURS + LAYOUT SENIOR) ----------
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
        background: radial-gradient(circle at top, #0f172a 0, #020617 45%, #020617 100%);
        color: #e5e7eb;
    }

    /* Conteneur principal */
    .main .block-container {
        padding-top: 0.5rem;
        padding-bottom: 2.5rem;
        max-width: 1200px;
    }

    /* Topbar sombre type SaaS */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.9rem 1.3rem;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(148, 163, 184, 0.45);
        backdrop-filter: blur(18px);
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.9);
        margin-bottom: 1rem;
    }
    .topbar-left {
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .topbar-logo {
        width: 28px;
        height: 28px;
        border-radius: 9px;
        background: linear-gradient(135deg, #1f6feb, #3b82f6);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #e5e7eb;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .topbar-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #e5e7eb;
    }
    .topbar-sub {
        font-size: 0.78rem;
        color: #9ca3af;
    }
    .topbar-pill {
        font-size: 0.78rem;
        padding: 0.2rem 0.7rem;
        border-radius: 999px;
        background: rgba(15,23,42,0.9);
        border: 1px solid rgba(148,163,184,0.7);
        color: #e5e7eb;
    }

    /* En-tête gradient (TES COULEURS) */
    .hero {
        padding: 1.8rem 2.2rem;
        border-radius: 20px;
        background: linear-gradient(120deg, #1f6feb, #3b82f6, #06b6d4);
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 22px 45px rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(191, 219, 254, 0.5);
    }
    .hero-title {
        font-size: 2.0rem;
        font-weight: 750;
        margin-bottom: 0.3rem;
        letter-spacing: -0.03em;
    }
    .hero-subtitle {
        font-size: 0.96rem;
        opacity: 0.9;
        max-width: 720px;
    }
    .hero-tags {
        margin-top: 0.8rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
    }
    .hero-tag {
        padding: 0.22rem 0.7rem;
        border-radius: 999px;
        border: 1px solid rgba(226, 232, 240, 0.85);
        background: rgba(15, 23, 42, 0.18);
        font-size: 0.76rem;
    }

    /* Carte d'infos à droite (TES COULEURS) */
    .info-card {
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        background: linear-gradient(145deg, rgba(15,23,42,0.96), rgba(15,23,42,0.9));
        color: #e5e7eb;
        border: 1px solid rgba(148, 163, 184, 0.55);
        box-shadow: 0 18px 35px rgba(15, 23, 42, 0.85);
    }
    .info-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #e5e7eb;
    }
    .info-badge {
        display: inline-block;
        padding: 0.18rem 0.65rem;
        border-radius: 999px;
        font-size: 0.7rem;
        border: 1px solid rgba(148, 163, 184, 0.8);
        margin-bottom: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #9ca3af;
    }

    /* Boutons d’exemple (TES COULEURS) */
    .stButton > button[kind="secondary"] {
        border-radius: 999px !important;
        border: 1px solid rgba(148, 163, 184, 0.7) !important;
        padding: 0.3rem 0.75rem !important;
        font-size: 0.8rem !important;
        background: rgba(15, 23, 42, 0.85) !important;
        color: #e5e7eb !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: #3b82f6 !important;
        background: rgba(15, 23, 42, 0.95) !important;
    }

    /* Chat wrapper sombre (TES COULEURS) */
    .chat-wrapper {
        border-radius: 20px;
        padding: 1.2rem 1.4rem 0.9rem 1.4rem;
        background: radial-gradient(circle at top left, rgba(30,64,175,0.45), rgba(15,23,42,0.98));
        border: 1px solid rgba(148, 163, 184, 0.6);
        box-shadow: 0 20px 50px rgba(15, 23, 42, 0.95);
    }

    /* Footer */
    .footer {
        margin-top: 2rem;
        font-size: 0.78rem;
        color: #6b7280;
        text-align: center;
    }

    /* Messages chat */
    .stChatMessage {
        border-radius: 14px;
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.45rem;
    }
    .stChatMessage[data-testid="stChatMessage"] {
        background: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- INIT SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "conversations" not in st.session_state:
    # liste de dict: {id, title, messages}
    st.session_state["conversations"] = []

if "current_conv_id" not in st.session_state:
    st.session_state["current_conv_id"] = None

# ---------- FONCTIONS HISTORIQUE / SAUVEGARDE ----------
CONV_DIR = "conversations"


def ensure_conv_dir():
    os.makedirs(CONV_DIR, exist_ok=True)


def save_conversation_to_file(conv: dict):
    """Sauvegarde une conversation dans un fichier JSON (logs)."""
    ensure_conv_dir()
    filename = f"{conv['id']}.json"
    path = os.path.join(CONV_DIR, filename)
    data = {
        "id": conv["id"],
        "title": conv["title"],
        "messages": [
            {"role": role, "content": content} for role, content in conv["messages"]
        ],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_conversation_from_current():
    """Crée un objet conversation à partir de l'historique actuel."""
    if not st.session_state["messages"]:
        return None
    first_user_msg = next(
        (content for role, content in st.session_state["messages"] if role == "user"),
        "Conversation sans titre",
    )
    title = (first_user_msg[:60] + "…") if len(first_user_msg) > 60 else first_user_msg
    conv_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    return {
        "id": conv_id,
        "title": title,
        "messages": st.session_state["messages"].copy(),
    }


def load_conversation(conv_id: str):
    """Charge une conversation depuis st.session_state."""
    for conv in st.session_state["conversations"]:
        if conv["id"] == conv_id:
            st.session_state["messages"] = conv["messages"].copy()
            st.session_state["current_conv_id"] = conv_id
            return


# ---------- INITIALISATION API GROQ ----------
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("La variable d'environnement GROQ_API_KEY n'est pas définie.")
    st.stop()

client = Groq(api_key=api_key)

# ---------- TOPBAR ----------
st.markdown(
    """
    <div class="topbar">
        <div class="topbar-left">
            <div class="topbar-logo">R</div>
            <div>
                <div class="topbar-title">Rise • Assistant Logement</div>
                <div class="topbar-sub">Prototype d’assistant IA pour la gestion locative</div>
            </div>
        </div>
        <div class="topbar-pill">
            PoC Alternance – Ali Wari
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- EN-TÊTE ----------
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Assistant Logement – PoC Rise</div>
        <div class="hero-subtitle">
            Un assistant conversationnel qui aide les locataires à décrire un problème
            (fuite, eau chaude, nuisances…) et à obtenir des actions concrètes, priorisées
            et compréhensibles.
        </div>
        <div class="hero-tags">
            <span class="hero-tag">PropTech • IA & LLM</span>
            <span class="hero-tag">Analyse de problème</span>
            <span class="hero-tag">Conseils actionnables</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- BOUTON NOUVELLE CONVERSATION ----------
reset_col, _ = st.columns([1, 5])
with reset_col:
    if st.button("🔄 Nouvelle conversation"):
        # On sauvegarde uniquement si c'est une conversation nouvelle (jamais encore enregistrée)
        if st.session_state["messages"] and st.session_state["current_conv_id"] is None:
            conv = create_conversation_from_current()
            if conv is not None:
                st.session_state["conversations"].append(conv)
                save_conversation_to_file(conv)

        st.session_state["messages"] = []
        st.session_state["current_conv_id"] = None
        st.rerun()

st.caption(
    "Ce prototype combine un modèle LLM (Groq) et une base de connaissances logement pour produire des réponses guidées."
)

# ---------- CHARGEMENT BASE DE CONNAISSANCES ----------
@st.cache_data
def load_knowledge():
    try:
        with open("connaissances_logement.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


knowledge_base = load_knowledge()
if not knowledge_base:
    st.warning(
        "⚠️ Le fichier 'connaissances_logement.txt' est vide ou introuvable. Les réponses seront moins pertinentes."
    )

# ---------- LAYOUT EN 2 COLONNES ----------
col_chat, col_info = st.columns([2.2, 1])

# ===== COLONNE DROITE : INFOS + EXEMPLES + HISTORIQUE =====
with col_info:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown(
        '<div class="info-badge">Vue produit & métier</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="info-title">Comment fonctionne l’assistant ?</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        - Le locataire décrit son problème en langage naturel  
        - L’IA recoupe avec des cas types (fuite, eau chaude, nuisances, etc.)  
        - La réponse est structurée : analyse, actions, interlocuteurs, urgence  
        - L’historique peut alimenter un futur back-office Rise (suivi d’incidents)  
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---", unsafe_allow_html=True)
    st.markdown(
        '<div class="info-title">Exemples de situations</div>',
        unsafe_allow_html=True,
    )

    examples = {
        "Plus d’eau chaude 💧": "Je n’ai plus d’eau chaude depuis ce matin.",
        "Fuite d’eau au plafond 💦": "J’ai une fuite d’eau au plafond du salon.",
        "Voisin très bruyant 🎧": "Mon voisin met la musique très fort la nuit.",
        "Moisissures dans la salle de bain 🧫": "J’ai des moisissures noires dans la salle de bain.",
    }

    example_clicked = None
    for label, text in examples.items():
        if st.button(label, key=f"ex_{label}", type="secondary"):
            example_clicked = text

    st.markdown("---", unsafe_allow_html=True)
    st.markdown(
        '<div class="info-title">Historique des conversations (session)</div>',
        unsafe_allow_html=True,
    )

    if st.session_state["conversations"]:
        titles = [
            f"{i+1}. {conv['title']}" for i, conv in enumerate(st.session_state["conversations"])
        ]
        conv_choice = st.selectbox(
            "Recharger une discussion :",
            options=["— Aucune —"] + titles,
            index=0,
        )
        if conv_choice != "— Aucune —":
            idx = titles.index(conv_choice)
            selected_conv = st.session_state["conversations"][idx]
            if st.button("📂 Recharger cette discussion"):
                load_conversation(selected_conv["id"])
                st.rerun()
    else:
        st.caption("Aucune discussion sauvegardée dans cette session pour le moment.")

    st.markdown(
        """
        <hr style="margin-top: 1rem; margin-bottom: 0.5rem; opacity: 0.5;">
        <small>
        Ce PoC peut être connecté à un back-office (tickets, SLA, interventions) pour un suivi global du parc locatif.
        </small>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ===== COLONNE GAUCHE : CHAT =====
with col_chat:
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

    # Affichage de l’historique
    for role, content in st.session_state["messages"]:
        with st.chat_message(role):
            st.markdown(content)

    # Gestion input (exemple ou saisie libre)
    user_text = None

    if example_clicked:
        user_text = example_clicked

    chat_input = st.chat_input("Décrivez le problème rencontré dans le logement…")
    if chat_input:
        user_text = chat_input

    if user_text:
        # Ajouter le message utilisateur
        st.session_state["messages"].append(("user", user_text))

        with st.chat_message("assistant"):
            with st.spinner("Analyse du problème…"):

                system_prompt = f"""
Tu es un assistant spécialisé dans les problèmes de logement.

Tu disposes de la base de connaissances suivante (problèmes fréquents : fuite, eau chaude,
serrure, nuisances sonores, moisissures, etc.) :

{knowledge_base}

Règles :
- Analyse précisément le problème du locataire.
- Appuie-toi sur la base de connaissances quand c’est possible.
- Donne des conseils concrets, prudents et actionnables.
- Indique clairement si la situation est urgente ou non.
- Réponds toujours en français, avec un ton simple et rassurant.

Format de réponse STRICT :
1. **Analyse du problème**
2. **Actions immédiates**
3. **Qui prévenir ?**
4. **Niveau d'urgence (faible / moyenne / élevée)**
"""

                messages = [{"role": "system", "content": system_prompt}]
                for role, content in st.session_state["messages"]:
                    messages.append({"role": role, "content": content})

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.2,
                )

                answer = response.choices[0].message.content
                st.markdown(answer)

        st.session_state["messages"].append(("assistant", answer))
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown(
    """
    <div class="footer">
        PoC Assistant Logement – conçu par <b>Ali Wari</b> pour Rise • IA & LLM appliqués à la PropTech.
    </div>
    """,
    unsafe_allow_html=True,
)

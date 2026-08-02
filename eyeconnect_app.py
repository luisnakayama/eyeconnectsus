import streamlit as st
from datetime import datetime, timedelta
import random
import time
from PIL import Image
import io
import base64

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EyeConnect SUS",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Modern Minimalist Theme */
    :root {
        --primary: #0066CC;
        --primary-light: #E6F2FF;
        --primary-hover: #0052A3;
        --danger: #DC2626;
        --warning: #EA580C;
        --success: #16A34A;
        --neutral-dark: #1F2937;
        --neutral-gray: #6B7280;
        --neutral-light: #F3F4F6;
        --neutral-lighter: #FAFAFA;
        --border-color: #E5E7EB;
    }

    /* Global */
    [data-testid="stAppViewContainer"] {
        background-color: #FAFAFA;
        color: var(--neutral-dark);
    }
    [data-testid="stSidebar"] {
        background-color: #1F2937 !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar Navigation */
    [data-testid="stSidebar"] .stButton button,
    [data-testid="stSidebar"] button {
        background: #FFFFFF !important;
        color: #1F2937 !important;
        border: none !important;
        text-align: left !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        padding: 12px 16px !important;
        width: 100% !important;
        border-radius: 8px !important;
        margin-bottom: 6px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    [data-testid="stSidebar"] .stButton button *,
    [data-testid="stSidebar"] button * {
        color: #1F2937 !important;
    }
    [data-testid="stSidebar"] span {
        color: #1F2937 !important;
    }
    [data-testid="stSidebar"] .stButton button:hover,
    [data-testid="stSidebar"] button:hover {
        background: #F0F1F3 !important;
        color: #1F2937 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15) !important;
    }
    [data-testid="stSidebar"] .active-nav button,
    [data-testid="stSidebar"] .active-nav button * {
        background-color: var(--primary) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 8px rgba(0, 102, 204, 0.3) !important;
    }

    /* Primary Buttons */
    .stButton > button[kind="primary"] {
        background: var(--primary) !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
        padding: 10px 20px !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: var(--primary-hover) !important;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.15) !important;
    }

    /* Secondary Buttons */
    .stButton > button:not([kind="primary"]) {
        background: var(--neutral-light) !important;
        color: var(--neutral-dark) !important;
        font-weight: 600 !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:not([kind="primary"]):hover {
        background: #F0F1F3 !important;
        border-color: #D1D5DB !important;
    }

    /* Cards */
    .card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
        margin-bottom: 16px;
        transition: all 0.2s ease;
    }
    .card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    /* Card default text - only if not already colored */
    .card > div:not([style*="color"]) {
        color: var(--neutral-dark);
    }
    .card-blue { border-top: 3px solid var(--primary); }
    .card-green { border-top: 3px solid var(--success); }
    .card-purple { border-top: 3px solid #8B5CF6; }
    .card-orange { border-top: 3px solid var(--warning); }

    /* Stat Boxes */
    .stat-box {
        background: white;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
        transition: all 0.2s ease;
    }
    .stat-box:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary) !important;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.85rem;
        color: var(--neutral-gray) !important;
        margin-top: 8px;
        font-weight: 500;
    }

    /* Classification Badges */
    .badge-emergencia {
        background: #FFDDDD;
        color: #991B1B;
        border: 1px solid #FBBFBF;
        border-radius: 20px;
        padding: 7px 16px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
    }
    .badge-urgente {
        background: #FEF08A;
        color: #92400E;
        border: 1px solid #FCD34D;
        border-radius: 20px;
        padding: 7px 16px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
    }
    .badge-eletivo {
        background: #DCFCE7;
        color: #166534;
        border: 1px solid #BBDF8D;
        border-radius: 20px;
        padding: 7px 16px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
    }

    /* Welcome Banner */
    .welcome-banner {
        background: linear-gradient(135deg, var(--primary) 0%, #0052A3 100%);
        border-radius: 8px;
        padding: 28px 32px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.15);
    }
    .welcome-banner * {
        color: white !important;
    }

    /* Chat Bubbles */
    .chat-user {
        background: var(--primary);
        color: white;
        border-radius: 16px 16px 4px 16px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 75%;
        margin-left: auto;
        text-align: right;
    }
    .chat-specialist {
        background: var(--neutral-light);
        color: var(--neutral-dark);
        border-radius: 16px 16px 16px 4px;
        padding: 12px 16px;
        margin: 8px 0;
        max-width: 75%;
        border: 1px solid var(--border-color);
    }
    .chat-time {
        font-size: 0.75rem;
        color: var(--neutral-gray);
        margin-top: 4px;
    }

    /* Protocol Card */
    .protocol-card {
        background: white;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        border: 1px solid var(--border-color);
        border-left: 3px solid var(--primary);
        margin-bottom: 12px;
    }

    /* Typography */
    h1, h2, h3 {
        color: var(--neutral-dark);
        font-weight: 700;
        line-height: 1.3;
    }
    h1 { font-size: 2rem; }
    h2 { font-size: 1.5rem; }
    h3 { font-size: 1.25rem; }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--neutral-dark);
        margin-bottom: 20px;
        letter-spacing: -0.3px;
    }

    /* Form Elements */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        color: var(--neutral-dark) !important;
        background-color: white !important;
        border-color: var(--border-color) !important;
        border-radius: 6px !important;
        font-size: 0.95rem !important;
    }
    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: var(--neutral-gray) !important;
    }

    label {
        color: var(--neutral-dark) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Selectbox Styling */
    .stSelectbox label,
    .stMultiSelect label,
    .stRadio label,
    .stCheckbox label {
        color: var(--neutral-dark) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Radio Button Text */
    .stRadio {
        color: var(--neutral-dark) !important;
    }
    .stRadio * {
        color: var(--neutral-dark) !important;
    }
    .stRadio span {
        color: var(--neutral-dark) !important;
        font-weight: 500 !important;
    }

    /* Checkbox Text */
    .stCheckbox {
        color: var(--neutral-dark) !important;
    }
    .stCheckbox * {
        color: var(--neutral-dark) !important;
    }
    .stCheckbox label {
        color: var(--neutral-dark) !important;
        font-weight: 500 !important;
    }
    .stCheckbox span {
        color: var(--neutral-dark) !important;
    }

    /* Alert Messages - Error, Warning, Success */
    .stAlert {
        color: var(--neutral-dark) !important;
    }
    .stAlert * {
        color: var(--neutral-dark) !important;
    }
    .stAlert div {
        color: var(--neutral-dark) !important;
    }
    .stAlert p {
        color: var(--neutral-dark) !important;
    }
    .stAlert span {
        color: var(--neutral-dark) !important;
    }
    .stAlert strong {
        color: var(--neutral-dark) !important;
    }

    .stSelectbox [data-baseweb="select"] {
        background-color: white !important;
    }
    .stSelectbox button {
        background-color: white !important;
        color: var(--neutral-dark) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }
    .stSelectbox button:hover {
        background-color: var(--neutral-lighter) !important;
        border-color: #D1D5DB !important;
    }

    .stSelectbox [data-baseweb="select"] * {
        color: var(--neutral-dark) !important;
        background-color: white !important;
    }
    .stSelectbox input {
        color: var(--neutral-dark) !important;
        background-color: white !important;
    }

    /* Dropdown Options */
    [role="option"] {
        color: var(--neutral-dark) !important;
        background-color: white !important;
    }
    [role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background-color: var(--primary-light) !important;
        color: var(--primary) !important;
    }

    [role="listbox"] {
        background-color: white !important;
        border: 1px solid var(--border-color) !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session state init ────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "boas_vindas"
if "casos" not in st.session_state:
    st.session_state.casos = [
        {
            "id": "ATD-001", "paciente": "Maria Silva", "idade": 67, "sexo": "F",
            "queixa": "Dor intensa no olho direito com perda visual súbita",
            "classificacao": "emergencia", "data": datetime.now() - timedelta(hours=2),
            "status": "Aguardando especialista", "olho": "OD",
            "sintomas": ["Dor intensa", "Perda súbita da visão"],
            "imagens": [], "teleconsulta": [],
        },
        {
            "id": "ATD-002", "paciente": "João Santos", "idade": 45, "sexo": "M",
            "queixa": "Sensação de corpo estranho no olho esquerdo após acidente de trabalho",
            "classificacao": "urgente", "data": datetime.now() - timedelta(hours=5),
            "status": "Em teleconsultoria", "olho": "OE",
            "sintomas": ["Corpo estranho", "Trauma ocular"],
            "imagens": [], "teleconsulta": [
                {"de": "Dr. Carlos (Especialista)", "msg": "Já vi as imagens. Parece corpo estranho metálico superficial. Pode tentar irrigação com SF 0,9%. Se não sair, encaminhe para urgência oftalmológica.", "hora": "14:32"},
            ],
        },
        {
            "id": "ATD-003", "paciente": "Ana Oliveira", "idade": 32, "sexo": "F",
            "queixa": "Olho vermelho há 3 dias, secreção amarelada, sem dor significativa",
            "classificacao": "eletivo", "data": datetime.now() - timedelta(days=1),
            "status": "Respondido", "olho": "AO",
            "sintomas": [],
            "imagens": [], "teleconsulta": [
                {"de": "Dra. Patrícia (Especialista)", "msg": "Quadro compatível com conjuntivite bacteriana. Iniciar colírio de tobramicina 0,3% 4x/dia por 7 dias. Retorno se não melhorar.", "hora": "09:15"},
            ],
        },
    ]
if "chat_msgs" not in st.session_state:
    st.session_state.chat_msgs = {
        "ATD-001": [],
        "ATD-002": [
            {"de": "Você", "msg": "Dr. Carlos, paciente com corpo estranho no olho após serrar madeira. Olho muito irritado.", "hora": "14:25"},
            {"de": "Dr. Carlos (Especialista)", "msg": "Já vi as imagens. Parece corpo estranho metálico superficial. Pode tentar irrigação com SF 0,9%. Se não sair, encaminhe para urgência oftalmológica.", "hora": "14:32"},
        ],
        "ATD-003": [
            {"de": "Você", "msg": "Olá Dra. Patrícia, paciente com olho vermelho há 3 dias e secreção amarelada.", "hora": "09:10"},
            {"de": "Dra. Patrícia (Especialista)", "msg": "Quadro compatível com conjuntivite bacteriana. Iniciar colírio de tobramicina 0,3% 4x/dia por 7 dias. Retorno se não melhorar.", "hora": "09:15"},
        ],
    }
if "novo_caso_step" not in st.session_state:
    st.session_state.novo_caso_step = 1
if "novo_caso_data" not in st.session_state:
    st.session_state.novo_caso_data = {}

# ─── Specialists (mock) ────────────────────────────────────────────────────────
ESPECIALISTAS = [
    {"nome": "Dr. Carlos Mendonça", "crm": "CRM/SP 45231", "subespecialidade": "Retina e Vítreo", "online": True, "tempo_resposta": "~8 min"},
    {"nome": "Dra. Patrícia Alves", "crm": "CRM/RJ 38910", "subespecialidade": "Córnea e Superfície Ocular", "online": True, "tempo_resposta": "~10 min"},
    {"nome": "Dr. Fernando Costa", "crm": "CRM/MG 52108", "subespecialidade": "Glaucoma", "online": True, "tempo_resposta": "~15 min"},
    {"nome": "Dra. Renata Lima", "crm": "CRM/BA 29874", "subespecialidade": "Urgências Oftalmológicas", "online": False, "tempo_resposta": "—"},
    {"nome": "Dr. Gustavo Neves", "crm": "CRM/PR 41652", "subespecialidade": "Oftalmopediatria", "online": False, "tempo_resposta": "—"},
    {"nome": "Dra. Juliana Rocha", "crm": "CRM/RS 33741", "subespecialidade": "Plástica Ocular", "online": True, "tempo_resposta": "~20 min"},
    {"nome": "Dr. André Pinto", "crm": "CRM/CE 28563", "subespecialidade": "Visão Subnormal", "online": False, "tempo_resposta": "—"},
    {"nome": "Dra. Camila Ferreira", "crm": "CRM/GO 37192", "subespecialidade": "Retina e Vítreo", "online": True, "tempo_resposta": "~12 min"},
]

PROTOCOLOS = [
    {
        "titulo": "Olho Vermelho Agudo",
        "categoria": "Urgência",
        "cor": "#E53935",
        "resumo": "Diagnóstico diferencial e manejo do olho vermelho na atenção primária.",
        "conteudo": [
            "1. Verificar acuidade visual em ambos os olhos",
            "2. Investigar: dor, fotofobia, secreção, trauma, uso de lentes",
            "3. 🔴 Sinais de alerta: visão turva + dor + fotofobia → EMERGÊNCIA",
            "4. Conjuntivite viral: sem tratamento específico, compressa fria",
            "5. Conjuntivite bacteriana: antibiótico tópico (tobramicina ou ciprofloxacino)",
            "6. Glaucoma agudo: náusea, visão em halos, córnea turva → URGÊNCIA HOSPITALAR",
        ],
    },
    {
        "titulo": "Trauma Ocular",
        "categoria": "Emergência",
        "cor": "#E53935",
        "resumo": "Avaliação e conduta inicial em trauma ocular na UBS/UPA.",
        "conteudo": [
            "1. NÃO remover corpo estranho perfurante — cobrir com curativo oclusivo",
            "2. Não pressionar o globo ocular",
            "3. Corpo estranho superficial: irrigar com SF 0,9% por 15 min",
            "4. Queimadura química: irrigar IMEDIATAMENTE com grande volume de água/SF",
            "5. Trauma contuso: verificar hifema, diplopia, enoftalmia → TCE?",
            "6. Encaminhar para oftalmologia toda suspeita de perfuração",
        ],
    },
    {
        "titulo": "Perda Visual Súbita",
        "categoria": "Emergência",
        "cor": "#E53935",
        "resumo": "Conduta na perda visual súbita — tempo é visão.",
        "conteudo": [
            "1. OCLUSÃO ARTERIAL RETINIANA: emergência — janela de 90 minutos",
            "2. AINE IV + massagem ocular suave (reduzir PIO)",
            "3. Acionar SAMU / transferir para hospital com oftalmologia",
            "4. Descolamento de retina: flashes + floaters + 'cortina' → urgência cirúrgica",
            "5. Verificar PA, glicemia, ECG (investigar causa sistêmica)",
            "6. AVC: perda visual homônima bilateral → neurologia",
        ],
    },
    {
        "titulo": "Conjuntivite Neonatal",
        "categoria": "Urgência",
        "cor": "#FB8C00",
        "resumo": "Oftalmia neonatal — diagnóstico e tratamento.",
        "conteudo": [
            "1. Primeiras 24h: gonocócica → ceftriaxona IM + lavagem ocular",
            "2. 5-14 dias: clamídia → azitromicina oral por 14 dias",
            "3. Coleta de swab conjuntival antes de iniciar antibiótico",
            "4. Tratar parceiro sexual da mãe",
            "5. Notificar IST na gestante",
        ],
    },
    {
        "titulo": "Retinopatia Diabética — Rastreio",
        "categoria": "Eletivo",
        "cor": "#43A047",
        "resumo": "Protocolo de rastreio e encaminhamento para diabéticos.",
        "conteudo": [
            "1. Todo DM tipo 1 deve fazer fundo de olho após 5 anos de diagnóstico",
            "2. DM tipo 2: fundo de olho no diagnóstico e anualmente",
            "3. Sem retinopatia: repetir em 1-2 anos",
            "4. Retinopatia não proliferativa leve: repetir em 1 ano",
            "5. Retinopatia não proliferativa moderada/grave: encaminhar em 3 meses",
            "6. Retinopatia proliferativa ou EMD: encaminhar em até 30 dias",
        ],
    },
    {
        "titulo": "Glaucoma — Rastreio e Encaminhamento",
        "categoria": "Eletivo",
        "cor": "#43A047",
        "resumo": "Identificação de suspeitos e critérios de encaminhamento.",
        "conteudo": [
            "1. Fatores de risco: HF de glaucoma, >40 anos, miopia alta, DM, hipertensão",
            "2. PIO > 21 mmHg → suspeito → encaminhar para avaliação completa",
            "3. Escavação do nervo óptico (C/D) > 0,6 ou assimétrica → suspeito",
            "4. Glaucoma agudo de ângulo fechado: EMERGÊNCIA (ver protocolo de olho vermelho)",
            "5. Encaminhamento eletivo para confirmação diagnóstica e início de tratamento",
        ],
    },
]

# ─── Helpers ──────────────────────────────────────────────────────────────────
def classificar(sintomas):
    emergencia = {"Dor intensa", "Perda súbita da visão"}
    urgente = {"Trauma ocular", "Corpo estranho"}
    if any(s in emergencia for s in sintomas):
        return "emergencia"
    if any(s in urgente for s in sintomas):
        return "urgente"
    return "eletivo"

def badge_class(classi):
    return {"emergencia": "badge-emergencia", "urgente": "badge-urgente", "eletivo": "badge-eletivo"}[classi]

def badge_text(classi):
    return {"emergencia": "🔴 Emergência", "urgente": "🟡 Urgente", "eletivo": "🟢 Eletivo"}[classi]

def nav(page):
    st.session_state.page = page
    st.rerun()

def card_left_border(color):
    return f"border-left: 5px solid {color};"

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Top Logo - NSD
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("images/nsd.jpg", use_container_width=True)

    st.markdown("""
    <div style='text-align:center; padding: 12px 0 16px 0;'>
        <div style='font-size:1.3rem; font-weight:800; letter-spacing:1px; color:white;'>EyeConnect SUS</div>
        <div style='font-size:0.7rem; opacity:0.9; margin-top:6px; color:white;'>Teleconsultoria Oftalmológica</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.7rem; opacity:0.5; padding: 0 16px 8px; text-transform:uppercase; letter-spacing:1px;'>Menu Principal</div>", unsafe_allow_html=True)

    pages = [
        ("boas_vindas", "🏠", "Bem-vindo"),
        ("inicio", "📊", "Dashboard"),
        ("novo_atendimento", "➕", "Novo Atendimento"),
        ("historico", "📋", "Histórico"),
        ("teleconsultoria", "💬", "Teleconsultoria"),
        ("protocolos", "📖", "Protocolos Clínicos"),
        ("especialistas", "👨‍⚕️", "Especialistas"),
        ("notificacoes", "🔔", "Notificações"),
        ("perfil", "👤", "Perfil"),
    ]

    for key, icon, label in pages:
        active = "active-nav" if st.session_state.page == key else ""
        with st.container():
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                nav(key)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.2); margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='padding:0 16px; font-size:0.75rem; opacity:0.7;'>
        <div>Projeto do Núcleo de Saúde Digital da UNIFESP - GAT 9</div>
        <div style='margin-top:6px;'>Dr(a). Profissional de Saúde</div>
        <div style='margin-top:4px; opacity:0.6;'>CRM/SP 12345</div>
    </div>
    """, unsafe_allow_html=True)

    # Bottom Logo - PET-Saúde
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    st.image("images/PET_HORZINTALCOR.png", use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: BOAS-VINDAS (SPLASH SCREEN)
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "boas_vindas":
    # Hide sidebar on welcome page
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stMainBlockContainer"] {
            width: 100% !important;
            margin-left: 0 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""<div style='text-align:center; padding: 60px 20px;'><div style='font-size:3rem; margin-bottom:20px;'>👁️</div><div style='font-size:2.5rem; font-weight:900; color:#0066CC; letter-spacing:1px;'>EyeConnect</div><div style='font-size:1.5rem; font-weight:700; color:#1F2937; margin-top:4px;'>SUS</div><div style='margin-top:40px; margin-bottom:40px;'><div style='font-size:1.5rem; font-weight:700; color:#1F2937; margin-bottom:12px;'>Bem-vindo(a)!</div><div style='font-size:1rem; color:#6B7280; line-height:1.6; margin-bottom:8px;'>Conecte-se aos especialistas em oftalmologia para apoiar sua decisão clínica.</div><div style='font-size:0.9rem; color:#6B7280;'>Cuidado que transforma vidas.</div></div><div style='margin-top:40px; display:flex; flex-direction:column; gap:12px;'>""", unsafe_allow_html=True)

        if st.button("NOVO ATENDIMENTO", use_container_width=True, key="welcome_novo"):
            st.session_state.page = "novo_atendimento"
            st.rerun()

        if st.button("HISTÓRICO", use_container_width=True, key="welcome_hist"):
            st.session_state.page = "historico"
            st.rerun()

        if st.button("TELECONSULTORIA", use_container_width=True, key="welcome_tele"):
            st.session_state.page = "teleconsultoria"
            st.rerun()

        if st.button("PROTOCOLOS", use_container_width=True, key="welcome_prot"):
            st.session_state.page = "protocolos"
            st.rerun()

        st.markdown("""</div><div style='margin-top:60px; padding-top:30px; border-top:1px solid #E5E7EB;'><div style='font-size:0.8rem; color:#9CA3AF; display:flex; align-items:center; justify-content:center; gap:8px;'><span>🛡️</span><span>Ambiente seguro e confidencial</span></div><div style='font-size:0.75rem; color:#D1D5DB; margin-top:8px;'>Conforme LGPD e normas do SUS</div></div></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: INÍCIO
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "inicio":

    # Top Logos
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.image("images/nsd.jpg", use_container_width=True)
    with col3:
        st.image("images/PET_HORZINTALCOR.png", use_container_width=True)

    st.markdown("""
    <div class='welcome-banner'>
        <div style='font-size:1.5rem; font-weight:800;'>Dashboard</div>
        <div style='margin-top:8px; opacity:0.85; font-size:0.95rem;'>
            Gerencie seus atendimentos e teleconsultorias
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    online_count = sum(1 for e in ESPECIALISTAS if e["online"])
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class='stat-box'>
            <div class='stat-number'>{online_count}</div>
            <div class='stat-label'>Especialistas<br>Online</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='stat-box'>
            <div class='stat-number' style='color:#2E7D32;'>12 min</div>
            <div class='stat-label'>Tempo médio<br>de resposta</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class='stat-box'>
            <div class='stat-number' style='color:#E65100;'>145</div>
            <div class='stat-label'>Atendimentos<br>hoje</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick actions
    st.markdown("<div class='section-title'>Ações Rápidas</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class='card card-blue'>
            <div style='font-size:1.8rem;'>➕</div>
            <div style='font-weight:700; margin-top:8px; color:#1F2937;'>Novo Atendimento</div>
            <div style='font-size:0.85rem; color:#6B7280; margin-top:4px;'>Iniciar triagem de um novo caso</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Iniciar →", key="btn_novo", use_container_width=True):
            st.session_state.novo_caso_step = 1
            st.session_state.novo_caso_data = {}
            nav("novo_atendimento")

    with col2:
        st.markdown("""<div class='card card-green'>
            <div style='font-size:1.8rem;'>📋</div>
            <div style='font-weight:700; margin-top:8px; color:#1F2937;'>Histórico</div>
            <div style='font-size:0.85rem; color:#6B7280; margin-top:4px;'>Acompanhe seus casos</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Ver histórico →", key="btn_hist", use_container_width=True):
            nav("historico")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""<div class='card card-purple'>
            <div style='font-size:1.8rem;'>💬</div>
            <div style='font-weight:700; margin-top:8px; color:#1F2937;'>Teleconsultoria</div>
            <div style='font-size:0.85rem; color:#6B7280; margin-top:4px;'>Fale com um especialista</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Consultar →", key="btn_tele", use_container_width=True):
            nav("teleconsultoria")

    with col4:
        st.markdown("""<div class='card card-orange'>
            <div style='font-size:1.8rem;'>📖</div>
            <div style='font-weight:700; margin-top:8px; color:#1F2937;'>Protocolos Clínicos</div>
            <div style='font-size:0.85rem; color:#6B7280; margin-top:4px;'>Acesse fluxos e condutas</div>
        </div>""", unsafe_allow_html=True)
        if st.button("Ver protocolos →", key="btn_prot", use_container_width=True):
            nav("protocolos")

    # Recent cases
    st.markdown("<br><div class='section-title'>Casos Recentes</div>", unsafe_allow_html=True)
    for caso in st.session_state.casos[:3]:
        delta = datetime.now() - caso["data"]
        if delta.days > 0:
            tempo = f"{delta.days}d atrás"
        elif delta.seconds // 3600 > 0:
            tempo = f"{delta.seconds // 3600}h atrás"
        else:
            tempo = f"{delta.seconds // 60}min atrás"

        col_a, col_b = st.columns([4, 1])
        with col_a:
            st.markdown(f"""<div class='card' style='margin-bottom:8px;'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div>
                        <span style='font-weight:700; color:#222;'>{caso['paciente']}</span>
                        <span style='color:#888; font-size:0.8rem; margin-left:8px;'>{caso['id']}</span>
                    </div>
                    <span class='{badge_class(caso["classificacao"])}' style='font-size:0.8rem; padding:4px 12px;'>{badge_text(caso["classificacao"])}</span>
                </div>
                <div style='color:#555; font-size:0.85rem; margin-top:8px;'>{caso['queixa'][:70]}...</div>
                <div style='color:#aaa; font-size:0.75rem; margin-top:6px;'>{tempo} · {caso["status"]}</div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: NOVO ATENDIMENTO
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "novo_atendimento":
    st.markdown("<div class='section-title'>➕ Novo Atendimento</div>", unsafe_allow_html=True)

    # Progress bar
    steps = ["Dados do Paciente", "Queixa Principal", "Apoio à Decisão", "Imagens", "Resultado"]
    step = st.session_state.novo_caso_step
    progress = (step - 1) / (len(steps) - 1)
    st.progress(progress)
    cols_steps = st.columns(len(steps))
    for i, (col, s) in enumerate(zip(cols_steps, steps)):
        with col:
            color = "#1565C0" if i + 1 == step else ("#2E7D32" if i + 1 < step else "#ccc")
            st.markdown(f"<div style='text-align:center; color:{color}; font-size:0.75rem; font-weight:{'700' if i+1==step else '400'};'>{s}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    data = st.session_state.novo_caso_data

    # ── STEP 1: Dados do Paciente ─────────────────────────────────────────────
    if step == 1:
        st.markdown("#### 👤 Dados do Paciente")
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                nome = st.text_input("Nome completo *", value=data.get("nome", ""))
            with col2:
                idade = st.number_input("Idade *", min_value=0, max_value=120, value=data.get("idade", 0))
            with col3:
                sexo = st.selectbox("Sexo *", ["", "Feminino", "Masculino", "Outro"], index=["", "Feminino", "Masculino", "Outro"].index(data.get("sexo", "")))

            col4, col5 = st.columns(2)
            with col4:
                cartao_sus = st.text_input("Cartão SUS", value=data.get("cartao_sus", ""))
            with col5:
                ubs = st.text_input("UBS de origem", value=data.get("ubs", "UBS Central"))

        if st.button("Próximo →", type="primary", use_container_width=True):
            if not nome or not sexo or idade == 0:
                st.error("Por favor, preencha todos os campos obrigatórios (*).")
            else:
                st.session_state.novo_caso_data.update({"nome": nome, "idade": idade, "sexo": sexo, "cartao_sus": cartao_sus, "ubs": ubs})
                st.session_state.novo_caso_step = 2
                st.rerun()

    # ── STEP 2: Queixa Principal ──────────────────────────────────────────────
    elif step == 2:
        st.markdown("#### 👁️ Queixa Principal")
        olho = st.radio("Olho afetado", ["OD (Olho Direito)", "OE (Olho Esquerdo)", "AO (Ambos os Olhos)"], horizontal=True, index=["OD (Olho Direito)", "OE (Olho Esquerdo)", "AO (Ambos os Olhos)"].index(data.get("olho", "OD (Olho Direito)")))
        queixa = st.text_area("Descreva a queixa principal *", value=data.get("queixa", ""), height=120, placeholder="Ex.: Paciente relata dor intensa no olho direito há 2 horas, com baixa da visão...")
        ha_quanto = st.selectbox("Há quanto tempo?", ["< 1 hora", "1-6 horas", "6-24 horas", "1-3 dias", "> 3 dias"], index=["< 1 hora", "1-6 horas", "6-24 horas", "1-3 dias", "> 3 dias"].index(data.get("ha_quanto", "< 1 hora")))

        col1, col2 = st.columns(2)
        with col1:
            acuidade_od = st.text_input("Acuidade Visual OD", value=data.get("acuidade_od", ""), placeholder="Ex.: 20/40")
        with col2:
            acuidade_oe = st.text_input("Acuidade Visual OE", value=data.get("acuidade_oe", ""), placeholder="Ex.: 20/20")

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Voltar", use_container_width=True):
                st.session_state.novo_caso_step = 1
                st.rerun()
        with col_next:
            if st.button("Próximo →", type="primary", use_container_width=True):
                if not queixa:
                    st.error("Descreva a queixa principal.")
                else:
                    st.session_state.novo_caso_data.update({
                        "olho": olho.split()[0], "queixa": queixa,
                        "ha_quanto": ha_quanto, "acuidade_od": acuidade_od, "acuidade_oe": acuidade_oe,
                    })
                    st.session_state.novo_caso_step = 3
                    st.rerun()

    # ── STEP 3: Checklist de Apoio à Decisão ─────────────────────────────────
    elif step == 3:
        st.markdown("#### ✅ Apoio à Decisão — Checklist de Sinais de Alerta")
        st.info("Marque todos os sinais e sintomas presentes no paciente:")

        st.markdown("##### 🔴 Sinais de Emergência")
        dor_intensa = st.checkbox("**Dor intensa** — dor ocular severa, súbita ou progressiva", value=data.get("dor_intensa", False))
        perda_visao = st.checkbox("**Perda súbita da visão** — baixa visual aguda em um ou ambos os olhos", value=data.get("perda_visao", False))

        st.markdown("##### 🟡 Sinais de Urgência")
        trauma = st.checkbox("**Trauma ocular** — impacto, contusão ou ferimento no olho/órbita", value=data.get("trauma", False))
        corpo_estranho = st.checkbox("**Corpo estranho** — sensação ou evidência de CE no olho", value=data.get("corpo_estranho", False))

        st.markdown("##### 🟢 Outros Sintomas")
        col1, col2 = st.columns(2)
        with col1:
            olho_vermelho = st.checkbox("Olho vermelho / hiperemia", value=data.get("olho_vermelho", False))
            secrecao = st.checkbox("Secreção ocular", value=data.get("secrecao", False))
            fotofobia = st.checkbox("Fotofobia", value=data.get("fotofobia", False))
        with col2:
            diplopia = st.checkbox("Diplopia (visão dupla)", value=data.get("diplopia", False))
            flashes = st.checkbox("Flashes / moscas volantes", value=data.get("flashes", False))
            cefaleia = st.checkbox("Cefaleia associada", value=data.get("cefaleia", False))

        # Live classification
        sintomas_selecionados = []
        if dor_intensa: sintomas_selecionados.append("Dor intensa")
        if perda_visao: sintomas_selecionados.append("Perda súbita da visão")
        if trauma: sintomas_selecionados.append("Trauma ocular")
        if corpo_estranho: sintomas_selecionados.append("Corpo estranho")

        classi = classificar(sintomas_selecionados)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Pré-classificação em tempo real:**")

        if classi == "emergencia":
            st.markdown("""<div style='background:#FFEBEE; border:2px solid #EF5350; border-radius:12px; padding:16px; text-align:center;'>
                <div style='font-size:1.6rem;'>🔴</div>
                <div style='font-size:1.2rem; font-weight:800; color:#C62828;'>EMERGÊNCIA</div>
                <div style='color:#C62828; margin-top:6px;'>Encaminhar IMEDIATAMENTE para urgência oftalmológica ou acionar especialista agora.</div>
            </div>""", unsafe_allow_html=True)
        elif classi == "urgente":
            st.markdown("""<div style='background:#FFF8E1; border:2px solid #FFA726; border-radius:12px; padding:16px; text-align:center;'>
                <div style='font-size:1.6rem;'>🟡</div>
                <div style='font-size:1.2rem; font-weight:800; color:#E65100;'>URGENTE</div>
                <div style='color:#E65100; margin-top:6px;'>Avaliação especializada em até 24 horas. Iniciar teleconsultoria.</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style='background:#E8F5E9; border:2px solid #66BB6A; border-radius:12px; padding:16px; text-align:center;'>
                <div style='font-size:1.6rem;'>🟢</div>
                <div style='font-size:1.2rem; font-weight:800; color:#2E7D32;'>ELETIVO</div>
                <div style='color:#2E7D32; margin-top:6px;'>Pode aguardar consulta oftalmológica eletiva. Use teleconsultoria assíncrona.</div>
            </div>""", unsafe_allow_html=True)

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Voltar", use_container_width=True):
                st.session_state.novo_caso_step = 2
                st.rerun()
        with col_next:
            if st.button("Próximo →", type="primary", use_container_width=True):
                st.session_state.novo_caso_data.update({
                    "dor_intensa": dor_intensa, "perda_visao": perda_visao,
                    "trauma": trauma, "corpo_estranho": corpo_estranho,
                    "olho_vermelho": olho_vermelho, "secrecao": secrecao,
                    "fotofobia": fotofobia, "diplopia": diplopia,
                    "flashes": flashes, "cefaleia": cefaleia,
                    "classificacao": classi, "sintomas": sintomas_selecionados,
                })
                st.session_state.novo_caso_step = 4
                st.rerun()

    # ── STEP 4: Upload de Imagens ─────────────────────────────────────────────
    elif step == 4:
        st.markdown("#### 📷 Upload de Imagens do Olho")
        st.markdown("Envie fotos do olho do paciente para auxiliar o especialista na avaliação.")

        col1, col2 = st.columns([3, 2])
        with col1:
            uploaded_files = st.file_uploader(
                "Selecione as imagens (JPG, PNG)",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                key="img_uploader"
            )
            if uploaded_files:
                st.success(f"{len(uploaded_files)} imagem(ns) carregada(s)")
                cols_img = st.columns(min(len(uploaded_files), 3))
                for i, f in enumerate(uploaded_files[:3]):
                    with cols_img[i]:
                        st.image(f, caption=f.name, use_container_width=True)

        with col2:
            st.markdown("""<div class='card' style='background:#E3F2FD;'>
                <div style='font-weight:700; color:#1565C0; margin-bottom:8px;'>💡 Dicas para boas fotos</div>
                <div style='font-size:0.85rem; color:#444; line-height:1.7;'>
                ✓ Use boa iluminação<br>
                ✓ Foque na região afetada<br>
                ✓ Tire de perto (5–10 cm)<br>
                ✓ Evite flash direto<br>
                ✓ Inclua olho fechado e aberto<br>
                ✓ Foto com luz lateral ajuda
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown("""<div class='card'>
                <div style='font-weight:700; color:#444; margin-bottom:8px;'>📱 Câmera do celular</div>
                <div style='font-size:0.8rem; color:#666;'>Tire as fotos com a câmera do celular e transfira para o computador, ou use este app diretamente no smartphone.</div>
            </div>""", unsafe_allow_html=True)

        imagens_salvas = [f.name for f in (uploaded_files or [])]

        col_back, col_next = st.columns(2)
        with col_back:
            if st.button("← Voltar", use_container_width=True):
                st.session_state.novo_caso_step = 3
                st.rerun()
        with col_next:
            if st.button("Finalizar e Classificar →", type="primary", use_container_width=True):
                st.session_state.novo_caso_data["imagens"] = imagens_salvas
                st.session_state.novo_caso_step = 5
                st.rerun()

    # ── STEP 5: Resultado ─────────────────────────────────────────────────────
    elif step == 5:
        d = st.session_state.novo_caso_data
        classi = d.get("classificacao", "eletivo")

        st.markdown("#### 🎯 Resultado da Triagem")

        # Main classification badge
        if classi == "emergencia":
            st.markdown("""<div style='background:#FFEBEE; border:2px solid #EF5350; border-radius:16px; padding:24px; text-align:center; margin-bottom:20px;'>
                <div style='font-size:3rem;'>🔴</div>
                <div style='font-size:2rem; font-weight:900; color:#C62828;'>EMERGÊNCIA</div>
                <div style='color:#C62828; margin-top:8px; font-size:1rem;'>Encaminhar IMEDIATAMENTE</div>
            </div>""", unsafe_allow_html=True)
        elif classi == "urgente":
            st.markdown("""<div style='background:#FFF8E1; border:2px solid #FFA726; border-radius:16px; padding:24px; text-align:center; margin-bottom:20px;'>
                <div style='font-size:3rem;'>🟡</div>
                <div style='font-size:2rem; font-weight:900; color:#E65100;'>URGENTE</div>
                <div style='color:#E65100; margin-top:8px; font-size:1rem;'>Avaliação em até 24 horas</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style='background:#E8F5E9; border:2px solid #66BB6A; border-radius:16px; padding:24px; text-align:center; margin-bottom:20px;'>
                <div style='font-size:3rem;'>🟢</div>
                <div style='font-size:2rem; font-weight:900; color:#2E7D32;'>ELETIVO</div>
                <div style='color:#2E7D32; margin-top:8px; font-size:1rem;'>Consulta eletiva — teleconsultoria assíncrona</div>
            </div>""", unsafe_allow_html=True)

        # Summary
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""<div class='card'>
                <div style='font-weight:700; margin-bottom:10px; color:#222;'>👤 Paciente</div>
                <div style='color:#222;'><b>Nome:</b> {d.get('nome')}</div>
                <div style='color:#222;'><b>Idade:</b> {d.get('idade')} anos · {d.get('sexo')}</div>
                <div style='color:#222;'><b>Olho:</b> {d.get('olho')}</div>
                <div style='margin-top:8px; color:#222;'><b>Queixa:</b> {d.get('queixa', '')[:80]}...</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            sintomas = d.get("sintomas", [])
            outros = [k for k in ["olho_vermelho","secrecao","fotofobia","diplopia","flashes","cefaleia"] if d.get(k)]
            outros_labels = {"olho_vermelho": "Olho vermelho", "secrecao": "Secreção", "fotofobia": "Fotofobia", "diplopia": "Diplopia", "flashes": "Flashes/moscas", "cefaleia": "Cefaleia"}
            st.markdown(f"""<div class='card'>
                <div style='font-weight:700; margin-bottom:10px; color:#222;'>✅ Sinais Marcados</div>
                {''.join([f"<div style='color:#222;'>⚠️ {s}</div>" for s in sintomas]) if sintomas else '<div style="color:#888">Nenhum sinal de alarme</div>'}
                {''.join([f"<div style='color:#666'>• {outros_labels[s]}</div>" for s in outros]) if outros else ""}
            </div>""", unsafe_allow_html=True)

        # Recommended actions
        st.markdown("#### 📋 Conduta Recomendada")
        if classi == "emergencia":
            st.error("🚨 **Ação imediata:** Acione o SAMU (192) ou encaminhe o paciente à UPA/pronto-socorro com serviço de oftalmologia. Inicie teleconsulta síncrona agora.")
        elif classi == "urgente":
            st.warning("⚠️ **Ação em até 24h:** Inicie teleconsultoria assíncrona agora. O especialista retornará em até 12 minutos. Oriente o paciente a retornar se houver piora.")
        else:
            st.success("✅ **Ação eletiva:** Registre o caso e inicie teleconsultoria assíncrona. Agende consulta oftalmológica de rotina em 30-60 dias.")

        # Save case
        novo_id = f"ATD-{str(len(st.session_state.casos) + 1).zfill(3)}"

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("💾 Salvar Caso", type="primary", use_container_width=True):
                novo_caso = {
                    "id": novo_id,
                    "paciente": d.get("nome"),
                    "idade": d.get("idade"),
                    "sexo": d.get("sexo", "")[0] if d.get("sexo") else "F",
                    "queixa": d.get("queixa"),
                    "classificacao": classi,
                    "data": datetime.now(),
                    "status": "Aguardando teleconsultoria",
                    "olho": d.get("olho"),
                    "sintomas": d.get("sintomas", []),
                    "imagens": d.get("imagens", []),
                    "teleconsulta": [],
                }
                st.session_state.casos.insert(0, novo_caso)
                st.session_state.chat_msgs[novo_id] = []
                st.success(f"✅ Caso {novo_id} salvo com sucesso!")
                st.balloons()
                st.session_state.novo_caso_step = 1
                st.session_state.novo_caso_data = {}
        with col_b:
            if st.button("💬 Iniciar Teleconsultoria", use_container_width=True):
                if "nome" in d:
                    novo_caso = {
                        "id": novo_id, "paciente": d.get("nome"),
                        "idade": d.get("idade"), "sexo": d.get("sexo", "")[0] if d.get("sexo") else "F",
                        "queixa": d.get("queixa"), "classificacao": classi,
                        "data": datetime.now(), "status": "Em teleconsultoria",
                        "olho": d.get("olho"), "sintomas": d.get("sintomas", []),
                        "imagens": d.get("imagens", []), "teleconsulta": [],
                    }
                    st.session_state.casos.insert(0, novo_caso)
                    st.session_state.chat_msgs[novo_id] = []
                    st.session_state.novo_caso_step = 1
                    st.session_state.novo_caso_data = {}
                st.session_state.page = "teleconsultoria"
                st.rerun()
        with col_c:
            if st.button("🔄 Novo Caso", use_container_width=True):
                st.session_state.novo_caso_step = 1
                st.session_state.novo_caso_data = {}
                st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HISTÓRICO
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "historico":
    st.markdown("<div class='section-title'>📋 Histórico de Atendimentos</div>", unsafe_allow_html=True)

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_classi = st.selectbox("Classificação", ["Todas", "🔴 Emergência", "🟡 Urgente", "🟢 Eletivo"])
    with col2:
        filtro_status = st.selectbox("Status", ["Todos", "Aguardando especialista", "Em teleconsultoria", "Respondido"])
    with col3:
        busca = st.text_input("🔍 Buscar paciente", placeholder="Nome ou ID...")

    st.markdown("<br>", unsafe_allow_html=True)

    # Filter logic
    casos_filtrados = st.session_state.casos
    if filtro_classi != "Todas":
        mapa = {"🔴 Emergência": "emergencia", "🟡 Urgente": "urgente", "🟢 Eletivo": "eletivo"}
        casos_filtrados = [c for c in casos_filtrados if c["classificacao"] == mapa[filtro_classi]]
    if filtro_status != "Todos":
        casos_filtrados = [c for c in casos_filtrados if c["status"] == filtro_status]
    if busca:
        casos_filtrados = [c for c in casos_filtrados if busca.lower() in c["paciente"].lower() or busca.upper() in c["id"]]

    st.markdown(f"**{len(casos_filtrados)} caso(s) encontrado(s)**")

    for caso in casos_filtrados:
        delta = datetime.now() - caso["data"]
        if delta.days > 0:
            tempo = f"{delta.days} dia(s) atrás"
        elif delta.seconds // 3600 > 0:
            tempo = f"{delta.seconds // 3600}h atrás"
        else:
            tempo = f"{delta.seconds // 60}min atrás"

        with st.expander(f"**{caso['id']}** — {caso['paciente']}, {caso.get('idade','')} anos · {badge_text(caso['classificacao'])} · {tempo}"):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**Queixa:** {caso['queixa']}")
                st.markdown(f"**Olho:** {caso.get('olho', '—')} &nbsp;&nbsp; **Status:** {caso['status']}")
                if caso.get("sintomas"):
                    st.markdown("**Sinais de alerta:** " + ", ".join(caso["sintomas"]))
                if caso.get("imagens"):
                    st.markdown(f"📷 {len(caso['imagens'])} imagem(ns) anexada(s)")
            with col_b:
                st.markdown(f"<div class='{badge_class(caso['classificacao'])}' style='margin-top:10px;'>{badge_text(caso['classificacao'])}</div>", unsafe_allow_html=True)

            if caso.get("teleconsulta"):
                st.markdown("**Resposta do especialista:**")
                for msg in caso["teleconsulta"]:
                    st.info(f"👨‍⚕️ **{msg['de']}** ({msg['hora']}): {msg['msg']}")

            if st.button("💬 Abrir Teleconsultoria", key=f"tele_{caso['id']}"):
                st.session_state["caso_ativo"] = caso["id"]
                nav("teleconsultoria")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: TELECONSULTORIA
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "teleconsultoria":
    st.markdown("<div class='section-title'>💬 Teleconsultoria</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["💬 Assíncrona (Chat)", "📹 Síncrona (Videochamada)"])

    with tab1:
        col_list, col_chat = st.columns([1, 2])

        with col_list:
            st.markdown("**Selecione o caso:**")
            for caso in st.session_state.casos:
                n_msgs = len(st.session_state.chat_msgs.get(caso["id"], []))
                is_active = st.session_state.get("caso_ativo") == caso["id"]
                bg = "#E3F2FD" if is_active else "white"
                bord = "#1565C0" if is_active else "#eee"

                st.markdown(f"""<div style='background:{bg}; border:2px solid {bord}; border-radius:10px;
                    padding:10px 12px; margin-bottom:8px; cursor:pointer;'>
                    <div style='font-weight:700; font-size:0.85rem; color:#222;'>{caso['paciente']}</div>
                    <div style='font-size:0.75rem; color:#666;'>{caso['id']} · {badge_text(caso["classificacao"])}</div>
                    <div style='font-size:0.75rem; color:#888;'>{n_msgs} mensagen(s)</div>
                </div>""", unsafe_allow_html=True)
                if st.button("Abrir", key=f"open_{caso['id']}", use_container_width=True):
                    st.session_state["caso_ativo"] = caso["id"]
                    st.rerun()

        with col_chat:
            caso_id = st.session_state.get("caso_ativo")
            if not caso_id:
                st.info("← Selecione um caso para iniciar a teleconsultoria.")
            else:
                caso = next((c for c in st.session_state.casos if c["id"] == caso_id), None)
                if caso:
                    st.markdown(f"#### {caso['paciente']} · {caso['id']}")
                    st.markdown(f"<span class='{badge_class(caso['classificacao'])}'>{badge_text(caso['classificacao'])}</span>", unsafe_allow_html=True)
                    st.caption(f"Queixa: {caso['queixa']}")
                    st.markdown("---")

                    # Chat history
                    msgs = st.session_state.chat_msgs.get(caso_id, [])
                    chat_html = ""
                    for m in msgs:
                        if m["de"] == "Você":
                            chat_html += f"""<div class='chat-user'>
                                {m['msg']}
                                <div class='chat-time'>{m['hora']}</div>
                            </div>"""
                        else:
                            chat_html += f"""<div class='chat-specialist'>
                                <div style='font-size:0.75rem; font-weight:700; color:#1565C0; margin-bottom:4px;'>👨‍⚕️ {m['de']}</div>
                                {m['msg']}
                                <div class='chat-time'>{m['hora']}</div>
                            </div>"""

                    if chat_html:
                        st.markdown(f"<div style='max-height:350px; overflow-y:auto; padding:8px;'>{chat_html}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='text-align:center; color:#aaa; padding:40px;'>Nenhuma mensagem ainda. Inicie a consulta abaixo.</div>", unsafe_allow_html=True)

                    st.markdown("---")

                    # Specialist selector
                    especialistas_online = [e for e in ESPECIALISTAS if e["online"]]
                    esp_selecionado = st.selectbox(
                        "Encaminhar para:",
                        [f"{e['nome']} — {e['subespecialidade']} ({e['tempo_resposta']})" for e in especialistas_online],
                        key="esp_select"
                    )

                    # Message input
                    nova_msg = st.text_area("Sua mensagem:", height=80, key="nova_msg", placeholder="Descreva o caso, sintomas, achados ao exame...")

                    col_img, col_send = st.columns([1, 2])
                    with col_img:
                        img_chat = st.file_uploader("📎 Anexar imagem", type=["jpg","png"], key=f"img_{caso_id}")
                    with col_send:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("📤 Enviar Mensagem", type="primary", use_container_width=True):
                            if nova_msg or img_chat:
                                hora = datetime.now().strftime("%H:%M")
                                msg_text = nova_msg if nova_msg else ""
                                if img_chat:
                                    msg_text += f" [📷 Imagem: {img_chat.name}]"

                                if caso_id not in st.session_state.chat_msgs:
                                    st.session_state.chat_msgs[caso_id] = []
                                st.session_state.chat_msgs[caso_id].append({"de": "Você", "msg": msg_text, "hora": hora})

                                # Mock auto-response
                                respostas_mock = {
                                    "emergencia": "⚠️ Recebemos sua mensagem com prioridade EMERGÊNCIA. Dr(a). responsável foi notificado(a). Retorno em até 5 minutos. Enquanto isso, mantenha o paciente em repouso e evite pressionar o globo ocular.",
                                    "urgente": "Recebi as informações. Vou analisar as imagens enviadas e retorno em breve com a conduta recomendada.",
                                    "eletivo": "Caso recebido. Analisarei e retornarei com orientações em até 30 minutos.",
                                }

                                esp_nome = esp_selecionado.split(" — ")[0]
                                st.session_state.chat_msgs[caso_id].append({
                                    "de": f"{esp_nome} (Especialista)",
                                    "msg": respostas_mock.get(caso["classificacao"], "Mensagem recebida. Retorno em breve."),
                                    "hora": datetime.now().strftime("%H:%M"),
                                })
                                st.rerun()

    with tab2:
        st.markdown("#### 📹 Teleconsulta Síncrona — Videochamada")

        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.markdown("""<div class='card'>
                <div style='font-size:1.1rem; font-weight:700; margin-bottom:12px;'>Como funciona</div>
                <div style='font-size:0.9rem; color:#444; line-height:1.8;'>
                1. Selecione o caso e o especialista disponível<br>
                2. O especialista recebe a solicitação de videochamada<br>
                3. Ao aceitar, a chamada se inicia automaticamente<br>
                4. Pode incluir o paciente ou ser médico-médico<br>
                5. Ao final, o especialista registra a conduta no sistema
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown("**Selecionar caso:**")
            caso_video = st.selectbox("Caso", [f"{c['id']} — {c['paciente']}" for c in st.session_state.casos])

            st.markdown("**Especialista disponível:**")
            for esp in ESPECIALISTAS:
                status_color = "#4CAF50" if esp["online"] else "#ccc"
                status_text = f"🟢 Online · {esp['tempo_resposta']}" if esp["online"] else "⚫ Offline"
                st.markdown(f"""<div style='background:white; border-radius:10px; padding:12px 16px;
                    margin-bottom:8px; box-shadow:0 1px 4px rgba(0,0,0,0.08);
                    border-left:4px solid {status_color};'>
                    <div style='font-weight:700; color:#222;'>{esp['nome']}</div>
                    <div style='font-size:0.8rem; color:#666;'>{esp['subespecialidade']} · {esp['crm']}</div>
                    <div style='font-size:0.8rem; margin-top:4px; color:#555;'>{status_text}</div>
                </div>""", unsafe_allow_html=True)

        with col_b:
            st.markdown("""<div class='card' style='background:#E8EAF6; text-align:center; padding:32px;'>
                <div style='font-size:4rem;'>📹</div>
                <div style='font-weight:700; font-size:1.1rem; color:#1A237E; margin-top:12px;'>Videochamada</div>
                <div style='color:#666; font-size:0.85rem; margin-top:8px;'>Conecte com especialistas em tempo real para casos complexos</div>
            </div>""", unsafe_allow_html=True)

            if st.button("📞 Solicitar Videochamada", type="primary", use_container_width=True):
                with st.spinner("Conectando com o especialista..."):
                    time.sleep(2)
                st.success("✅ Solicitação enviada! O especialista responderá em instantes.")
                st.info("Em um app real, aqui abriria a interface de videochamada (ex.: Whereby, Jitsi, Zoom SDK ou WebRTC).")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PROTOCOLOS CLÍNICOS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "protocolos":
    st.markdown("<div class='section-title'>📖 Protocolos Clínicos</div>", unsafe_allow_html=True)

    busca_prot = st.text_input("🔍 Buscar protocolo", placeholder="Ex.: trauma, glaucoma, conjuntivite...")
    st.markdown("<br>", unsafe_allow_html=True)

    prot_filtrados = PROTOCOLOS
    if busca_prot:
        prot_filtrados = [p for p in PROTOCOLOS if busca_prot.lower() in p["titulo"].lower() or busca_prot.lower() in p["resumo"].lower()]

    for p in prot_filtrados:
        cat_color = {"Emergência": "#EF5350", "Urgência": "#FFA726", "Eletivo": "#66BB6A"}.get(p["categoria"], "#1565C0")
        with st.expander(f"**{p['titulo']}** — _{p['categoria']}_"):
            st.markdown(f"<span style='background:{cat_color}20; color:{cat_color}; border:1px solid {cat_color}; border-radius:20px; padding:3px 12px; font-size:0.8rem; font-weight:700;'>{p['categoria']}</span>", unsafe_allow_html=True)
            st.markdown(f"*{p['resumo']}*")
            st.markdown("---")
            for linha in p["conteudo"]:
                st.markdown(linha)

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("💬 Abrir Teleconsultoria sobre este protocolo", key=f"prot_tele_{p['titulo']}"):
                    nav("teleconsultoria")
            with col_b:
                if st.button("📤 Compartilhar protocolo", key=f"prot_share_{p['titulo']}"):
                    st.info("Em um app real, geraria PDF para compartilhar com a equipe.")

    st.markdown("---")
    st.markdown("""<div class='card' style='background:#E3F2FD; text-align:center;'>
        <div style='font-weight:700; color:#1565C0;'>🎓 Educação Permanente</div>
        <div style='font-size:0.85rem; color:#444; margin-top:8px;'>
        Os protocolos são atualizados trimestralmente com base nas diretrizes do CFM e CBO (Conselho Brasileiro de Oftalmologia).
        Dúvidas sobre condutas? Inicie uma teleconsultoria!
        </div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: ESPECIALISTAS
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "especialistas":
    st.markdown("<div class='section-title'>👨‍⚕️ Especialistas</div>", unsafe_allow_html=True)

    online_count = sum(1 for e in ESPECIALISTAS if e["online"])
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class='stat-box' style='background:#E8F5E9;'>
            <div class='stat-number' style='color:#2E7D32;'>{online_count}</div>
            <div class='stat-label'>Online agora</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='stat-box'>
            <div class='stat-number'>{len(ESPECIALISTAS)}</div>
            <div class='stat-label'>Total de especialistas</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    filtro_online = st.checkbox("Mostrar apenas especialistas online", value=False)
    especialistas_mostrar = [e for e in ESPECIALISTAS if e["online"]] if filtro_online else ESPECIALISTAS

    for esp in especialistas_mostrar:
        status_color = "#4CAF50" if esp["online"] else "#9E9E9E"
        status_label = f"🟢 Online · Resposta {esp['tempo_resposta']}" if esp["online"] else "⚫ Offline"

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""<div class='card' style='border-left:4px solid {status_color};'>
                <div style='display:flex; justify-content:space-between;'>
                    <div>
                        <div style='font-weight:800; font-size:1rem; color:#222;'>{esp['nome']}</div>
                        <div style='color:#666; font-size:0.85rem;'>{esp['subespecialidade']}</div>
                        <div style='color:#888; font-size:0.8rem;'>{esp['crm']}</div>
                    </div>
                    <div style='text-align:right;'>
                        <div style='font-size:0.8rem; color:{status_color}; font-weight:600;'>{status_label}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            if esp["online"]:
                if st.button("💬 Consultar", key=f"esp_{esp['nome']}", use_container_width=True):
                    nav("teleconsultoria")

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: NOTIFICAÇÕES
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "notificacoes":
    st.markdown("<div class='section-title'>🔔 Notificações</div>", unsafe_allow_html=True)

    notifs = [
        {"tipo": "resposta", "msg": "Dra. Patrícia respondeu o caso ATD-003 — Ana Oliveira", "tempo": "há 15 min", "lida": False, "cor": "#1565C0"},
        {"tipo": "emergencia", "msg": "⚠️ Caso ATD-001 classificado como EMERGÊNCIA — aguarda resposta do especialista", "tempo": "há 2 horas", "lida": False, "cor": "#C62828"},
        {"tipo": "resposta", "msg": "Dr. Carlos respondeu o caso ATD-002 — João Santos", "tempo": "há 3 horas", "lida": True, "cor": "#1565C0"},
        {"tipo": "sistema", "msg": "Novo protocolo adicionado: Retinopatia Diabética — Atualização 2025", "tempo": "há 1 dia", "lida": True, "cor": "#E65100"},
        {"tipo": "sistema", "msg": "8 especialistas online agora. Tempo médio de resposta: 12 minutos.", "tempo": "há 2 dias", "lida": True, "cor": "#2E7D32"},
    ]

    nao_lidas = sum(1 for n in notifs if not n["lida"])
    st.markdown(f"**{nao_lidas} notificação(ões) não lida(s)**")
    st.markdown("<br>", unsafe_allow_html=True)

    for n in notifs:
        bg = "#F8F9FF" if not n["lida"] else "white"
        bord = n["cor"] if not n["lida"] else "#eee"
        dot = "🔵 " if not n["lida"] else ""

        st.markdown(f"""<div style='background:{bg}; border:1px solid {bord}; border-left:4px solid {bord};
            border-radius:10px; padding:14px 18px; margin-bottom:10px;'>
            <div style='font-size:0.9rem; color:#222;'>{dot}{n['msg']}</div>
            <div style='font-size:0.75rem; color:#aaa; margin-top:6px;'>{n['tempo']}</div>
        </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: PERFIL
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "perfil":
    st.markdown("<div class='section-title'>👤 Perfil</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""<div style='background:#1A237E; border-radius:50%; width:80px; height:80px;
            display:flex; align-items:center; justify-content:center; font-size:2.5rem; margin:auto;'>
            👩‍⚕️
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("### Dr(a). Profissional de Saúde")
        st.markdown("**CRM/SP 12345** · Médico(a) de Família e Comunidade")
        st.markdown("🏥 UBS Central — São Paulo/SP")

    st.markdown("---")

    with st.form("perfil_form"):
        st.markdown("#### ✏️ Editar Dados")
        col1, col2 = st.columns(2)
        with col1:
            nome_p = st.text_input("Nome completo", "Dr(a). Profissional de Saúde")
            crm_p = st.text_input("CRM", "CRM/SP 12345")
        with col2:
            especialidade_p = st.text_input("Especialidade", "Médico(a) de Família e Comunidade")
            ubs_p = st.text_input("UBS / Unidade", "UBS Central — São Paulo/SP")

        notif_pref = st.multiselect("Preferências de notificação",
            ["Resposta de especialista", "Casos de emergência", "Novos protocolos", "Relatórios semanais"],
            default=["Resposta de especialista", "Casos de emergência"])

        if st.form_submit_button("💾 Salvar Alterações", type="primary"):
            st.success("Perfil atualizado com sucesso!")

    st.markdown("---")
    st.markdown("#### 📊 Minhas Estatísticas")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class='stat-box'><div class='stat-number'>47</div><div class='stat-label'>Casos abertos</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='stat-box'><div class='stat-number' style='color:#2E7D32;'>38</div><div class='stat-label'>Respondidos</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='stat-box'><div class='stat-number' style='color:#E65100;'>6</div><div class='stat-label'>Urgentes</div></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class='stat-box'><div class='stat-number' style='color:#C62828;'>3</div><div class='stat-label'>Emergências</div></div>""", unsafe_allow_html=True)

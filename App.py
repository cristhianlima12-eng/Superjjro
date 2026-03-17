import streamlit as st

# Configuração da página
st.set_page_config(page_title="SUPER JJ SNIPER", layout="centered")

# --- CSS DE FORÇA BRUTA PARA MANTER 3 COLUNAS NO CELULAR ---
st.markdown("""
    <style>
    /* Esconder cabeçalhos e menus */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 0.5rem; background-color: #0d1117;}

    /* FORÇA AS COLUNAS A FICAREM LADO A LADO NO CELULAR (33% CADA) */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
    }
    div[data-testid="column"] {
        width: 33.33% !important;
        flex: 1 1 33.33% !important;
        min-width: 33.33% !important;
    }

    /* Estilo dos Botões */
    .stButton > button {
        width: 100%;
        height: 55px !important;
        border-radius: 4px;
        font-weight: bold;
        font-size: 20px !important;
        color: white !important;
        border: 1px solid #444;
        margin-bottom: 2px;
    }

    /* Cores das Células */
    .btn-red > div > button { background-color: #da3633 !important; }
    .btn-black > div > button { background-color: #161b22 !important; }
    .btn-zero > div > button { 
        background-color: #238636 !important; 
        height: 65px !important;
        margin-bottom: 8px;
    }

    /* Alerta de Entrada no TOPO */
    .stAlert { margin-bottom: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DO SISTEMA ---
RODA = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
VERMELHOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

if 'hist' not in st.session_state: st.session_state.hist = []
if 'puxadas' not in st.session_state: st.session_state.puxadas = {}
if 'op' not in st.session_state: st.session_state.op = {"ativo": False, "alvos": [], "msg": ""}

def registrar(num):
    hist = st.session_state.hist
    if st.session_state.op["ativo"]:
        if num in st.session_state.op["alvos"] or num == 0:
            st.toast("✅ GREEN!", icon="✅")
            st.session_state.op["ativo"] = False
    
    if len(hist) > 0:
        ult = hist[-1]
        if ult not in st.session_state.puxadas: st.session_state.puxadas[ult] = []
        st.session_state.puxadas[ult].append(num)
    
    st.session_state.hist.append(num)
    
    puxs = st.session_state.puxadas.get(num, [])
    if puxs:
        comum = max(set(puxs), key=puxs.count)
        if puxs.count(comum) >= 2:
            idx = RODA.index(comum)
            vizis = [RODA[(idx+i)%37] for i in range(-2, 3)]
            st.session_state.op.update({"ativo": True, "alvos": vizis, "msg": f"🚨 MANIPULAÇÃO: {num} → {comum}"})

# --- INTERFACE ---

# 1. ATUALIZAÇÕES E ENTRADAS (TOPO)
if st.session_state.op["ativo"]:
    st.warning(f"**{st.session_state.op['msg']}**")
else:
    st.info("🔍 MONITORANDO... AGUARDANDO PADRÃO.")

# 2. TABELA DE NÚMEROS (MEIO)
# Botão Zero Ocupando o Topo
st.markdown('<div class="btn-zero">', unsafe_allow_html=True)
if st.button("0"):
    registrar(0); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Grid 3 Colunas Fixas (1-2-3, 4-5-6...)
for i in range(0, 12):
    cols = st.columns(3)
    for j in range(3):
        n = (i * 3) + j + 1
        cor = "btn-red" if n in VERMELHOS else "btn-black"
        with cols[j]:
            st.markdown(f'<div class="{cor}">', unsafe_allow_html=True)
            if st.button(str(n)):
                registrar(n); st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# 3. HISTÓRICO (BAIXO)
if st.session_state.hist:
    st.write("---")
    st.caption(f"HISTÓRICO: {st.session_state.hist[-12:]}")

if st.button("🗑️ RESET"):
    st.session_state.clear(); st.rerun()

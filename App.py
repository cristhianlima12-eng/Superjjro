import streamlit as st

# Configuração para esconder menus e focar no App
st.set_page_config(page_title="SUPER JJ SNIPER", page_icon="🎯", layout="centered")

# --- CSS PROFISSIONAL PARA CELULAR ---
st.markdown("""
    <style>
    /* Esconder cabeçalhos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container principal */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    
    /* Estilo dos botões de números */
    .stButton > button {
        width: 100%;
        height: 60px !important;
        border-radius: 10px;
        font-size: 20px !important;
        font-weight: bold;
        margin-bottom: 5px;
        border: 1px solid #444;
    }
    
    /* Botão Zero */
    .zero-btn > div > div > button {
        background-color: #008000 !important;
        color: white !important;
        height: 70px !important;
    }

    /* Cores dos alertas */
    .stAlert {
        border-radius: 15px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SEQUÊNCIA E REGRAS ---
RODA = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
VERMELHOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

# Inicialização
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'mapa_puxadas' not in st.session_state:
    st.session_state.mapa_puxadas = {}
if 'operacao' not in st.session_state:
    st.session_state.operacao = {"ativo": False, "alvos": [], "ciclo": 1, "msg": "", "cor": "info"}

def obter_vizinhos(num, qtd=2):
    idx = RODA.index(num)
    return [RODA[(idx + i) % 37] for i in range(-qtd, qtd + 1)]

def registrar(num):
    hist = st.session_state.historico
    op = st.session_state.operacao
    
    if op["ativo"]:
        if num in op["alvos"] or num == 0:
            st.toast(f"✅ GREEN NO {num}!", icon="✅")
            st.session_state.operacao["ativo"] = False
        else:
            if op["ciclo"] < 3:
                st.session_state.operacao["ciclo"] += 1
            else:
                st.toast(f"❌ LOSS NO {num}", icon="❌")
                st.session_state.operacao["ativo"] = False

    if len(hist) > 0:
        ultimo = hist[-1]
        if ultimo not in st.session_state.mapa_puxadas:
            st.session_state.mapa_puxadas[ultimo] = []
        st.session_state.mapa_puxadas[ultimo].append(num)
    
    st.session_state.historico.append(num)
    
    # Analisar Padrão
    if not st.session_state.operacao["ativo"]:
        # 1. Repetição
        if hist[-10:].count(num) >= 2:
            st.session_state.operacao.update({"ativo": True, "alvos": obter_vizinhos(num), "ciclo": 1, "msg": f"🚨 REPETIÇÃO: ÁREA DO {num}", "cor": "warning"})
        # 2. Puxada
        puxados = st.session_state.mapa_puxadas.get(num, [])
        if puxados:
            mais_comum = max(set(puxados), key=puxados.count)
            if puxados.count(mais_comum) >= 2:
                st.session_state.operacao.update({"ativo": True, "alvos": obter_vizinhos(mais_comum), "ciclo": 1, "msg": f"🚨 MANIPULAÇÃO: {num} -> {mais_comum}", "cor": "error"})

# --- INTERFACE ---
st.markdown("<h3 style='text-align: center; color: white;'>SUPER JJ SNIPER</h3>", unsafe_allow_html=True)

# Alerta no topo
op = st.session_state.operacao
if op["ativo"]:
    if op["cor"] == "warning": st.warning(f"**{op['msg']}** \n\nGALE: {op['ciclo']-1}/2")
    else: st.error(f"**{op['msg']}** \n\nGALE: {op['ciclo']-1}/2")
else:
    st.info(f"Monitorando... Giros: {len(st.session_state.historico)}")

# Botão Zero Grande
st.markdown('<div class="zero-btn">', unsafe_allow_html=True)
if st.button("ZERO (0)"): 
    registrar(0)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Grid de Números 3 colunas (Ideal para Celular)
cols = st.columns(3)
for i in range(1, 37):
    col_idx = (i - 1) % 3
    cor_btn = "red" if i in VERMELHOS else "black"
    if cols[col_idx].button(f"{i}"):
        registrar(i)
        st.rerun()

st.write("---")
if st.button("🗑️ LIMPAR TUDO"):
    st.session_state.historico = []
    st.session_state.mapa_puxadas = {}
    st.session_state.operacao["ativo"] = False
    st.rerun()

if st.session_state.historico:
    st.caption(f"Últimos: {st.session_state.historico[-8:]}")

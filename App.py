import streamlit as st

# Configurações de exibição do App
st.set_page_config(page_title="SUPER JJ SNIPER", page_icon="🎯", layout="centered")

# --- CSS PARA ORGANIZAÇÃO VERTICAL (ESTILO APP PROFISSIONAL) ---
st.markdown("""
    <style>
    /* Esconde elementos desnecessários */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding-top: 1rem; background-color: #0d1117;} 

    /* Estilo dos Alertas no TOPO */
    .alerta-topo {
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
        border: 2px solid #30363d;
    }

    /* Estilo do TABULEIRO no MEIO */
    .stButton > button {
        width: 100%;
        height: 45px !important;
        border-radius: 5px;
        font-weight: bold;
        font-size: 16px !important;
        color: white !important;
    }
    
    /* Botão Zero */
    .btn-zero > div > button {
        background-color: #238636 !important;
        height: 55px !important;
        margin-bottom: 10px;
    }

    /* Cores dos Números */
    .btn-red > div > button { background-color: #da3633 !important; }
    .btn-black > div > button { background-color: #21262d !important; }

    /* Estilo do HISTÓRICO no RODAPÉ */
    .historico-rodape {
        background-color: #161b22;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #30363d;
        color: #8b949e;
        font-family: monospace;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DO SISTEMA ---
RODA = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
VERMELHOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

if 'historico' not in st.session_state: st.session_state.historico = []
if 'mapa_puxadas' not in st.session_state: st.session_state.mapa_puxadas = {}
if 'operacao' not in st.session_state: st.session_state.operacao = {"ativo": False, "alvos": [], "msg": "", "gale": 0}

def registrar(num):
    hist = st.session_state.historico
    op = st.session_state.operacao
    
    # 1. Conferência de Green
    if op["ativo"]:
        if num in op["alvos"] or num == 0:
            st.toast("🎯 GREEN!", icon="✅")
            st.session_state.operacao["ativo"] = False
        else:
            if op["gale"] < 2:
                st.session_state.operacao["gale"] += 1
            else:
                st.toast("❌ LOSS", icon="❌")
                st.session_state.operacao["ativo"] = False

    # 2. Aprendizado de Manipulação
    if len(hist) > 0:
        ult = hist[-1]
        if ult not in st.session_state.mapa_puxadas: st.session_state.mapa_puxadas[ult] = []
        st.session_state.mapa_puxadas[ult].append(num)
    
    st.session_state.historico.append(num)
    
    # 3. Gerar Novo Sinal (Se livre)
    if not st.session_state.operacao["ativo"]:
        puxados = st.session_state.mapa_puxadas.get(num, [])
        if puxados:
            mais_comum = max(set(puxados), key=puxados.count)
            if puxados.count(mais_comum) >= 2:
                idx = RODA.index(mais_comum)
                vizis = [RODA[(idx+i)%37] for i in range(-2, 3)]
                st.session_state.operacao.update({"ativo": True, "alvos": vizis, "msg": f"🚨 MANIPULAÇÃO: {num} → {mais_comum}", "gale": 0})

# --- INTERFACE: 1. TOPO (ATUALIZAÇÕES E SINAIS) ---
st.markdown("<h2 style='text-align: center; color: #58a6ff;'>SUPER JJ SNIPER</h2>", unsafe_allow_html=True)

op = st.session_state.operacao
if op["ativo"]:
    st.warning(f"**{op['msg']}**  \n🎯 Jogue no {op['alvos'][2]} e +2 vizinhos cada lado.  \n⚠️ Gale: {op['gale']}/2")
else:
    st.info("🔍 MONITORANDO... AGUARDANDO PADRÃO DE MANIPULAÇÃO.")

# --- INTERFACE: 2. MEIO (TABELA DE NÚMEROS) ---
# Botão Zero
st.markdown('<div class="btn-zero">', unsafe_allow_html=True)
if st.button("ZERO - 0"): 
    registrar(0); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Grid 3 Colunas (Formato Mesa)
cols = st.columns(3)
for i in range(1, 37):
    col_idx = (i - 1) % 3
    cor_class = "btn-red" if i in VERMELHOS else "btn-black"
    st.markdown(f'<div class="{cor_class}">', unsafe_allow_html=True)
    if cols[col_idx].button(str(i)):
        registrar(i); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- INTERFACE: 3. BAIXO (HISTÓRICO) ---
st.markdown("<br>", unsafe_allow_html=True)
if st.session_state.historico:
    ultimos = " | ".join([f"{n:02d}" for n in st.session_state.historico[-10:]])
    st.markdown(f'<div class="historico-rodape">HISTÓRICO: {ultimos}</div>', unsafe_allow_html=True)

if st.button("🗑️ REINICIAR MESA"):
    st.session_state.clear(); st.rerun()
    

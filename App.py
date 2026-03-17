import streamlit as st

st.set_page_config(page_title="SUPER JJ CASINO", page_icon="🎰", layout="wide")

# --- CSS ESTILO CASSINO REAL ---
st.markdown("""
    <style>
    /* Esconder tudo do Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 1rem; background-color: #064e3b;} /* Verde Feltro de Cassino */
    
    /* Grade da Roleta (3 colunas horizontais) */
    .roulette-grid {
        display: grid;
        grid-template-columns: repeat(12, 1fr);
        gap: 4px;
        margin-top: 10px;
    }
    
    /* Botões Gerais */
    .stButton > button {
        width: 100%;
        height: 50px !important;
        border-radius: 4px;
        font-size: 16px !important;
        font-weight: bold;
        color: white !important;
        border: 1px solid #ffffff33;
    }
    
    /* Cores Específicas */
    .btn-red > div > button { background-color: #be123c !important; } /* Vermelho */
    .btn-black > div > button { background-color: #1a1a1a !important; } /* Preto */
    .btn-zero > div > button { background-color: #15803d !important; height: 60px !important; } /* Zero Verde */
    
    /* Alerta de Sniper */
    .stAlert { border: 2px solid #fbbf24; background-color: #1e293b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA ---
RODA = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
VERMELHOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

if 'historico' not in st.session_state: st.session_state.historico = []
if 'mapa_puxadas' not in st.session_state: st.session_state.mapa_puxadas = {}
if 'operacao' not in st.session_state: st.session_state.operacao = {"ativo": False, "alvos": [], "msg": ""}

def registrar(num):
    hist = st.session_state.historico
    if st.session_state.operacao["ativo"]:
        if num in st.session_state.operacao["alvos"] or num == 0:
            st.toast(f"🍀 GREEN!", icon="✅")
            st.session_state.operacao["ativo"] = False
    if len(hist) > 0:
        ult = hist[-1]
        if ult not in st.session_state.mapa_puxadas: st.session_state.mapa_puxadas[ult] = []
        st.session_state.mapa_puxadas[ult].append(num)
    st.session_state.historico.append(num)
    # Analisar Puxada
    puxados = st.session_state.mapa_puxadas.get(num, [])
    if puxados:
        mais_comum = max(set(puxados), key=puxados.count)
        if puxados.count(mais_comum) >= 2:
            idx = RODA.index(mais_comum)
            vizis = [RODA[(idx+i)%37] for i in range(-2, 3)]
            st.session_state.operacao.update({"ativo": True, "alvos": vizis, "msg": f"🚨 MANIPULAÇÃO: {num} → {mais_comum}"})

# --- INTERFACE ---
st.markdown("<h2 style='text-align: center; color: #fbbf24;'>SUPER JJ CASINO SNIPER</h2>", unsafe_allow_html=True)

if st.session_state.operacao["ativo"]:
    st.warning(f"**{st.session_state.operacao['msg']}**")

# Botão Zero (Cobre a largura toda)
st.markdown('<div class="btn-zero">', unsafe_allow_html=True)
if st.button("0"): registrar(0); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Criando as 3 fileiras clássicas (3, 2, 1 / 6, 5, 4...)
for r in [3, 2, 1]:
    cols = st.columns(12)
    for c in range(12):
        num = (c * 3) + r
        cor_class = "btn-red" if num in VERMELHOS else "btn-black"
        st.markdown(f'<div class="{cor_class}">', unsafe_allow_html=True)
        if cols[c].button(str(num)):
            registrar(num)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
if st.button("🗑️ REINICIAR MESA"):
    st.session_state.clear()
    st.rerun()
                         

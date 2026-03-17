import streamlit as st

st.set_page_config(page_title="SUPER JJ SNIPER", layout="centered")

# --- CSS PARA FORÇAR 3 COLUNAS NO CELULAR ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {padding: 1rem; background-color: #0d1117;}
    
    /* Força os botões a ficarem lado a lado mesmo no celular */
    div[data-testid="column"] {
        width: 31% !important;
        flex: 1 1 31% !important;
        min-width: 31% !important;
        margin: 1%;
    }
    
    .stButton > button {
        width: 100%;
        height: 55px !important;
        border-radius: 8px;
        font-weight: bold;
        font-size: 18px !important;
    }
    
    .btn-red > div > button { background-color: #da3633 !important; }
    .btn-black > div > button { background-color: #21262d !important; }
    .btn-zero > div > button { background-color: #238636 !important; height: 65px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA ---
VERMELHOS = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]

if 'historico' not in st.session_state: st.session_state.historico = []

# --- INTERFACE ---
st.markdown("<h2 style='text-align: center; color: #58a6ff;'>SUPER JJ SNIPER</h2>", unsafe_allow_html=True)

# Botão Zero
st.markdown('<div class="btn-zero">', unsafe_allow_html=True)
if st.button("ZERO - 0"): 
    st.session_state.historico.append(0)
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Grid de Números (Lado a Lado)
for row in range(0, 12):
    cols = st.columns(3)
    for col_idx in range(3):
        num = (row * 3) + col_idx + 1
        cor_class = "btn-red" if num in VERMELHOS else "btn-black"
        with cols[col_idx]:
            st.markdown(f'<div class="{cor_class}">', unsafe_allow_html=True)
            if st.button(str(num)):
                st.session_state.historico.append(num)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# Histórico no Final
if st.session_state.historico:
    st.write("---")
    st.write(f"Histórico: {st.session_state.historico[-10:]}")
    

import streamlit as st
import pandas as pd

# Configuração da Página para parecer um App Nativo
st.set_page_config(page_title="SUPER JJ SNIPER", page_icon="🎯", layout="centered")

# CSS para deixar os botões com cara de roleta no celular
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #333;
        color: white;
        font-weight: bold;
    }
    .stButton > button:active { background-color: #555; }
    </style>
    """, unsafe_allow_html=True)

# Sequência real da Roleta Europeia
RODA = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
VERMELHOS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

# Inicialização da Memória do App
if 'historico' not in st.session_state:
    st.session_state.historico = []
if 'mapa_puxadas' not in st.session_state:
    st.session_state.mapa_puxadas = {}
if 'operacao' not in st.session_state:
    st.session_state.operacao = {"ativo": False, "alvos": [], "ciclo": 1, "msg": ""}

def obter_vizinhos(num, qtd=2):
    if num not in RODA: return []
    idx = RODA.index(num)
    return [RODA[(idx + i) % 37] for i in range(-qtd, qtd + 1)]

def registrar_numero(num):
    hist = st.session_state.historico
    
    # Se estiver em operação, verifica Green/Loss
    if st.session_state.operacao["ativo"]:
        if num in st.session_state.operacao["alvos"] or num == 0:
            st.toast(f"✅ GREEN NO {num}!", icon="✅")
            st.session_state.operacao["ativo"] = False
        else:
            if st.session_state.operacao["ciclo"] < 3:
                st.session_state.operacao["ciclo"] += 1
            else:
                st.toast(f"❌ LOSS NO {num}", icon="❌")
                st.session_state.operacao["ativo"] = False

    # Motor de Aprendizado
    if len(hist) > 0:
        ultimo = hist[-1]
        if ultimo not in st.session_state.mapa_puxadas:
            st.session_state.mapa_puxadas[ultimo] = []
        st.session_state.mapa_puxadas[ultimo].append(num)
    
    st.session_state.historico.append(num)
    
    # Analisa Próxima Jogada (Se não estiver em operação)
    if not st.session_state.operacao["ativo"]:
        analisar_puxada(num)

def analisar_puxada(num_atual):
    hist = st.session_state.historico
    # 1. Repetição
    if hist[-10:].count(num_atual) >= 2:
        st.session_state.operacao.update({
            "ativo": True, "alvos": obter_vizinhos(num_atual), "ciclo": 1,
            "msg": f"🚨 REPETIÇÃO DETECTADA: VIZINHOS DO {num_atual}"
        })
    # 2. Puxada Aprendida
    puxados = st.session_state.mapa_puxadas.get(num_atual, [])
    if puxados:
        mais_comum = max(set(puxados), key=puxados.count)
        if puxados.count(mais_comum) >= 2:
            st.session_state.operacao.update({
                "ativo": True, "alvos": obter_vizinhos(mais_comum), "ciclo": 1,
                "msg": f"🚨 MANIPULAÇÃO: {num_atual} PUXA {mais_comum}"
            })

# --- INTERFACE DO APP ---
st.title("🎯 SUPER JJ SNIPER")

# Painel de Alerta Dinâmico
if st.session_state.operacao["ativo"]:
    st.warning(f"{st.session_state.operacao['msg']} \n\n GALE: {st.session_state.operacao['ciclo']-1}/2")
else:
    st.success(f"MONITORANDO... GIROS: {len(st.session_state.historico)}")

# Tabuleiro de Botões (3 colunas para celular)
cols = st.columns(3)
if cols[1].button("0", type="primary", use_container_width=True):
    registrar_numero(0)
    st.rerun()

for i in range(1, 37):
    col_idx = (i - 1) % 3
    label = str(i)
    if cols[col_idx].button(label, use_container_width=True):
        registrar_numero(i)
        st.rerun()

st.divider()
if st.button("🗑️ LIMPAR MEMÓRIA DO ROBÔ"):
    st.session_state.historico = []
    st.session_state.mapa_puxadas = {}
    st.session_state.operacao["ativo"] = False
    st.rerun()

# Log de Histórico
if st.session_state.historico:
    st.write("Últimos Giros:", st.session_state.historico[-10:])

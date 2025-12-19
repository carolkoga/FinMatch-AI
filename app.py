import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

from modules.generator import gerar_dados
from modules.matcher import conciliar_dados
from modules.database import salvar_auditoria, ler_historico

st.set_page_config(
    page_title="FinMatch AI - Auditoria", 
    page_icon="🛡️", 
    layout="wide"
)

st.title("🛡️ FinMatch AI: Reconciliação Bancária Inteligente")
st.markdown("""
Esta ferramenta utiliza **IA Generativa** para identificar discrepâncias financeiras e sugerir conciliações entre o extrato bancário e o sistema interno.
---
""")

st.sidebar.header("⚙️ Configurações")
n_transacoes = st.sidebar.slider("Número de transações para teste", 5, 50, 10)

if st.sidebar.button("🎲 Gerar Novos Dados"):
    if 'resultado' in st.session_state:
        del st.session_state['resultado']
    
    df_sis, df_bco = gerar_dados(n_transacoes)
    
    st.session_state['df_sis'] = df_sis
    st.session_state['df_bco'] = df_bco
    st.sidebar.success(f"{n_transacoes} transações geradas!")

col1, col2 = st.columns(2)

if 'df_sis' in st.session_state and 'df_bco' in st.session_state:
    with col1:
        st.subheader("🏢 Sistema ERP (Esperado)")
        st.dataframe(st.session_state['df_sis'], width='stretch')
    
    with col2:
        st.subheader("🏦 Extrato Bancário (Real)")
        st.dataframe(st.session_state['df_bco'], width='stretch')

    st.divider()
    if st.button("🚀 Iniciar Conciliação com IA"):
        with st.spinner("O Gemini está analisando as divergências e cruzando dados..."):
            resultado_df = conciliar_dados(st.session_state['df_bco'], st.session_state['df_sis'])
            st.session_state['resultado'] = resultado_df

    if 'resultado' in st.session_state:
        st.header("📊 Resultado da Auditoria")
        # Debug visual temporário
        st.subheader("🔍 Inspeção de Debug (Somente Desenvolvedor)")
        st.write("Colunas detectadas:", list(st.session_state['resultado'].columns))
        st.json(st.session_state['resultado'].iloc[0].to_dict())
        
        def colorir_metodo(val):
            color = '#90EE90' if 'Heurística' in str(val) else '#FFD700'
            return f'background-color: {color}; color: black'

        st.dataframe(
            st.session_state['resultado'].style.map(colorir_metodo, subset=['Metodo']), 
            width="stretch" 
        )
        
        # Botão de Salvar
        if st.button("💾 Salvar Auditoria no Banco de Dados (Cloud)"):
            with st.spinner("Conectando ao Neon PostgreSQL..."):
                sucesso = salvar_auditoria(st.session_state['resultado'])
                if sucesso:
                    st.success("✅ Dados persistidos na nuvem!")
                    st.session_state['historico'] = ler_historico()
                else:
                    st.error("❌ Falha ao salvar no banco.")

    st.divider()
    st.subheader("📜 Histórico de Auditoria (Cloud DB)")

    if 'historico' not in st.session_state:
        st.session_state['historico'] = ler_historico()

    col_hist1, col_hist2 = st.columns([1, 4])
    with col_hist1:
        if st.button("🔄 Atualizar Histórico"):
            st.session_state['historico'] = ler_historico()

    if st.session_state.get('historico'):
        df_hist = pd.DataFrame(st.session_state['historico'])
        st.dataframe(df_hist, uwidth='stretch')
    else:
        st.info("Nenhum histórico encontrado no banco de dados.")
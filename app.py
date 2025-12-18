import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from modules.generator import gerar_dados
from modules.matcher import conciliar_dados

load_dotenv()

st.title("🛡️ FinMatch AI: Reconciliação Bancária Inteligente")
st.markdown("""
Esta ferramenta utiliza **IA Generativa** para identificar discrepâncias financeiras e sugerir conciliações entre o extrato bancário e o sistema interno.
""")

st.sidebar.header("Configurações")
n_transacoes = st.sidebar.slider("Número de transações para teste", 5, 50, 10)

if st.sidebar.button("🎲 Gerar Novos Dados"):
    df_sis, df_bco = gerar_dados(n_transacoes)
    st.session_state['df_sis'] = df_sis
    st.session_state['df_bco'] = df_bco
    st.sidebar.success("Dados gerados!")

col1, col2 = st.columns(2)

if 'df_sis' in st.session_state:
    with col1:
        st.subheader("🏢 Sistema ERP (Esperado)")
        st.dataframe(st.session_state['df_sis'], use_container_width=True)
    
    with col2:
        st.subheader("🏦 Extrato Bancário (Real)")
        st.dataframe(st.session_state['df_bco'], use_container_width=True)

    if st.button("🚀 Iniciar Conciliação com IA"):
        with st.spinner("O Gemini está analisando as divergências..."):
            resultado = conciliar_dados(st.session_state['df_bco'], st.session_state['df_sis'])
            
            st.divider()
            st.header("📊 Resultado da Auditoria")

            st.dataframe(resultado, use_container_width=True)
            st.success("Processamento concluído!")



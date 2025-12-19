import os
from dotenv import load_dotenv
import pandas as pd
from modules.llm_client import get_client

load_dotenv()

def conciliar_dados(df_banco, df_sistema):
    """Cruzar os dados do banco com o sistema."""
    resultados = []
    valor_atual = linha_banco['Valor_Extrato']

    for index, linha_banco in df_banco.iterrows():
        match_exato = df_sistema[df_sistema['Valor_Previsto'] == linha_banco['Valor_Extrato']]

        if not match_exato.empty:
            res={
                "ID_Transacao": linha_banco['ID_Transacao'],
                "Valor": valor_atual,
                "status": "✅ Conciliado",
                "Metodo": "Heurística (Valor Exato)", 
                "Usou_IA": False,
                "detalhes": f"Correspondência encontrada para o título {match_exato.iloc[0]['ID_Titulo']}"}

        else:
            #não encontrou valor, encamiha para o AI analisar.

            print(f"🤖 Chamando IA para: {linha_banco['Descricao_Banco']}")

            candidatos = df_sistema.to_dict()

            analise_ai = analisar_com_ai(linha_banco, candidatos)

            res = {
                "ID_Transacao": linha_banco['ID_Transacao'],
                "Valor": valor_atual,
                "status": "⚠️ Analisado por IA",
                "metodo": "Inteligência Artificial",
                "Usou_IA": True,
                "detalhes": analise_ai}
            
        resultados.append(res)
    return pd.DataFrame(resultados)

def analisar_com_ai(transacao_banco, candidatos_sistema):
    """Usa o Gemini 2.5 Flash para analisar a transação."""
    client = get_client()
    prompt = f"""
        Como um auditor financeiro, analise se esta transação do banco:
    {transacao_banco['Descricao_Banco']} no valor de {transacao_banco['Valor_Extrato']}
    
    Pode ser referente a um destes títulos do sistema:
    {candidatos_sistema}
    
    Responda de forma curta: Se encontrou um match, diga qual o ID_Titulo e o porquê (ex: variação de taxa). 
    Se não encontrou, diga que não há correspondência.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt)
        return response.text
    except Exception as e:
        return f"Erro na AI: {e}"

if __name__ == '__main__':
    from modules.generator import gerar_dados
    df_sis, df_bco = gerar_dados(5)
    df_final = conciliar_dados(df_bco, df_sis)
    print(df_final)
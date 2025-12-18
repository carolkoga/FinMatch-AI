import pandas as pd
from faker import Faker
import random
from datetime import timedelta

fake = Faker('pt_BR')

def gerar_dados(n_linhas=20):
    """Gerar dois DataFrames simulando um cenário de conciliação bancária.
    n_linhas: Quantidade de títulos a srem criados no sistema."""

    dados_sistema=[]
    dados_banco=[]

    print(f'🎲 Gerando {n_linhas} transações sintéticas...')

    for i in range (n_linhas):
        valor_base = round(random.uniform(100.00, 500.00), 2)
        data_vencimento = fake.date_this_month()
        empresa_cliente = fake.company()
        id_titulo = f"TIT-{1000 + i}"

        dados_sistema.append({
            "ID_Titulo": id_titulo,
            "Data_Vencimento": data_vencimento,
            "Valor_Previsto": valor_base,
            "Cliente": empresa_cliente,
            "Descricao": f"Fatura {fake.bs()}"})
        
        #simula o pagaento no banco com ruídos.
        #geração de pendencias de clientes (80% de chance d cliente pagar)

        if random.random() < 0.80:
            #introduzindo anomalias para teste de AI e variação de data (pagamntos caindo entre 0 e 3 dias.)
            dias_atraso = random.randint(0, 3)
            data_pagamento = data_vencimento + timedelta(days=dias_atraso)

            #variação de valor (ex:taxa de banco)
            valor_final = valor_base
            if random.random() < 0.3:
                taxa = 1.50
                valor_final = round(valor_base - taxa, 2)

            dados_banco.append({
                "ID_Transacao": f"TRX-{5000 + i}",
                "Data_Extrato": data_pagamento,
                "Valor_Extrato": valor_final,
                # A descrição no banco costuma ser ruim/curta
                "Descricao_Banco": f"PGTO {empresa_cliente.split()[0].upper()} DOC {id_titulo[-4:]}"})
            
    df_sistema = pd.DataFrame(dados_sistema)
    df_banco = pd.DataFrame(dados_banco)
    return df_sistema, df_banco

if __name__ == "__main__":
    df_sis, df_bco = gerar_dados(20)

    print("\n--- 🏢 SISTEMA INTERNO (O que a empresa espera) ---")
    print(df_sis[['ID_Titulo', 'Data_Vencimento', 'Valor_Previsto', 'Cliente']].head())
    
    print("\n--- 🏦 EXTRATO BANCÁRIO (O que realmente aconteceu) ---")
    print(df_bco[['ID_Transacao', 'Data_Extrato', 'Valor_Extrato', 'Descricao_Banco']].head())
    
    print("\n✅ Dados gerados com sucesso!")

import os
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor, execute_values
from dotenv import load_dotenv

load_dotenv()

# Configuração do limite de linhas (Rolling Logs)
LIMITE_REGISTROS = 700

def get_db():
    """Estabelece conexão segura com Neon Postgres"""
    try:
        url = os.getenv("DATABASE_URL")
        if not url:
            print("❌ Erro: DATABASE_URL não encontrada no arquivo .env")
            return None
        conn = psycopg2.connect(url)
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

def limpeza_db(cursor):
    """Mantém apenas os últimos X registros para economizar espaço"""
    try:
        query = """
            DELETE FROM audit_logs 
            WHERE id NOT IN (
                SELECT id FROM audit_logs 
                ORDER BY data_conciliacao DESC 
                LIMIT %s
            )
        """
        cursor.execute(query, (LIMITE_REGISTROS,))
        print(f"🧹 Limpeza realizada: Mantendo apenas os últimos {LIMITE_REGISTROS} logs.")
    except Exception as e:
        print(f"⚠️ Erro na limpeza do banco: {e}")

def salvar_auditoria(df_resultados):
    """Salva o DataFrame no banco com mapeamento dinâmico de colunas"""
    
    # --- DEBUG ---
    print("\n--- 🕵️ DEBUG DO BANCO DE DADOS ---")
    print(f"Colunas recebidas: {list(df_resultados.columns)}")
    
    # 1. Normalização: Cria cópia para não alterar o original
    df_limpo = df_resultados.copy()
    
    # Mapeamento de sinônimos (Case Insensitive)
    mapeamento = {
        'id_transacao': ['id', 'id_transacao', 'id_transação', 'id transacao'],
        'valor': ['valor', 'valor_total', 'quantia', 'amount', 'valor_extrato'],
        'status': ['status', 'resultado', 'situação'],
        'metodo': ['metodo', 'método', 'conciliação'],
        'usou_ia': ['ia', 'usou_ia', 'ia_utilizada'],
        'detalhes': ['detalhes', 'justificativa', 'rationale']
    }

    # Função interna auxiliar para encontrar a coluna correta
    def encontrar_coluna(df, nomes_possiveis):
        for col in df.columns:
            if col.lower().strip() in nomes_possiveis:
                return col
        return None

    try:
        # Tenta descobrir os nomes reais das colunas no DataFrame
        col_id = encontrar_coluna(df_limpo, mapeamento['id_transacao'])
        col_valor = encontrar_coluna(df_limpo, mapeamento['valor'])
        col_status = encontrar_coluna(df_limpo, mapeamento['status'])
        col_metodo = encontrar_coluna(df_limpo, mapeamento['metodo'])
        col_ia = encontrar_coluna(df_limpo, mapeamento['usou_ia'])
        col_detalhes = encontrar_coluna(df_limpo, mapeamento['detalhes'])

        # Validação simples
        if not col_valor:
            print("⚠️ Aviso: Coluna de VALOR não encontrada. Será salvo como 0.0")

        # 2. Conexão e Inserção
        conn = get_db()
        if not conn: return False
        
        with conn:
            with conn.cursor() as cur:
                dados_para_inserir = []
                
                # Loop corrigido (com indentação e dois pontos)
                for _, row in df_limpo.iterrows():
                    val_id = str(row[col_id]) if col_id else "N/A"
                    val_valor = float(row[col_valor]) if col_valor else 0.0
                    val_status = str(row[col_status]) if col_status else "Erro"
                    val_metodo = str(row[col_metodo]) if col_metodo else "N/A"
                    val_ia = bool(row[col_ia]) if col_ia else False
                    val_detalhes = str(row[col_detalhes]) if col_detalhes else ""

                    dados_para_inserir.append((
                        val_id, val_valor, val_status, 
                        val_metodo, val_ia, val_detalhes
                    ))
                
                query = """
                    INSERT INTO audit_logs (id_transacao, valor, status, metodo, usou_ia, detalhes)
                    VALUES %s
                """
                execute_values(cur, query, dados_para_inserir)
                limpeza_db(cur)
                
        print("✅ Dados salvos com sucesso!")
        return True

    except Exception as e:
        print(f"❌ ERRO TÉCNICO NO DB: {e}")
        return False
    finally:
        # Fecha a conexão se ela foi aberta
        if 'conn' in locals() and conn: conn.close()

def ler_historico():
    """Lê os últimos 50 registros de auditorias"""
    conn = get_db()
    if not conn: return []
    
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM audit_logs ORDER BY data_conciliacao DESC LIMIT 50")
                return cur.fetchall()
    except Exception as e:
        print(f"Erro ao ler histórico: {e}")
        return []
    finally:
        if conn: conn.close()

# --- ÁREA DE TESTE (Só roda via terminal direto) ---
if __name__ == "__main__":
    print("\n🧪 INICIANDO TESTE DE CONEXÃO E INSERÇÃO...")
    
    # 1. Cria um DataFrame falso para testar
    print("1. Criando dados falsos (Mock)...")
    dados_teste = pd.DataFrame([{
        "ID_Transacao": "TESTE_CONSOLE_001",
        "Valor": 99.90,
        "Status": "Teste",
        "Metodo": "Script Manual",
        "Usou_IA": False,
        "Detalhes": "Inserção direta via database.py"
    }])
    
    # 2. Tenta salvar
    print("2. Tentando salvar no Neon...")
    sucesso = salvar_auditoria(dados_teste)
    
    # 3. Verifica se salvou
    if sucesso:
        print("\n3. Lendo histórico para confirmar...")
        historico = ler_historico()
        if historico and historico[0]['id_transacao'] == "TESTE_CONSOLE_001":
            print(f"✅ SUCESSO TOTAL! Registro encontrado: {historico[0]}")
        else:
            print(f"⚠️ Salvou, mas o último registro é diferente: {historico[0] if historico else 'Vazio'}")
    else:
        print("❌ Falha no teste.")
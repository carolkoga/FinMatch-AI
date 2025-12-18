import os
import psycopg2
from psycopg2.extras import RealDictCursor, execute_values
from dotenv import load_dotenv

load_dotenv()

# Configuração do limite de linhas
LIMITE_REGISTROS = 700

def get_db():
    """Estabelece conexão segura com Neon Postgres"""
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

def limpeza_db(cursor):
    """Mantém apenas os últimos X registros (Rolling Logs)"""
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
    conn = get_db()
    if not conn:
        return False

    try:
        with conn:
            with conn.cursor() as cur:
                dados_para_inserir = [
                    (
                        str(row['ID_Transacao']), 
                        float(row['Valor']), 
                        str(row['Status']), 
                        str(row['Metodo']), 
                        bool(row['Usou_IA']), 
                        str(row['Detalhes'])
                    )
                    for _, row in df_resultados.iterrows()
                ]
                
                query = """
                    INSERT INTO audit_logs (id_transacao, valor, status, metodo, usou_ia, detalhes)
                    VALUES %s
                """
                
                execute_values(cur, query, dados_para_inserir)

                limpeza_db(cur)
                
        print("✅ Dados de auditoria salvos no Neon com sucesso!")
        return True
    
    except Exception as e:
        print(f"❌ Erro ao salvar/limpar banco: {e}")
        return False
    finally:
        if conn:
            conn.close()

def ler_historico():
    """Lê os últimos 50 registros de auditorias para exibição"""
    conn = get_db()
    if not conn:
        return []
    
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM audit_logs ORDER BY data_conciliacao DESC LIMIT 50")
                rows = cur.fetchall()
                return rows
    except Exception as e:
        print(f"Erro ao ler histórico: {e}")
        return []
    finally:
        if conn:
            conn.close()
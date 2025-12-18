import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()
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
    """Mantém apenas os últimos 700 registros"""
    try:
        cursor.execute(f"""
        DELETE FROM audit_logs WHERE id NOT IN (SELECT id FROM audit_logs ORDEM BY data_conciliacao DESC LIMIT {LIMITE_REGISTROS})
        """)

        print(f"🧹 Limpeza realizada: Mantendo apenas os últimos {LIMITE_REGISTROS} logs.")

    except Exception as e:
        print(f"⚠️ Erro na limpeza do banco: {e}")

def salvar_auditoria(df_resultados):
    conn = get_db()
    if not conn:
        return False

    try:
        cur = conn.cursor()
        for _, row in df_resultado.iterrows():
            cur.execute("""
            INSERT INTO audit_logs (id_transacao, valor, status, metodo, usou_ia, detalhes)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (row['ID_Transacao'], row['Valor'], row['Status'], 
                row['Metodo'], bool(row['Usou_IA']), row['Detalhes']))

        limpeza_db(cur)
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Dados de auditoria salvos no Neon com sucesso!")
        return True
   
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def ler_historico():
    """Lê os últimos 50 registros de auditorias"""
    conn = get_db()
    if not conn:
        return[]
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.excute("SELECT * FROM audit_logs ORDER BY data_conciliacao DESC LIMIT 50")
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Erro ao ler histórico: {e}")
        return []
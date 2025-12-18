import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    """Estabelece conexao com banco de dados"""

    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conecta: {e}")
        return None
    
if __name__ == "__main__":
    print("🚀 Tentando conectar ao banco de dados...")
    conexao=connect_db()

    if conexao:
        print("✅ Conexão estabelecida com sucesso!")
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()
            print(f"✔️ Versão do PostgreSQL: {db_version[0]}")
            cursor.close()
        except psycopg2.Error as e:
            print(f"⚠️ Erro ao executar consulta: {e}")
        finally:
            conexao.close()
            print("🔌 Conexão fechada.")
    else:
        print("👎 Não foi possível estabelecer a conexão. Verifique o erro acima e seu arquivo .env.")

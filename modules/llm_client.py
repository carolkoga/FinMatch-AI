import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_client():
        """Retorna o cliente configurado para o Gemini."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError ("Gemini Key not found.")
        return genai.Client(api_key=api_key)

def testar_conexao():
    try:
        client = get_client()
        response = client.models.generate_content(model="gemini-2.5-flash", contents="Diga: 'FinMatch conectado com Sucesso!'")
        return f"✅ Sucesso! Resposta: {response.text}"
    except Exception as e:
        return f"❌ Erro na função de conexão: {e}"

if __name__=='__main__':
    print("Testando conexão com Gemini 2.5...")
    print(testar_conexao())
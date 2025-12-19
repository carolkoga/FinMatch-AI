# 🛡️ FinMatch AI - Conciliação Financeira Inteligente

> **Automated Financial Reconciliation System powered by Gemini AI & PostgreSQL**

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Docker](https://img.shields.io/badge/Docker-Container-blue?logo=docker)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red?logo=streamlit)
![Gemini AI](https://img.shields.io/badge/AI-Google_Gemini-orange?logo=google)
![PostgreSQL](https://img.shields.io/badge/Database-Neon_Postgres-336791?logo=postgresql)

## 📋 Sobre o Projeto

O **FinMatch AI** é uma solução de Engenharia de Dados desenvolvida para automatizar o processo crítico de conciliação financeira entre extratos bancários e registros de sistemas ERP.

Diferente de sistemas tradicionais baseados apenas em regras rígidas, este projeto utiliza uma **Arquitetura Híbrida**:
1.  **Camada Heurística (Racional):** Identifica correspondências exatas de valor e ID instantaneamente.
2.  **Camada de IA (Cognitiva):** Utiliza LLMs (Google Gemini 1.5 Flash) para analisar discrepâncias complexas, variações de taxas, erros de digitação e descrições semânticas, atuando como um "Auditor Digital".

Os resultados são persistidos em um banco de dados **PostgreSQL (Neon)** para fins de auditoria e conformidade.

---

## 🚀 Arquitetura e Tecnologias

O projeto foi construído seguindo princípios de **Microsserviços** e **Containerização**, garantindo isolamento e reprodutibilidade.

* **Frontend:** Streamlit (Interface Interativa para upload e validação).
* **Core Engine:** Python + Pandas (Processamento de dados e pipelines ETL).
* **Inteligência Artificial:** Google Gemini 2.5 Flash (SDK `google-genai`).
* **Persistência:** PostgreSQL via Neon Serverless (Armazenamento de logs de auditoria).
* **Infraestrutura:** Docker & Docker Compose (Orquestração de ambiente).

---

## 🛠️ Estrutura do Projeto

```bash
FinMatch-AI/
├── modules/
│   ├── generator.py      # Gerador de dados sintéticos para testes de stress
│   ├── matcher.py        # Motor de conciliação (Lógica Híbrida + IA)
│   ├── database.py       # Camada de persistência e conexão segura (Postgres)
│   └── llm_client.py     # Cliente de conexão com a API do Gemini
├── app.py                # Aplicação principal (Streamlit)
├── Dockerfile            # Receita da imagem do container
├── docker-compose.yml    # Orquestração do serviço e volumes
├── requirements.txt      # Dependências do Python
└── .env                  # Variáveis de ambiente (Segurança)

```

---

## ⚙️ Instalação e Execução

### Pré-requisitos

* [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado.
* Uma chave de API do [Google Gemini](https://aistudio.google.com/).
* Uma string de conexão do [Neon Database](https://neon.tech/).

### 1. Clonar o Repositório

```bash
git clone [https://github.com/carolkoga/FinMatch-AI.git]
cd FinMatch-AI

```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e preencha com suas credenciais. **Este arquivo é ignorado pelo Git por segurança.**

```ini
# Exemplo de .env
GOOGLE_API_KEY="sua_chave_do_gemini_aqui"
DATABASE_URL="postgres://usuario:senha@endpoint.neon.tech/neondb?sslmode=require"

```

### 3. Executar com Docker (Recomendado)

Para subir o ambiente completo de forma isolada:

```bash
docker-compose up --build

```

O sistema estará disponível em: **http://localhost:8501**

> **Nota:** Graças à configuração de *Volumes* no Docker, qualquer alteração no código local reflete instantaneamente no container, facilitando o desenvolvimento.

---

## 🛡️ Destaques de Segurança & Engenharia

* **Isolamento de Ambiente:** O uso do Docker garante que a aplicação rode em um ambiente Linux controlado (`python:3.11-slim`), livre de conflitos de dependências do host.
* **Sanitização de Dados:** O pipeline de ingestão no `database.py` normaliza nomes de colunas e tipos de dados para prevenir erros de injeção e inconsistência no banco SQL.
* **Gestão de Segredos:** Nenhuma credencial é "hardcoded". Todas as chaves sensíveis são injetadas via variáveis de ambiente (`.env`) em tempo de execução.
* **Logs de Auditoria:** Cada decisão tomada pela IA é registrada no banco de dados com data, status e a justificativa gerada pelo modelo, permitindo rastreabilidade total (Audit Trail).

---

## 🧪 Como Testar

1. Acesse a interface web.
2. Utilize o botão lateral para **"Gerar Dados Sintéticos"**.
3. O sistema criará transações no "Banco" e no "Sistema Interno" com divergências intencionais.
4. O Matcher tentará conciliar automaticamente. Transações complexas serão enviadas para a IA.
5. Clique em **"Salvar Auditoria"** para persistir os dados no PostgreSQL na nuvem.

---

## 📞 Contato

**Seu Nome** *Cibersegurança & Engenharia de Dados* [LinkedIn](https://www.linkedin.com/in/carolinekoga/) | [GitHub](https://github.com/carolkoga)


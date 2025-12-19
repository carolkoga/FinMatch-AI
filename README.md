# 🛡️ FinMatch AI - Reconciliação Bancária Inteligente

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![Status](https://img.shields.io/badge/Status-MVP-green)

> **Uma solução de auditoria financeira automatizada que utiliza Inteligência Artificial Generativa para identificar discrepâncias e realizar conciliação bancária complexa.**

---

## 📋 Sobre o Projeto

O **FinMatch AI** é uma ferramenta desenvolvida para resolver um dos maiores gargalos das operações financeiras: a conciliação manual de transações divergentes. 

Diferente de sistemas tradicionais que buscam apenas correspondência exata, este projeto implementa uma **Arquitetura Híbrida**:
1.  **Motor Heurístico:** Resolve casos óbvios (valores e datas exatas) com alta performance.
2.  **Agente de IA (LLM):** Atua como um auditor humano, analisando descrições vagas, variações de taxas e datas para justificar "matches" complexos.

Este projeto demonstra competências em **Engenharia de Dados**, **Integração de APIs de IA** e **Segurança de Aplicação**.

---

## 🚀 Funcionalidades Principais

* **Gerador de Dados Sintéticos (Faker):** Criação de cenários realistas de transações bancárias e registros de ERP, injetando propositalmente ruídos (taxas, atrasos, descrições diferentes) para teste de estresse.
* **Motor de Conciliação Híbrido:** Prioriza a lógica determinística (regras) para economia de custos e usa LLM (Google Gemini) apenas para exceções.
* **Trilha de Auditoria (Explainability):** Cada decisão tomada pela IA é acompanhada de uma justificativa lógica ("Rationale"), garantindo transparência no processo.
* **Dashboard Interativo:** Interface construída em Streamlit para visualização de dados e upload de arquivos.
* **Segurança:** Gerenciamento de segredos via variáveis de ambiente (`.env`).

---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.10+
* **Frontend/UI:** Streamlit
* **Manipulação de Dados:** Pandas
* **Inteligência Artificial:** Google Gemini 1.5 Flash (via `google-genai`)
* **Ambiente:** Virtualenv (`venv`)

---

## ⚙️ Como Executar Localmente

Siga os passos abaixo para rodar o projeto na sua máquina:

### 1. Clone o repositório
```bash
git clone [https://github.com/carolkoga/FinMatch-AI]
cd FinMatch-AI

```

### 2. Configure o Ambiente Virtual

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt

```

### 4. Configure as Credenciais

Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API do Google Gemini:

```env
GEMINI_API_KEY="sua_chave_aqui"

```

*(Nota: O arquivo .env é ignorado pelo Git para segurança)*

### 5. Execute a Aplicação

Para rodar o servidor Streamlit em modo local (seguro):

```bash
streamlit run app.py --server.address 127.0.0.1

```

---

## 📂 Estrutura do Projeto

```text
FinMatch-AI/
├── app.py                # Interface principal (Frontend Streamlit)
├── modules/
│   ├── generator.py      # Gera dados sintéticos (Banco vs Sistema)
│   ├── matcher.py        # Motor de conciliação (Regras + IA)
│   └── llm_client.py     # Cliente de conexão segura com a API Gemini
├── .env                  # Variáveis de ambiente (Não versionado)
├── .gitignore            # Arquivos ignorados pelo Git
├── requirements.txt      # Dependências do projeto
└── README.md             # Documentação

```

---

## 🔒 Aspectos de Cibersegurança e Infra

Embora seja um MVP, o projeto segue princípios de segurança:

* **Segregação de Credenciais:** Nenhuma chave de API é hardcoded no código fonte.
* **Loopback Restriction:** A aplicação é configurada para rodar em `127.0.0.1`, reduzindo a superfície de ataque em redes compartilhadas.
* **Sanitização de Dependências:** Uso de ambiente virtual isolado para evitar conflitos e vulnerabilidades sistêmicas.

---

## 🚧 Próximos Passos (Roadmap)

* [ ] Containerização da aplicação com **Docker**.
* [ ] Persistência de dados em banco **PostgreSQL (Neon)** usando `psycopg2`.
* [ ] Implementação de logs estruturados para monitoramento.
* [ ] Pipeline de CI/CD para deploy automático.

---

## 🤝 Autor

Desenvolvido por **Carol Koga** *Estudante de Cibersegurança & Cloud Infrastructure*

```
```

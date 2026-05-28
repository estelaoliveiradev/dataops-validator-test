# 🚀 DataOps Accounting Reconciliator (MVP)

Este é um Produto Mínimo Viável (MVP) de uma aplicação web desenvolvida para automatizar a **homologação de roteirizações contábeis**. O objetivo principal é substituir a conferência manual e visual por um pipeline de dados automatizado, garantindo integridade e agilidade na esteira de DataOps contábil.

## 🎯 Objetivos do Projeto

- **Automação de Validação:** Cruzar o Plano de Homologação (Expectativa) com o Relatório de Roteirização (Realidade).
- **Redução de Erros:** Identificar divergências de códigos de roteiro (TTs) de forma sistêmica.
- **Visualização Analítica:** Oferecer um dashboard intuitivo para tomada de decisão rápida sobre a saúde da malha contábil.
- **Processamento Eficiente:** Executar toda a engenharia de dados em memória, garantindo performance e conformidade (sem persistência temporária de arquivos).

---

## 🛠️ Tech Stack

- **Linguagem:** Python 3.10+
- **Web Framework:** Flask (Microframework)
- **Engine de Dados:** Pandas (Processamento in-memory)
- **Gestão de Dependências:** Poetry
- **Frontend:** HTML5, Tailwind CSS e FontAwesome (UI responsiva)
- **Gráficos:** Plotly Express
- **Servidor WSGI:** Waitress (Otimizado para Windows)

---

## 📋 Lógica de Negócio (Regras de Validação)

O sistema realiza um `Left Join` entre a base de expectativa e a realidade, classificando cada cenário em:

1.  ✅ **Sensibilizado com Sucesso:** Quando o código gerado pelo sistema é idêntico ao esperado pelo time de qualidade.
2.  ⚠️ **Divergente:** Quando o cenário foi disparado, mas o código de roteiro (TT) gerado é diferente da expectativa.
3.  ❌ **Não Sensibilizado:** Quando o cenário mapeado no plano sequer foi encontrado nos dados processados (furo de cobertura).

---

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.10 ou superior instalado.
- Poetry instalado (`pip install poetry`).

### Passo a Passo

1.  **Clonar o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/conciliador-contabil.git
    cd conciliador-contabil
    ```

2.  **Instalar dependências:**
    ```bash
    poetry install
    ```

3.  **Executar a aplicação:**
    
    *Modo Desenvolvimento (Debug):*
    ```bash
    poetry run python app.py
    ```
    
    *Modo Produção (Windows/Waitress):*
    ```powershell
    # No Windows (PowerShell)
    $env:FLASK_ENV="production"
    poetry run python app.py
    ```

4.  **Acessar o sistema:**
    Abra o navegador em `http://localhost:5000` (ou `:8080` em produção).

---

## 📖 Como Usar

1.  **Download dos Templates:** Na tela inicial, baixe os modelos de Excel (`PH` e `POF`). Eles possuem as colunas exatas que o motor de processamento espera.
2.  **Preenchimento:** Preencha os dados contábeis nos arquivos Excel ou gere um CSV com o mesmo schema.
3.  **Upload:** Arraste os arquivos para os campos correspondentes na interface.
4.  **Processamento:** Clique em "Processar Conciliação".
5.  **Análise:** 
    - Verifique a **Acurácia Geral** nos cards superiores.
    - Analise a distribuição de erros no **Gráfico de Status**.
    - Consulte a tabela de **Log de Conciliação** para identificar exatamente quais cenários precisam de correção técnica.

---

## 📂 Estrutura do Projeto

```text
├── templates/
│   └── index.html      # Interface UI (Tailwind + Plotly)
├── app.py              # Backend Flask e Motor de Dados (Pandas)
├── pyproject.toml      # Configurações do Poetry e Dependências
├── poetry.lock         # Travamento de versões das bibliotecas
└── README.md           # Documentação do projeto
```

---

## 🛡️ Boas Práticas Implementadas

- **Sanitização de Dados:** O sistema limpa espaços em branco e padroniza nomes de colunas automaticamente.
- **Resiliência de Tipagem:** Converte automaticamente códigos numéricos para string, evitando falsos negativos causados pela formatação do Excel.
- **Segurança de Memória:** Processamento via `BytesIO`, evitando a criação de arquivos temporários no servidor.
- **UX Adaptativa:** Interface amigável com feedbacks visuais de erro e sucesso.

--- 

**Engenheiro Responsável:** [Estela de Oliveira/Codex]
**Versão:** 1.2.0 (Suporte nativo a Excel e Poetry)
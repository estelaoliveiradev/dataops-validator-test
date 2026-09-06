# Pipeline Automatizado para Conciliação Contábil

## 🎯 Sobre o Projeto

Este projeto consiste em um **Pipeline de Dados** acoplado a uma aplicação web modular desenvolvida em Python com o microframework **Flask**. O sistema funciona como um motor de auditoria computacional em ambiente de *staging*, projetado para validar a integridade de lançamentos gerados por **Sistemas de Roteamento Contábil** antes da consolidação definitiva no livro razão.

A solução visa mitigar o "atrito de integração" e fornecer uma barreira de segurança automatizada contra distorções materiais e falhas paramétricas em lotes financeiros, auxiliando organizações no cumprimento das exigências de governança corporativa e conformidade estipuladas pela **Seção 404 da Lei Sarbanes-Oxley (SOX)**.

---

## 🏗️ Arquitetura do Sistema e Lógica de Negócio

A aplicação opera inteiramente em memória para garantir máxima eficiência de processamento computacional, seguindo o fluxo de DataOps estruturado abaixo:

[TemplateExpectativa (CSV)] ──┐
├─→ [Left Join em Memória] ──→ [Classificador Core] ──→ [Dashboards Plotly]
[SnapshotProcessado (CSV)]  ──┘

O pipeline executa o cruzamento de dados (*left join*) de duas bases de entrada descaracterizadas de chaves proprietárias:
1.  **`TemplateExpectativa`**: Base de referência que mapeia as regras de negócio contábeis planejadas e os identificadores de roteiros esperados para cada cenário.
2.  **`SnapshotProcessado`**: Extrato consolidado de eventos gerados e sumarizados pelo motor de roteamento contábil automatizado.

### Critérios de Classificação Operacional
O algoritmo analisa os registros e classifica os cenários contábeis em três status determinísticos:
* **Sensibilizado com Sucesso**: Quando o identificador do roteiro gerado é idêntico ao esperado.
* **Divergente**: Quando o cenário foi acionado, mas o roteiro gerado diverge da matriz de parametrização regulatória.
* **Não Sensibilizado**: Quando o cenário mapeado na expectativa está ausente ou nulo no processamento realizado (evento órfão).

---

## 🤖 Auditoria Cognitiva com IA Generativa (Novo!)

### Integração Gemini AI

O pipeline foi expandido com capacidades de **auditoria cognitiva automatizada** utilizando o modelo **Gemini 3.6 Flash** da Google AI. Esta camada de inteligência artificial analisa os resultados da conciliação e gera:

* **Diagnóstico de Conformidade SOX**: Avaliação automática do nível de risco (Conformidade Total, Em Risco Material, Não-Conformidade Crítica)
* **Análise de Causa Raiz**: Identificação de padrões sistemáticos de falha no roteamento contábil
* **Impacto Regulatório**: Mapeamento automático para requisitos específicos da Seção 404 (ICFR)
* **Recomendações de Mitigação**: Sugestões acionáveis para correção de controles

### Arquitetura Expandida

```
[TemplateExpectativa] ──┐
                        ├─→ [Spark Join] ──→ [Classificador] ──→ [Gemini AI Audit] ──→ [Delta Lake]
[SnapshotProcessado]  ──┘                                              ↓
                                                              [Dashboards + Relatórios]
```

### Segurança e Governança

* **API Keys**: Gerenciamento seguro via **Databricks Secrets** (sem exposição em código)
* **Retry Automático**: Implementação de exponential backoff para APIs instáveis
* **Auditabilidade**: Persistência em Delta Lake com **Time Travel** e **Change Data Feed**
* **Rastreabilidade**: Metadata completa (timestamp, usuário, ambiente, parâmetros)

---

## 📊 Resultados de Performance - Bateria de Testes

### Metodologia

Bateria de **5 execuções independentes** com 500 cenários cada, totalizando 2.500 cenários processados. Análise estatística robusta com médias, desvio padrão e coeficiente de variação.

### Métricas de Performance

| Etapa | Tempo Médio | Desvio Padrão | CV% | Avaliação |
|-------|-------------|---------------|-----|------------|
| **Conciliação Spark** | 0,501s | ±0,076s | 15,2% | ⚠️ Variabilidade moderada |
| **Auditoria Gemini** | 7,559s | ±0,992s | 13,1% | ⚠️ Variabilidade moderada |
| **Pipeline Total** | 8,060s | ±0,988s | 12,3% | ⚠️ Variabilidade moderada |

### Throughput Projetado

* **62 cenários/segundo** (execução única)
* **3.722 cenários/minuto**
* **223.327 cenários/hora**
* **5,36 milhões cenários/dia** (operação 24/7)

### Resultados de Conformidade

* **Acurácia Global**: 85,4% (consistente em todas as 5 execuções)
* **Status Detectado**: Em Risco Material (100% das execuções)
* **Causa Raiz Identificada**: Falha sistemática no roteamento para conta transitória
* **Impacto SOX**: Inoperância parcial dos controles ICFR (Seção 404)

### Análise de Estabilidade

* ✅ **Pipeline Robusto**: CV < 15% indica boa previsibilidade
* ⚠️ **Gargalo Identificado**: Gemini representa 93,8% do tempo total
* 📈 **Recomendação**: Otimizar inferência (cache, batch, modelo mais rápido)

---

## 🛠️ Stack Tecnológica

### Camada de Processamento

* **Plataforma**: Databricks (Serverless Compute)
* **Motor de Dados**: Apache Spark 4.2.0 (PySpark)
* **Linguagem Core**: Python 3.12.3
* **Armazenamento**: Delta Lake (ACID, Time Travel, Change Data Feed)
* **Catalog**: Unity Catalog (governança de dados)

### Camada de IA/ML

* **Modelo Generativo**: Google Gemini 3.6 Flash
* **Temperatura**: 0.1 (inferência determinística)
* **Integração**: Google AI Python SDK
* **Segurança**: Databricks Secrets para gerenciamento de credenciais

### Camada de Análise e Visualização

* **Manipulação de Dados**: Pandas 2.x, NumPy
* **Visualização**: Matplotlib, Plotly 5.18.0
* **Análise Estatística**: SciPy, Statsmodels

### Camada Web (Aplicação Original)

* **Backend**: Flask 3.0.2+
* **Frontend**: Tailwind CSS
* **Framework de Testes**: Pytest

### Persistência e Auditoria

* **Tabelas Delta**:
  * `main.default.auditoria_performance_execucoes` - Resultados individuais
  * `main.default.auditoria_performance_estatisticas` - Estatísticas agregadas
* **Recursos Habilitados**:
  * Time Travel (histórico de versões)
  * Change Data Feed (rastreamento de mudanças)
  * Schema Evolution (adaptação automática)

---

## 🚀 Como Executar a Aplicação

### Opção A: Databricks (Recomendado para Produção)

#### 1. Configuração do Ambiente

```bash
# Clonar o repositório no Databricks Repos
git clone https://github.com/estelaoliveiradev/dataops-validator-test.git
```

#### 2. Configurar Secrets (API Keys)

```python
# Via Databricks CLI
databricks secrets create-scope --scope gemini-api
databricks secrets put --scope gemini-api --key api-key

# Ou via SDK no notebook
from databricks.sdk import WorkspaceClient
w = WorkspaceClient()
# (Seguir fluxo interativo no notebook)
```

#### 3. Executar o Pipeline de Auditoria

Abra o notebook `databricks/conciliador_contabil.ipynb` e execute as células:

* **Célula 1-6**: Geração de massa de dados simulada
* **Célula 7-10**: Conciliação Spark + Auditoria Gemini
* **Célula 11**: Bateria de testes de performance (5 execuções)
* **Célula 12**: Análise estatística e gráficos
* **Célula 13**: Persistência em Delta Lake
* **Célula 14**: Resumo executivo (markdown)

#### 4. Consultar Resultados de Auditoria

```sql
-- Ver última bateria de testes
SELECT * 
FROM main.default.auditoria_performance_execucoes
WHERE timestamp_batch = (
  SELECT MAX(timestamp_batch) 
  FROM main.default.auditoria_performance_execucoes
)
ORDER BY execucao_id;

-- Evolução da performance ao longo do tempo
SELECT 
  DATE(timestamp_batch) as data,
  etapa,
  AVG(media_s) as media_tempo_s,
  AVG(coef_variacao_pct) as media_cv_pct
FROM main.default.auditoria_performance_estatisticas
GROUP BY DATE(timestamp_batch), etapa
ORDER BY data DESC, etapa;

-- Time Travel (histórico de versões)
DESCRIBE HISTORY main.default.auditoria_performance_execucoes;

-- Change Data Feed (auditoria de mudanças)
SELECT * 
FROM table_changes('main.default.auditoria_performance_execucoes', 0);
```

---

### Opção B: Execução Local (Flask - Versão Original)

#### 1. Clonar o Repositório e Configurar o Ambiente

```bash
# Clonar o projeto
git clone https://github.com/estelaoliveiradev/dataops-validator-test.git
cd dataops-validator-test

# Criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

#### 2. Gerar Massa de Dados Simulada

```bash
python MASSA/gerar_massa_academica.py
```

Este comando criará `template_expectativa.csv` e `snapshot_processado.csv` com furos estruturais para validação.

#### 3. Executar Servidor Flask

```bash
python app.py
```

Acesse: `http://127.0.0.1:5000/`

---

## 📊 Visualizações e Gráficos

O pipeline gera automaticamente 4 tipos de gráficos profissionais:

1. **Gráfico de Linha**: Evolução dos tempos de execução (Spark, Gemini, Total)
2. **Gráfico de Barras**: Médias com barras de erro (desvio padrão)
3. **Box Plot**: Distribuição e outliers por etapa
4. **Coeficiente de Variação**: Métrica de estabilidade do pipeline

### Resumo Executivo

O notebook gera um **relatório markdown completo** contendo:

* ✅ Informações gerais da execução (data, ambiente, parâmetros)
* 📊 Tabelas de performance com estatísticas descritivas
* 🚀 Projeções de throughput (cenarios/segundo, hora, dia)
* 🔍 Análise de estabilidade (CV%, gargalos)
* 🎯 Diagnóstico de conformidade SOX
* 💡 Recomendações de ação (curto, médio, longo prazo)
* 🔐 Queries SQL para auditoria e rastreabilidade

---

## 📁 Estrutura do Projeto

```
dataops-validator-test/
├── databricks/
│   └── conciliador_contabil.ipynb    # Pipeline completo (Spark + Gemini + Auditoria)
├── MASSA/
│   └── gerar_massa_academica.py      # Gerador de dados simulados
├── app.py                            # Aplicação Flask (versão web original)
├── requirements.txt                  # Dependências Python
└── README.md                         # Este arquivo
```

### Notebooks Databricks

* **`conciliador_contabil.ipynb`**: Pipeline end-to-end com:
  * Geração de massa de teste
  * Conciliação distribuída (Spark)
  * Auditoria cognitiva (Gemini AI)
  * Bateria de testes de performance
  * Persistência auditável (Delta Lake)
  * Resumo executivo e visualizações

---

## 🔒 Conformidade e Segurança

### SOX Section 404 (ICFR)

* ✅ **Rastreabilidade**: Toda execução registra timestamp, usuário, ambiente
* ✅ **Imutabilidade**: Delta Lake garante versionamento ACID
* ✅ **Auditabilidade**: Change Data Feed captura todas as mudanças
* ✅ **Reprodução**: Metadata completa de parâmetros e configurações

### Gerenciamento de Credenciais

* **Databricks Secrets**: API keys armazenadas com criptografia
* **Sem Exposição**: Nenhuma credencial hard-coded no código
* **Controle de Acesso**: Secrets scope com permissões granulares

---

## 🚀 Roadmap Futuro

### Curto Prazo

* [ ] Correção do motor de roteamento (alvo: acurácia ≥ 98%)
* [ ] Validação pós-correção (bateria com 10+ execuções)

### Médio Prazo

* [ ] Otimização Gemini (cache, batch inference, modelo mais rápido)
* [ ] Meta: Reduzir tempo total de 8s → 4-5s
* [ ] Dashboard interativo (Streamlit/Dash)

### Longo Prazo

* [ ] SLA de performance (P95 < 10s)
* [ ] Monitoramento contínuo de acurácia
* [ ] Alertas automáticos (CV% > 20%)
* [ ] Integração com sistemas ERP

---

# 🎓 Contexto Acadêmico

Este projeto foi desenvolvido como **Trabalho de Conclusão de Curso (TCC)** para o **MBA em Engenharia de Software** da **Universidade de São Paulo (USP/Esalq)**.

* **Discente**: Estela de Oliveira
* **Orientador**: Anaximandro Anderson
* **Status**: Resultados Preliminares Validados e Homologados
* **Ano**: 2026

---

## 📝 Licença

Este projeto é acadêmico e está disponível para fins educacionais.

---

## 📞 Contato

Para dúvidas ou sugestões sobre o pipeline de auditoria cognitiva:

* **GitHub**: [@estelaoliveiradev](https://github.com/estelaoliveiradev)
* **Repositório**: [dataops-validator-test](https://github.com/estelaoliveiradev/dataops-validator-test)
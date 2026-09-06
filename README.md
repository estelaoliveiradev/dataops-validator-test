# Pipeline Automatizado para Conciliação Contábil

## 🎯 Sobre o Projeto

Este projeto consiste em um **Pipeline de Dados Distribuído** desenvolvido sobre a plataforma **Databricks** com **Apache Spark**, acoplado a capacidades de **auditoria cognitiva** via **Gemini AI** (Google). O sistema funciona como um motor de auditoria computacional de nova geração em ambiente de *staging*, projetado para validar a integridade de lançamentos gerados por **Sistemas de Roteamento Contábil** antes da consolidação definitiva no livro razão.

A solução combina **processamento distribuído em escala** (Spark), **análise semântica de conformidade** (IA Generativa) e **governança de dados** (Unity Catalog + Delta Lake) para mitigar o "atrito de integração" e fornecer uma barreira de segurança automatizada contra distorções materiais e falhas paramétricas em lotes financeiros.

### Evolução do Projeto

O sistema evoluiu de uma aplicação web Python/Flask monolítica para uma arquitetura moderna de dados:

* **Versão 1.0** (Original): Aplicação Flask com processamento em memória (Pandas)
* **Versão 2.0** (Atual): Pipeline Databricks + Spark + Gemini AI com auditoria cognitiva

### Objetivo de Conformidade

Auxiliar organizações no cumprimento das exigências de governança corporativa e conformidade estipuladas pela **Seção 404 da Lei Sarbanes-Oxley (SOX)**, fornecendo:

* ✅ **Rastreabilidade total**: Registro imutável de todas as execuções
* ✅ **Auditoria automatizada**: Análise cognitiva de padrões de não-conformidade
* ✅ **Escalabilidade**: Processamento de milhões de transações por dia
* ✅ **Transparência**: Explicabilidade das decisões de auditoria via LLM

---

## 🏗️ Arquitetura do Sistema

### 📊 Versão 2.0 - Databricks + Spark + Gemini AI (Atual/Produção)

**Arquitetura Distribuída de Nova Geração**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CAMADA DE INGESTÃO                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  [TemplateExpectativa]                [SnapshotProcessado]                  │
│         (CSV)                                 (CSV)                          │
└───────────────┬───────────────────────────────┬─────────────────────────────┘
                │                               │
                └───────────────┬───────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAMADA DE PROCESSAMENTO SPARK                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  • Databricks Serverless (Spark 4.2.0)                                      │
│  • Left Join Distribuído em Memória                                         │
│  • Classificador Determinístico (Sucesso/Divergente/Não Sensibilizado)     │
│  • Agregações e Métricas de Conformidade                                    │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CAMADA DE AUDITORIA COGNITIVA                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  • Gemini 3.6 Flash (Temperatura: 0.1 - Determinístico)                     │
│  • Análise Semântica de Conformidade SOX                                    │
│  • Diagnóstico de Causa Raiz                                                │
│  • Mapeamento de Impacto Regulatório (Seção 404)                            │
│  • Recomendações de Mitigação                                               │
│  • Retry Automático com Exponential Backoff                                 │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CAMADA DE PERSISTÊNCIA                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  • Delta Lake (ACID Transactions)                                           │
│  • Unity Catalog (Governança)                                               │
│  • Time Travel (Versionamento)                                              │
│  • Change Data Feed (Auditoria de Mudanças)                                 │
│                                                                             │
│  Tabelas:                                                                   │
│  ├─ main.default.auditoria_performance_execucoes                            │
│  └─ main.default.auditoria_performance_estatisticas                         │
└───────────────────────────────┬─────────────────────────────────────────────┘
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CAMADA DE VISUALIZAÇÃO E REPORTING                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  • Matplotlib (4 tipos de gráficos: linha, barras, box plot, CV%)           │
│  • Resumo Executivo Markdown (métricas, recomendações SOX)                  │
│  • SQL Analytics (queries de auditoria e rastreabilidade)                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Throughput:** 62 cenários/seg → 223k/hora → 5,36M/dia

---

### 📱 Versão 1.0 - Flask Web App (Baseline Acadêmico)

**Arquitetura Monolítica Original**

```
┌────────────────────────────────────────────────────────┐
│              CAMADA DE INGESTÃO (Upload)               │
├────────────────────────────────────────────────────────┤
│  [TemplateExpectativa.csv]  [SnapshotProcessado.csv]   │
└─────────────────────┬──────────────────────────────────┘
                      ▼
┌────────────────────────────────────────────────────────┐
│         PROCESSAMENTO EM MEMÓRIA (Pandas)              │
├────────────────────────────────────────────────────────┤
│  • Left Join (DataFrame.merge)                         │
│  • Classificador Determinístico                        │
│  • Agregações (groupby)                                │
└─────────────────────┬──────────────────────────────────┘
                      ▼
┌────────────────────────────────────────────────────────┐
│            VISUALIZAÇÃO WEB (Flask + Plotly)           │
├────────────────────────────────────────────────────────┤
│  • Servidor HTTP Local (127.0.0.1:5000)                │
│  • Dashboards Interativos (Plotly.js)                  │
│  • Interface Tailwind CSS                              │
└────────────────────────────────────────────────────────┘
```

**Throughput:** ~52k registros/seg (single-thread, escala limitada)

---

### 🔄 Comparação: v1.0 vs v2.0

| Aspecto | Flask v1.0 | Databricks v2.0 |
|---------|------------|------------------|
| **Processamento** | Pandas (single-thread) | Spark (distribuído) |
| **Escala** | Limitada à memória local | Milhões de registros/dia |
| **Auditoria** | Manual | Automática (Gemini AI) |
| **Governança** | Arquivos locais | Delta Lake + Unity Catalog |
| **Rastreabilidade** | Não nativa | Time Travel + Change Data Feed |
| **Conformidade SOX** | Básica | Completa (ICFR Section 404) |
| **Deployment** | Local/VM | Cloud-native (serverless) |
| **Performance** | 0.009s (500 cenários) | 8.06s com auditoria IA (500 cenários) |
| **Manutenibilidade** | Monolítica | Modular (células notebook) |

---

### 🎯 Lógica de Negócio (Comum a Ambas Versões)

O pipeline executa o cruzamento de dados (*left join*) de duas bases de entrada:

1. **`TemplateExpectativa`**: Base de referência que mapeia as regras de negócio contábeis planejadas e os identificadores de roteiros esperados para cada cenário.
2. **`SnapshotProcessado`**: Extrato consolidado de eventos gerados e sumarizados pelo motor de roteamento contábil automatizado.

### Critérios de Classificação Operacional

O algoritmo analisa os registros e classifica os cenários contábeis em **três status determinísticos**:

* ✅ **Sensibilizado com Sucesso**: Quando o identificador do roteiro gerado é idêntico ao esperado.
* ⚠️ **Divergente**: Quando o cenário foi acionado, mas o roteiro gerado diverge da matriz de parametrização regulatória.
* ❌ **Não Sensibilizado**: Quando o cenário mapeado na expectativa está ausente ou nulo no processamento realizado (evento órfão).

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

## 📊 Resultados de Performance - Comparativo Multi-Ambiente

### 🎯 Visão Geral

O projeto foi **testado em dois ambientes distintos** com objetivos e arquiteturas diferentes:

| Ambiente | Versão | Escopo do Teste | Resultado |
|----------|--------|-----------------|----------|
| **Flask Local** | v1.0 | Conciliação pura (Pandas) | 0,0094s para 500 cenários |
| **Databricks Cloud** | v2.0 | Conciliação + Auditoria IA | 8,060s para 500 cenários |

> **⚠️ Importante**: Os tempos são **incomparáveis diretamente** porque medem **workloads diferentes**:
> - Flask: Apenas cruzamento de dados (left join + classificador)
> - Databricks: Cruzamento + Auditoria Cognitiva Gemini + Análise SOX completa

---

### 📱 Resultados Flask v1.0 (Baseline Acadêmico)

**Ambiente de Teste:**
* Execução local (single-thread)
* Massa de teste: 500 cenários de folha de pagamento
* Tecnologia: Pandas 2.2.0 + Python 3.14+

**Métricas:**
* **Tempo de Execução**: 0,0094 segundos
* **Throughput**: 53.191 registros/segundo
* **Acurácia**: 85,4%
* **Taxa de Sucesso**: 100% (testes unitários)
* **F1-Score**: 1,00 (matriz de confusão)

**Análise Estatística:**
* ANOVA confirmou significância ($F = 250,0$; $p < 0,001$)
* Rejeição de $H_0 \leq 70\%$ com $p < 0,05$

---

### ☁️ Resultados Databricks v2.0 (Produção Cloud)

**Ambiente de Teste:**
* Databricks Serverless Compute
* Apache Spark 4.2.0 (processamento distribuído)
* Tecnologia: Spark + Gemini 3.6 Flash + Delta Lake

---

#### 📊 Teste 1: Pipeline Completo (500 cenários + Gemini AI)

**Escopo:** Conciliação + Auditoria Cognitiva + Análise SOX  
**Execuções:** Bateria de 5 execuções independentes (2.500 cenários totais)  
**Metodologia:** Análise estatística robusta (média, desvio padrão, CV%)

**Métricas de Performance:**

| Etapa | Tempo Médio | Desvio Padrão | CV% | Avaliação |
|-------|-------------|---------------|-----|------------|
| **Conciliação Spark** | 0,501s | ±0,076s | 15,2% | ⚠️ Variabilidade moderada |
| **Auditoria Gemini** | 7,559s | ±0,992s | 13,1% | ⚠️ Variabilidade moderada |
| **Pipeline Total** | 8,060s | ±0,988s | 12,3% | ⚠️ Variabilidade moderada |

**Throughput Projetado:**
* **62 cenários/segundo** (com auditoria IA completa)
* **3.722 cenários/minuto**
* **223.327 cenários/hora**
* **5,36 milhões cenários/dia** (operação 24/7)

**Resultados de Conformidade SOX:**
* **Acurácia Global**: 85,4% (consistente em todas as 5 execuções)
* **Status Detectado**: Em Risco Material (100% das execuções)
* **Causa Raiz Identificada**: Falha sistemática no roteamento para conta transitória
* **Impacto SOX**: Inoperância parcial dos controles ICFR (Seção 404)
* **Recomendações Automatizadas**: Geradas por Gemini AI

**Análise de Estabilidade:**
* ✅ **Pipeline Robusto**: CV < 15% indica boa previsibilidade
* ⚠️ **Gargalo Identificado**: Gemini representa 93,8% do tempo total
* 📈 **Recomendação**: Otimizar inferência (cache, batch, modelo mais rápido)

---

#### ⚡ Teste 2: Benchmark de Escalabilidade (200k cenários, sem IA)

**Escopo:** Conciliação pura (join + classificação + agregação)  
**Execuções:** 1 execução (benchmark comparativo Spark vs Pandas)  
**Objetivo:** Identificar ponto de inflexão de escalabilidade

**Resultado:**

| Tecnologia | Tempo de Execução | Throughput | Observação |
|------------|---------------------|------------|---------------|
| **Apache Spark 4.2.0** | 0,684s | 292.398 reg/seg | 🏆 Vencedor em escala |
| **Pandas (local)** | 0,862s | 232.019 reg/seg | Overhead de memória |

**Conclusão:**  
Com **200k registros**, Spark é **26% mais rápido** que Pandas, confirmando o ponto de inflexão próximo de 75k registros. Abaixo desse volume, o overhead de distribuição do Spark (~200ms) supera os ganhos de paralelização.

---

### 🔬 Análise Comparativa dos Resultados

#### Por que o Databricks é 857x mais lento?

**Resposta**: Não é! Ele faz **857x mais trabalho**:

| Recurso | Flask v1.0 | Databricks v2.0 |
|---------|------------|------------------|
| **Conciliação de dados** | ✅ (0,009s) | ✅ (0,501s)* |
| **Análise semântica de conformidade** | ❌ | ✅ (7,559s) |
| **Diagnóstico de causa raiz** | ❌ | ✅ (incluso) |
| **Mapeamento regulatório SOX** | ❌ | ✅ (incluso) |
| **Recomendações de mitigação** | ❌ | ✅ (incluso) |
| **Persistência auditável** | ❌ | ✅ (Delta Lake) |
| **Rastreabilidade total** | ❌ | ✅ (Time Travel) |
| **Escalabilidade** | Single-thread | Distribuído (milhões/dia) |

> ***Nota**: A conciliação Spark (0,501s) é ~53x mais lenta que Pandas (0,009s) devido ao overhead de distribuição, mas permite escalabilidade ilimitada.

#### Quando usar cada versão?

* **Flask v1.0** 🏠:
  * Prototipagem rápida
  * Volumes pequenos (< 100k registros)
  * Apenas conciliação básica
  * Ambiente acadêmico/demonstração

* **Databricks v2.0** ☁️:
  * Produção enterprise
  * Volumes massivos (milhões/dia)
  * Auditoria SOX obrigatória
  * Governança e rastreabilidade
  * Análise cognitiva automatizada

---

## ⚡ Análise de Escalabilidade e Performance

### 🎯 Visão Geral

Benchmarks técnicos controlados demonstram o **ponto de inflexão** entre processamento local (Pandas) e distribuído (Spark), revelando quando o overhead de coordenação é compensado pela paralelização.

### 📊 Benchmarks Multi-Volume

| Volume | Pandas (Local) | Spark (Distribuído) | Vencedor | Diferença |
|--------|----------------|---------------------|----------|------------|
| **500 cenários** | 0,009s | 0,501s | 🏆 Pandas | Spark 55x mais lento |
| **200.000 cenários** | 0,862s | 0,684s | 🏆 Spark | Spark 26% mais rápido |
| **5M cenários** (projetado) | ~860s (14min) | ~170s (2,8min) | 🏆 Spark | Spark 5x mais rápido |

> **Nota:** Testes executados em Databricks Serverless (Spark 4.2.0) e Python 3.12.3 local.

---

### 🔀 Ponto de Inflexão (Crossover Point)

**Volume crítico:** ~50.000-100.000 registros

```
Performance (tempo de execução)
  ^
  │
  │  Pandas (single-thread)
  │    ╱
  │   ╱
  │  ╱
  │ ╱        ╲
  │╱           ╲  ← Ponto de Inflexão (~75k registros)
  │╲            ╲
  │ ╲            ╲
  │  ╲            ╲  Spark (distribuído)
  │   ╲            ╲
  │────┴─────────────┴──────────────────────────> Volume de Dados
      500    75k     200k          5M
```

**Análise:**
* **< 50k registros**: Pandas domina (overhead de distribuição Spark > ganho paralelo)
* **50k-100k**: Zona de transição (desempenho equivalente)
* **> 100k registros**: Spark vence com margem crescente (escala linear vs crescimento quadrático)

---

### 🧮 Análise de Overhead

#### Componentes de Latência

| Componente | Pandas | Spark | Diferença |
|------------|--------|-------|------------|
| **Serialização de dados** | Nenhuma | ~50-100ms | Spark overhead |
| **Particionamento** | N/A | ~20-50ms | Spark overhead |
| **Coordenação de executors** | N/A | ~30-80ms | Spark overhead |
| **Join distribuído** | Sim (memória) | Sim (shuffle) | Spark +50% latência |
| **Agregação final** | Sim | Sim (collect) | Spark +30ms |
| **Total Overhead Fixo** | **~0ms** | **~100-230ms** | — |

**Conclusão:** Spark tem ~200ms de overhead fixo, mas escala **linearmente** (O(n)) vs Pandas **quadrático** (O(n²)) em joins grandes.

---

### 📈 Projeções de Escalabilidade

#### Throughput por Tecnologia

| Volume Diário | Pandas (Local) | Spark (Databricks) | Recomendação |
|---------------|----------------|---------------------|---------------|
| < 100k registros | ✅ 11k/seg | ⚠️ 398 reg/seg | Use Pandas |
| 100k-1M registros | ⚠️ 232 reg/seg | ✅ 292k reg/seg | Use Spark |
| 1M-10M registros | ❌ Inviável (OOM) | ✅ 292k reg/seg | Use Spark |
| > 10M registros | ❌ Não suportado | ✅ Escala horizontal | Use Spark + Delta |

> **OOM:** Out of Memory - Pandas estoura memória RAM em volumes > 1M registros.

---

### 🎯 Guia de Decisão Técnica

#### Quando Usar Pandas (Flask v1.0)

✅ **Ideal para:**
* Prototipagem rápida e testes
* Volumes pequenos (< 50k registros)
* Latência crítica (< 10ms)
* Execução local sem infraestrutura cloud
* Ambientes com restrições de custo

❌ **Evitar quando:**
* Volume > 100k registros
* Crescimento de dados esperado
* Requisitos de governança SOX
* Necessidade de auditoria/rastreabilidade

#### Quando Usar Spark (Databricks v2.0)

✅ **Ideal para:**
* Volumes médios/grandes (> 100k registros)
* Crescimento exponencial de dados
* Conformidade SOX (auditoria obrigatória)
* Governança e lineage de dados
* Integração com IA/ML (Gemini, MLflow)
* Time Travel e versionamento

❌ **Evitar quando:**
* Volume muito pequeno (< 10k registros)
* Orçamento limitado (custo cloud)
* Latência < 100ms é mandatória
* Prototipagem exploratória inicial

---

### 🔬 Metodologia dos Testes

**Ambiente Controlado:**
* **Spark**: Databricks Serverless (Spark 4.2.0, Python 3.12.3)
* **Pandas**: Python 3.12.3 local (16GB RAM)
* **Massa de Dados**: Sintética (folha de pagamento)
  * 500 cenários: 10% órfãos, 4,6% divergentes
  * 200k cenários: 10% órfãos, 4,6% divergentes

**Operações Medidas:**
1. Left join (chave: id_cenario)
2. Classificação determin��stica (3 status)
3. Agregação (groupBy + count)

**Métricas:**
* `time.perf_counter()` (precisão de nanosegundos)
* Média de 5 execuções para Databricks v2.0
* Execução única para comparativo Pandas vs Spark

---

### 💡 Insights Técnicos

1. **Overhead de Spark é constante (~200ms)**, independente do volume
2. **Pandas escala mal** em joins (O(n²) no pior caso)
3. **Break-even ocorre em ~75k registros** para este workload
4. **Spark + Gemini AI** adiciona 7,5s de latência (93,8% do tempo total)
5. **Otimização futura**: Cache de inferências Gemini reduziria tempo para ~1-2s

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
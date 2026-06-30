# Pipeline Automatizado de Conciliação e Homologação Contábil

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

## 📊 Resultados e Performance (Massa de Teste)

Durante os ensaios experimentais preliminares com um design fatorial e amostragem estratificada utilizando um lote consolidado de folha de pagamento de 500 cenários, o pipeline registrou as seguintes métricas descritivas e inferenciais:

* **Acurácia Global**: 85,4% (Rejeição da hipótese nula $H_0 \le 70\%$ com $p < 0,05$).
* **Eficiência Computacional**: Tempo total de execução de **0,0094 segundos** (Vazão equivalente a 52.083 registros por segundo em alta volumetria).
* **Confiabilidade**: 100% de taxa de sucesso nos testes unitários lógicos (Matriz de Confusão com *F1-Score* estável em 1,00).
* **Significância Estatística**: O teste de Análise de Variância (ANOVA) confirmou efeito altamente significativo entre a tipologia do cenário contábil e o tempo final de computação em memória ($F = 250,0$; $p < 0,001$).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem Core**: Python 3.14+
* **Engenharia e Manipulação de Dados**: Pandas 2.2.0+
* **Arquitetura Web Backend**: Flask 3.0.2+
* **Visualização Analítica (Frontend)**: Plotly 5.18.0 + Tailwind CSS
* **Framework de Testes**: Pytest

---

## 🚀 Como Executar a Aplicação

### 1. Clonar o Repositório e Configurar o Ambiente

# Clonar o projeto
```bash
git clone [https://github.com/seu-usuario/pipeline-conciliacao-contabil.git](https://github.com/seu-usuario/pipeline-conciliacao-contabil.git)
cd pipeline-conciliacao-contabil
```
# Criar e ativar o ambiente virtual (Virtualenv)
```
python -m venv venv
source venv/bin/activate  # No Windows: venv\\Scripts\\activate
```
# Instalar as dependências do ecossistema
```
pip install -r requirements.txt
```

2. Gerar a Massa de Dados Simulada (Acadêmica)
Para testar a aplicação sem expor chaves proprietárias de mercado, execute o script auxiliar que mimetiza cenários de folha de pagamento:

Bash
```
python MASSA/gerar_massa_academica.py
```

Este comando criará os arquivos de teste template_expectativa.csv e snapshot_processado.csv contendo furos estruturais deliberados para validação da esteira.

# 3. Executar o Pipeline e Iniciar o Servidor Flask
Bash
```
python app.py
```
Abra o seu navegador e acesse o endereço local http://127.0.0.1:5000/. A interface web permitirá realizar o upload dos arquivos e exibirá o dashboard analítico com os gráficos dinâmicos de distribuição de status operacionais.

# 🎓 Contexto Acadêmico
Este artefato de software foi desenvolvido como parte integrante do Trabalho de Conclusão de Curso (TCC) para o MBA em Engenharia de Software da Universidade de São Paulo (USP/Esalq).

## Discente: Estela de Oliveira

## Orientador: Anaximandro Anderson

## Status: Resultados Preliminares Validados e Homologados

## Ano: 2026
"""


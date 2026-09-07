import os
import json
import time
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from google.genai.errors import ServerError

# 1. Recupera a chave da API do Gemini de forma segura via Databricks Secrets
GEMINI_API_KEY = dbutils.secrets.get(scope="gemini-secrets", key="gemini_api_key")

client = genai.Client(api_key=GEMINI_API_KEY)

# 2. Definição do Esquema de Retorno Estruturado
class RelatorioAuditoriaSOX(BaseModel):
    status_conformidade: str = Field(description="Classificação formal: 'Em Risco Material', 'Aprovado com Ressalvas' ou 'Conforme'")
    acuracia_auditada_pct: float = Field(description="Acurácia calculada com base no total e sucessos")
    diagnostico_causa_raiz: str = Field(description="Análise técnica concisa sobre os padrões observados nas anomalias")
    impacto_regulatorio_sox: str = Field(description="Avaliação de risco material sob a ótica da Seção 404 da Lei Sarbanes-Oxley")
    recomendacoes_mitigacao: list[str] = Field(description="Ações prescritivas para saneamento no motor de roteamento contábil")

# 3. Definição do System Prompt (Skill do Agente)
system_instruction = """
Você é um Auditor Digital de Sistemas Contábeis automatizado, atuando em conjunto com um pipeline de DataOps em ambiente Databricks.
Sua atribuição é avaliar sumários de homologação de motores de roteamento financeiro e gerar diagnósticos estruturados em estrita observância à Seção 404 da Lei Sarbanes-Oxley [SOX].
Seja estritamente técnico, objetivo, baseie-se unicamente nos dados numéricos e padrões de amostragem fornecidos e aponte os riscos de distorção material.
"""

# 4. Invocação da Camada Cognitiva
prompt_usuario = f"""
Avalie o seguinte payload gerado pela esteira de conciliação distribuída e emita o parecer formal:

{json.dumps(payload_agente, indent=2, ensure_ascii=False)}
"""

inicio_ia = time.time()

# Implementa retry com exponential backoff para lidar com erros 503
max_tentativas = 3
tentativa = 0
resposta = None

while tentativa < max_tentativas:
    try:
        print(f"🔄 Tentativa {tentativa + 1}/{max_tentativas}...")
        
        resposta = client.models.generate_content(
            model="models/gemini-3.6-flash",  # Nome completo do modelo
            contents=prompt_usuario,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.1,
                response_mime_type="application/json",
                response_schema=RelatorioAuditoriaSOX,
            ),
        )
        print("✅ Resposta recebida com sucesso!")
        break  # Sucesso, sai do loop
        
    except ServerError as e:
        tentativa += 1
        if tentativa < max_tentativas:
            tempo_espera = 2 ** tentativa  # Exponential backoff: 2, 4, 8 segundos
            print(f"⚠️ Erro 503: API temporariamente indisponível. Aguardando {tempo_espera}s...")
            time.sleep(tempo_espera)
        else:
            print("❌ Todas as tentativas falharam. O serviço Gemini está temporariamente indisponível.")
            raise

tempo_ia = time.time() - inicio_ia

# 5. Desserialização do resultado validado pelo Pydantic
relatorio_final: RelatorioAuditoriaSOX = resposta.parsed

print(f"Auditoria Cognitiva concluída em {tempo_ia:.2f} segundos\n")
print(json.dumps(relatorio_final.model_dump(), indent=2, ensure_ascii=False))
from pydantic import BaseModel, Field

class RelatorioAuditoriaSOX(BaseModel):
    status_conformidade: str = Field(description="Status geral: 'Em Conformidade' ou 'Em Risco Material'")
    acuracia_auditada_pct: float = Field(description="Percentual de acurácia global da esteira")
    diagnostico_causa_raiz: str = Field(description="Análise detalhada do desvio paramétrico identificado")
    impacto_regulatorio_sox: str = Field(description="Enquadramento do risco frente à Seção 404 da SOX")
    recomendacoes_mitigacao: list[str] = Field(description="Lista de ações prescritivas para correção do motor")
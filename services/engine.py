import pandas as pd
import time

class ReconciliadorEngine:
    @staticmethod
    def processar(file_esperado, file_dadosbase):
        start_time = time.time()
        
        # Leitura dos dados
        df_esperado = pd.read_csv(file_esperado)
        df_dadosbase = pd.read_csv(file_dadosbase)
        
        # Join (Left Join para garantir que todos os cenários do plano apareçam)
        df_merge = pd.merge(
            df_esperado, 
            df_dadosbase[['id_origem', 'contabilizacao_gerada', 'valor_lancamento']], 
            left_on='id_cenario', 
            right_on='id_origem', 
            how='left'
        )
        
        # Lógica de Classificação
        def classificar(row):
            if pd.isna(row['id_origem']):
                return "Não Sensibilizado"
            elif row['contabilizacao_esperada'] == row['contabilizacao_gerada']:
                return "Sensibilizado com Sucesso"
            else:
                return "Divergente"
        
        df_merge['status'] = df_merge.apply(classificar, axis=1)
        
        # Métricas
        total_cenarios = len(df_esperado)
        sucessos = len(df_merge[df_merge['status'] == "Sensibilizado com Sucesso"])
        acuracia = (sucessos / total_cenarios) * 100
        tempo_proc = round(time.time() - start_time, 4)
        
        # Preparar dados para o gráfico
        resumo_status = df_merge['status'].value_counts().to_dict()
        
        return {
            "detalhes": df_merge.to_dict(orient='records'),
            "metricas": {
                "acuracia": round(acuracia, 2),
                "tempo": tempo_proc,
                "total": total_cenarios
            },
            "grafico": resumo_status
        }
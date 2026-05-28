import pandas as pd
import time

class ReconciliadorEngine:
    @staticmethod
    def processar(file_ph, file_pof):
        start_time = time.time()
        
        # Leitura dos dados
        df_ph = pd.read_csv(file_ph)
        df_pof = pd.read_csv(file_pof)
        
        # Join (Left Join para garantir que todos os cenários do plano apareçam)
        df_merge = pd.merge(
            df_ph, 
            df_pof[['id_origem', 'tt_gerada', 'valor_lancamento']], 
            left_on='id_cenario', 
            right_on='id_origem', 
            how='left'
        )
        
        # Lógica de Classificação
        def classificar(row):
            if pd.isna(row['id_origem']):
                return "Não Sensibilizado"
            elif row['tt_esperada'] == row['tt_gerada']:
                return "Sensibilizado com Sucesso"
            else:
                return "Divergente"
        
        df_merge['status'] = df_merge.apply(classificar, axis=1)
        
        # Métricas
        total_cenarios = len(df_ph)
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
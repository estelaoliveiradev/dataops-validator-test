import pandas as pd
import numpy as np

def generate_sample_data():
    # 1. Cenario_Esperado (Expectativa)
    ph_data = {
        'id_cenario': range(1, 11),
        'nome_cenario': [f"Cenário de Teste {i}" for i in range(1, 11)],
        'contabilizacao_esperada': [100, 100, 200, 200, 300, 300, 400, 500, 600, 700]
    }
    df_esperado = pd.DataFrame(ph_data)
    df_esperado.to_csv('base_esperado.csv', index=False)

    # 2. Cenario_Realizado (Realidade)
    # Simulando: 6 Sucessos, 2 Divergentes, 2 Não Sensibilizados (faltantes)
    pof_data = {
        'id_origem': [1, 2, 3, 4, 5, 6, 7, 8],
        'carteira_financeira': ['PF', 'PJ', 'PF', 'PJ', 'PF', 'PJ', 'PF', 'PJ'],
        'contabilizacao_gerada': [100, 100, 200, 205, 300, 300, 410, 500], # IDs 4 e 7 são divergentes
        'valor_lancamento': np.random.uniform(100, 5000, 8)
    }
    df_dadosbase = pd.DataFrame(pof_data)
    df_dadosbase.to_csv('base_dadosbase.csv', index=False)
    
    print("Arquivos 'base_esperado.csv' e 'base_dadosbase.csv' gerados com sucesso!")

if __name__ == "__main__":
    generate_sample_data()
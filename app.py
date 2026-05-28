import pandas as pd
import time
import json
import io
import os
import plotly
import plotly.express as px
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# --- CAMADA DE SERVIÇO (Data Engine) ---

class ReconciliadorEngine:
    """Classe especialista em processamento e conciliação de dados."""
    
    @staticmethod
    def ler_arquivo(file):
        """Detecta a extensão e lê CSV ou Excel para um DataFrame."""
        filename = file.filename.lower()
        try:
            if filename.endswith('.csv'):
                file.seek(0)
                # Tentamos utf-8, se falhar usamos latin-1 (comum em CSVs de ERPs brasileiros)
                try:
                    return pd.read_csv(file, encoding='utf-8')
                except UnicodeDecodeError:
                    file.seek(0)
                    return pd.read_csv(file, encoding='latin-1')
            
            elif filename.endswith(('.xlsx', '.xls')):
                file.seek(0)
                return pd.read_excel(file, engine='openpyxl')
            
            else:
                raise ValueError("Formato de arquivo não suportado. Use CSV ou Excel.")
        except Exception as e:
            raise ValueError(f"Erro ao processar o arquivo {filename}: {str(e)}")

    @staticmethod
    def processar(file_ph, file_pof):
        """Executa a esteira de DataOps: Cruzamento, Validação e Métricas."""
        start_time = time.time()
        
        # 1. Leitura polimórfica
        df_ph = ReconciliadorEngine.ler_arquivo(file_ph)
        df_pof = ReconciliadorEngine.ler_arquivo(file_pof)
        
        # 2. Sanitização (Remover espaços e colocar em minúsculo para evitar erros de digitação)
        df_ph.columns = df_ph.columns.str.strip().str.lower()
        df_pof.columns = df_pof.columns.str.strip().str.lower()
        
        # 3. Validação de Schema
        cols_ph = {'id_cenario', 'nome_cenario', 'tt_esperada'}
        cols_pof = {'id_origem', 'tt_gerada'}
        
        if not cols_ph.issubset(df_ph.columns):
            raise ValueError(f"Cenario_Esperado incompleta. Colunas necessárias: {cols_ph}")
        if not cols_pof.issubset(df_pof.columns):
            raise ValueError(f"Cenario_Realizado incompleta. Colunas necessárias: {cols_pof}")

        # 4. Join Core (Left Join para manter a expectativa como guia)
        df_merge = pd.merge(
            df_ph, 
            df_pof[['id_origem', 'tt_gerada', 'valor_lancamento']] if 'valor_lancamento' in df_pof.columns else df_pof[['id_origem', 'tt_gerada']], 
            left_on='id_cenario', 
            right_on='id_origem', 
            how='left'
        )
        
        # 5. Lógica de Classificação (Comparação robusta convertendo para string)
        def classificar(row):
            if pd.isna(row['id_origem']):
                return "Não Sensibilizado"
            
            # Convertemos para string e removemos .0 (caso o Excel leia como float)
            esp = str(row['tt_esperada']).replace('.0', '').strip()
            ger = str(row['tt_gerada']).replace('.0', '').strip()
            
            if esp == ger:
                return "Sensibilizado com Sucesso"
            else:
                return "Divergente"
        
        df_merge['status'] = df_merge.apply(classificar, axis=1)
        
        # 6. Cálculo de Métricas
        total = len(df_ph)
        sucessos = len(df_merge[df_merge['status'] == "Sensibilizado com Sucesso"])
        acuracia = (sucessos / total) * 100 if total > 0 else 0
        tempo_total = round(time.time() - start_time, 4)
        
        return {
            "detalhes": df_merge.to_dict(orient='records'),
            "metricas": {
                "acuracia": round(acuracia, 2),
                "tempo": tempo_total,
                "total": total
            },
            "grafico": df_merge['status'].value_counts().to_dict()
        }

# --- ROTAS FLASK ---

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    graphJSON = None
    erro = None

    if request.method == 'POST':
        file_ph = request.files.get('file_ph')
        file_pof = request.files.get('file_pof')
        
        if file_ph and file_pof:
            try:
                resultado = ReconciliadorEngine.processar(file_ph, file_pof)
                
                # Gerar Gráfico Plotly
                fig = px.pie(
                    names=list(resultado['grafico'].keys()), 
                    values=list(resultado['grafico'].values()),
                    color=list(resultado['grafico'].keys()),
                    color_discrete_map={
                        'Sensibilizado com Sucesso': '#10B981', 
                        'Divergente': '#EF4444', 
                        'Não Sensibilizado': '#F59E0B'
                    },
                    hole=0.4
                )
                fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), showlegend=True)
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                
            except Exception as e:
                erro = str(e)
        else:
            erro = "Selecione ambos os arquivos para processar a conciliação."
    
    return render_template('index.html', resultado=resultado, graphJSON=graphJSON, erro=erro)


@app.route('/download_template/<tipo>')
def download_template(tipo):
    """Gera um arquivo Excel de modelo em memória."""
    output = io.BytesIO()
    
    if tipo == 'ph':
        df = pd.DataFrame({
            'id_cenario': [1, 2],
            'nome_cenario': ['Exemplo: Venda Cartão Debito', 'Exemplo: Pagamento Aluguel'],
            'tt_esperada': [100, 550]
        })
        filename = "template_expectativa_PH.xlsx"
    else:
        df = pd.DataFrame({
            'id_origem': [1],
            'carteira_financeira': ['MATRIZ'],
            'tt_gerada': [100],
            'valor_lancamento': [1250.00]
        })
        filename = "template_realidade_POF.xlsx"
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Instrucoes')
    
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )

# --- EXECUÇÃO (Suporte Windows com Waitress) ---

if __name__ == '__main__':
    # Define o ambiente: 'development' ou 'production'
    # No Windows Terminal: set FLASK_ENV=production
    env = os.getenv('FLASK_ENV', 'development')

    if env == 'production':
        from waitress import serve
        print(">>> Iniciando Servidor de Produção (Waitress)")
        print(">>> Acesse: http://localhost:8080")
        serve(app, host='0.0.0.0', port=8080)
    else:
        print(">>> Iniciando Servidor de Desenvolvimento (Debug Mode)")
        app.run(debug=True, port=5000)
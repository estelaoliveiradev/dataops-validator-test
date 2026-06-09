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
    def processar(file_template_expectativa, file_snapshot_processado):
        """Executa a esteira de DataOps: Cruzamento, Validação e Métricas com nomenclatura acadêmica."""
        start_time = time.time()
        
        # 1. Leitura polimórfica
        df_template = ReconciliadorEngine.ler_arquivo(file_template_expectativa)
        df_snapshot = ReconciliadorEngine.ler_arquivo(file_snapshot_processado)
        
        # 2. Sanitização (Remover espaços e colocar em minúsculo para evitar erros de digitação)
        df_template.columns = df_template.columns.str.strip().str.lower()
        df_snapshot.columns = df_snapshot.columns.str.strip().str.lower()
        
        # 3. Validação de Schema
        cols_template = {'id_cenario', 'nome_cenario', 'id_roteiro_esperado'}
        cols_snapshot = {'id_origem', 'id_roteiro_gerado'}
        
        if not cols_template.issubset(df_template.columns):
            raise ValueError(f"TemplateExpectativa incompleto. Colunas necessárias: {cols_template}")
        if not cols_snapshot.issubset(df_snapshot.columns):
            raise ValueError(f"SnapshotProcessado incompleto. Colunas necessárias: {cols_snapshot}")

        # 4. Join Core (Left Join para manter o template de expectativa como guia)
        colunas_snapshot = ['id_origem', 'id_roteiro_gerado']
        if 'segmento_carteira' in df_snapshot.columns:
            colunas_snapshot.append('segmento_carteira')
        if 'valor_evento' in df_snapshot.columns:
            colunas_snapshot.append('valor_evento')
        
        df_merge = pd.merge(
            df_template, 
            df_snapshot[colunas_snapshot], 
            left_on='id_cenario', 
            right_on='id_origem', 
            how='left'
        )
        
        # 5. Lógica de Classificação (Comparação robusta de roteiros convertendo para string)
        def classificar_homologacao(row):
            if pd.isna(row['id_origem']):
                return "Não Sensibilizado"
            
            # Convertemos para string e removemos .0 (caso leia como float)
            roteiro_esperado = str(row['id_roteiro_esperado']).replace('.0', '').strip()
            roteiro_gerado = str(row['id_roteiro_gerado']).replace('.0', '').strip()
            
            if roteiro_esperado == roteiro_gerado:
                return "Sensibilizado com Sucesso"
            else:
                return "Divergente"
        
        df_merge['status_homologacao'] = df_merge.apply(classificar_homologacao, axis=1)
        
        # 6. Cálculo de Métricas
        total = len(df_template)
        sucessos = len(df_merge[df_merge['status_homologacao'] == "Sensibilizado com Sucesso"])
        acuracia = (sucessos / total) * 100 if total > 0 else 0
        tempo_total = round(time.time() - start_time, 4)
        
        return {
            "detalhes": df_merge.to_dict(orient='records'),
            "metricas": {
                "acuracia": round(acuracia, 2),
                "tempo": tempo_total,
                "total": total
            },
            "grafico": df_merge['status_homologacao'].value_counts().to_dict()
        }

# --- ROTAS FLASK ---

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    graphJSON = None
    erro = None

    if request.method == 'POST':
        file_template = request.files.get('file_template_expectativa')
        file_snapshot = request.files.get('file_snapshot_processado')
        
        if file_template and file_snapshot:
            try:
                resultado = ReconciliadorEngine.processar(file_template, file_snapshot)
                
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
    
    if tipo == 'template':
        df = pd.DataFrame({
            'id_cenario': [1, 2],
            'nome_cenario': ['Exemplo: Roteiro 1 - Folha Padrão', 'Exemplo: Roteiro 2 - Folha Especial'],
            'id_roteiro_esperado': [100, 550]
        })
        filename = "template_expectativa.xlsx"
    else:
        df = pd.DataFrame({
            'id_origem': [1],
            'segmento_carteira': ['MATRIZ'],
            'id_roteiro_gerado': [100],
            'valor_evento': [1250.00]
        })
        filename = "snapshot_processado.xlsx"
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Dados')
    
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
        print(">>> Acesse: hcontabilizacaop://localhost:8080")
        serve(app, host='0.0.0.0', port=8080)
    else:
        print(">>> Iniciando Servidor de Desenvolvimento (Debug Mode)")
        app.run(debug=True, port=5000)
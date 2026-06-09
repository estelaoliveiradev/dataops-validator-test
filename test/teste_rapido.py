"""
Script de teste simplificado para validação rápida da lógica
sem dependências externas pesadas
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Teste de importação
try:
    from app import ReconciliadorEngine
    print("✓ ReconciliadorEngine importado com sucesso")
except Exception as e:
    print(f"✗ Erro na importação: {e}")
    sys.exit(1)

import pandas as pd
import tempfile
import os

def teste_leitura_csv():
    """Testa leitura de arquivo CSV."""
    print("\n🧪 Teste 1: Leitura de CSV")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
        f.write("id_cenario,nome_cenario,id_roteiro_esperado\n")
        f.write("1,Teste 1,100\n")
        f.write("2,Teste 2,200\n")
        temp_file = f.name
    
    try:
        with open(temp_file, 'rb') as file_obj:
            file_obj.filename = "template_test.csv"
            df = ReconciliadorEngine.ler_arquivo(file_obj)
            
            assert len(df) == 2
            assert 'id_cenario' in df.columns
            print(f"  ✓ Arquivo lido com sucesso: {len(df)} linhas")
            return True
    except Exception as e:
        print(f"  ✗ Erro: {e}")
        return False
    finally:
        os.unlink(temp_file)

def teste_processamento_100_acuracia():
    """Testa processamento com 100% de acurácia."""
    print("\n🧪 Teste 2: Processamento com 100% acurácia")
    
    df_template = pd.DataFrame({
        'id_cenario': [1, 2, 3],
        'nome_cenario': ['A', 'B', 'C'],
        'id_roteiro_esperado': [100, 200, 300]
    })
    
    df_snapshot = pd.DataFrame({
        'id_origem': [1, 2, 3],
        'id_roteiro_gerado': [100, 200, 300],
        'segmento_carteira': ['MATRIZ', 'FILIAL', 'MATRIZ'],
        'valor_evento': [1000, 2000, 3000]
    })
    
    with tempfile.TemporaryDirectory() as tmpdir:
        template_file = os.path.join(tmpdir, "template.csv")
        snapshot_file = os.path.join(tmpdir, "snapshot.csv")
        
        df_template.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        try:
            with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
                f_template.filename = "template.csv"
                f_snapshot.filename = "snapshot.csv"
                
                resultado = ReconciliadorEngine.processar(f_template, f_snapshot)
                
                acuracia = resultado['metricas']['acuracia']
                assert acuracia == 100.0, f"Esperado 100%, obtive {acuracia}%"
                print(f"  ✓ Acurácia: {acuracia}%")
                print(f"  ✓ Total: {resultado['metricas']['total']}")
                print(f"  ✓ Tempo: {resultado['metricas']['tempo']}s")
                return True
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            return False

def teste_status_classificacao():
    """Testa classificação correta de status_homologacao."""
    print("\n🧪 Teste 3: Classificação de Status")
    
    df_template = pd.DataFrame({
        'id_cenario': [1, 2, 3, 4],
        'nome_cenario': ['A', 'B', 'C', 'D'],
        'id_roteiro_esperado': [100, 200, 300, 400]
    })
    
    # Apenas 3 de 4 processados: 2 corretos, 1 divergente
    df_snapshot = pd.DataFrame({
        'id_origem': [1, 2, 3],
        'id_roteiro_gerado': [100, 200, 999],  # 999 é divergente
        'segmento_carteira': ['MATRIZ', 'FILIAL', 'MATRIZ'],
        'valor_evento': [1000, 2000, 3000]
    })
    
    with tempfile.TemporaryDirectory() as tmpdir:
        template_file = os.path.join(tmpdir, "template.csv")
        snapshot_file = os.path.join(tmpdir, "snapshot.csv")
        
        df_template.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        try:
            with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
                f_template.filename = "template.csv"
                f_snapshot.filename = "snapshot.csv"
                
                resultado = ReconciliadorEngine.processar(f_template, f_snapshot)
                
                grafico = resultado['grafico']
                acuracia = resultado['metricas']['acuracia']
                
                print(f"  ✓ Sensibilizado com Sucesso: {grafico.get('Sensibilizado com Sucesso', 0)}")
                print(f"  ✓ Divergente: {grafico.get('Divergente', 0)}")
                print(f"  ✓ Não Sensibilizado: {grafico.get('Não Sensibilizado', 0)}")
                print(f"  ✓ Acurácia: {acuracia}%")
                
                assert grafico['Sensibilizado com Sucesso'] == 2
                assert grafico['Divergente'] == 1
                assert grafico['Não Sensibilizado'] == 1
                assert acuracia == 50.0
                
                return True
        except Exception as e:
            print(f"  ✗ Erro: {e}")
            import traceback
            traceback.print_exc()
            return False

def teste_colunas_obrigatorias():
    """Testa validação de colunas obrigatórias."""
    print("\n🧪 Teste 4: Validação de Colunas Obrigatórias")
    
    # Template sem coluna obrigatória
    df_template_incompleto = pd.DataFrame({
        'id_cenario': [1],
        'nome_cenario': ['Teste']
        # Falta 'id_roteiro_esperado'
    })
    
    df_snapshot = pd.DataFrame({
        'id_origem': [1],
        'id_roteiro_gerado': [100],
        'segmento_carteira': ['MATRIZ'],
        'valor_evento': [1000]
    })
    
    with tempfile.TemporaryDirectory() as tmpdir:
        template_file = os.path.join(tmpdir, "template.csv")
        snapshot_file = os.path.join(tmpdir, "snapshot.csv")
        
        df_template_incompleto.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        try:
            with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
                f_template.filename = "template.csv"
                f_snapshot.filename = "snapshot.csv"
                
                try:
                    resultado = ReconciliadorEngine.processar(f_template, f_snapshot)
                    print(f"  ✗ Deveria ter lançado ValueError")
                    return False
                except ValueError as ve:
                    if "TemplateExpectativa incompleto" in str(ve):
                        print(f"  ✓ ValueError capturado corretamente: {ve}")
                        return True
                    else:
                        print(f"  ✗ Erro incorreto: {ve}")
                        return False
        except Exception as e:
            print(f"  ✗ Erro inesperado: {e}")
            return False

def main():
    print("=" * 70)
    print("TESTES DE FUNCIONALIDADE - PIPELINE DE HOMOLOGAÇÃO")
    print("=" * 70)
    
    testes = [
        teste_leitura_csv,
        teste_processamento_100_acuracia,
        teste_status_classificacao,
        teste_colunas_obrigatorias
    ]
    
    resultados = []
    for teste in testes:
        try:
            resultados.append(teste())
        except Exception as e:
            print(f"✗ Teste falhou com exceção: {e}")
            import traceback
            traceback.print_exc()
            resultados.append(False)
    
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    
    passou = sum(resultados)
    total = len(resultados)
    
    print(f"\n✓ Testes passaram: {passou}/{total}")
    
    if passou == total:
        print("\n🎉 Todos os testes passaram com sucesso!")
        return 0
    else:
        print(f"\n⚠️  {total - passou} teste(s) falharam")
        return 1

if __name__ == '__main__':
    sys.exit(main())

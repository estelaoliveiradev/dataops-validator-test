#!/usr/bin/env python3
"""
EXEMPLO PRÁTICO DE USO - Pipeline de Homologação de Roteiros

Este script demonstra como usar o pipeline em um caso real:
Validação de processamento de folha de pagamento com diferentes roteiros.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'conciliador_contabil'))

from app import ReconciliadorEngine
import pandas as pd
import tempfile
import os


def exemplo_simples():
    """Exemplo 1: Caso simples com 5 registros."""
    print("\n" + "="*70)
    print("EXEMPLO 1: Validação Simples de Roteiros")
    print("="*70)
    
    # Criar dados
    template = pd.DataFrame({
        'id_cenario': [1, 2, 3, 4, 5],
        'nome_cenario': [
            'Folha Padrão', 
            'Folha Especial', 
            'Folha Bônus',
            'Folha Integração',
            'Folha Reprocessamento'
        ],
        'id_roteiro_esperado': [100, 200, 300, 400, 500]
    })
    
    # Snapshot com alguns acertos, divergências e órfãos
    snapshot = pd.DataFrame({
        'id_origem': [1, 2, 3, 5],  # Falta ID 4 (não sensibilizado)
        'id_roteiro_gerado': [100, 999, 300, 500],  # ID 2 divergente
        'segmento_carteira': ['MATRIZ', 'FILIAL_SP', 'FILIAL_MG', 'DISTRIBUIÇÃO'],
        'valor_evento': [1000, 2000, 3000, 5000]
    })
    
    print("\n📋 TEMPLATE EXPECTATIVA (dados esperados):")
    print(template.to_string(index=False))
    
    print("\n📋 SNAPSHOT PROCESSADO (dados realizados):")
    print(snapshot.to_string(index=False))
    
    # Processar
    with tempfile.TemporaryDirectory() as tmpdir:
        template_file = os.path.join(tmpdir, "template.csv")
        snapshot_file = os.path.join(tmpdir, "snapshot.csv")
        
        template.to_csv(template_file, index=False)
        snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_t, open(snapshot_file, 'rb') as f_s:
            f_t.filename = "template.csv"
            f_s.filename = "snapshot.csv"
            resultado = ReconciliadorEngine.processar(f_t, f_s)
    
    # Exibir resultados
    print("\n📊 RESULTADO DA HOMOLOGAÇÃO:")
    print("-" * 70)
    
    print(f"\n✓ Acurácia: {resultado['metricas']['acuracia']}%")
    print(f"✓ Total de cenários: {resultado['metricas']['total']}")
    print(f"✓ Tempo de processamento: {resultado['metricas']['tempo']}s")
    
    print(f"\n📈 Distribuição de Status:")
    for status, count in resultado['grafico'].items():
        pct = (count / resultado['metricas']['total']) * 100
        print(f"  {status}: {count} ({pct:.1f}%)")
    
    print(f"\n📄 Detalhes de Cada Registro:")
    print("-" * 70)
    
    for detalhe in resultado['detalhes']:
        status = detalhe['status_homologacao']
        emoji = "✓" if status == "Sensibilizado com Sucesso" else "⚠️" if status == "Divergente" else "✗"
        
        print(f"\n{emoji} ID {detalhe['id_cenario']}: {detalhe['nome_cenario']}")
        print(f"   Roteiro Esperado: {detalhe['id_roteiro_esperado']}")
        
        if pd.notna(detalhe.get('id_roteiro_gerado')):
            print(f"   Roteiro Gerado: {detalhe['id_roteiro_gerado']}")
            print(f"   Valor: R$ {detalhe.get('valor_evento', 'N/A')}")
        
        print(f"   Status: {status}")


def exemplo_massa_grande():
    """Exemplo 2: Processamento em massa com muitos registros."""
    print("\n\n" + "="*70)
    print("EXEMPLO 2: Processamento em Massa")
    print("="*70)
    
    print("\n🔄 Gerando 500 cenários...")
    
    # Template grande
    roteiros = [100, 110, 120, 200, 210, 300, 310]
    template = pd.DataFrame({
        'id_cenario': range(1, 501),
        'nome_cenario': [f'Processamento {i}' for i in range(1, 501)],
        'id_roteiro_esperado': [roteiros[i % len(roteiros)] for i in range(500)]
    })
    
    # Snapshot com 90% sensibilização e 95% acurácia
    sensibilizados = int(500 * 0.90)
    acurados = int(sensibilizados * 0.95)
    
    ids_snap = list(range(1, sensibilizados + 1))
    roteiros_gerados = []
    
    for i in range(sensibilizados):
        roteiro_esperado = template.iloc[i]['id_roteiro_esperado']
        if i < acurados:
            roteiros_gerados.append(roteiro_esperado)
        else:
            # Divergente
            roteiros_gerados.append(999)
    
    snapshot = pd.DataFrame({
        'id_origem': ids_snap,
        'id_roteiro_gerado': roteiros_gerados,
        'segmento_carteira': ['MATRIZ'] * len(ids_snap),
        'valor_evento': [1000 + i*10 for i in range(len(ids_snap))]
    })
    
    print(f"✓ Template: {len(template)} registros")
    print(f"✓ Snapshot: {len(snapshot)} registros")
    
    # Processar
    with tempfile.TemporaryDirectory() as tmpdir:
        template_file = os.path.join(tmpdir, "template.csv")
        snapshot_file = os.path.join(tmpdir, "snapshot.csv")
        
        template.to_csv(template_file, index=False)
        snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_t, open(snapshot_file, 'rb') as f_s:
            f_t.filename = "template.csv"
            f_s.filename = "snapshot.csv"
            resultado = ReconciliadorEngine.processar(f_t, f_s)
    
    print("\n📊 RESULTADO:")
    print(f"✓ Acurácia: {resultado['metricas']['acuracia']}%")
    print(f"✓ Tempo: {resultado['metricas']['tempo']}s")
    
    print(f"\n📈 Distribuição:")
    for status, count in resultado['grafico'].items():
        pct = (count / 500) * 100
        print(f"  {status}: {count} ({pct:.1f}%)")


def exemplo_analise_divergencias():
    """Exemplo 3: Análise detalhada de divergências."""
    print("\n\n" + "="*70)
    print("EXEMPLO 3: Análise de Divergências")
    print("="*70)
    
    # Cenário com múltiplas divergências
    template = pd.DataFrame({
        'id_cenario': [1, 2, 3, 4, 5, 6],
        'nome_cenario': ['A', 'B', 'C', 'D', 'E', 'F'],
        'id_roteiro_esperado': [100, 200, 300, 400, 500, 600]
    })
    
    snapshot = pd.DataFrame({
        'id_origem': [1, 2, 3, 4, 5],  # Falta ID 6
        'id_roteiro_gerado': [100, 999, 300, 999, 500],  # IDs 2 e 4 divergentes
        'segmento_carteira': ['SEG_A', 'SEG_B', 'SEG_C', 'SEG_D', 'SEG_E'],
        'valor_evento': [1000, 2000, 3000, 4000, 5000]
    })
    
    # Processar
    with tempfile.TemporaryDirectory() as tmpdir:
        template_file = os.path.join(tmpdir, "template.csv")
        snapshot_file = os.path.join(tmpdir, "snapshot.csv")
        
        template.to_csv(template_file, index=False)
        snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_t, open(snapshot_file, 'rb') as f_s:
            f_t.filename = "template.csv"
            f_s.filename = "snapshot.csv"
            resultado = ReconciliadorEngine.processar(f_t, f_s)
    
    print("\n🔍 DIVERGÊNCIAS ENCONTRADAS:")
    
    divergentes = [d for d in resultado['detalhes'] 
                   if d['status_homologacao'] == 'Divergente']
    
    for div in divergentes:
        print(f"\n⚠️  ID {div['id_cenario']}: {div['nome_cenario']}")
        print(f"   Esperado: {div['id_roteiro_esperado']}")
        print(f"   Gerado: {div['id_roteiro_gerado']}")
        print(f"   Segmento: {div.get('segmento_carteira', 'N/A')}")
    
    nao_sensibilizados = [d for d in resultado['detalhes'] 
                          if d['status_homologacao'] == 'Não Sensibilizado']
    
    if nao_sensibilizados:
        print(f"\n\n✗ NÃO SENSIBILIZADOS (órfãos):")
        for orfen in nao_sensibilizados:
            print(f"   ID {orfen['id_cenario']}: {orfen['nome_cenario']}")


def main():
    """Executa todos os exemplos."""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█  EXEMPLOS PRÁTICOS - PIPELINE DE HOMOLOGAÇÃO DE ROTEIROS" + " " * 9 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    try:
        exemplo_simples()
        exemplo_massa_grande()
        exemplo_analise_divergencias()
        
        print("\n\n" + "="*70)
        print("✅ TODOS OS EXEMPLOS EXECUTADOS COM SUCESSO")
        print("="*70)
        print("\n💡 Dicas:")
        print("  1. Customize os dados conforme sua necessidade")
        print("  2. Use ReconciliadorEngine.processar() em seu código")
        print("  3. Acesse resultado['metricas'] para KPIs")
        print("  4. Acesse resultado['detalhes'] para análise linha a linha")
        print("  5. Acesse resultado['grafico'] para visualizações")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())

"""
Testes Unitários e de Integração - Pipeline de Homologação de Roteiros
=======================================================================

Suite de testes para validar a funcionalidade do motor de conciliação
de roteiros usando nomenclatura universal em Engenharia de Dados.
"""

import pytest
import pandas as pd
import io
import json
import os
import sys
from pathlib import Path

# Adicionar o diretório pai ao path para importar o app
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app, ReconciliadorEngine


class TestReconciliadorEngineAcademico:
    """Testes unitários para a classe ReconciliadorEngine com nomenclatura acadêmica."""

    @pytest.fixture
    def df_template_expectativa_exemplo(self):
        """Cria um DataFrame exemplo para template de roteiros esperados."""
        return pd.DataFrame({
            'id_cenario': [1, 2, 3, 4, 5],
            'nome_cenario': [
                'Folha Padrão 1',
                'Folha Padrão 2',
                'Folha Especial 1',
                'Folha Especial 2',
                'Folha Bônus'
            ],
            'id_roteiro_esperado': [100, 110, 200, 210, 300]
        })

    @pytest.fixture
    def df_snapshot_processado_exemplo(self):
        """Cria um DataFrame exemplo para snapshot do processamento realizado."""
        return pd.DataFrame({
            'id_origem': [1, 2, 3, 5],
            'segmento_carteira': ['MATRIZ', 'FILIAL_SP', 'FILIAL_MG', 'DISTRIBUIÇÃO'],
            'id_roteiro_gerado': [100, 110, 200, 300],
            'valor_evento': [1000.00, 2000.00, 3000.00, 5000.00]
        })

    @pytest.fixture
    def csv_template_arquivo(self, tmp_path, df_template_expectativa_exemplo):
        """Cria um arquivo CSV temporário com template de expectativa."""
        csv_file = tmp_path / "template_expectativa.csv"
        df_template_expectativa_exemplo.to_csv(csv_file, index=False, encoding='utf-8')
        return open(csv_file, 'rb')

    @pytest.fixture
    def csv_snapshot_arquivo(self, tmp_path, df_snapshot_processado_exemplo):
        """Cria um arquivo CSV temporário com snapshot de processamento."""
        csv_file = tmp_path / "snapshot_processado.csv"
        df_snapshot_processado_exemplo.to_csv(csv_file, index=False, encoding='utf-8')
        return open(csv_file, 'rb')

    def test_ler_arquivo_csv_utf8(self, csv_template_arquivo):
        """Testa leitura de arquivo CSV em UTF-8."""
        csv_template_arquivo.filename = "template_expectativa.csv"
        df = ReconciliadorEngine.ler_arquivo(csv_template_arquivo)
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert 'id_cenario' in df.columns
        assert 'id_roteiro_esperado' in df.columns

    def test_ler_arquivo_csv_latin1(self, tmp_path):
        """Testa leitura de arquivo CSV em Latin-1 (codificação comum em sistemas legados)."""
        df_teste = pd.DataFrame({
            'id_cenario': [1],
            'nome_cenario': ['Folha com Acentuação'],
            'id_roteiro_esperado': [100]
        })
        csv_file = tmp_path / "template_latin1.csv"
        df_teste.to_csv(csv_file, index=False, encoding='latin-1')
        
        with open(csv_file, 'rb') as f:
            f.filename = "template_latin1.csv"
            df = ReconciliadorEngine.ler_arquivo(f)
        
        assert len(df) == 1
        assert 'Acentuação' in str(df.values)

    def test_ler_arquivo_extensao_invalida(self, tmp_path):
        """Testa erro ao ler arquivo com extensão não suportada."""
        invalid_file = tmp_path / "dados_invalidos.txt"
        invalid_file.write_text("dados inválidos")
        
        with open(invalid_file, 'rb') as f:
            f.filename = "dados_invalidos.txt"
            with pytest.raises(ValueError, match="Formato de arquivo não suportado"):
                ReconciliadorEngine.ler_arquivo(f)

    def test_processar_sucesso_completo(self, csv_template_arquivo, csv_snapshot_arquivo):
        """Testa processamento bem-sucedido com dados válidos."""
        csv_template_arquivo.filename = "template_expectativa.csv"
        csv_snapshot_arquivo.filename = "snapshot_processado.csv"
        
        resultado = ReconciliadorEngine.processar(csv_template_arquivo, csv_snapshot_arquivo)
        
        # Validar estrutura do retorno
        assert 'detalhes' in resultado
        assert 'metricas' in resultado
        assert 'grafico' in resultado
        
        # Validar métricas
        metricas = resultado['metricas']
        assert 'acuracia' in metricas
        assert 'tempo' in metricas
        assert 'total' in metricas
        assert 0 <= metricas['acuracia'] <= 100
        assert metricas['total'] == 5

    def test_status_homologacao_classificacao(self, csv_template_arquivo, csv_snapshot_arquivo):
        """Testa se a classificação de status_homologacao está correta."""
        csv_template_arquivo.filename = "template_expectativa.csv"
        csv_snapshot_arquivo.filename = "snapshot_processado.csv"
        
        resultado = ReconciliadorEngine.processar(csv_template_arquivo, csv_snapshot_arquivo)
        detalhes = resultado['detalhes']
        
        # Verificar que todos têm status_homologacao
        for item in detalhes:
            assert 'status_homologacao' in item
            assert item['status_homologacao'] in [
                'Sensibilizado com Sucesso',
                'Divergente',
                'Não Sensibilizado'
            ]
        
        # Validar contagens esperadas
        status_count = resultado['grafico']
        assert 'Sensibilizado com Sucesso' in status_count

    def test_processar_colunas_obrigatorias_template(self, tmp_path, csv_snapshot_arquivo):
        """Testa erro quando colunas obrigatórias faltam no TemplateExpectativa."""
        df_incompleto = pd.DataFrame({
            'id_cenario': [1],
            'nome_cenario': ['Teste']
        })
        csv_file = tmp_path / "template_incompleto.csv"
        df_incompleto.to_csv(csv_file, index=False)
        
        with open(csv_file, 'rb') as f:
            f.filename = "template_incompleto.csv"
            csv_snapshot_arquivo.filename = "snapshot_processado.csv"
            
            with pytest.raises(ValueError, match="TemplateExpectativa incompleto"):
                ReconciliadorEngine.processar(f, csv_snapshot_arquivo)

    def test_processar_colunas_obrigatorias_snapshot(self, tmp_path, csv_template_arquivo):
        """Testa erro quando colunas obrigatórias faltam no SnapshotProcessado."""
        df_incompleto = pd.DataFrame({
            'id_origem': [1]
        })
        csv_file = tmp_path / "snapshot_incompleto.csv"
        df_incompleto.to_csv(csv_file, index=False)
        
        with open(csv_file, 'rb') as f:
            csv_template_arquivo.filename = "template_expectativa.csv"
            f.filename = "snapshot_incompleto.csv"
            
            with pytest.raises(ValueError, match="SnapshotProcessado incompleto"):
                ReconciliadorEngine.processar(csv_template_arquivo, f)

    def test_processar_sanitizacao_nomes_coluna(self, tmp_path):
        """Testa se os nomes de coluna são sanitizados (lowercase, sem espaços)."""
        df_template = pd.DataFrame({
            '  ID_Cenario  ': [1],
            ' Nome_Cenario ': ['Teste'],
            'ID_Roteiro_Esperado': [100]
        })
        df_snapshot = pd.DataFrame({
            ' ID_Origem ': [1],
            'ID_Roteiro_Gerado': [100],
            'Valor_Evento': [1000]
        })
        
        template_file = tmp_path / "template_dirty.csv"
        snapshot_file = tmp_path / "snapshot_dirty.csv"
        df_template.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
            f_template.filename = "template_dirty.csv"
            f_snapshot.filename = "snapshot_dirty.csv"
            
            resultado = ReconciliadorEngine.processar(f_template, f_snapshot)
            assert 'detalhes' in resultado

    def test_processar_acuracia_100_porcento(self, tmp_path):
        """Testa cenário onde todos os roteiros têm sucesso (100% acurácia)."""
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
        
        template_file = tmp_path / "template_perfeito.csv"
        snapshot_file = tmp_path / "snapshot_perfeito.csv"
        df_template.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
            f_template.filename = "template_perfeito.csv"
            f_snapshot.filename = "snapshot_perfeito.csv"
            
            resultado = ReconciliadorEngine.processar(f_template, f_snapshot)
            assert resultado['metricas']['acuracia'] == 100.0

    def test_processar_acuracia_zero_porcento(self, tmp_path):
        """Testa cenário onde nenhum roteiro tem sucesso (0% acurácia)."""
        df_template = pd.DataFrame({
            'id_cenario': [1, 2],
            'nome_cenario': ['A', 'B'],
            'id_roteiro_esperado': [100, 200]
        })
        df_snapshot = pd.DataFrame({
            'id_origem': [1, 2],
            'id_roteiro_gerado': [999, 999],
            'segmento_carteira': ['MATRIZ', 'FILIAL'],
            'valor_evento': [1000, 2000]
        })
        
        template_file = tmp_path / "template_divergente.csv"
        snapshot_file = tmp_path / "snapshot_divergente.csv"
        df_template.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
            f_template.filename = "template_divergente.csv"
            f_snapshot.filename = "snapshot_divergente.csv"
            
            resultado = ReconciliadorEngine.processar(f_template, f_snapshot)
            assert resultado['metricas']['acuracia'] == 0.0

    def test_processar_nao_sensibilizado(self, tmp_path):
        """Testa caso onde registros não são sensibilizados (orphans no join)."""
        df_template = pd.DataFrame({
            'id_cenario': [1, 2, 3, 4],
            'nome_cenario': ['A', 'B', 'C', 'D'],
            'id_roteiro_esperado': [100, 200, 300, 400]
        })
        df_snapshot = pd.DataFrame({
            'id_origem': [1, 2, 3],
            'id_roteiro_gerado': [100, 200, 300],
            'segmento_carteira': ['MATRIZ', 'FILIAL', 'MATRIZ'],
            'valor_evento': [1000, 2000, 3000]
        })
        
        template_file = tmp_path / "template_parcial.csv"
        snapshot_file = tmp_path / "snapshot_parcial.csv"
        df_template.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
            f_template.filename = "template_parcial.csv"
            f_snapshot.filename = "snapshot_parcial.csv"
            
            resultado = ReconciliadorEngine.processar(f_template, f_snapshot)
            
            grafico = resultado['grafico']
            assert 'Não Sensibilizado' in grafico
            assert grafico['Não Sensibilizado'] == 1
            assert resultado['metricas']['acuracia'] == 75.0

    def test_processar_roteiros_como_float(self, tmp_path):
        """Testa se roteiros lidos como float são comparados corretamente."""
        df_template = pd.DataFrame({
            'id_cenario': [1],
            'nome_cenario': ['Teste'],
            'id_roteiro_esperado': [100.0]
        })
        df_snapshot = pd.DataFrame({
            'id_origem': [1],
            'id_roteiro_gerado': [100],
            'segmento_carteira': ['MATRIZ'],
            'valor_evento': [1000]
        })
        
        template_file = tmp_path / "template_float.csv"
        snapshot_file = tmp_path / "snapshot_float.csv"
        df_template.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
            f_template.filename = "template_float.csv"
            f_snapshot.filename = "snapshot_float.csv"
            
            resultado = ReconciliadorEngine.processar(f_template, f_snapshot)
            assert resultado['metricas']['acuracia'] == 100.0


class TestFlaskAppAcademico:
    """Testes de integração para as rotas Flask com nomenclatura acadêmica."""

    @pytest.fixture
    def client(self):
        """Cria um cliente Flask para testes."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_index_get(self, client):
        """Testa GET na rota index."""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'html' in response.data.lower() or b'<!doctype' in response.data.lower()

    def test_index_post_sem_arquivos(self, client):
        """Testa POST na rota index sem arquivos."""
        response = client.post('/', data={})
        
        assert response.status_code == 200
        assert b'arquivo' in response.data.lower()

    def test_index_post_um_arquivo_faltando(self, client, tmp_path):
        """Testa POST com apenas um arquivo."""
        csv_file = tmp_path / "teste.csv"
        pd.DataFrame({
            'id_cenario': [1],
            'nome_cenario': ['A'],
            'id_roteiro_esperado': [100]
        }).to_csv(csv_file, index=False)
        
        with open(csv_file, 'rb') as f:
            response = client.post('/', data={'file_template_expectativa': (f, 'teste.csv')})
        
        assert response.status_code == 200
        assert b'arquivo' in response.data.lower()

    def test_index_post_com_arquivos_validos(self, client, tmp_path):
        """Testa POST com arquivos válidos."""
        df_template = pd.DataFrame({
            'id_cenario': [1, 2],
            'nome_cenario': ['A', 'B'],
            'id_roteiro_esperado': [100, 200]
        })
        df_snapshot = pd.DataFrame({
            'id_origem': [1, 2],
            'id_roteiro_gerado': [100, 200],
            'segmento_carteira': ['MATRIZ', 'FILIAL'],
            'valor_evento': [1000, 2000]
        })
        
        template_file = tmp_path / "template.csv"
        snapshot_file = tmp_path / "snapshot.csv"
        df_template.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
            response = client.post('/', data={
                'file_template_expectativa': (f_template, 'template.csv'),
                'file_snapshot_processado': (f_snapshot, 'snapshot.csv')
            })
        
        assert response.status_code == 200

    def test_index_post_arquivo_formato_invalido(self, client, tmp_path):
        """Testa POST com arquivo em formato inválido."""
        invalid_file = tmp_path / "invalido.txt"
        invalid_file.write_text("dados inválidos")
        
        csv_file = tmp_path / "snapshot.csv"
        pd.DataFrame({
            'id_origem': [1],
            'id_roteiro_gerado': [100]
        }).to_csv(csv_file, index=False)
        
        with open(invalid_file, 'rb') as f_invalid, open(csv_file, 'rb') as f_csv:
            response = client.post('/', data={
                'file_template_expectativa': (f_invalid, 'invalido.txt'),
                'file_snapshot_processado': (f_csv, 'snapshot.csv')
            })
        
        assert response.status_code == 200
        assert b'erro' in response.data.lower() or b'nao suportado' in response.data.lower()

    def test_download_template_expectativa(self, client):
        """Testa download do template de expectativa."""
        response = client.get('/download_template/template')
        
        assert response.status_code == 200
        assert 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in response.content_type

    def test_download_snapshot_processado(self, client):
        """Testa download do snapshot processado."""
        response = client.get('/download_template/snapshot')
        
        assert response.status_code == 200
        assert 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in response.content_type


class TestIntegracaoCompleta:
    """Testes de integração completos do pipeline de homologação."""

    def test_fluxo_homologacao_completo(self, tmp_path):
        """Testa o fluxo completo: upload → processamento → resultado de homologação."""
        
        df_template = pd.DataFrame({
            'id_cenario': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'nome_cenario': [
                'Processamento Folha 1', 'Processamento Folha 2', 'Processamento Folha 3',
                'Folha Especial 1', 'Folha Especial 2', 'Folha Bônus 1',
                'Processamento Folha 4', 'Processamento Folha 5', 'Folha Especial 3',
                'Folha Bônus 2'
            ],
            'id_roteiro_esperado': [100, 110, 100, 200, 200, 300, 100, 110, 200, 300]
        })
        
        df_snapshot = pd.DataFrame({
            'id_origem': [1, 2, 3, 4, 5, 7, 8, 9],
            'segmento_carteira': ['MATRIZ', 'FILIAL_SP', 'FILIAL_MG', 'MATRIZ', 'FILIAL_RJ', 'MATRIZ', 'FILIAL_SP', 'FILIAL_MG'],
            'id_roteiro_gerado': [100, 110, 100, 200, 999, 100, 110, 200],
            'valor_evento': [1000, 2000, 1500, 3000, 2500, 1200, 2200, 3100]
        })
        
        template_file = tmp_path / "template.csv"
        snapshot_file = tmp_path / "snapshot.csv"
        df_template.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
            f_template.filename = "template.csv"
            f_snapshot.filename = "snapshot.csv"
            resultado = ReconciliadorEngine.processar(f_template, f_snapshot)
        
        metricas = resultado['metricas']
        assert metricas['total'] == 10
        assert metricas['acuracia'] == 70.0
        
        grafico = resultado['grafico']
        assert grafico['Sensibilizado com Sucesso'] == 7
        assert grafico['Divergente'] == 1
        assert grafico['Não Sensibilizado'] == 2
        
        detalhes = resultado['detalhes']
        assert len(detalhes) == 10

    def test_fluxo_100_nao_sensibilizado(self, tmp_path):
        """Testa cenário onde nenhum registro é sensibilizado."""
        
        df_template = pd.DataFrame({
            'id_cenario': [1, 2, 3],
            'nome_cenario': ['A', 'B', 'C'],
            'id_roteiro_esperado': [100, 200, 300]
        })
        
        df_snapshot = pd.DataFrame({
            'id_origem': pd.Series([], dtype=int),
            'id_roteiro_gerado': pd.Series([], dtype=int),
            'segmento_carteira': pd.Series([], dtype=str),
            'valor_evento': pd.Series([], dtype=float)
        })
        
        template_file = tmp_path / "template_vazio.csv"
        snapshot_file = tmp_path / "snapshot_vazio.csv"
        df_template.to_csv(template_file, index=False)
        df_snapshot.to_csv(snapshot_file, index=False)
        
        with open(template_file, 'rb') as f_template, open(snapshot_file, 'rb') as f_snapshot:
            f_template.filename = "template_vazio.csv"
            f_snapshot.filename = "snapshot_vazio.csv"
            resultado = ReconciliadorEngine.processar(f_template, f_snapshot)
        
        assert resultado['metricas']['acuracia'] == 0.0
        assert resultado['grafico']['Não Sensibilizado'] == 3


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

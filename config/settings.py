from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURAÇÕES
# ============================================================

AGUARDAR_NOVA_EXPORTACAO = False

# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

PASTA_BASE = BASE_DIR / "base"
PASTA_RESULTADOS = BASE_DIR / "resultados"
PASTA_RAW = BASE_DIR / "data" / "raw"
PASTA_CONTROLE = BASE_DIR / "data" / "controle"

ARQUIVO_CSV = PASTA_BASE / "base.csv"

ARQUIVO_CONTROLE = PASTA_CONTROLE / "ultima_base_processada.txt"

# ============================================================
# ARQUIVO DE SAÍDA
# ============================================================

def obter_arquivo_saida() -> Path:
    """
    Retorna o caminho completo do relatório da execução atual.
    O arquivo terá data e hora no nome.
    """

    PASTA_RESULTADOS.mkdir(
        parents=True,
        exist_ok=True,
    )

    data_hora = datetime.now().strftime("%Y%m%d_%H%M%S")

    return PASTA_RESULTADOS / f"consulta_instalacoes_{data_hora}.xlsx"


# ============================================================
# MAPEAMENTO DE COLUNAS
# ============================================================

MAPEAMENTO_COLUNAS = {
    "PROCESSO": "PROCESSO",
    "CENTRO_DE_TRABALHO": "CENTRO_DE_TRABALHO",
    "UNIDADE_LEITURA": "ROTEIRO_DE_LEITURA",
    "LOCALIDADE": "LOCALIDADE",
    "UT": "UT",
    "LOTE": "LOTE",
    "CLASSE_COMPLETA": "CLASSE_SUBCLASSE",
    "ENDERECO": "ENDERECO",
    "NOME": "NOME",
    "INSTALACAO": "INSTALACAO",
    "NOTA_SERVICO": "NOTA_SERVICO",
    "DATA_CRIACAO_NS": "DATA_CRIACAO_NOTA",
    "DATA_CONC_ACAO": "DATA_CONCLUSAO",
    "RESPONSAVEL": "RESPONSAVEL",
    "ACAO_CRIADA": "SERVICO_EXECUTADO",
    "TIPO_NOTA_NS": "TIPO_DE_NOTA",
    "STATUS_CURTO": "STATUS",
    "OBSERVACAO": "OBS_REJE_EXEC",
}


# ============================================================
# COLUNAS QUE AINDA SERÃO PREENCHIDAS
# ============================================================

COLUNAS_PENDENTES = [
    "AREA",
    "DATA_LIGACAO",
    "CATEGORIA",
    "CLIENTE_CORPORATIVO",
    "GESTOR_RESPONSAVEL",
    "STATUS_INSTALACAO",
    "PN",
    "ENTRADA",
    "NOTA_GERADA",
    "OBSERVACAO_STATUS",
    "OBS_COMPLEMENTAR",
    "ANALISES_E_INFORMACOES",
    "CENTRO_DO_TRABALHO",
    "ML21",
    "MED_INST",
    "MEDIDOR_COM_DEFEITO",
    "TIPO_MED",
    "CLASSIFICACAO",
    "CONTRATO",
]


# ============================================================
# ORDEM FINAL DAS COLUNAS
# ============================================================

ORDEM_COLUNAS = [
    "PROCESSO",
    "CENTRO_DE_TRABALHO",
    "ROTEIRO_DE_LEITURA",
    "LOCALIDADE",
    "AREA",
    "UT",
    "DATA_LIGACAO",
    "CLASSE_SUBCLASSE",
    "CATEGORIA",
    "LOTE",
    "ENDERECO",
    "CLIENTE_CORPORATIVO",
    "GESTOR_RESPONSAVEL",
    "STATUS_INSTALACAO",
    "PN",
    "NOME",
    "DATA_CRIACAO_NOTA",
    "ENTRADA",
    "NOTA_GERADA",
    "OBSERVACAO_STATUS",
    "OBS_COMPLEMENTAR",
    "ANALISES_E_INFORMACOES",
    "INSTALACAO",
    "NOTA_SERVICO",
    "DATA_CONCLUSAO",
    "RESPONSAVEL",
    "CENTRO_DO_TRABALHO",
    "SERVICO_EXECUTADO",
    "TIPO_DE_NOTA",
    "STATUS",
    "OBS_REJE_EXEC",
    "ML21",
    "MED_INST",
    "MEDIDOR_COM_DEFEITO",
    "TIPO_MED",
    "CLASSIFICACAO",
    "CONTRATO",
]
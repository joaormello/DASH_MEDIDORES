from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

PASTA_BASE = BASE_DIR / "base"
PASTA_RAW = BASE_DIR / "data" / "raw"

ARQUIVO_CSV = PASTA_BASE / "base.csv"
ARQUIVO_SAIDA = PASTA_BASE / "consulta_instalacoes.xlsx"


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


ORDEM_COLUNAS = [
    # A
    "PROCESSO",

    # B
    "CENTRO_DE_TRABALHO",

    # C
    "ROTEIRO_DE_LEITURA",

    # D
    "LOCALIDADE",

    # E
    "AREA",

    # F
    "UT",

    # G
    "DATA_LIGACAO",

    # H
    "CLASSE_SUBCLASSE",

    # I
    "CATEGORIA",

    # J
    "LOTE",

    # K
    "ENDERECO",

    # L
    "CLIENTE_CORPORATIVO",

    # M
    "GESTOR_RESPONSAVEL",

    # N
    "STATUS_INSTALACAO",

    # O
    "PN",

    # P
    "NOME",

    # Q
    "DATA_CRIACAO_NOTA",

    # R
    "ENTRADA",

    # S
    "NOTA_GERADA",

    # T
    "OBSERVACAO_STATUS",

    # U
    "OBS_COMPLEMENTAR",

    # V
    "ANALISES_E_INFORMACOES",

    # W
    "INSTALACAO",

    # X
    "NOTA_SERVICO",

    # Y
    "DATA_CONCLUSAO",

    # Z
    "RESPONSAVEL",

    # AA
    "CENTRO_DO_TRABALHO",

    # AB
    "SERVICO_EXECUTADO",

    # AC
    "TIPO_DE_NOTA",

    # AD
    "STATUS",

    # AE
    "OBS_REJE_EXEC",

    # AF
    "ML21",

    # AG
    "MED_INST",

    # AH
    "MEDIDOR_COM_DEFEITO",

    # AI
    "TIPO_MED",

    # AJ
    "CLASSIFICACAO",

    # AK
    "CONTRATO",
]
from pathlib import Path
from services.excel_service import obter_instalacoes_gera_nota_modifica

import pandas as pd


# ============================================================
# CONFIGURAÇÕES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

ARQUIVO_CSV = BASE_DIR / "base" / "base.csv"

ARQUIVO_SAIDA = BASE_DIR / "base" / "consulta_instalacoes.xlsx"

# definindo a lista de instalações
lista_instalacoes = obter_instalacoes_gera_nota_modifica()

# Informe aqui as instalações que deseja consultar.
# Mantenha entre aspas para preservar zeros à esquerda.
INSTALACOES_BUSCADAS = lista_instalacoes


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def normalizar_instalacao(valor) -> str:
    """
    Padroniza o número da instalação para facilitar a comparação.

    Exemplos:
    123456.0 -> 123456
    ' 00123456 ' -> 00123456
    """
    if pd.isna(valor):
        return ""

    valor = str(valor).strip()

    if valor.endswith(".0"):
        valor = valor[:-2]

    return valor


def ler_arquivo_csv(caminho: Path) -> pd.DataFrame:
    """
    Tenta ler o CSV usando diferentes combinações de encoding
    e separador.

    Retorna o DataFrame assim que encontra uma leitura válida.
    """

    tentativas = [
        {"encoding": "utf-16", "sep": "\t"},
        {"encoding": "utf-16-le", "sep": "\t"},
        {"encoding": "utf-16-be", "sep": "\t"},
        {"encoding": "utf-16", "sep": ";"},
        {"encoding": "utf-16", "sep": ","},
        {"encoding": "utf-8-sig", "sep": ";"},
        {"encoding": "utf-8-sig", "sep": ","},
        {"encoding": "latin-1", "sep": ";"},
        {"encoding": "latin-1", "sep": ","},
        {"encoding": "cp1252", "sep": ";"},
        {"encoding": "cp1252", "sep": ","},
    ]

    erros = []

    for tentativa in tentativas:
        encoding = tentativa["encoding"]
        separador = tentativa["sep"]

        try:
            df_teste = pd.read_csv(
                caminho,
                sep=separador,
                encoding=encoding,
                dtype=str,
                low_memory=False,
            )

            # Uma leitura válida deve ter mais de uma coluna
            if len(df_teste.columns) > 1:
                print("\nArquivo lido com sucesso.")
                print(f"Encoding utilizado: {encoding}")
                print(f"Separador utilizado: {repr(separador)}")
                print(f"Quantidade de linhas: {len(df_teste)}")
                print(f"Quantidade de colunas: {len(df_teste.columns)}")

                return df_teste

        except (
            UnicodeDecodeError,
            pd.errors.ParserError,
            UnicodeError,
            ValueError,
        ) as erro:
            erros.append(
                f"Encoding={encoding}, separador={repr(separador)}: {erro}"
            )

    mensagem_erros = "\n".join(erros)

    raise RuntimeError(
        "Não foi possível ler o arquivo CSV com os formatos testados.\n\n"
        f"Tentativas realizadas:\n{mensagem_erros}"
    )


def ajustar_largura_colunas(planilha) -> None:
    """
    Ajusta a largura das colunas da planilha do Excel.
    """

    for coluna in planilha.columns:
        maior_tamanho = 0
        letra_coluna = coluna[0].column_letter

        for celula in coluna:
            valor = "" if celula.value is None else str(celula.value)
            maior_tamanho = max(maior_tamanho, len(valor))

        planilha.column_dimensions[letra_coluna].width = min(
            maior_tamanho + 2,
            50,
        )


# ============================================================
# VALIDAÇÕES INICIAIS
# ============================================================

if not ARQUIVO_CSV.exists():
    raise FileNotFoundError(
        f"O arquivo CSV não foi encontrado:\n{ARQUIVO_CSV}"
    )

ARQUIVO_SAIDA.parent.mkdir(
    parents=True,
    exist_ok=True,
)

print(f"Lendo arquivo:\n{ARQUIVO_CSV}")


# ============================================================
# LEITURA DO CSV
# ============================================================

df = ler_arquivo_csv(ARQUIVO_CSV)


# ============================================================
# LIMPEZA DOS NOMES DAS COLUNAS
# ============================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
    .str.replace("\ufeff", "", regex=False)
)

print("\nColunas encontradas:")
print(df.columns.tolist())


# ============================================================
# VALIDAÇÃO DA COLUNA INSTALAÇÃO
# ============================================================

if "INSTALACAO" not in df.columns:
    raise KeyError(
        "A coluna 'INSTALACAO' não foi encontrada no arquivo.\n\n"
        f"Colunas disponíveis:\n{df.columns.tolist()}"
    )


# ============================================================
# NORMALIZAÇÃO DAS INSTALAÇÕES
# ============================================================

df["INSTALACAO"] = df["INSTALACAO"].apply(
    normalizar_instalacao
)

instalacoes_normalizadas = [
    normalizar_instalacao(instalacao)
    for instalacao in INSTALACOES_BUSCADAS
]

# Remove valores vazios e duplicados da lista
instalacoes_normalizadas = list(
    dict.fromkeys(
        instalacao
        for instalacao in instalacoes_normalizadas
        if instalacao
    )
)

if not instalacoes_normalizadas:
    raise ValueError(
        "Nenhuma instalação válida foi informada em "
        "'INSTALACOES_BUSCADAS'."
    )


# ============================================================
# FILTRO DAS INSTALAÇÕES
# ============================================================

resultado = df[
    df["INSTALACAO"].isin(instalacoes_normalizadas)
].copy()


# ============================================================
# MANTER SOMENTE UMA LINHA POR INSTALAÇÃO
# ============================================================

if "DATA_CRIACAO_NS" in resultado.columns:
    resultado["_DATA_ORDENACAO"] = pd.to_datetime(
        resultado["DATA_CRIACAO_NS"],
        dayfirst=True,
        errors="coerce",
    )

    # A linha com a data de criação mais recente fica primeiro
    resultado = resultado.sort_values(
        by=["INSTALACAO", "_DATA_ORDENACAO"],
        ascending=[True, False],
        na_position="last",
    )

    # Mantém apenas uma ocorrência para cada instalação
    resultado = resultado.drop_duplicates(
        subset=["INSTALACAO"],
        keep="first",
    )

    resultado = resultado.drop(
        columns=["_DATA_ORDENACAO"]
    )

else:
    print(
        "\nA coluna DATA_CRIACAO_NS não foi encontrada. "
        "Será mantida a primeira ocorrência de cada instalação."
    )

    resultado = resultado.drop_duplicates(
        subset=["INSTALACAO"],
        keep="first",
    )


# ============================================================
# COLUNAS CONFIRMADAS
# ============================================================

mapeamento_colunas = {
    "INSTALACAO": "INSTALACAO",
    "CENTRO_DE_TRABALHO": "CENTRO_DE_TRABALHO",
    "UNIDADE_LEITURA": "ROTEIRO_DE_LEITURA",
    "LOCALIDADE": "LOCALIDADE",
    "UT": "UT",
    "LOTE": "LOTE",
    "CLASSE_COMPLETA": "CLASSE",
    "ENDERECO": "ENDERECO",
    "NOME": "NOME",
    "DATA_CRIACAO_NS": "DATA_CRIACAO_NOTA",
    "OBSERVACAO": "OBS_COMPLEMENTAR",
    "NOTA_SERVICO": "NOTA"
}


# ============================================================
# VERIFICAÇÃO DAS COLUNAS
# ============================================================

colunas_ausentes = [
    coluna
    for coluna in mapeamento_colunas
    if coluna not in resultado.columns
]

if colunas_ausentes:
    print("\nAtenção: algumas colunas não foram encontradas no CSV:")

    for coluna in colunas_ausentes:
        print(f"- {coluna}")


# Cria em branco as colunas confirmadas que não existirem
for coluna in mapeamento_colunas:
    if coluna not in resultado.columns:
        resultado[coluna] = ""


# ============================================================
# SELEÇÃO E RENOMEAÇÃO
# ============================================================

resultado_final = resultado[
    list(mapeamento_colunas.keys())
].rename(
    columns=mapeamento_colunas
)


# ============================================================
# COLUNAS PENDENTES
# ============================================================

colunas_pendentes = [
    "AREA",
    "DATA_LIGACAO",
    "SUBCLASSE",
    "CATEGORIA",
    "CLIENTE_CORPORATIVO",
    "PN",
    "ANALISES_E_INFORMACOES",
    "SERVICO_EXECUTADO",
]

for coluna in colunas_pendentes:
    resultado_final[coluna] = ""


# ============================================================
# ORDEM FINAL DAS COLUNAS
# ============================================================

ordem_colunas = [
    "INSTALACAO",
    "CENTRO_DE_TRABALHO",
    "ROTEIRO_DE_LEITURA",
    "LOCALIDADE",
    "AREA",
    "UT",
    "DATA_LIGACAO",
    "CLASSE",
    "SUBCLASSE",
    "CATEGORIA",
    "LOTE",
    "ENDERECO",
    "CLIENTE_CORPORATIVO",
    "PN",
    "NOME",
    "NOTA",
    "DATA_CRIACAO_NOTA",
    "OBS_COMPLEMENTAR",
    "ANALISES_E_INFORMACOES",
    "SERVICO_EXECUTADO",
]

resultado_final = resultado_final[
    ordem_colunas
]


# ============================================================
# ORDENAÇÃO POR INSTALAÇÃO
# ============================================================

resultado_final = resultado_final.sort_values(
    by="INSTALACAO",
    ascending=True,
).reset_index(drop=True)


# ============================================================
# INSTALAÇÕES NÃO ENCONTRADAS
# ============================================================

instalacoes_encontradas = set(
    resultado_final["INSTALACAO"]
    .dropna()
    .astype(str)
    .tolist()
)

instalacoes_nao_encontradas = [
    instalacao
    for instalacao in instalacoes_normalizadas
    if instalacao not in instalacoes_encontradas
]

df_nao_encontradas = pd.DataFrame(
    {
        "INSTALACAO_NAO_ENCONTRADA": instalacoes_nao_encontradas
    }
)


# ============================================================
# GERAÇÃO DO EXCEL
# ============================================================

try:
    with pd.ExcelWriter(
        ARQUIVO_SAIDA,
        engine="openpyxl",
    ) as writer:

        resultado_final.to_excel(
            writer,
            sheet_name="Resultado",
            index=False,
        )

        df_nao_encontradas.to_excel(
            writer,
            sheet_name="Nao encontradas",
            index=False,
        )

        # Ajusta a largura das colunas
        for nome_aba in writer.sheets:
            planilha = writer.sheets[nome_aba]

            ajustar_largura_colunas(planilha)

            # Congela o cabeçalho
            planilha.freeze_panes = "A2"

            # Ativa o filtro automático
            planilha.auto_filter.ref = planilha.dimensions

except PermissionError as erro:
    raise PermissionError(
        "Não foi possível salvar o arquivo Excel.\n"
        "Verifique se o arquivo já está aberto no Excel:\n"
        f"{ARQUIVO_SAIDA}"
    ) from erro


# ============================================================
# RESULTADO
# ============================================================

print("\nProcessamento concluído.")
print(
    f"Instalações solicitadas: "
    f"{len(instalacoes_normalizadas)}"
)
print(
    f"Registros encontrados: "
    f"{len(resultado_final)}"
)
print(
    f"Instalações não encontradas: "
    f"{len(instalacoes_nao_encontradas)}"
)
print(
    f"Arquivo gerado em:\n{ARQUIVO_SAIDA}"
)

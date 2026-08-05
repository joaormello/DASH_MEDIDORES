import pandas as pd

from config.settings import (
    COLUNAS_PENDENTES,
    MAPEAMENTO_COLUNAS,
    ORDEM_COLUNAS,
)
from utils.helpers import normalizar_instalacao


def normalizar_lista_instalacoes(instalacoes: list) -> list[str]:
    instalacoes_normalizadas = [
        normalizar_instalacao(instalacao)
        for instalacao in instalacoes
    ]

    return list(
        dict.fromkeys(
            instalacao
            for instalacao in instalacoes_normalizadas
            if instalacao
        )
    )


def filtrar_instalacoes(
    df: pd.DataFrame,
    instalacoes: list[str],
) -> pd.DataFrame:
    if "INSTALACAO" not in df.columns:
        raise KeyError(
            "A coluna 'INSTALACAO' não foi encontrada no CSV."
        )

    df = df.copy()

    df["INSTALACAO"] = df["INSTALACAO"].apply(
        normalizar_instalacao
    )

    return df[
        df["INSTALACAO"].isin(instalacoes)
    ].copy()


def manter_registro_mais_recente(
    resultado: pd.DataFrame,
) -> pd.DataFrame:
    if resultado.empty:
        return resultado

    if "DATA_CRIACAO_NS" not in resultado.columns:
        return resultado.drop_duplicates(
            subset=["INSTALACAO"],
            keep="first",
        )

    resultado = resultado.copy()

    resultado["_DATA_ORDENACAO"] = pd.to_datetime(
        resultado["DATA_CRIACAO_NS"],
        dayfirst=True,
        errors="coerce",
    )

    colunas_ordenacao = [
        "INSTALACAO",
        "_DATA_ORDENACAO",
    ]

    ordem_crescente = [
        True,
        False,
    ]

    if "NOTA_SERVICO" in resultado.columns:
        resultado["_NOTA_ORDENACAO"] = pd.to_numeric(
            resultado["NOTA_SERVICO"],
            errors="coerce",
        )

        colunas_ordenacao.append("_NOTA_ORDENACAO")
        ordem_crescente.append(False)

    resultado = resultado.sort_values(
        by=colunas_ordenacao,
        ascending=ordem_crescente,
        na_position="last",
    )

    resultado = resultado.drop_duplicates(
        subset=["INSTALACAO"],
        keep="first",
    )

    colunas_auxiliares = [
        coluna
        for coluna in [
            "_DATA_ORDENACAO",
            "_NOTA_ORDENACAO",
        ]
        if coluna in resultado.columns
    ]

    return resultado.drop(columns=colunas_auxiliares)


def montar_resultado_final(
    resultado: pd.DataFrame,
) -> pd.DataFrame:
    resultado = resultado.copy()

    for coluna in MAPEAMENTO_COLUNAS:
        if coluna not in resultado.columns:
            resultado[coluna] = ""

    resultado_final = resultado[
        list(MAPEAMENTO_COLUNAS.keys())
    ].rename(columns=MAPEAMENTO_COLUNAS)

    for coluna in COLUNAS_PENDENTES:
        resultado_final[coluna] = ""

    resultado_final = resultado_final[
        ORDEM_COLUNAS
    ]

    return resultado_final.sort_values(
        by="INSTALACAO",
        ascending=True,
    ).reset_index(drop=True)


def obter_instalacoes_nao_encontradas(
    resultado_final: pd.DataFrame,
    instalacoes_buscadas: list[str],
) -> pd.DataFrame:
    encontradas = set(
        resultado_final["INSTALACAO"]
        .dropna()
        .astype(str)
        .tolist()
    )

    nao_encontradas = [
        instalacao
        for instalacao in instalacoes_buscadas
        if instalacao not in encontradas
    ]

    return pd.DataFrame({
        "INSTALACAO_NAO_ENCONTRADA": nao_encontradas
    })
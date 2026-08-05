from pathlib import Path

import pandas as pd

from utils.helpers import limpar_nomes_colunas


def ler_arquivo_csv(caminho: Path) -> pd.DataFrame:
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
            df = pd.read_csv(
                caminho,
                sep=separador,
                encoding=encoding,
                dtype=str,
                low_memory=False,
            )

            if len(df.columns) > 1:
                print("\nArquivo CSV lido com sucesso.")
                print(f"Encoding: {encoding}")
                print(f"Separador: {repr(separador)}")
                print(f"Linhas: {len(df)}")
                print(f"Colunas: {len(df.columns)}")

                return limpar_nomes_colunas(df)

        except (
            UnicodeDecodeError,
            pd.errors.ParserError,
            UnicodeError,
            ValueError,
        ) as erro:
            erros.append(
                f"Encoding={encoding}, "
                f"separador={repr(separador)}: {erro}"
            )

    raise RuntimeError(
        "Não foi possível ler o CSV.\n\n"
        + "\n".join(erros)
    )
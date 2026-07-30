from pathlib import Path
import pandas as pd


def obter_instalacoes_gera_nota_modifica():
    BASE_DIR = Path(__file__).resolve().parent.parent
    PASTA_RAW = BASE_DIR / "data" / "raw"

    arquivo = next(PASTA_RAW.glob("*.xlsx"))

    df = pd.read_excel(arquivo, sheet_name="Base Geral")

    df_filtrado = df[df["Status Ação"] == "Gerar Nota Modifica"]

    lista_instalacoes = []

    for instalacao in df_filtrado["Instalação"]:
        instalacao = str(instalacao).strip().zfill(10)
        lista_instalacoes.append(instalacao)

    return lista_instalacoes
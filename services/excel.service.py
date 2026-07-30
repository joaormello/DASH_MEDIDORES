import pandas as pd 


arquivo = r"C:\Users\BR0459067248\Documents\dash_medidores\DASH_MEDIDORES\Cópia de Base Foto Validada_até 23.07.xlsx"
df = pd.read_excel(arquivo, sheet_name = "Base Geral")


def filtrar_gera_nota_modifica(df):
    return df[
        df["Status Ação"] == "Gerar Nota Modifica"
    ]

df_filtrado = filtrar_gera_nota_modifica(df)

lista_instalacoes = (

    df_filtrado["Instalação"]
    .tolist()
)

print(lista_instalacoes)
import pandas as pd 

def carregar_excel(caminho_arquivo, sheet_name):                #LE O EXCEL
    return pd.read_excel(caminho_arquivo, sheet_name= sheet_name)


def filtrar_gera_nota_modifica(df):     #FILTRA A COLUNA STATUS AÇÃO PARA ACHAR SOMENTE VALORES "GERAR NOTA MODIFICA"
    return df[

        df["Status Ação"] == "Gerar Nota Modifica"

    ]

def obter_instalacoes(df_filtrado):    #CRIA UMA LISTA COM OS VALORES DAS INSTALAÇÕES CUJA COLUNA É GERAR NOTA MODIFICA
    return(

        df_filtrado["Instalação"]
        .drop_duplicates()
        .astype(str)
        .tolist()

    )


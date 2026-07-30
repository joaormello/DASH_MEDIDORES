from config.settings import (ARQUIVO_EXCEL, SHEET_NAME)
from services.excel_service import carregar_excel, filtrar_gera_nota_modifica, obter_instalacoes 

def main():

    df = carregar_excel(ARQUIVO_EXCEL, SHEET_NAME)
    df_filtrado = filtrar_gera_nota_modifica(df)
    instalacoes = obter_instalacoes(df_filtrado)
    print(instalacoes)



if __name__ == "__main__":
    main()

from config.settings import (
    ARQUIVO_CSV,
    ARQUIVO_CONTROLE,
    obter_arquivo_saida,
    AGUARDAR_NOVA_EXPORTACAO
)

from services.excel_service import (
    obter_instalacoes_gera_nota_modifica,
)

from services.csv_service import (
    ler_arquivo_csv,
)

from services.arquivo_service import (
    esperar_nova_exportacao,
    salvar_ultima_execucao,
)

from services.consulta_service import (
    normalizar_lista_instalacoes,
    filtrar_instalacoes,
    manter_registro_mais_recente,
    montar_resultado_final,
    obter_instalacoes_nao_encontradas,
)

from services.exportacao_service import (
    exportar_resultado_excel,
)


def main() -> None:

    # =====================================================
    # ETAPA 1 - OBTER AS INSTALAÇÕES DA PLANILHA
    # =====================================================

    print("Buscando instalações na planilha...")

    lista_instalacoes = (
        obter_instalacoes_gera_nota_modifica()
    )

    if not lista_instalacoes:
        raise ValueError(
            "Nenhuma instalação com o status "
            "'Gerar Nota Modifica' foi encontrada."
        )

    print(
        f"{len(lista_instalacoes)} instalações "
        "encontradas na planilha."
    )


    # =====================================================
    # ETAPA 2 - NORMALIZAR AS INSTALAÇÕES
    # =====================================================

    instalacoes_normalizadas = normalizar_lista_instalacoes(
        lista_instalacoes
    )

    if not instalacoes_normalizadas:
        raise ValueError(
            "Nenhuma instalação válida foi encontrada "
            "após a normalização."
        )

    print(
        f"{len(instalacoes_normalizadas)} instalações "
        "válidas após a normalização."
    )


    # =====================================================
    # ETAPA 3 - AGUARDAR NOVA EXPORTAÇÃO (PRODUÇÃO)
    # =====================================================

    if AGUARDAR_NOVA_EXPORTACAO:

        print("\n[MODO DESENVOLVIMENTO]")
        print("Utilizando o base.csv existente.\n")

        data_modificacao_csv = None

    else:

        data_modificacao_csv = esperar_nova_exportacao(
            caminho_arquivo=ARQUIVO_CSV,
            caminho_controle=ARQUIVO_CONTROLE,
            intervalo=30,
            timeout=1800,
            tempo_estabilidade=5,
        )


    # =====================================================
    # ETAPA 4 - LER O CSV
    # =====================================================

    print(f"\nLendo o arquivo CSV:\n{ARQUIVO_CSV}")

    df_csv = ler_arquivo_csv(
        ARQUIVO_CSV
    )


    # =====================================================
    # ETAPA 5 - FILTRAR AS INSTALAÇÕES NO CSV
    # =====================================================

    resultado = filtrar_instalacoes(
        df=df_csv,
        instalacoes=instalacoes_normalizadas,
    )

    print(
        f"\n{len(resultado)} registros encontrados "
        "antes da remoção de duplicidades."
    )


    # =====================================================
    # ETAPA 6 - MANTER UMA LINHA POR INSTALAÇÃO
    # =====================================================

    resultado = manter_registro_mais_recente(
        resultado
    )


    # =====================================================
    # ETAPA 7 - MONTAR O RESULTADO FINAL
    # =====================================================

    resultado_final = montar_resultado_final(
        resultado
    )


    # =====================================================
    # ETAPA 8 - IDENTIFICAR AS NÃO ENCONTRADAS
    # =====================================================

    df_nao_encontradas = (
        obter_instalacoes_nao_encontradas(
            resultado_final=resultado_final,
            instalacoes_buscadas=instalacoes_normalizadas,
        )
    )


    # =====================================================
    # ETAPA 9 - DEFINIR O NOVO ARQUIVO DE SAÍDA
    # =====================================================

    arquivo_saida = obter_arquivo_saida()


    # =====================================================
    # ETAPA 10 - EXPORTAR PARA EXCEL
    # =====================================================

    exportar_resultado_excel(
        resultado=resultado_final,
        nao_encontradas=df_nao_encontradas,
        caminho_saida=arquivo_saida,
    )


    # =====================================================
    # ETAPA 11 - REGISTRAR A BASE COMO PROCESSADA
    # =====================================================

    if not AGUARDAR_NOVA_EXPORTACAO:

        salvar_ultima_execucao(
            caminho_controle=ARQUIVO_CONTROLE,
            data_modificacao=data_modificacao_csv,
        )


    # =====================================================
    # RESUMO
    # =====================================================

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
        f"{len(df_nao_encontradas)}"
    )

    print(
        f"Arquivo salvo em:\n{arquivo_saida}"
    )


if __name__ == "__main__":
    main()
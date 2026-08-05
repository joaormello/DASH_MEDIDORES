from pathlib import Path

import pandas as pd


def ajustar_largura_colunas(planilha) -> None:
    for coluna in planilha.columns:
        maior_tamanho = 0
        letra_coluna = coluna[0].column_letter

        for celula in coluna:
            valor = (
                ""
                if celula.value is None
                else str(celula.value)
            )

            maior_tamanho = max(
                maior_tamanho,
                len(valor),
            )

        planilha.column_dimensions[
            letra_coluna
        ].width = min(maior_tamanho + 2, 50)


def exportar_resultado_excel(
    resultado: pd.DataFrame,
    nao_encontradas: pd.DataFrame,
    caminho_saida: Path,
) -> None:
    caminho_saida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    try:
        with pd.ExcelWriter(
            caminho_saida,
            engine="openpyxl",
        ) as writer:
            resultado.to_excel(
                writer,
                sheet_name="Resultado",
                index=False,
            )

            nao_encontradas.to_excel(
                writer,
                sheet_name="Nao encontradas",
                index=False,
            )

            for planilha in writer.sheets.values():
                ajustar_largura_colunas(planilha)
                planilha.freeze_panes = "A2"
                planilha.auto_filter.ref = (
                    planilha.dimensions
                )

    except PermissionError as erro:
        raise PermissionError(
            "Não foi possível salvar o Excel. "
            "Verifique se ele está aberto:\n"
            f"{caminho_saida}"
        ) from erro
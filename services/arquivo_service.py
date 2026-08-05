from pathlib import Path
from datetime import datetime
import time


def obter_data_modificacao(caminho_arquivo: Path) -> float:
    """
    Retorna a data de modificação do arquivo em formato timestamp.
    """

    return caminho_arquivo.stat().st_mtime


def ler_ultima_execucao(caminho_controle: Path) -> float:
    """
    Lê o timestamp da última base processada.

    Retorna 0 caso o arquivo de controle ainda não exista
    ou esteja inválido.
    """

    if not caminho_controle.exists():
        return 0.0

    try:
        conteudo = caminho_controle.read_text(
            encoding="utf-8"
        ).strip()

        return float(conteudo)

    except (ValueError, OSError):
        return 0.0


def salvar_ultima_execucao(
    caminho_controle: Path,
    data_modificacao: float,
) -> None:
    """
    Salva o timestamp da base que foi processada com sucesso.
    """

    caminho_controle.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    caminho_controle.write_text(
        str(data_modificacao),
        encoding="utf-8",
    )


def arquivo_esta_estavel(
    caminho_arquivo: Path,
    tempo_verificacao: int = 5,
) -> bool:
    """
    Verifica se o arquivo parou de crescer.
    """

    try:
        tamanho_inicial = caminho_arquivo.stat().st_size

        if tamanho_inicial == 0:
            return False

        data_inicial = caminho_arquivo.stat().st_mtime

        time.sleep(tempo_verificacao)

        tamanho_final = caminho_arquivo.stat().st_size
        data_final = caminho_arquivo.stat().st_mtime

        return (
            tamanho_inicial == tamanho_final
            and data_inicial == data_final
        )

    except FileNotFoundError:
        return False


def esperar_nova_exportacao(
    caminho_arquivo: Path,
    caminho_controle: Path,
    intervalo: int = 30,
    timeout: int = 1800,
    tempo_estabilidade: int = 5,
) -> float:
    """
    Aguarda uma exportação mais recente que a última processada.

    Retorna o timestamp do CSV que deverá ser salvo no controle
    somente após o processamento terminar com sucesso.
    """

    caminho_arquivo = Path(caminho_arquivo)
    caminho_controle = Path(caminho_controle)

    ultima_execucao = ler_ultima_execucao(
        caminho_controle
    )

    limite = time.time() + timeout

    print("\nAguardando uma nova exportação do Spotfire...")
    print(f"Arquivo esperado: {caminho_arquivo}")

    if ultima_execucao > 0:
        data_anterior = datetime.fromtimestamp(
            ultima_execucao
        )

        print(
            "Última base processada: "
            f"{data_anterior:%d/%m/%Y %H:%M:%S}"
        )

    while time.time() < limite:

        if not caminho_arquivo.exists():
            print("O arquivo ainda não existe.")

        else:
            data_modificacao = obter_data_modificacao(
                caminho_arquivo
            )

            if data_modificacao <= ultima_execucao:
                data_csv = datetime.fromtimestamp(
                    data_modificacao
                )

                print(
                    "O CSV encontrado já foi processado. "
                    f"Modificado em {data_csv:%d/%m/%Y %H:%M:%S}."
                )

            elif arquivo_esta_estavel(
                caminho_arquivo,
                tempo_verificacao=tempo_estabilidade,
            ):
                data_csv = datetime.fromtimestamp(
                    data_modificacao
                )

                tamanho_mb = (
                    caminho_arquivo.stat().st_size
                    / 1024
                    / 1024
                )

                print(
                    "Nova exportação encontrada e pronta."
                )
                print(
                    f"Modificação: "
                    f"{data_csv:%d/%m/%Y %H:%M:%S}"
                )
                print(f"Tamanho: {tamanho_mb:.2f} MB")

                return data_modificacao

            else:
                print(
                    "O CSV existe, mas ainda está sendo gravado."
                )

        print(
            f"Nova verificação em {intervalo} segundos..."
        )

        time.sleep(intervalo)

    raise TimeoutError(
        "Nenhuma nova exportação completa foi encontrada "
        f"dentro de {timeout} segundos."
    )
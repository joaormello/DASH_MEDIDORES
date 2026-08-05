from pathlib import Path
import time


def esperar_arquivo(
    caminho_arquivo: Path,
    intervalo: int = 30,
    timeout: int = 1800
):
    """
    Aguarda até que o arquivo exista e esteja totalmente gravado.

    Args:
        caminho_arquivo: Caminho do arquivo.
        intervalo: Tempo entre verificações (segundos).
        timeout: Tempo máximo de espera (segundos).
    """

    print(f"Aguardando arquivo: {caminho_arquivo.name}")

    tempo_inicial = time.time()

    while True:

        if caminho_arquivo.exists():

            tamanho_1 = caminho_arquivo.stat().st_size

            time.sleep(2)

            tamanho_2 = caminho_arquivo.stat().st_size

            if tamanho_1 == tamanho_2:
                print("Arquivo encontrado e finalizado.")
                return

        if time.time() - tempo_inicial > timeout:
            raise TimeoutError(
                f"O arquivo {caminho_arquivo.name} não foi encontrado dentro do tempo limite."
            )

        print("Arquivo ainda não disponível. Aguardando...")
        time.sleep(intervalo)
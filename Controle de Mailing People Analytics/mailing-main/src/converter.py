import os
import pandas as pd
import csv
from tqdm import tqdm


PASTA_ORIGEM = r"C:\Users\51316_italo\Documents\CB\mailing-main\Bases Para Limpar"
PASTA_DESTINO = r"C:\Users\51316_italo\Documents\CB\mailing-main\Bases Limpas"


def limpa_para_csv():
    os.makedirs(PASTA_DESTINO, exist_ok=True)

    arquivos = [
        f for f in os.listdir(PASTA_ORIGEM)
        if f.lower().endswith(('.csv', '.xls', '.xlsx'))
    ]

    if not arquivos:
        print("Nenhum arquivo encontrado para limpar.")
        return

    print("Iniciando limpeza e padronização dos arquivos...")

    for arquivo in tqdm(arquivos, desc="Limpando arquivos", unit="arquivo"):
        caminho_origem = os.path.join(PASTA_ORIGEM, arquivo)
        nome_base = os.path.splitext(arquivo)[0]
        caminho_destino = os.path.join(PASTA_DESTINO, f"{nome_base}.csv")

        try:
            if arquivo.lower().endswith(('.xls', '.xlsx')):
                df = pd.read_excel(caminho_origem, dtype=str)
            else:
                df = pd.read_csv(
                    caminho_origem,
                    sep=None,
                    engine="python",
                    encoding="utf-8",
                    dtype=str
                )

            df = df.fillna("")

            df.to_csv(
                caminho_destino,
                index=False,
                sep=",",
                encoding="utf-8",
                quoting=csv.QUOTE_ALL,
                lineterminator="\n"
            )

        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")

    print("Processo concluído. Arquivos limpos disponíveis na pasta de destino.")


if __name__ == "__main__":
    limpa_para_csv()

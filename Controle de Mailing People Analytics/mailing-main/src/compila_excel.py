import os
import pandas as pd
from tqdm import tqdm
import csv


def compila_excel(path):
    compiled_file_name = 'arquivo_compilado.csv'

    files = [
        file for file in os.listdir(path)
        if file.endswith(('.xlsx', '.xls', '.csv')) and file != compiled_file_name
    ]

    print("Iniciando leitura e compilação dos arquivos...")
    output_file = os.path.join(path, compiled_file_name)
    all_dataframes = []

    for file in tqdm(files, desc="Processando arquivos", unit="arquivo"):
        file_path = os.path.join(path, file)
        try:
            if file.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path)
            elif file.endswith('.csv'):
                # lê tentando detectar automaticamente
                df = pd.read_csv(
                    file_path,
                    sep=None,
                    engine="python",
                    encoding="utf-8",
                    dtype=str
                )
            all_dataframes.append(df.astype(str))
        except Exception as e:
            print(f"Erro ao processar o arquivo {file}: {e}")

    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True).fillna("")

        print("Salvando o arquivo compilado no padrão universal...")
        combined_df.to_csv(
            output_file,
            index=False,
            sep=",",
            encoding="utf-8",
            quoting=csv.QUOTE_ALL,
            lineterminator="\n"
        )

        print(f"Arquivo gerado com sucesso: {output_file}")
    else:
        print("Nenhum arquivo foi processado.")


if __name__ == "__main__":
    while True:
        path = input("Por favor, insira o caminho da pasta: ")
        if os.path.isdir(path):
            break
        print("Caminho inválido.")
    compila_excel(path)

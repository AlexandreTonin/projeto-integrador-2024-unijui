import pandas as pd

caminho_do_arquivo_csv = 'dados.csv'

dados = pd.read_csv(caminho_do_arquivo_csv)

print(dados.head())

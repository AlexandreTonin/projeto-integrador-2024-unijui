import pandas as pd

# Ler o arquivo CSV
def transformarHorasEmMeses():
  df = pd.read_csv('InmetFinal.csv', sep=',')

  # Converter a coluna DATA para o tipo datetime
  df['DATA'] = pd.to_datetime(df['DATA'], format='%Y-%m-%d')

  # Extrair o ano e o mês da coluna DATA
  df['ANO_MES'] = df['DATA'].dt.to_period('M')

  # Substituir as vírgulas por pontos nas colunas de temperatura e precipitação para permitir a conversão para float
  df['TEMPERATURA'] = df['TEMPERATURA'].str.replace(',', '.').astype(float)
  df['PRECIPITACAO'] = df['PRECIPITACAO'].str.replace(',', '.').astype(float)

  # Converter a coluna UMIDADE para float
  df['UMIDADE'] = df['UMIDADE'].astype(float)

  # Agrupar os dados pelo ano e mês e calcular as médias e somas
  result = df.groupby('ANO_MES').agg({
      'PRECIPITACAO': 'sum',
      'TEMPERATURA': 'mean',
      'UMIDADE': 'mean'
  }).reset_index()

  # Renomear as colunas para refletir as operações realizadas
  result.columns = ['ANO_MES', 'PRECIPITACAO_TOTAL', 'TEMPERATURA_MEDIA', 'UMIDADE_MEDIA']

  # Exibir o DataFrame resultante (opcional)
  print(result)

  # Salvar o resultado em um novo arquivo CSV
  result.to_csv('inmetFinalAgrupados.csv', index=False)

def separarEstacoes():
    # Ler o arquivo CSV
    df = pd.read_csv('inmetFinalAgrupados.csv')

    # Verificar se as colunas esperadas estão presentes no DataFrame
    expected_columns = ['ANO_MES', 'PRECIPITACAO_TOTAL', 'TEMPERATURA_MEDIA', 'UMIDADE_MEDIA']
    if not all(col in df.columns for col in expected_columns):
        print("O arquivo CSV não contém todas as colunas necessárias.")
        return

    # Adicionar a coluna de mês para facilitar a filtragem
    df['MES'] = df['ANO_MES'].str.split('-', expand=True)[1].astype(int)

    # Separar os dados por estação
    inverno = df[(df['MES'] >= 4) & (df['MES'] <= 9)]
    verao = df[(df['MES'] >= 10) | (df['MES'] <= 3)]

    # Remover a coluna de mês antes de salvar
    inverno = inverno.drop(columns=['MES'])
    verao = verao.drop(columns=['MES'])

    # Salvar os resultados em novos arquivos CSV
    inverno.to_csv('dados_inverno.csv', index=False)
    verao.to_csv('dados_verao.csv', index=False)

def anosParesImpares():
    # Ler os arquivos CSV das estações de verão e inverno
    df_verao = pd.read_csv('dados_verao.csv')
    df_inverno = pd.read_csv('dados_inverno.csv')

    # Verificar se as colunas esperadas estão presentes nos DataFrames
    expected_columns = ['ANO_MES', 'PRECIPITACAO_TOTAL', 'TEMPERATURA_MEDIA', 'UMIDADE_MEDIA']
    if not all(col in df_verao.columns for col in expected_columns) or not all(col in df_inverno.columns for col in expected_columns):
        print("Os arquivos CSV não contêm todas as colunas necessárias.")
        return

    # Adicionar a coluna de ano para facilitar a filtragem
    df_verao['ANO'] = df_verao['ANO_MES'].str.split('-', expand=True)[0].astype(int)
    df_inverno['ANO'] = df_inverno['ANO_MES'].str.split('-', expand=True)[0].astype(int)

    # Separar os dados de verão por ano par e ímpar
    pares_verao = df_verao[df_verao['ANO'] % 2 == 0]
    impares_verao = df_verao[df_verao['ANO'] % 2 != 0]

    # Separar os dados de inverno por ano par e ímpar
    pares_inverno = df_inverno[df_inverno['ANO'] % 2 == 0]
    impares_inverno = df_inverno[df_inverno['ANO'] % 2 != 0]

    # Remover a coluna de ano antes de salvar
    pares_verao = pares_verao.drop(columns=['ANO'])
    impares_verao = impares_verao.drop(columns=['ANO'])
    pares_inverno = pares_inverno.drop(columns=['ANO'])
    impares_inverno = impares_inverno.drop(columns=['ANO'])

    # Salvar os resultados em novos arquivos CSV
    pares_verao.to_csv('dados_verao_pares.csv', index=False)
    impares_verao.to_csv('dados_verao_impares.csv', index=False)
    pares_inverno.to_csv('dados_inverno_pares.csv', index=False)
    impares_inverno.to_csv('dados_inverno_impares.csv', index=False)

def agruparPorAno():
    # Lista dos nomes dos arquivos de entrada e saída
    arquivos_entrada = ['dados_inverno_pares.csv', 'dados_inverno_impares.csv', 'dados_verao_pares.csv', 'dados_verao_impares.csv']
    arquivos_saida = ['inverno_pares_por_ano.csv', 'inverno_impares_por_ano.csv', 'verao_pares_por_ano.csv', 'verao_impares_por_ano.csv']

    # Iterar sobre os arquivos de entrada e saída
    for i, arquivo_entrada in enumerate(arquivos_entrada):
        # Ler o arquivo CSV de entrada
        df = pd.read_csv(arquivo_entrada)

        # Agrupar os dados por ano e calcular as médias e somas
        result = df.groupby(df['ANO_MES'].str[:4]).agg({
            'PRECIPITACAO_TOTAL': 'sum',
            'TEMPERATURA_MEDIA': 'mean',
            'UMIDADE_MEDIA': 'mean'
        }).reset_index()

        # Renomear a coluna para refletir o agrupamento por ano
        result.columns = ['ANO', 'PRECIPITACAO_TOTAL', 'TEMPERATURA_MEDIA', 'UMIDADE_MEDIA']

        # Salvar o resultado em um novo arquivo CSV
        result.to_csv(arquivos_saida[i], index=False)

transformarHorasEmMeses()
separarEstacoes()
anosParesImpares()
agruparPorAno()
import os
import fitz
import pandas as pd
import logging

def transforma_em_float(dados):
    for i in range(len(dados)):
        if dados[i][3]:
            if '.' in dados[i][3]:
                dados[i][3] = dados[i][3].replace('.', '')
            dados[i][3] = dados[i][3].replace(',', '.')
            dados[i][3] = float(dados[i][3])
    return dados

def remover_saldo(dataframe):
    return dataframe[~dataframe[2].str.contains('pagamento|saldo em rotativo', case=False)]

def criar_tabelas():
    dfs = []  # Lista para armazenar os DataFrames encontrados
    for docs in os.listdir('../resources/pdf'):
        doc = fitz.open('../resources/pdf/' + docs)
        for page in doc:
            tabs = page.find_tables()
            if tabs.tables:
                tabela = tabs[0].extract()
                df = pd.DataFrame(tabela)
                dfs.append(df)  # Adiciona o DataFrame à lista
    return pd.concat(dfs, ignore_index=True)  # Concatena todos os DataFrames encontrados

def criar_dataframe():
    writer = pd.ExcelWriter(r"../output/arquivo_final.xlsx", engine='xlsxwriter')
    try:
        df_tabelas = criar_tabelas()
        df_tabelas = transforma_em_float(df_tabelas.values.tolist())  # Transforma em float
        df_tabelas = pd.DataFrame(df_tabelas)
        df_tabelas = remover_saldo(df_tabelas)
        df_tabelas.to_excel(writer, "Todas_Folhas", index=False)
        logging.info("Arquivo gerado com sucesso. Verifique o arquivo 'arquivo_final.xlsx' no diretório 'output'")
        writer.close()
    except Exception as e:
        logging.error(f"Método Criar DataFrame: Ocorreu um erro ao gerar o arquivo: {e}")

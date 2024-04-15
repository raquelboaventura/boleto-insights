import os

import fitz
import pandas
import logging


def iterar_dicionario(dados):
    for i in range(len(dados)):  # percorre o dados:
        if dados[i][3]:
            if '.' in dados[i][3]:
                dados[i][3] = dados[i][3].replace('.', '')
            dados[i][3] = dados[i][3].replace(',', '.')
            dados[i][3] = float(dados[i][3])
    return dados

def criar_dataframe():
    writer = pandas.ExcelWriter(r"../output/arquivo_final.xlsx", engine='xlsxwriter')
    try:
        for docs in os.listdir('../resources/pdf'):
            doc = fitz.open('../resources/pdf/' + docs)
            df = pandas.DataFrame()
            for page in doc:
                tabs = page.find_tables()  # locate and extract any tables on page
                i = 0
                if tabs.tables:  # at least one table found?
                    tabela = tabs[i].extract()
                    df = df._append(tabela)
                    for index, row in df.iterrows():
                        if isinstance(row[2], str) and (
                                "pagamento" in row[2].lower() or "saldo em rotativo" in row[2].lower()):
                            df.drop(index, inplace=True)
                records = df.to_dict("records")
                records = iterar_dicionario(records)
            df = pandas.DataFrame(records).to_excel(writer, f"Page_{docs}")
            logging.info("Arquivo gerado com sucesso. Verifique o arquivo 'arquivo_final.xlsx' no diretorio 'output'")
        writer.close()
    except Exception as e:
        logging.error(f"Ocorreu um erro ao gerar o arquivo: {e.with_traceback()}")

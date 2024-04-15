import logging

import pandas
from src.chat_ia import chat
from src.pdf import criar_dataframe


def criar_arquivo_insights(soma, descricao, groupby):
    try:
        with open("../output/insights.txt", 'w') as f:
            f.write(f"O valor total da fatura é {soma}\n\n.")
            f.write("Ao aplicar o metodo description() nos dados do boleto, obtemos: \n" + str(descricao) + "\n\n")
            f.write("Agrupando por coluna 2 (descricao dos gastos), temos: \n\n")
            f.write("Data                  Valor\n")
            f.write("-------------------  -----\n")
            for linha in range(len(groupby)):
                f.write(f"{groupby['Data'][linha]:<23}  {groupby['Valor'][linha]:.1f}\n")
            f.write("\n\n")
            logging.info("Arquivo insights criado com sucesso. Verifique o caminho: ../output/insights.txt")
    except Exception as e:
        logging.error(f"Ocorreu um erro ao gerar o arquivo: {e.with_traceback()}")

def gerar_insights():
    criar_dataframe()
    try:
        with open("../output/arquivo_final.xlsx", 'rb') as f:
            df = pandas.read_excel(f)
            COLUNA_VALORES = df.iloc[:, 4]
            soma_valores = round(COLUNA_VALORES.sum())
            descricao_boleto = COLUNA_VALORES.describe()
            resultado_groupby = df.groupby(2)[3].sum().reset_index()
            resultado_groupby.columns = ['Data', 'Valor']
            criar_arquivo_insights(soma_valores,descricao_boleto, resultado_groupby)
            chat()
    except Exception as e:
        logging.error(f"Ocorreu um erro ao gerar o arquivo: {e.with_traceback()}")

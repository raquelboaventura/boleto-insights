import logging

import pandas
from src.utilities.pdf import criar_dataframe
from src.utilities.chat_ia import chat
import os

output_path = os.path.dirname("../../output")

def criar_arquivo_insights(soma, descricao, groupby):
    logging.log(logging.INFO, "Gerando arquivo insights...")
    try:
        with open("../../output/insights.txt", 'w') as f:
            f.write(f"O valor total da fatura é {soma}\n\n.")
            f.write("Ao aplicar o metodo description() nos dados do boleto, obtemos: \n" + str(descricao) + "\n\n")
            f.write("Agrupando pela descricao dos gastos, temos: \n\n")
            f.write("Data                  Valor\n")
            f.write("-------------------  -----\n")
            for linha in range(len(groupby)):
                f.write(f"{groupby['Data'][linha]:<23}  {groupby['Valor'][linha]:.1f}\n")
            f.write("\n\n")
            logging.info("Arquivo insights criado com sucesso. Verifique o caminho: ../output/insights.txt")
    except Exception as e:
        logging.error(f"Método criar_arquivo_insights | Ocorreu um erro ao gerar o arquivo: {e}")


def gerar_insights():
    criar_dataframe()
    try:
        with open("../../output/arquivo_final.xlsx", 'rb') as f:
            df = pandas.read_excel(f)
            COLUNA_VALORES = df.iloc[:, 3]
            soma_valores = round(COLUNA_VALORES.sum())
            descricao_boleto = COLUNA_VALORES.describe()
            # resultado_groupby = df.groupby(df.columns[2])[df.columns[3]].sum().reset_index()
            df.columns = ['Data', 'Valor', 'Despesa', 'Saldo']
            criar_arquivo_insights(soma_valores,descricao_boleto, df)
            return chat()
    except Exception as e:
        logging.error(f"Em método gerar insights: Ocorreu um erro ao gerar o arquivo: {e}")

gerar_insights()
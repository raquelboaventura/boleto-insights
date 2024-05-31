import asyncio
import os
import fitz
import pandas as pd

from utilities.chat_ia import chat
from utilities.configs import get_logger

logger = get_logger()


def transforma_em_float(dados):
    for i, linha in enumerate(dados):
        if len(linha) > 3 and linha[3] and linha[3].strip():
            dados[i][3] = float(linha[3].replace('.', '').replace(',', '.'))
    return dados


def exclui_strings(lista):
    strings_desejadas = ['pagamento', 'saldo em rotativo']
    for string in strings_desejadas:
        for item in lista[:]:  # Usamos lista[:] para criar uma cópia da lista original
            if string in item:
                lista.remove(item)
    return lista


async def criar_tabelas():
    pdf_dir = os.path.abspath("..\src\input")
    logger.debug(f"Diretório PDF: {pdf_dir}")

    if not os.path.exists(pdf_dir):
        logger.info(f"Diretório {pdf_dir} não existe. Criando o diretório.")
        os.makedirs(pdf_dir)
    else:
        logger.info(f"Diretório {pdf_dir} já existe.")

    files = os.listdir(pdf_dir)
    logger.debug(f"Arquivos encontrados no diretório {pdf_dir}: {files}")

    tasks = []

    for doc in files:
        try:
            logger.info(f"entrando no processamento do pdfs: {doc}")
            tasks.append(processar_documento(doc))  # Pass the document name as an argument
        except Exception as e:
            logger.error(f"Erro processando documento '{doc}': {e}")

    if tasks:
        results = await asyncio.gather(*tasks)
        logger.info(f"processamento concluído: {results}")  # Print the results
        return results
    else:
        logger.info("Nenhum documento para processar.")
        return []


async def processar_documento(doc):
    logger.info(f"Iniciando o processamento do documento: {doc}")
    pdf_dir = os.path.abspath("..\src\input")
    doc_path = os.path.join(pdf_dir, doc)
    logger.debug(f"Tentando abrir o documento: {doc_path}")

    if not os.path.exists(doc_path):
        logger.error(f"O arquivo '{doc_path}' não existe.")
        return f"Erro: O arquivo '{doc_path}' não existe."

    dfs = []
    try:
        doc = fitz.open(doc_path)
        logger.info(f"Arquivo '{doc_path}' aberto com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao abrir o documento '{doc_path}': {e}")
        return f"Erro ao abrir o documento '{doc_path}': {e}"

    count = 0
    for page in doc:
        logger.info(f"Processando a página {page.number}")
        tabs = page.find_tables()
        logger.info(f"Encontradas {(tabs)} tabelas na página {page.number}")
        if tabs and tabs.tables:
            tabela = tabs[0].extract()
            tabela = transforma_em_float(tabela)
            tabela = exclui_strings(tabela)
            df = pd.DataFrame(tabela)
            dfs.append(df)
            chat(f"O detalhamento do boleto {doc_path}, pagina {page.number} de {len(doc)}, está a seguir: {df}")
            count += 1
        logger.info(f"Finalizando a página {page.number}")
    resposta_gemini = chat("Sumarize todas as informações e retorne os insights no template.")
    if resposta_gemini is not None:
        logger.info(f"Resposta do Gemini gerada com sucesso!")
        return resposta_gemini
    else:
        return "Nenhuma tabela processada ou interação com o Gemini realizada"

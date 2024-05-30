import re

from loguru import logger
import os
import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
import datetime
import mistune
from bs4 import BeautifulSoup

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.5,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2000,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[])
convo.send_message("Você é uma assistente virtual para ajudar as pessoas a controlar seus gastos."
                   "Seu papel é dar a elas insights do que pode ser melhorado "
                   "para que tenham uma vida financeira saudável."
                   "Responda usando o seguinte template: "
                   "Exemplo de resposta: "
                   "1. Economias Possíveis"
                   "Com um gasto médio de R$ 12,80 em compras do *99pop*, você poderia economizar cerca de R$ 153,"
                   "60 por ano optando por alternativas mais econômicas de transporte"
                   "Seu gasto médio de R$ 35 em refeições no *Burger King App* é significativamente maior do que "
                   "outras opções de refeições. Considerar cozinhar mais refeições em casa ou procurar opções mais "
                   "baratas pode economizar cerca de R$ 420 por ano"
                   "2. Análise de Gastos"
                   "A categoria *Outros* representa a maior parcela (35%) do seu orçamento mensal. Uma análise mais "
                   "detalhada desses gastos pode identificar áreas onde você pode economizar"
                   "Os gastos com *Entretenimento* também são significativos (15%). Explorar atividades gratuitas ou "
                   "de baixo custo pode reduzir esses gastos"
                   "3. Planejamento Financeiro"
                   "Criar um orçamento mensal detalhado o ajudará a rastrear seus gastos e identificar áreas onde "
                   "você pode cortar"
                   "Acompanhe seus gastos por meio de aplicativos ou planilhas para obter uma melhor compreensão de "
                   "seus hábitos financeiros"
                   "4. Controle de Despesas"
                   "Considere usar dinheiro ou cartões pré-pagos para controlar seus gastos e evitar compras por "
                   "impulso"
                   "Negociar descontos em boletos e anuidades de cartões de crédito também pode reduzir as despesas "
                   "fixas"
                   "5. Priorização de Gastos"
                   "Priorize seus gastos com base em necessidades (habitação, alimentação, transporte) e desejos ("
                   "entretenimento, compras)"
                   " Considere reduzir gastos desnecessários para aumentar suas economias"
                   "6. Planejamento de Objetivos"
                   "Defina metas financeiras de curto e longo prazo, como comprar uma casa ou se aposentar "
                   "confortavelmente"
                   " Crie um plano para atingir essas metas economizando e investindo uma parte de sua renda"
                   "Conclusão:"
                   "Implementando essas medidas, você pode melhorar significativamente sua vida financeira. Lembre-se "
                   "que economizar dinheiro é uma jornada, não um destino. Esteja paciente e disciplinado e você verá "
                   "os resultados com o tempo."
                   )


def markdown_para_texto(markdown_text):
    html = mistune.markdown(markdown_text)
    # Use BeautifulSoup to remove HTML tags and get text
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()


def get_last_text(data):
    try:
        logger.debug(f"Data received in get_last_text: {data}")
        texts = re.findall(r'text: "(.*?)"', data)
        logger.debug(f"Extracted texts: {texts}")
        return texts[-1] if texts else None
    except Exception as e:
        logger.error(f"Erro na função get_last_text: {e}")
        return None


def chat(message):
    try:
        logger.debug(f"Message received: {message}")
        convo.send_message(message)

        if not isinstance(convo.history, list):
            raise ValueError(f"convo.history deve ser uma lista, mas é {type(convo.history)}")

        df = pd.DataFrame({'Resposta': [convo.history]})
        df.to_csv(f"../../output/historico-{datetime.datetime.now().date()}.txt", index=False)

        logger.debug("Histórico da conversa:")
        logger.debug(convo.history)

        response = str(convo.history)

        logger.debug("Print da response >>>>")
        logger.debug(response)
        logger.debug(f"Comprimento da response: {len(response)}")

        last_text = get_last_text(response)

        logger.debug("Print do último texto >>>>")
        logger.debug(last_text)

        if last_text:
            return last_text
        else:
            raise ValueError("Nenhum texto foi encontrado")
    except Exception as e:
        logger.error(f"Função Chat | {e.args}")
        return None

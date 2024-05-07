import logging
import os

import google.generativeai as genai
import pandas as pd
from dotenv import load_dotenv
import datetime

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
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

convo = model.start_chat(history=[
])

convo.send_message(
    "você ajuda outras pessoas a se organizarem financeiramente."
    "elas enviam a você detalhes de 4 boletos de meses anteriores, detalhes de gastos e"
    "sua renda mensal. Seu papel é dar a elas insights do que pode ser melhorado "
    "para que tenham uma vida financeira saudável. Responda usando o seguinte template:"
    "Olá, (nome da pessoa)! Vamos melhorar ter alguns insights sobre o que pode ser melhorado?"
    "Destaque o total do boleto e os gastos e o valor da renda mensal."
    "1. Economias Possíveis. 2. Análise de Gastos."
    "3. Planejamento Financeiro. 4. Controle de Despesas. 5. Priorização de Gastos. "
    "6. Planejamento de Objetivos. 7. Conclua dando uma boa resolução."
)


def chat():
    try:
        with open("../output/insights.txt", 'r+') as f:
            details = f.read()
            historico = convo.send_message(details).text
            f.write(f"Resposta: {historico}\n")
            df = pd.DataFrame({'Resposta': [historico]})
            df.to_csv(f"../output/historico-{datetime.datetime.now().date()}.txt", index=False)
    except FileNotFoundError:
        logging.error("Arquivo insights.txt não encontrado")
    except Exception as e:
        logging.error(e)

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
    "você é uma pessoa que ajuda outras a se organizarem financeiramente."
    "elas enviam a você alguns detalhes sobre suas contas, sobre os gastos e"
    "sua renda mensal. Seu papel é dar a elas insights do que pode ser melhorado "
    "para que tenham uma vida financeira saudável. Responda utilizando os seguintes criterios:"
    "Olá, (nome da pessoa)! Vamos melhorar ter alguns insights sobre o que pode ser melhorado?"
    "Destaque o total do boleto e os gastos e o valor da renda mensal."
    "1. Economias Possíveis. 2. Análise de Gastos."
    "3. Planejamento Financeiro. 4. Controle de Despesas. 5. Priorização de Gastos. "
    "6. Planejamento de Objetivos. 7. Conclua dando uma boa resolução."
)


def chat():
    nome = str(input("Qual é o seu nome?\n"))
    renda_mensal = float(input("Qual é a sua renda mensal?\n"))
    with open("../output/insights.txt", 'r+') as f:
        f.write(f"O nome da pessoa: {nome}\n")
        f.write(f"Valor da renda mensal: {renda_mensal}\n")
        details = f.read()
        historico = convo.send_message(details)
        historico_df = pd.DataFrame(historico)
        historico_df.to_csv(f"../output/historico-{datetime.datetime.now().date()}.txt", index=False)

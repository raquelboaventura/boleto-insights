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
                   "Responda usando o seguinte template: Destaque o total do boleto e "
                   "os gastos e o valor gasto em cada categoria."
                   "Contextualização Inicial: Adicionar uma breve introdução sobre a "
                   "importância do controle financeiro e como"
                   "pequenas mudanças podem ter um grande impacto."
                   "Detalhamento dos Dados: utilize informações específicas dos boletos, tipo de compra, recorrencia, forma de pagamento, etc."
                   "Exemplos de Insights: Dar exemplos concretos melhoras e economias."
                   "Dicas Práticas: Incluir dicas simples e práticas para melhorar o controle financeiro."
                   "Análise de Tendências: Além dos gastos atuais, analisar as tendências ao longo do tempo para identificar padrões."
                   "Incentivo à Ação: Incluir uma seção que incentive a pessoa a tomar medidas imediatas com base nos insights."
                   "Inclusão de Recursos: Fornecer links ou recursos adicionais para ajudar a pessoa a melhorar sua educação "
                   "financeira."
                   "Exemplo de resposta: "
                   "1. Economias Possíveis"
                   " Com um gasto médio de R$ 12,80 em compras do *99pop*, você poderia economizar cerca de R$ 153,60 por ano optando por alternativas mais econômicas de transporte"
                   " Seu gasto médio de R$ 35 em refeições no *Burger King App* é significativamente maior do que outras opções de refeições. Considerar cozinhar mais refeições em casa ou procurar opções mais baratas pode economizar cerca de R$ 420 por ano"
                   "2. Análise de Gastos"
                   " A categoria *Outros* representa a maior parcela (35%) do seu orçamento mensal. Uma análise mais detalhada desses gastos pode identificar áreas onde você pode economizar"
                   " Os gastos com *Entretenimento* também são significativos (15%). Explorar atividades gratuitas ou de baixo custo pode reduzir esses gastos"
                   "3. Planejamento Financeiro"
                   " Criar um orçamento mensal detalhado o ajudará a rastrear seus gastos e identificar áreas onde você pode cortar"
                   " Acompanhe seus gastos por meio de aplicativos ou planilhas para obter uma melhor compreensão de seus hábitos financeiros"
                   "4. Controle de Despesas"
                   " Considere usar dinheiro ou cartões pré-pagos para controlar seus gastos e evitar compras por impulso"
                   " Negociar descontos em boletos e anuidades de cartões de crédito também pode reduzir as despesas fixas"
                   "5. Priorização de Gastos"
                   " Priorize seus gastos com base em necessidades (habitação, alimentação, transporte) e desejos (entretenimento, compras)"
                   " Considere reduzir gastos desnecessários para aumentar suas economias"
                   "6. Planejamento de Objetivos"
                   " Defina metas financeiras de curto e longo prazo, como comprar uma casa ou se aposentar confortavelmente"
                   " Crie um plano para atingir essas metas economizando e investindo uma parte de sua renda"
                   "Conclusão:"
                   "Implementando essas medidas, você pode melhorar significativamente sua vida financeira. Lembre-se que economizar dinheiro é uma jornada, não um destino. Esteja paciente e disciplinado e você verá os resultados com o tempo."
                   )


def chat():
    try:
        with open("../../output/insights.txt", 'r+') as f:
            details = f.read()
            historico = convo.send_message(details).text
            f.write(f"Resposta: {historico}\n")
            df = pd.DataFrame({'Resposta': [historico]})
            df.to_csv(f"../../output/historico-{datetime.datetime.now().date()}.txt", index=False)
            return convo.history
    except FileNotFoundError:
        logging.error("Método Chat | Arquivo insights.txt não encontrado")
    except Exception as e:
        logging.error(e)

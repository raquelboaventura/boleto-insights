
![Logo](https://github.com/raquelboaventura/boleto-insights/blob/main/resources/4.png)


# boleto insights

um programa que recebe seus boletos e retorna dicas de economias possíveis, análise de gastos, planejamento financeiro, controle de despesas, priorização de gastos e planejamento de objetivos.


## Rodando localmente

Clone o projeto

```bash
  git clone https://github.com/raquelboaventura/boleto-insights.git
```

Entre no diretório do projeto

```bash
  cd boleto-insights
```

Necessário criar um ambiente virtual:

```python
  python3 -m venv nome_do_ambiente_virtual
```

Ativar o ambiente virtual: 

```python
  nome_do_ambiente_virtual\Scripts\Activate
```

Instalar as dependências: 

```python
pip install -r requirements.txt  
```


## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`OPENAI_API_KEY` => chave da AI do Gemini

`URL` => url para chamar a API da AI do Gemini


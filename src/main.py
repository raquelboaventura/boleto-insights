from src.utilities.pdf import criar_tabelas
from loguru import logger
from quart import Quart, jsonify, request
import asyncio
import json
from src.utilities.chat_ia import chat, markdown_para_texto


app = Quart(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/insights", methods=["POST"])
async def insights():
    try:
        insights_result = await criar_tabelas()
        logger.info(f"insights_result: {insights_result}")
        if insights_result is None:
            raise TypeError("insights_result é None")
        full_message = "\n\n".join(insights_result)
        full_message = markdown_para_texto(full_message)
        logger.info(f"full_message: {full_message}")
        return jsonify({"message": full_message, "status_code": 200}), 200
    except TypeError as e:
        logger.error(f"Erro de tipo: {e}")
        return jsonify({"message": "Erro ao gerar insights", "status_code": 500}), 500
    except Exception as e:
        logger.error(f"Erro geral: {e}")
        return jsonify({"message": "Erro ao processar a solicitação", "status_code": 500}), 500


@app.route('/upload', methods=['POST'])
async def upload_file():
    # Verifica se foi enviado um arquivo na requisição
    if 'file' not in (await request.files):
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    file = (await request.files)['file']

    # Verifica se o arquivo é um PDF
    if file.filename.endswith('.pdf'):
        # Salva o arquivo no diretório desejado
        await file.save(os.path.join('static/pdf', file.filename))
        return jsonify({'message': 'Arquivo enviado com sucesso'}), 200
    else:
        return jsonify({'error': 'Arquivo enviado não é um PDF'}), 400


if __name__ == "__main__":
    app.run()
from utilities.pdf import criar_tabelas, directory_cleaner
from loguru import logger
from quart import Quart, jsonify, request, render_template
import os


app = Quart(__name__)


@app.route("/")
async def home():
    return await render_template('index.html')


@app.route("/insights", methods=["GET"])
async def insights():
    try:
        insights_result = await criar_tabelas()
        logger.info(f"insights_result: {insights_result}")
        if insights_result is None:
            raise TypeError("insights_result é None")
        full_message = "\n\n".join(insights_result)
        #full_message = markdown_para_texto(full_message)
        logger.info(f"full_message: {full_message}")
        # Chama o método para limpar o diretório
        logger.info("Limpando o diretório")
        directory_cleaner()
        return jsonify({"message": full_message, "status_code": 200}), 200
    except TypeError as e:
        logger.error(f"Erro de tipo: {e}")
        return jsonify({"message": "Erro ao gerar insights", "status_code": 500}), 500
    except Exception as e:
        logger.error(f"Erro geral: {e}")
        return jsonify({"message": "Erro ao processar a solicitação", "status_code": 500}), 500

@app.route("/upload", methods=["POST"])
async def upload_file():
    logger.info("entrando na requisição /upload")
    if 'files[]' not in (await request.files):
        logger.info("Nenhum arquivo identificado :(")
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400

    files = (await request.files).getlist('files[]')
    logger.info(f"FILES: {files}")

    for file in files:   # Verifica se o arquivo é um PDF
        logger.info(f"entrando no loop: {file}")
        if file.filename.endswith('.pdf'):
            # Salva o arquivo no diretório desejado
            await file.save(os.path.join('..\src\input', file.filename))
            logger.info(f"arquivo salvo com sucesso! -> {file}")
        else:
            logger.error(f"deu ruim: {file}")
            return jsonify({'error': 'Arquivo enviado não é um PDF'}), 400

    logger.info("arquivos processados com sucesso! /upload finalizado.")
    return jsonify({'message': 'Arquivos enviados com sucesso'}), 200



if __name__ == "__main__":
    app.run()

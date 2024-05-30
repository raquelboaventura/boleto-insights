from loguru import logger
import sys
from datetime import datetime


current_date = datetime.now().strftime("%Y-%m-%d")
# Configurações do logger
logger.remove()  # Remove qualquer configuração de log padrão
logger.add(sys.stdout, level="DEBUG", format="{time} | {level} | {name}:{function}:{line} - {message}", colorize=True)
logger.add(f"logs/file_{current_date}.log", rotation="500 MB", level="INFO", format="{time} | {level} | {name}:{"
                                                                                    "function}:{line} - {message}",
           colorize=True)


def get_logger():
    return logger

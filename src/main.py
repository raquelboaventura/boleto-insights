from src.utilities.output import gerar_insights
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"


@app.route("/insights")
def insights():
    gerar_insights()
    return "Insights generated successfully!"

if __name__ == "__main__":
    app.run(debug=True)
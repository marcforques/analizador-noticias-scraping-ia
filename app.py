from flask import Flask, render_template

from modelos.analisis_sentimiento import calcular_sentimiento_transformer
from modelos.generar_informe import generar_informe
from modelos.scraping import scraping_noticias


app = Flask(__name__)


@app.route("/")
def index():
    # Obtenemos las noticias 
    noticias_scrapeadas = scraping_noticias()

    # Analizamos el sentimiento de las noticias
    score = calcular_sentimiento_transformer(noticias_scrapeadas)

    # Generamos el informe con la información obtenida
    resultado_analisis = generar_informe(noticias_scrapeadas, score)

    return render_template("index.html", noticias=noticias_scrapeadas, analisis=resultado_analisis)


if __name__ == "__main__":
    app.run(debug=True, port=5000)

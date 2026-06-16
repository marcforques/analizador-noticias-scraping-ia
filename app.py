import os

from flask import Flask, request, render_template, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timezone

from modelos.analisis_sentimiento import calcular_sentimiento_transformer
from modelos.generar_informe import generar_informe
from modelos.scraping import scraping_noticias

load_dotenv()

def guardar_noticias(noticias, usuario):
    # Borramos las noticias del análisis anterior
    coleccion_noticias.delete_many({})

    documentos = []

    for noticia in noticias:
        documento = noticia.copy()

        documento["usuario"] = usuario
        documento["fecha_scraping"] = datetime.now(timezone.utc)
        documento["fuente"] = "El Economista"

        documentos.append(documento)

    if documentos:
        coleccion_noticias.insert_many(documentos)


def obtener_noticias():
    noticias_bd = list(
        coleccion_noticias.find(
            {},
            {"_id": 0}
        )
    )

    return noticias_bd


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave-desarrollo")

client = MongoClient(os.getenv("MONGODB_URI"))

db = client["scrapper-ia"]
coleccion_usuarios = db["usuarios"]
coleccion_noticias = db["noticias"]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["login"]
        password = request.form["password"]
        
        usuario_bd = coleccion_usuarios.find_one({"login": usuario, "password": password})
        
        if usuario_bd:
            session["usuario"] = usuario
            return redirect(url_for("inicio"))
        
        return render_template("login.html", error=True)
    
    return render_template("login.html")


@app.route("/inicio")
def inicio():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("home.html", usuario=session["usuario"])


@app.route("/analizar", methods=["POST"])
def analizar():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    # Obtenemos las noticias 
    noticias_scrapeadas = scraping_noticias()
    
    if not noticias_scrapeadas:
        return render_template(
            "home.html",
            usuario=session["usuario"],
            error_analisis="No se han podido obtener noticias."
        )
    
    # Analizamos el sentimiento de las noticias
    score = calcular_sentimiento_transformer(noticias_scrapeadas)

    # Guardamos las noticias analizadas en MongoDB
    guardar_noticias(noticias_scrapeadas, session["usuario"])
    
    # Cogemos las noticias de la DB
    noticias_bd = obtener_noticias()
    
    # Generamos el informe con la información obtenida
    resultado_analisis = generar_informe(noticias_bd, score)

    return render_template("index.html", noticias=noticias_bd, analisis=resultado_analisis, usuario=session["usuario"])

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True, port=5000)

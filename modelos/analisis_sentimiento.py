from transformers import pipeline


print("Cargando el modelo multilingue para el analisis de sentimiento...")
pipeline_sentimiento = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)


def calcular_sentimiento_transformer(noticias):
    score_total = 0.0

    if not noticias:
        return 0.0

    for noticia in noticias:
        resultado = pipeline_sentimiento(noticia["titular"])[0]

        etiqueta = resultado["label"]
        estrellas = int(etiqueta.split()[0])

        score_conv = (estrellas - 3) / 2

        noticia["score_transformer"] = round(score_conv, 2)
        noticia["estrellas_transformer"] = etiqueta

        if estrellas > 3:
            noticia["sentimiento_transformer"] = "Positivo"
        elif estrellas < 3:
            noticia["sentimiento_transformer"] = "Negativo"
        else:
            noticia["sentimiento_transformer"] = "Neutro"

        score_total += score_conv

    score_media_mercado = round(score_total / len(noticias), 2)
    return score_media_mercado

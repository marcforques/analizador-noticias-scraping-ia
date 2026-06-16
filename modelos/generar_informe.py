import json
import re
import time

import ollama


DEBUG_OLLAMA = True


def generar_informe(noticias, score):
    datos = f"Score calculado por el transformer: {score}\n\n"

    for idx, n in enumerate(noticias):
        datos += f"- Noticia {idx+1}: {n['titular']} | Sentimiento Transformer: {n['sentimiento_transformer']} (Score: {n['score_transformer']})\n"

    prompt = f"""
    Actua como un estratega jefe de inversion y experto macroeconomico. Tu tarea es redactar un informe de mercado diario basandote en los datos analizados por el modelo Transformer.

    DATOS DEL TRANSFORMER:
    {datos}

    Debes estructurar tu respuesta SOLO en un formato JSON valido.
    La estructura exacta del JSON debe ser:
    {{
        "justificacion": "Tu analisis experto detallado. Conecta los titulares con el score calculado por el Transformer para explicar la situacion del mercado.",
        "factores_clave": ["Factor economico 1", "Factor economico 2", "Factor economico 3"]
    }}
    """

    try:
        modelo_ollama = "llama3.2"
        inicio_ollama = time.time()
        respuesta = ollama.chat(
            model=modelo_ollama,
            messages=[{"role": "user", "content": prompt}],
            format="json",
            options={"temperature": 0.3}
        )

        texto_ia = respuesta["message"]["content"].strip()

        if DEBUG_OLLAMA:
            print("\nRespuesta recibida desde Ollama:")
            print(f"Modelo solicitado: {modelo_ollama}")
            print(f"Tiempo de respuesta: {time.time() - inicio_ollama:.2f} segundos")
            print("Contenido bruto:")
            print(texto_ia)

        if "```json" in texto_ia:
            texto_ia = texto_ia.split("```json")[1].split("```")[0].strip()
        elif "```" in texto_ia:
            texto_ia = texto_ia.split("```")[1].split("```")[0].strip()

        try:
            resultado_json = json.loads(texto_ia)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", texto_ia, re.DOTALL)
            if not match:
                raise
            resultado_json = json.loads(match.group(0), strict=False)

        for clave in ("justificacion"):
            if clave in resultado_json and "justificacion" not in resultado_json:
                resultado_json["justificacion"] = resultado_json.pop(clave)
                break

        resultado_json.setdefault("veredicto", "Cautela")
        resultado_json.setdefault("justificacion", "El modelo no devolvio una justificacion completa.")
        resultado_json.setdefault("factores_clave", ["Datos de mercado", "Sentimiento agregado", "Noticias recientes"])
        resultado_json["score_sentimiento"] = score
        return resultado_json

    except Exception as e:
        print(f"Error en Ollama: {e}")
        return {
            "veredicto": "Error de Procesamiento",
            "justificacion": f"No se pudo generar el informe dinamico. El score calculado por el Transformer es {score}.",
            "factores_clave": ["Error de API Local"],
            "score_sentimiento": score
        }

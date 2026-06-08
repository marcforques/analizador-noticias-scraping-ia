# Analizador de Noticias.

Aplicacion Flask que extrae titulares recientes de El Economista, calcula el sentimiento con un modelo Transformer multilingue y genera un informe breve usando Ollama.

El objetivo del proyecto es analizar una muestra de noticias recientes.

## Estructura

```text
PROYECTO/
+-- app.py
+-- modelos/
|   +-- scraping.py
|   +-- analisis_sentimiento.py
|   +-- generar_informe.py
+-- templates/
|   +-- index.html
+-- README.md
+-- .gitignore
+-- requirements.txt
```

## Que hace cada archivo

- `app.py`: inicia Flask y coordina todo el flujo.
- `modelos/scraping.py`: abre El Economista con Selenium y obtiene titulares.
- `modelos/analisis_sentimiento.py`: analiza cada titular con `nlptown/bert-base-multilingual-uncased-sentiment`.
- `modelos/generar_informe.py`: llama a Ollama para generar una justificacion en formato JSON.
- `templates/index.html`: interfaz visual del dashboard.

## Requisitos

- Python 3.10 o superior.
- Google Chrome instalado.
- ChromeDriver compatible con tu version de Chrome.
- Ollama instalado y ejecutandose.
- Modelo `llama3.2` descargado en Ollama.


## Flujo de la aplicacion

1. Selenium abre `https://www.eleconomista.es/ultimas-noticias/`.
2. Se extraen hasta 15 titulares.
3. El modelo Transformer asigna estrellas y score a cada titular.
4. Ollama genera una justificacion general usando esos datos.
5. Flask renderiza el resultado en el dashboard.

## Notas

- La puntuacion se calcula sobre una muestra limitada de titulares.
- El resultado debe interpretarse como sentimiento informativo.
- Si El Economista cambia su HTML, puede ser necesario ajustar los XPATH de `scraping.py`.

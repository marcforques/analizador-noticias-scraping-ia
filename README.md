# Analizador de Noticias con Scraping e IA

Aplicacion web desarrollada con Flask que extrae titulares recientes de El Economista, calcula el sentimiento de cada noticia con un modelo Transformer multilingue y genera un informe de mercado mediante Ollama.

El proyecto combina scraping, procesamiento de lenguaje natural e IA generativa local para construir un pequeno dashboard de analisis informativo.

## Objetivo

Analizar una muestra de titulares recientes y obtener una lectura rapida del posible tono del mercado:

- Extraccion automatica de titulares desde una fuente de noticias economicas.
- Clasificacion de sentimiento con `nlptown/bert-base-multilingual-uncased-sentiment`.
- Calculo de un score agregado entre `-1.0` y `1.0`.
- Generacion de una justificacion macroeconomica con `llama3.2` ejecutado en Ollama.
- Visualizacion del resultado en un dashboard web.

## Vista general

La aplicacion abre la pagina de ultimas noticias de El Economista, obtiene hasta 15 titulares, analiza cada texto y muestra:

- Titulares extraidos en directo.
- Estrellas asignadas por el modelo Transformer.
- Score medio de sentimiento.
- Veredicto e interpretacion generados por IA.
- Factores clave de riesgo u oportunidad.

## Estructura del proyecto

```text
analizador-noticias-scraping-ia/
+-- app.py
+-- modelos/
|   +-- scraping.py
|   +-- analisis_sentimiento.py
|   +-- generar_informe.py
+-- templates/
|   +-- index.html
+-- .gitignore
+-- requirements.txt
+-- README.md
```

## Que hace cada archivo

- `app.py`: inicia Flask y coordina el flujo completo de la aplicacion.
- `modelos/scraping.py`: usa Selenium para abrir El Economista y obtener titulares recientes.
- `modelos/analisis_sentimiento.py`: analiza cada titular con un Transformer multilingue de Hugging Face.
- `modelos/generar_informe.py`: envia los resultados a Ollama y pide una respuesta estructurada en JSON.
- `templates/index.html`: renderiza el dashboard con Bootstrap y Font Awesome.
- `requirements.txt`: contiene las dependencias necesarias de Python.
- `.gitignore`: excluye entornos virtuales, caches, logs, zips y `chromedriver.exe`.

## Requisitos

- Python 3.10 o superior.
- Google Chrome instalado.
- ChromeDriver compatible con la version instalada de Chrome, o conexion a internet para que `webdriver-manager` lo descargue.
- Ollama instalado y ejecutandose en local.
- Modelo `llama3.2` descargado en Ollama.

## Instalacion

1. Clonar el repositorio:

```bash
git clone https://github.com/marcforques/analizador-noticias-scraping-ia.git
cd analizador-noticias-scraping-ia
```

2. Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

En macOS o Linux:

```bash
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Preparar Ollama:

```bash
ollama pull llama3.2
ollama serve
```

> Si Ollama ya esta abierto como servicio o aplicacion de escritorio, no hace falta ejecutar `ollama serve`.

## Ejecucion

Con el entorno virtual activado:

```bash
python app.py
```

Despues abre en el navegador:

```text
http://127.0.0.1:5000/
```

La primera ejecucion puede tardar mas porque el modelo Transformer puede descargarse desde Hugging Face y quedar cacheado localmente.

## Flujo de la aplicacion

1. Selenium abre `https://www.eleconomista.es/ultimas-noticias/`.
2. Se acepta el aviso de cookies si aparece.
3. Se extraen hasta 15 titulares.
4. El modelo Transformer asigna estrellas y un score a cada titular.
5. Se calcula un score medio agregado.
6. Ollama genera un informe en formato JSON con veredicto, justificacion y factores clave.
7. Flask renderiza los resultados en el dashboard.

## Interpretacion del score

El score de sentimiento se normaliza entre `-1.0` y `1.0`:

- `-1.0`: tono muy negativo.
- `0.0`: tono neutro.
- `1.0`: tono muy positivo.

La puntuacion se obtiene a partir de las estrellas del modelo Transformer:

```text
1 estrella  -> -1.0
2 estrellas -> -0.5
3 estrellas ->  0.0
4 estrellas ->  0.5
5 estrellas ->  1.0
```

## Limitaciones

- El analisis se basa en titulares, no en el contenido completo de las noticias.
- La muestra esta limitada a un maximo de 15 titulares.
- El resultado debe interpretarse como una senal informativa, no como recomendacion financiera.
- Si El Economista cambia su HTML, puede ser necesario ajustar los selectores XPath de `modelos/scraping.py`.
- La calidad del informe depende del modelo local disponible en Ollama.

## Posibles mejoras

- Permitir elegir la fuente de noticias desde la interfaz.
- Guardar historico de scores en una base de datos.
- Anadir graficos de evolucion temporal.
- Incluir analisis por sectores o palabras clave.
- Ejecutar el scraping en segundo plano para mejorar la experiencia de usuario.
- Anadir tests unitarios para el calculo de sentimiento y el parseo de la respuesta de Ollama.

## Publicacion en GitHub

El repositorio esta preparado para publicarse sin subir archivos pesados o generados localmente. En particular, `.gitignore` excluye:

- Entornos virtuales.
- Caches de Python.
- Archivos `.env`.
- Logs.
- `chromedriver.exe`.
- Archivos `.zip`.

Comandos habituales para subirlo:

```bash
git add .
git commit -m "Completa documentacion inicial"
git branch -M main
git remote add origin https://github.com/marcforques/analizador-noticias-scraping-ia.git
git push -u origin main
```

Si el remoto ya existe, se puede revisar con:

```bash
git remote -v
```

## Aviso

Este proyecto tiene fines academicos y demostrativos. No constituye asesoramiento financiero ni debe usarse como unica base para tomar decisiones de inversion.

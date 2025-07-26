
# LeanAI – Chatbot Inteligente para FAQs de INGELEAN

[Repositorio en GitHub](https://github.com/krito1020/LeanAI.git)

## Descripción

**LeanAI** es un chatbot basado en inteligencia artificial, diseñado para automatizar y mejorar la atención al cliente de INGELEAN S.A.S., respondiendo preguntas frecuentes de manera natural, rápida y eficiente. El sistema utiliza NLP, embeddings semánticos y aprendizaje automático sobre un set robusto de FAQs, y es fácilmente ampliable y entrenable.

---

## Estructura del Proyecto

- `/app.py` – API principal del chatbot (Flask)
- `/requirements.txt` – Dependencias del proyecto
- `/FAQs_Ingelean_Limpio.xlsx` – Dataset limpio de preguntas y respuestas
- `/FAQs_Ingelean_Limpio.csv` – Versión CSV del dataset (para embeddings/modelo)
- `/02_embeddings.py` – Script para generar los embeddings del dataset
- `/faq_embeddings.npy` – Embeddings generados (binario, necesario para app.py)
- `/chatbot_model.pkl` y `/tfidf_vectorizer.pkl` – Modelo y vectorizador de preguntas frecuentes
- Otros notebooks, scripts y utilidades

---

## Instalación Local

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/krito1020/LeanAI.git
   cd LeanAI
   ```

2. **Instala las dependencias (recomendado: entorno virtual)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Genera embeddings si es necesario**
   ```bash
   python 02_embeddings.py
   ```

4. **Ejecuta el chatbot**
   ```bash
   python app.py
   ```
   Accede a la API en `http://localhost:5000/predict`

---

## Despliegue en Render

- Sube tu repositorio a Render siguiendo la documentación oficial.
- Asegúrate de incluir los archivos de modelo y embeddings (`chatbot_model.pkl`, `tfidf_vectorizer.pkl`, `faq_embeddings.npy`).
- Usa un **Procfile** con la línea:
  ```
  web: gunicorn app:app --bind 0.0.0.0:$PORT
  ```

---

## Uso en Google Colab

Puedes subir y ejecutar los scripts en Colab para entrenar el modelo, generar embeddings, o consultar la API local en entorno colaborativo.

---

## API REST

- **POST** `/predict`
  - **Body:** `{"pregunta": "¿Tu consulta aquí?"}`
  - **Response:**  
    ```json
    {
      "categoria": "Categoría detectada",
      "respuesta": "Respuesta sugerida por el chatbot",
      "confianza": 0.92
    }
    ```

---

## Contacto y Créditos

Desarrollado por el grupo IKIGAI CODERS y el equipo de INGELEAN S.A.S.  
Para sugerencias, mejoras o reportar problemas, abre un Issue en el [repositorio GitHub](https://github.com/krito1020/LeanAI.git).

---

¡Gracias por usar LeanAI!

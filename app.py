import pandas as pd
import joblib
from flask import Flask, request, jsonify
import numpy as np

# Carga el modelo entrenado y el vectorizador TF-IDF
model = joblib.load('chatbot_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Carga las preguntas y respuestas para sugerir la respuesta (opcional: puedes cargar el csv, pero mejor un dict si ya está entrenado)
faq_df = pd.read_csv('FAQs_Ingelean_Limpio.csv')
faq_dict = dict(zip(faq_df['PREGUNTA'].astype(str).str.lower(), faq_df['RESPUESTA']))

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    pregunta = data.get('pregunta', '')
    if not pregunta:
        return jsonify({'error': 'No se recibió la pregunta'}), 400

    # Vectoriza la pregunta
    pregunta_vec = vectorizer.transform([pregunta])
    pred_cat = model.predict(pregunta_vec)[0]
    proba = model.predict_proba(pregunta_vec)[0]
    confianza = float(np.max(proba))

    # Sugerir respuesta (puedes buscar la respuesta por pregunta exacta o por categoría)
    respuesta = faq_df[faq_df['CATEGORIA'] == pred_cat]['RESPUESTA'].values
    if len(respuesta) > 0:
        respuesta = respuesta[0]
    else:
        respuesta = "Lo siento, no tengo una respuesta precisa para tu consulta."

    return jsonify({
        'categoria': pred_cat,
        'respuesta': respuesta,
        'confianza': confianza
    })
@app.route('/', methods=['GET'])
def index():
    return "LeanAI Chatbot API está viva. Usa POST /predict para hacer consultas.", 200
if __name__ == '__main__':
    app.run(debug=True)



import joblib
import pandas as pd
import numpy as np
import re
from unicodedata import normalize
from flask import Flask, request, jsonify

from sentence_transformers import SentenceTransformer, util

# ========== CONFIGURACIÓN Y CARGA ==========
app = Flask(__name__)

# Carga modelo y vectorizador
model = joblib.load('chatbot_model.pkl')
vectorizer = joblib.load('tfidf_vectorizer.pkl')

# Carga dataset
faq_df = pd.read_csv('FAQs_Ingelean_Limpio.csv')

# Carga modelo y embeddings semánticos
semantic_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
faq_embeddings = np.load('faq_embeddings.npy')

def clean_text(text):
    text = str(text).lower()
    text = normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^a-z0-9\s¿?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ========== FUNCIONES PRINCIPALES ==========

def buscar_respuesta_categoria(pred_cat):
    respuestas_cat = faq_df[faq_df['CATEGORIA'] == pred_cat]['RESPUESTA']
    if not respuestas_cat.empty:
        return respuestas_cat.iloc[0]
    return None

def buscar_por_embedding(pregunta_usuario, threshold=0.82):
    pregunta_proc = clean_text(pregunta_usuario)
    emb_usuario = semantic_model.encode([pregunta_proc])[0]
    # Calcula similitud coseno con todas las preguntas de la base
    similitudes = util.cos_sim(emb_usuario, faq_embeddings)[0]
    idx_max = int(np.argmax(similitudes.cpu().numpy()))
    score_max = float(similitudes[idx_max])
    if score_max >= threshold:
        respuesta = faq_df.iloc[idx_max]['RESPUESTA']
        categoria = faq_df.iloc[idx_max]['CATEGORIA']
        return respuesta, categoria, score_max
    return None, None, score_max

# ========== ENDPOINTS ==========

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    pregunta = data.get('pregunta', '')
    pregunta_limpia = clean_text(pregunta)
    X = vectorizer.transform([pregunta_limpia])
    pred_cat = model.predict(X)[0]
    # (Opcional) Si tu modelo tiene predict_proba, podrías agregar aquí lógica por baja confianza

    # 1. Buscar respuesta directa por categoría
    respuesta = buscar_respuesta_categoria(pred_cat)
    if respuesta:
        return jsonify({'categoria': pred_cat, 'respuesta': respuesta, 'tipo': 'modelo'})

    # 2. Si no, buscar por embeddings
    respuesta_emb, cat_emb, score = buscar_por_embedding(pregunta)
    if respuesta_emb:
        return jsonify({'categoria': cat_emb, 'respuesta': respuesta_emb, 'tipo': 'embedding', 'similitud': round(score, 3)})

    # 3. Fallback: no encontrado
    return jsonify({'categoria': "Desconocido", 'respuesta': "Lo siento, no entendí tu pregunta. ¿Puedes reformularla?", 'tipo': 'fallback'})

@app.route('/')
def home():
    return "¡LeanAI activo en Render!"

# ========== RUN LOCAL ==========
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

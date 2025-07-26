
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

df = pd.read_csv('FAQs_Ingelean_Limpio.csv')
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
embeddings = model.encode(df['pregunta_limpia'].tolist(), convert_to_tensor=False)
np.save('faq_embeddings.npy', embeddings)
print("faq_embeddings.npy generado.")

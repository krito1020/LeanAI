
import pandas as pd
import re
from unicodedata import normalize

# Carga el Excel original
df = pd.read_excel('FAQs_Ingelean.xlsx')

# Verifica nombres de columnas
print("Columnas disponibles:", df.columns)

# Asegura que las columnas clave se llamen así (ajusta si es necesario):
# 'CATEGORIA', 'PREGUNTA', 'RESPUESTA'

def clean_text(text):
    text = str(text).lower()
    text = normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^a-z0-9\s¿?]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['pregunta_limpia'] = df['PREGUNTA'].apply(clean_text)
df.to_csv('FAQs_Ingelean_Limpio.csv', index=False, encoding='utf-8')
print("FAQs_Ingelean_Limpio.csv generado.")

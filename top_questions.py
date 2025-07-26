import pandas as pd
import matplotlib.pyplot as plt

# Ruta al archivo CSV de preguntas frecuentes
FILE_PATH = 'FAQs_Ingelean_Limpio.csv'

# Carga el archivo CSV
df = pd.read_csv(FILE_PATH)

# Especifica el nombre de la columna de preguntas
col_pregunta = 'PREGUNTA'

# Calcula el top N de preguntas más frecuentes
top_n = 10
top_questions = df[col_pregunta].value_counts().head(top_n)

# Muestra el ranking en pantalla
print(f"\nTop {top_n} preguntas más frecuentes en el chatbot:\n")
for idx, (question, count) in enumerate(top_questions.items(), 1):
    print(f"{idx}. {question} ({count} veces)")

# Guarda el ranking en un archivo CSV
top_questions.to_csv('top_preguntas_frecuentes.csv', header=['Cantidad'])
print("\nArchivo 'top_preguntas_frecuentes.csv' generado con el ranking.")

# Grafica el top 5 de preguntas más frecuentes
top_5 = top_questions.head(5)
plt.figure(figsize=(10, 5))
top_5.plot(kind='barh', color='skyblue')
plt.xlabel('Cantidad')
plt.ylabel('Pregunta')
plt.title('Top 5 preguntas más frecuentes')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

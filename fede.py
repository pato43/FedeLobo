import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial
st.set_page_config(page_title="Simulación de Parecidos al Fedelobo", layout="wide")

# --- Datos base (puedes cambiar las rutas o subir tus archivos) ---
csv_file = "fedelobo_simulacion.csv"  # Debes tenerlo en la misma carpeta
pdf_file = "fedelobo_paper.pdf"        # El PDF generado de tu paper

# Cargar datos
df = pd.read_csv(csv_file)

# --- Estilo gráfico ---
sns.set(style="whitegrid")

# --- Título ---
st.title("🧬 Simulación de Parecidos al Fedelobo")
st.markdown("""
Esta plataforma muestra el análisis matemático y la simulación realizada para estimar
cuántas personas en una población grande podrían parecerse al creador de contenido mexicano "Fedelobo".  
Se utilizó un modelo basado en distancia de Mahalanobis y distribución chi-cuadrada.
""")

# --- Resultados clave ---
st.header("🔍 Resultados Principales")
col1, col2, col3 = st.columns(3)
col1.metric("Personas Simuladas", "10,000")
col2.metric("Parecidos Simulados", "750")
col3.metric("Parecidos Esperados", "1,046 (modelo)")

st.write("---")

# --- Mostrar gráficos ---
st.header("📈 Visualizaciones")

# Gráfico PCA
st.subheader("Distribución PCA de Parecidos al Fedelobo")
fig, ax = plt.subplots(figsize=(8,6))
sns.scatterplot(
    data=df,
    x="PC1", y="PC2",
    hue="Parecido_a_Fedelobo",
    palette=["#a0aec0", "#f56565"],
    alpha=0.6
)
plt.title("Distribución PCA de Parecidos al Fedelobo")
plt.xlabel("Componente Principal 1")
plt.ylabel("Componente Principal 2")
plt.legend(title="¿Se parece al Fedelobo?")
st.pyplot(fig)

# --- Segundo gráfico: Crecimiento
st.subheader("Número de Parecidos vs Tamaño de Población")
population_sizes = list(range(1000, 21000, 2000))
parecidos_estimados = [int(0.075 * size) for size in population_sizes]

fig2, ax2 = plt.subplots(figsize=(8,6))
sns.lineplot(x=population_sizes, y=parecidos_estimados, marker="o", color="#f56565")
plt.title("Crecimiento Estimado de Parecidos")
plt.xlabel("Tamaño de la Población")
plt.ylabel("Número de Parecidos")
plt.grid(True)
st.pyplot(fig2)

st.write("---")

# --- Descargas ---
st.header("📥 Descargas disponibles")

with open(pdf_file, "rb") as pdf:
    st.download_button(
        label="📄 Descargar Paper PDF",
        data=pdf,
        file_name="fedelobo_paper.pdf",
        mime="application/pdf"
    )

with open(csv_file, "rb") as csv:
    st.download_button(
        label="📈 Descargar Base de Datos CSV",
        data=csv,
        file_name="fedelobo_simulacion.csv",
        mime="text/csv"
    )

st.write("---")

# --- Footer ---
st.markdown("""
---
*Desarrollado por Alexander Eduardo Rojas Garay*  
[LinkedIn](https://www.linkedin.com/in/alexander-eduardo-rojas-garay-b17471235/)
""")

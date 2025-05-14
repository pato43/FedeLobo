import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# Configuración de página
st.set_page_config(
    page_title="Dashboard Fedelobo Simulation", layout="wide", initial_sidebar_state="expanded"
)

# Logo del canal Fedelobo (coloca el archivo 'fedelobo_logo.png' en la carpeta o usa una URL)
st.logo_image = "fedelobo_logo.png"
st.image(st.logo_image, width=120)

# Título y descripción
st.title("🧬 Simulación de Parecidos al Fedelobo")
st.markdown(
    "**Ámbito:** México 🇲🇽  
    Análisis basado en distancia de Mahalanobis y distribución chi-cuadrada."
)

# --- Carga de datos ---
df = pd.read_csv("fedelobo_simulacion.csv")

# --- Panel lateral (filtros) ---
st.sidebar.header("Filtros de PCA")
pc1_min, pc1_max = st.sidebar.slider(
    "Rango de PC1",
    float(df["PC1"].min()),
    float(df["PC1"].max()),
    (float(df["PC1"].min()), float(df["PC1"].max()))
)
pc2_min, pc2_max = st.sidebar.slider(
    "Rango de PC2",
    float(df["PC2"].min()),
    float(df["PC2"].max()),
    (float(df["PC2"].min()), float(df["PC2"].max()))
)
df_filtered = df[
    (df["PC1"] >= pc1_min) & (df["PC1"] <= pc1_max) &
    (df["PC2"] >= pc2_min) & (df["PC2"] <= pc2_max)
]

# --- Métricas clave ---
col1, col2, col3 = st.columns(3)
col1.metric("Personas Simuladas", len(df))
col2.metric("Parecidos Simulados", int(df["Parecido_a_Fedelobo"].sum()))
col3.metric("Parecidos Esperados", "1,046 (modelo)")

st.write("---")

# --- Gráficos interactivos en dos columnas ---
chart_col1, chart_col2 = st.columns(2)

# Scatter PCA interactivo
chart_col1.subheader("📈 Distribución PCA Interactiva")
fig_scatter = px.scatter(
    df_filtered,
    x="PC1",
    y="PC2",
    color="Parecido_a_Fedelobo",
    color_discrete_map={0: "#a0aec0", 1: "#f56565"},
    labels={"Parecido_a_Fedelobo": "¿Se parece al Fedelobo?"},
    title="PCA Interactivo"
)
chart_col1.plotly_chart(fig_scatter, use_container_width=True)

# Línea de crecimiento
chart_col2.subheader("📊 Crecimiento de Parecidos")
population_sizes = list(range(1000, 21000, 2000))
parecidos_estimados = [int(0.075 * size) for size in population_sizes]
growth_df = pd.DataFrame({"Población": population_sizes, "Parecidos": parecidos_estimados})
fig_line = px.line(
    growth_df,
    x="Población",
    y="Parecidos",
    markers=True,
    title="Parecidos vs Tamaño de Población"
)
chart_col2.plotly_chart(fig_line, use_container_width=True)

st.write("---")

# --- Mapa de México con Pydeck ---
st.subheader("🗺️ Mapa de México: Punto Centrado")
mexico_map = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=23.6345, longitude=-102.5528, zoom=4.2, pitch=0
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame([{"lat": 23.6345, "lon": -102.5528}]),
            get_position=["lon", "lat"],
            get_radius=50000,
            get_color=[255, 0, 0, 140],
            pickable=False,
        )
    ],
)
st.pydeck_chart(mexico_map)

st.write("---")

# --- Descargas ---
st.header("📥 Descargas")
with open("fedelobo_paper.pdf", "rb") as pdf_file:
    st.download_button("Descargar Paper (PDF)", pdf_file, file_name="fedelobo_paper.pdf")
with open("fedelobo_simulacion.csv", "rb") as csv_file:
    st.download_button("Descargar datos CSV", csv_file, file_name="fedelobo_simulacion.csv")

st.write("---")

# --- Footer ---
st.markdown(
    "*Desarrollado por Alexander Eduardo Rojas Garay*  
    [LinkedIn](https://www.linkedin.com/in/alexander-eduardo-rojas-garay-b17471235/)")

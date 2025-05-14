import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# Configuración de página
st.set_page_config(
    page_title="Dashboard Fedelobo Simulation",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar: Descargas
st.sidebar.header("📥 Descargas")
with open("fedelobo_paper.pdf", "rb") as pdf_file:
    st.sidebar.download_button(
        "Descargar Paper (PDF)", pdf_file, file_name="fedelobo_paper.pdf"
    )
with open("fedelobo_simulacion.csv", "rb") as csv_file:
    st.sidebar.download_button(
        "Descargar datos CSV", csv_file, file_name="fedelobo_simulacion.csv"
    )

# Logo y título
logo_file = "fedelobo1.jpg"  # Actualiza con la ruta o URL de tu logo
st.image(logo_file, width=120)
st.title("🧬 Simulación de Parecidos al Fedelobo")
st.markdown(
    """
**Ámbito:** México 🇲🇽  
Análisis basado en distancia de Mahalanobis y distribución chi-cuadrada.
    """
)

# Carga de datos
df = pd.read_csv("fedelobo_simulacion.csv")

# Métricas clave
col1, col2, col3 = st.columns(3)
col1.metric("Personas Simuladas", f"{len(df):,}")
col2.metric("Parecidos Simulados", f"{int(0.075 * len(df)):,}")
col3.metric("Parecidos Esperados", "1,046 (modelo)")

st.write("---")

# Gráficos y mapa en grid
g1, g2, g3 = st.columns(3)

# PCA interactivo
g1.subheader("📈 PCA Interactivo")
fig_scatter = px.scatter(
    df,
    x="PC1", y="PC2",
    color="Parecido_a_Fedelobo",
    color_discrete_map={0: "#a0aec0", 1: "#f56565"},
    labels={"Parecido_a_Fedelobo": "¿Se parece al Fedelobo?"},
    title="Distribución PCA"
)
g1.plotly_chart(fig_scatter, use_container_width=True)

# Crecimiento de Parecidos
g2.subheader("📊 Crecimiento de Parecidos")
pop_sizes = list(range(1000, 21000, 2000))
parecidos = [int(0.075 * s) for s in pop_sizes]
growth_df = pd.DataFrame({"Población": pop_sizes, "Parecidos": parecidos})
fig_line = px.line(
    growth_df, x="Población", y="Parecidos",
    markers=True, title="Parecidos vs Tamaño de Población"
)
g2.plotly_chart(fig_line, use_container_width=True)

# Mapa de México (GeoJSON, estilo oscuro)
g3.subheader("🗺️ Mapa de México por Estado")
geojson_path = "mexicoHigh.json"
mexico_geo = pdk.Layer(
    "GeoJsonLayer",
    data=geojson_path,
    stroked=True,
    filled=True,
    get_fill_color=[200, 200, 200, 100],
    get_line_color=[40, 40, 40, 200],
)
deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=pdk.ViewState(latitude=23.6345, longitude=-102.5528, zoom=4.2),
    layers=[mexico_geo],
    height=350
)
g3.pydeck_chart(deck, use_container_width=True)

st.write("---")

# Footer
st.markdown(
    """
*Desarrollado por Alexander Eduardo Rojas Garay*  
[LinkedIn](https://www.linkedin.com/in/alexander-eduardo-rojas-garay-b17471235/)
    """
)

import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk

# Configuración de página
st.set_page_config(
    page_title="Dashboard Fedelobo Simulation",
    layout="wide"
)

# Carga de datos
df = pd.read_csv("fedelobo_simulacion.csv")

# Header: Logo y Título en columnas
logo_file = "fedelobo1.jpg"  # Actualiza con la ruta/URL de tu logo
col_logo, col_title = st.columns([1, 5])
col_logo.image(logo_file, width=100)
col_title.markdown(
    """
# 🧬 Simulación de Parecidos al Fedelobo  
**Ámbito:** México 🇲🇽  
Análisis basado en distancia de Mahalanobis y distribución chi-cuadrada.
    """
)

# Métricas clave
d1, d2, d3 = st.columns(3)
d1.metric("Personas Simuladas", f"{len(df):,}")
d2.metric("Parecidos Simulados", f"{int(0.075 * len(df)):,}")
d3.metric("Parecidos Esperados", "1,046 (modelo)")

st.markdown("---")

# Gráficos y mapa en layout de 3 columnas
g1, g2, g3 = st.columns(3)

# 1) PCA Interactivo
g1.subheader("📈 PCA Interactivo")
fig_scatter = px.scatter(
    df,
    x="PC1", y="PC2",
    color="Parecido_a_Fedelobo",
    color_discrete_map={0: "#a0aec0", 1: "#f56565"},
    labels={"Parecido_a_Fedelobo": "¿Se parece?"}
)
g1.plotly_chart(fig_scatter, use_container_width=True, height=300)

# 2) Crecimiento de Parecidos
g2.subheader("📊 Crecimiento de Parecidos")
pop_sizes = list(range(1000, 21000, 2000))
parecidos = [int(0.075 * s) for s in pop_sizes]
growth_df = pd.DataFrame({"Población": pop_sizes, "Parecidos": parecidos})
fig_line = px.line(
    growth_df,
    x="Población", y="Parecidos",
    markers=True
)
g2.plotly_chart(fig_line, use_container_width=True, height=300)

# 3) Mapa de México (GeoJSON, oscuro)
g3.subheader("🗺️ Mapa de México por Estado")
geojson_path = "mexicoHigh.json"
mexico_geo = pdk.Layer(
    "GeoJsonLayer",
    data=geojson_path,
    stroked=True,
    filled=True,
    get_fill_color=[80, 80, 80, 80],
    get_line_color=[200, 200, 200, 150]
)
deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v10",
    initial_view_state=pdk.ViewState(latitude=23.6345, longitude=-102.5528, zoom=4.2),
    layers=[mexico_geo],
    height=300
)
g3.pydeck_chart(deck, use_container_width=True)

st.markdown("---")

# Descargas al final en dos columnas
dl1, dl2 = st.columns(2)
dl1.download_button(
    "📄 Descargar Paper (PDF)",
    open("fedelobo_paper.pdf", "rb"),
    file_name="fedelobo_paper.pdf"
)
dl2.download_button(
    "📈 Descargar datos CSV",
    open("fedelobo_simulacion.csv", "rb"),
    file_name="fedelobo_simulacion.csv"
)

# Footer
st.markdown(
    """
---  
*Desarrollado por Alexander Eduardo Rojas Garay*  
[LinkedIn](https://www.linkedin.com/in/alexander-eduardo-rojas-garay-b17471235/)
    """
)

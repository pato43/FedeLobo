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

# Sidebar: Descargas y enlace
st.sidebar.header("📥 Descargas")
with open("fedelobo_paper.pdf", "rb") as pdf_file:
    st.sidebar.download_button("Descargar Paper (PDF)", pdf_file, file_name="fedelobo_paper.pdf")
with open("fedelobo_simulacion.csv", "rb") as csv_file:
    st.sidebar.download_button("Descargar datos CSV", csv_file, file_name="fedelobo_simulacion.csv")

# Logo y título
logo_file = "fedelobo1.jpg"  # Asegúrate de tener este archivo o usar URL
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

# --- Métricas clave (primera pantalla) ---
m1, m2, m3 = st.columns(3)
m1.metric("Personas Simuladas", f"{len(df):,}")
m2.metric("Parecidos Simulados", f"{int(0.075 * len(df)):,}")
m3.metric("Parecidos Esperados", "1,046 (modelo)")

# --- Gráficos y mapa en formato grid (primera pantalla) ---
g1, g2, g3 = st.columns(3)

# Gráfico PCA interactivo
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

# Gráfico línea de crecimiento
g2.subheader("📊 Crecimiento de Parecidos")
pop_sizes = list(range(1000, 21000, 2000))
parecidos = [int(0.075 * s) for s in pop_sizes]
growth_df = pd.DataFrame({"Población": pop_sizes, "Parecidos": parecidos})
fig_line = px.line(
    growth_df, x="Población", y="Parecidos",
    markers=True, title="Parecidos vs Población"
)
g2.plotly_chart(fig_line, use_container_width=True)

# Mapa centrado en CDMX
g3.subheader("🗺️ Ubicación CDMX")
mx_map = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=19.4326, longitude=-99.1332, zoom=9, pitch=0
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=pd.DataFrame([{"lat": 19.4326, "lon": -99.1332}]),
            get_position=["lon", "lat"],
            get_radius=20000,
            get_color=[255, 0, 0, 180],
            pickable=False,
        )
    ],
)
g3.pydeck_chart(mx_map)

# Footer
st.markdown(
    """
---  
*Desarrollado por Alexander Eduardo Rojas Garay*  
[LinkedIn](https://www.linkedin.com/in/alexander-eduardo-rojas-garay-b17471235/)
    """
)

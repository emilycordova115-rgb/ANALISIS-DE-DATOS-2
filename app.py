
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="PROECUADOR - Inteligencia Comercial", layout="wide")

# Datos Iniciales
raw_data = [
    {"Partida": "0306.17.19.00", "Producto": "Camarones y langostinos (Los demás)", "FOB": 829264250.97, "Peso": 73708419.85, "Sector": "Acuacultura", "Tipo": "Especialidad"},
    {"Partida": "2709.00.00.00", "Producto": "Aceites crudos de petróleo", "FOB": 782882983.81, "Peso": 1607062180.90, "Sector": "Petrolero", "Tipo": "Primario Puro"},
    {"Partida": "0603.11.00.00", "Producto": "Rosas frescas", "FOB": 417946959.96, "Peso": 45260714.69, "Sector": "Florícola", "Tipo": "Especialidad"},
    {"Partida": "0803.90.11.90", "Producto": "Bananos o plátanos frescos (Los demás)", "FOB": 281395189.50, "Peso": 277283032.71, "Sector": "Bananero", "Tipo": "Tradicional"},
    {"Partida": "2710.19.22.00", "Producto": "Fueloils (Fuel oil)", "FOB": 97333824.17, "Peso": 331629970.00, "Sector": "Petrolero", "Tipo": "Primario Puro"},
    {"Partida": "7108.12.00.00", "Producto": "Oro en bruto (Las demás formas)", "FOB": 91316479.71, "Peso": 12991.24, "Sector": "Minero", "Tipo": "Primario Puro"},
    {"Partida": "1801.00.19.90", "Producto": "Cacao en grano (Los demás)", "FOB": 90869753.72, "Peso": 32327152.00, "Sector": "Cacaotero", "Tipo": "Tradicional"},
    {"Partida": "2603.00.00.00", "Producto": "Minerales de cobre y sus concentrados", "FOB": 79488726.48, "Peso": 2629719.48, "Sector": "Minero", "Tipo": "Primario Puro"},
    {"Partida": "0306.17.11.00", "Producto": "Camarones enteros", "FOB": 76380476.51, "Peso": 14030538.77, "Sector": "Acuacultura", "Tipo": "Especialidad"},
    {"Partida": "0603.19.90.90", "Producto": "Las demás flores frescas", "FOB": 63519044.42, "Peso": 3508949.09, "Sector": "Florícola", "Tipo": "Especialidad"},
    {"Partida": "0803.90.11.10", "Producto": "Banano Orgánico Certificado", "FOB": 62029278.47, "Peso": 34135029.15, "Sector": "Bananero", "Tipo": "Especialidad"},
    {"Partida": "0306.17.99.90", "Producto": "Otros crustáceos (Los demás)", "FOB": 57475546.13, "Peso": 6928363.55, "Sector": "Acuacultura", "Tipo": "Especialidad"},
    {"Partida": "2616.90.10.00", "Producto": "Minerales de oro y sus concentrados", "FOB": 45491951.02, "Peso": 13176723.49, "Sector": "Minero", "Tipo": "Primario Puro"},
    {"Partida": "0603.19.10.00", "Producto": "Gypsophila (Lluvia, ilusión)", "FOB": 34101988.85, "Peso": 585667.03, "Sector": "Florícola", "Tipo": "Especialidad"}
]

df = pd.DataFrame(raw_data)
df['Precio_KG'] = df['FOB'] / df['Peso']

# Header
st.title("📊 Dirección de Inteligencia Comercial — PROECUADOR")
st.subheader("Cuadro de Mando Interactivo y Diagnóstico del Portafolio Exportable (Cierre 2025)")
st.markdown("---")

# Sidebar Filters
st.sidebar.header("Filtros de Control")
sector_filter = st.sidebar.multiselect("Selecciona el Sector Madre:", df['Sector'].unique(), default=df['Sector'].unique())
tipo_filter = st.sidebar.multiselect("Selecciona el Tipo Estructural:", df['Tipo'].unique(), default=df['Tipo'].unique())

filtered_df = df[(df['Sector'].isin(sector_filter)) & (df['Tipo'].isin(tipo_filter))]

# KPIs Row
total_fob = filtered_df['FOB'].sum()
total_peso = filtered_df['Peso'].sum()
extractivo_fob = df[df['Tipo'] == 'Primario Puro']['FOB'].sum()
total_fob_global = df['FOB'].sum()
vulnerabilidad = (extractivo_fob / total_fob_global) * 100

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Total Exportado FOB Seleccionado", f"${total_fob:,.2f} USD")
kpi2.metric("Volumen Movilizado Seleccionado", f"{total_peso:,.2f} KG")
kpi3.metric("Índice de Vulnerabilidad Extractiva (Global)", f"{vulnerabilidad:.2f}%")

st.markdown("---")

# Charts Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Participación de Ingresos por Sector Madre")
    fig_pie = px.pie(filtered_df, values='FOB', names='Sector', title='Distribución del Valor FOB', hole=0.4, color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("Análisis de Densidad Económica (Precio por KG)")
    fig_bar = px.bar(filtered_df.sort_values(by='Precio_KG', ascending=False), x='Producto', y='Precio_KG', color='Sector', title='Precio Promedio FOB por Kilogramo', labels={'Precio_KG':'USD por KG'})
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Data Table View
st.subheader("Detalle Arancelario Completo")
st.dataframe(filtered_df.style.format({'FOB': '${:,.2f}', 'Peso': '{:,.2f} KG', 'Precio_KG': '${:,.2f}'}))

# Tablas Teóricas / Cualitativas
st.markdown("---")
st.subheader("💡 Lentes de Análisis Avanzado")

tab1, tab2 = st.tabs(["Matriz de Aceptación Transcultural", "Estrategias de Escalamiento (Upgrading)"])

with tab1:
    st.markdown("### Índice de Aceptación Cultural Internacional por País Destino")
    cultural_matrix = pd.DataFrame([
        {"Producto": "Banano Orgánico Certificado", "Japón": "Media (Asimilación Premium)", "Estados Unidos": "Alta (Hibridación Wellness)", "Alemania": "Alta (Sostenibilidad Radical)"},
        {"Producto": "Rosas y Gypsophila", "Japón": "Alta (Minimalismo / Ikebana)", "Estados Unidos": "Alta (Diáspora / Estacional)", "Alemania": "Media (Exigencia Huella Carbono)"},
        {"Producto": "Cacao en Grano", "Japón": "Alta (Lujo / Regalo Estético)", "Estados Unidos": "Alta (Fusión Comercial)", "Alemania": "Alta (Certificación FairTrade)"}
    ])
    st.table(cultural_matrix)

with tab2:
    st.markdown("### Lineamientos para Romper la Trampa Centro-Periferia")
    st.info("**1. Cacao en Grano:** Transicionar del commodity bruto hacia la exportación de coberturas industriales finas y manteca de cacao orgánica certificada.")
    st.info("**2. Banano Orgánico:** Redirigir el esfuerzo de promoción hacia la Unión Europea para capturar la prima de precio del 80.2% frente al banano convencional.")

# streamlit_app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("basededatos.csv")  # replace with your actual file name

df = load_data()

# Dashboard Title
st.title("Dashboard de Riesgo del Cliente")

# Sidebar Filters
st.sidebar.header("Opción de Filtro")
risk_level = st.sidebar.multiselect("Seleccione el Nivel de Riesgo", options=df["Nivel de Riesgo"].unique(), default=df["Nivel de Riesgo"].unique())
payment_type = st.sidebar.multiselect("Seleccione el Tipo de Pago", options=df["tipo de pago"].unique(), default=df["tipo de pago"].unique())

# Filtered Data
filtered_df = df[(df["Nivel de Riesgo"].isin(risk_level)) & (df["tipo de pago"].isin(payment_type))]

# Key Figures
st.markdown("<h3 style='font-size:24px;'>Indicadores Clave</h3>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.metric("Clientes Totales", len(filtered_df))
col2.metric("Días de Retraso Promedio", round(filtered_df["max_dias"].mean(), 2))
col3.metric("Préstamos Pendientes Promedio", round(filtered_df["prestamos_outstanding"].mean(), 2))

# Agent/Client Table
st.markdown("<h3 style='font-size:24px;'>Visión General del Cliente</h3>", unsafe_allow_html=True)
st.dataframe(filtered_df[["ID_Cliente", "Nivel de Riesgo", "tipo de pago", "cuotas_pagadas",
                          "prestamos_outstanding", "prestamo_mora", "fecha_ultimo_pago", "fecha_proximo_pago"]].sort_values("Nivel de Riesgo"),
             use_container_width=True)

# Pie Chart – Distribution by Risk
st.markdown("<h3 style='font-size:24px;'>Clientes por Nivel de Riesgo</h3>", unsafe_allow_html=True)
fig_risk = px.pie(filtered_df, names="Nivel de Riesgo", title="Distribución de Riesgos", hole=0.4)
st.plotly_chart(fig_risk, use_container_width=True)

# Gráficas comparativas: Barra vs Dispersión
st.markdown("<h3 style='font-size:24px;'>Comparativa: Morosidad vs Deuda Activa</h3>", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("<h4 style='font-size:20px;'>Morosidad Promedio por Forma de Pago</h4>", unsafe_allow_html=True)

    fig_bar = px.bar(
        filtered_df.groupby("tipo de pago")["cuotas_tarde"].mean().reset_index(),
        x="tipo de pago",
        y="cuotas_tarde",
        color="tipo de pago",
        labels={"cuotas_tarde": "Cuotas Tarde Promedio", "tipo de pago": "Tipo de Pago"},
        title="Impuntualidad por Tipo de Pago"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    st.markdown("<h4 style='font-size:20px;'>Deuda Activa Frente a Préstamo en Mora</h4>", unsafe_allow_html=True)

    fig_scatter = px.scatter(
        filtered_df,
        x="prestamos_outstanding",
        y="prestamo_mora",
        color="Nivel de Riesgo",
        hover_data=["ID_Cliente"],
        labels={
            "prestamos_outstanding": "Préstamos Activos",
            "prestamo_mora": "Préstamos en Mora"
        },
        title="Préstamos Activos Frente a Préstamos Morosos"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


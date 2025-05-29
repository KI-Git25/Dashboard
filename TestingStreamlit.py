import streamlit as st
import pandas as pd

st.title("📊 Panel de Ventas - Análisis por Región y Vendedor")

#Subir archivo
uploaded_file = st.file_uploader("🔄 Sube el archivo Excel con los datos de vendedores", type=["xlsx"])

if uploaded_file is not None:
    @st.cache_data
    def load_data(file):
        df = pd.read_excel(file, sheet_name=0)
        df["NOMBRE_COMPLETO"] = df["NOMBRE"] + " " + df["APELLIDO"]
        df["PORCENTAJE DE VENTAS"] = df["PORCENTAJE DE VENTAS"].astype(float)
        df["VENTAS PROMEDIO"] = df["VENTAS TOTALES"] / df["UNIDADES VENDIDAS"]
        return df

    df = load_data(uploaded_file)

    #Sección 1 - Tabla por región
    with st.container():
        st.subheader("📍 Filtrar por Región")
        regiones = sorted(df["REGION"].dropna().unique())
        region = st.selectbox("Selecciona una región:", regiones)
        df_region = df[df["REGION"] == region]
        st.write("### Tabla de Datos Filtrada")
        st.dataframe(df_region, use_container_width=True)

    #Sección 2 - Gráficas
    with st.container():
        st.subheader("📈 Gráficas de la Región Seleccionada")
        st.write("### Unidades Vendidas")
        st.bar_chart(df_region.set_index("NOMBRE_COMPLETO")["UNIDADES VENDIDAS"])

        st.write("### Ventas Totales")
        st.bar_chart(df_region.set_index("NOMBRE_COMPLETO")["VENTAS TOTALES"])

        st.write("### Ventas Promedio")
        st.bar_chart(df_region.set_index("NOMBRE_COMPLETO")["VENTAS PROMEDIO"])

    #Sección 3 - Búsqueda de vendedor
    with st.container():
        st.subheader("🔍 Buscar Vendedor")
        vendedor_input = st.text_input("Escribe el nombre o apellido del vendedor:")
        if st.button("Buscar"):
            resultado = df[
                df["NOMBRE"].str.contains(vendedor_input, case=False, na=False) |
                df["APELLIDO"].str.contains(vendedor_input, case=False, na=False)
            ]
            if not resultado.empty:
                st.success(f"{len(resultado)} resultado(s) encontrado(s):")
                st.dataframe(resultado, use_container_width=True)
            else:
                st.warning("No se encontraron coincidencias.")
else:
    st.info("Por favor, sube un archivo Excel (.xlsx) para comenzar.")

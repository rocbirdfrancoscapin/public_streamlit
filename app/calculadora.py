import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

def calcular_business_case():
    st.title("Calculadora de Business Case: Prevención de Fraude en Pickit")
    
    st.subheader("Ingrese los datos para calcular el ROI y ahorro esperado")
    
    # Entradas del usuario
    auditorias_mensuales = st.number_input("Cantidad de auditorías manuales por mes", min_value=0, value=20000)
    costo_auditoria_manual = st.number_input("Costo promedio por auditoría manual (USD)", min_value=0.0, value=250.0)
    fraudes_mensuales = st.number_input("Cantidad de fraudes detectados por mes", min_value=0, value=100)
    costo_total_fraudes = st.number_input("Costo total de fraudes mensuales (USD)", min_value=0.0, value=20000.0)
    porcentaje_reduccion_auditorias = st.slider("Porcentaje esperado de reducción en auditorías manuales (%)", 0, 100, 50)
    porcentaje_reduccion_fraudes = st.slider("Porcentaje esperado de reducción en fraudes (%)", 0, 100, 40)
    inversion_inicial = st.number_input("Costo estimado de implementación de la solución (USD)", min_value=0.0, value=500000.0)
    
    if st.button("Calcular Business Case"):
        # Conversión de porcentajes
        porcentaje_reduccion_auditorias /= 100
        porcentaje_reduccion_fraudes /= 100
        
        # Cálculos de costos actuales
        costo_total_auditorias = auditorias_mensuales * costo_auditoria_manual
        auditorias_reducidas = auditorias_mensuales * (1 - porcentaje_reduccion_auditorias)
        costo_total_auditorias_reducido = auditorias_reducidas * costo_auditoria_manual
        fraudes_reducidos = fraudes_mensuales * (1 - porcentaje_reduccion_fraudes)
        costo_total_fraudes_reducido = costo_total_fraudes * (1 - porcentaje_reduccion_fraudes)
        
        # Ahorros
        ahorro_auditorias = costo_total_auditorias - costo_total_auditorias_reducido
        ahorro_fraudes = costo_total_fraudes - costo_total_fraudes_reducido
        ahorro_total = ahorro_auditorias + ahorro_fraudes
        meses_recuperacion = inversion_inicial / ahorro_total if ahorro_total > 0 else np.inf
        
        # Mostrar resultados
        st.subheader("Resultados")
        st.write(f"Reducción en auditorías manuales a: {auditorias_reducidas:,.0f} auditorías/mes")
        st.write(f"Nuevo costo total de auditorías: ${costo_total_auditorias_reducido:,.2f} USD")
        st.write(f"Reducción en fraudes a: {fraudes_reducidos:,.0f} casos/mes")
        st.write(f"Nuevo costo total de fraudes: ${costo_total_fraudes_reducido:,.2f} USD")
        st.write(f"Ahorro total estimado mensual: ${ahorro_total:,.2f} USD")
        st.write(f"Tiempo estimado de recuperación de inversión: {meses_recuperacion:.2f} meses")
        
        # Curva de amortización en 3 años (36 meses)
        meses = np.arange(1, 37)
        ahorro_acumulado = np.cumsum(np.full(36, ahorro_total))
        inversion_acumulada = np.full(36, inversion_inicial)
        roi_acumulado = (ahorro_acumulado - inversion_acumulada) / inversion_acumulada * 100
        
        # Crear DataFrame para visualización
        df = pd.DataFrame({
            "Meses": meses,
            "Ahorro Acumulado": ahorro_acumulado,
            "ROI Acumulado (%)": roi_acumulado
        })
        
        # Gráficos en BI con Plotly
        st.subheader("Tablero de BI - Proyección de ROI")
        fig = px.line(df, x="Meses", y=["Ahorro Acumulado", "ROI Acumulado (%)"],
                      title="Proyección de ROI a 3 años", markers=True)
        st.plotly_chart(fig)

        # Gráfica de amortización
        st.subheader("Gráfica de ROI Acumulado")
        fig, ax = plt.subplots()
        ax.plot(meses, roi_acumulado, marker='o', linestyle='-')
        ax.set_xlabel("Meses")
        ax.set_ylabel("ROI Acumulado (%)")
        ax.set_title("Curva de Amortización del ROI")
        ax.grid(True)
        st.pyplot(fig)

if __name__ == "__main__":
    calcular_business_case()
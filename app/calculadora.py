import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Función para cálculos de ahorros
def calcular_ahorros(auditorias_mensuales, costo_auditoria_manual, fraudes_mensuales, costo_total_fraudes,
                     porc_red_auditorias, porc_red_fraudes, inversion_inicial):
    # Costos actuales
    costo_total_auditorias = auditorias_mensuales * costo_auditoria_manual
    
    # Reducciones proyectadas
    auditorias_reducidas = auditorias_mensuales * (1 - porc_red_auditorias)
    costo_auditorias_reducido = auditorias_reducidas * costo_auditoria_manual
    fraudes_reducidos = fraudes_mensuales * (1 - porc_red_fraudes)
    costo_fraudes_reducido = costo_total_fraudes * (1 - porc_red_fraudes)
    
    # Ahorros
    ahorro_auditorias = costo_total_auditorias - costo_auditorias_reducido
    ahorro_fraudes = costo_total_fraudes - costo_fraudes_reducido
    ahorro_total = ahorro_auditorias + ahorro_fraudes
    
    # Tiempo de recuperación (evitar división por cero)
    meses_recuperacion = inversion_inicial / ahorro_total if ahorro_total > 0 else float('inf')
    
    return {
        "costo_total_auditorias": costo_total_auditorias,
        "auditorias_reducidas": auditorias_reducidas,
        "costo_auditorias_reducido": costo_auditorias_reducido,
        "fraudes_reducidos": fraudes_reducidos,
        "costo_fraudes_reducido": costo_fraudes_reducido,
        "ahorro_total": ahorro_total,
        "meses_recuperacion": meses_recuperacion
    }

# Función para generar proyección de ROI
def generar_proyeccion(ahorro_total, inversion_inicial, horizonte_meses=36):
    meses = np.arange(1, horizonte_meses + 1)
    ahorro_acumulado = np.cumsum(np.full(horizonte_meses, ahorro_total))
    inversion_acumulada = np.full(horizonte_meses, inversion_inicial)
    roi_acumulado = (ahorro_acumulado - inversion_acumulada) / inversion_acumulada * 100
    
    return pd.DataFrame({
        "Meses": meses,
        "Ahorro Acumulado (USD)": ahorro_acumulado,
        "ROI Acumulado (%)": roi_acumulado
    })

# Interfaz principal
def calcular_business_case():
    st.title("Calculadora de Business Case: Prevención de Fraude en Pickit")
    st.subheader("Ingrese los datos para calcular el ROI y ahorro esperado")

    # Entradas del usuario
    auditorias_mensuales = st.number_input("Auditorías manuales por mes", min_value=0, value=20000)
    costo_auditoria_manual = st.number_input("Costo por auditoría manual (USD)", min_value=0.0, value=5.0)
    fraudes_mensuales = st.number_input("Fraudes detectados por mes", min_value=0, value=100)
    costo_total_fraudes = st.number_input("Costo total de fraudes mensuales (USD)", min_value=0.0, value=20000.0)
    porc_red_auditorias = st.slider("Reducción esperada en auditorías (%)", 0, 100, 50) / 100
    porc_red_fraudes = st.slider("Reducción esperada en fraudes (%)", 0, 100, 40) / 100
    inversion_inicial = st.number_input("Costo de implementación (USD)", min_value=0.0, value=50000.0)
    
    if st.button("Calcular Business Case"):
        # Calcular ahorros
        resultados = calcular_ahorros(auditorias_mensuales, costo_auditoria_manual, fraudes_mensuales,
                                      costo_total_fraudes, porc_red_auditorias, porc_red_fraudes, inversion_inicial)
        
        # Validar resultados
        if resultados["ahorro_total"] <= 0:
            st.error("El ahorro total es cero o negativo. Revisa los valores ingresados.")
            return
        
        # Mostrar resultados en columnas
        st.subheader("Resultados")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Costo actual auditorías: ${resultados['costo_total_auditorias']:,.2f} USD")
            st.write(f"Auditorías reducidas: {resultados['auditorias_reducidas']:,.0f}/mes")
            st.write(f"Nuevo costo auditorías: ${resultados['costo_auditorias_reducido']:,.2f} USD")
        with col2:
            st.write(f"Fraudes reducidos: {resultados['fraudes_reducidos']:,.0f}/mes")
            st.write(f"Nuevo costo fraudes: ${resultados['costo_fraudes_reducido']:,.2f} USD")
            st.write(f"Ahorro total mensual: ${resultados['ahorro_total']:,.2f} USD")
        
        st.write(f"Tiempo de recuperación: {resultados['meses_recuperacion']:.2f} meses")
        
        # Proyección y visualización
        df_proyeccion = generar_proyeccion(resultados["ahorro_total"], inversion_inicial)
        st.subheader("Proyección de ROI a 3 años")
        fig = px.line(df_proyeccion, x="Meses", y=["Ahorro Acumulado (USD)", "ROI Acumulado (%)"],
                      title="Ahorro y ROI Acumulado", markers=True,
                      labels={"value": "Valor", "variable": "Métrica"})
        fig.update_layout(yaxis_title="USD / %", xaxis_title="Meses", hovermode="x unified")
        st.plotly_chart(fig)

if __name__ == "__main__":
    calcular_business_case()
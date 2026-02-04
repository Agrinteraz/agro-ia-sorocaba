import streamlit as st
import pandas as pd
import joblib # Ou pickle, dependendo de como você salvou seu modelo

# Configuração da página
st.set_page_config(page_title="Predição Safra - Sorocaba", page_icon="🌾")

st.title("🌾 Calculadora de Produtividade Agrícola")
st.subheader("Foco: Sorocaba e Região")

st.markdown("""
Esta ferramenta utiliza **Inteligência Artificial** para estimar a produtividade da sua lavoura 
com base no clima e histórico regional.
""")

# Barra lateral para entrada de dados
st.sidebar.header("Dados da Propriedade")

# Exemplo de campos que o produtor preencheria
chuva = st.sidebar.slider("Chuva esperada (mm)", 0, 500, 150)
temp = st.sidebar.slider("Temperatura média (°C)", 10, 45, 25)
area = st.sidebar.number_input("Área do plantio (Hectares)", min_value=1.0)

# Botão de cálculo
if st.button("Calcular Estimativa de Colheita"):
    # Aqui entraria o carregamento do seu modelo salvo:
    # modelo = joblib.load('modelo_produtividade.pkl')
    
    # Simulando um cálculo (Substitua pela lógica do seu modelo .ipynb)
    previsao_por_ha = (chuva * 0.2) + (temp * 0.5) # Exemplo fictício
    total_estimado = previsao_por_ha * area
    
    # Exibição dos resultados
    st.success(f"### Resultado Estimado")
    col1, col2 = st.columns(2)
    col1.metric("Produtividade", f"{previsao_por_ha:.2f} sacas/ha")
    col2.metric("Total da Safra", f"{total_estimado:.2f} sacas")
    
    st.info("Nota: Este cálculo é baseado no modelo treinado com dados históricos da região de Sorocaba.")

st.markdown("---")
st.caption("Desenvolvido por Agrinteraz - Especialista em IA para o Agro.")

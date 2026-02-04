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
st.subheader("📈 Tendência de Produtividade na Região")

# Criando dados simulados para Sorocaba e região
# Em um projeto real, esses dados viriam do seu CSV ou Banco de Dados
data_grafico = {
    'Ano': [2020, 2021, 2022, 2023, 2024, 2025],
    'Produtividade Média (kg/ha)': [4200, 4500, 4100, 4800, 5100, 4950]
}
df_historico = pd.DataFrame(data_grafico)

# Exibindo o gráfico de linha
st.line_chart(df_historico.set_index('Ano'))

st.write("""
*O gráfico acima mostra a evolução da produtividade média monitorada pela **Agrinteraz** nos municípios do sudoeste paulista. 
Note como as variações climáticas influenciam o resultado final.*
""")

st.markdown("---")
st.subheader("💡 Consultoria Personalizada")
st.write("""
Este modelo utiliza dados regionais, mas cada propriedade tem suas particularidades. 
A **Agrinteraz** desenvolve análises exclusivas para a sua fazenda, utilizando:
* Dados históricos do seu talhão.
* Sensores de solo e estações meteorológicas locais.
* Relatórios de saúde da cultura via satélite.
""")

# Botão que simula um CTA (Chamada para Ação)
if st.button("Solicitar Diagnóstico para minha Propriedade"):
    st.info("Entre em contato conosco pelo e-mail: agrinteraz@gmail.com ou via WhatsApp (15) 981806430")


st.markdown("---")
st.caption("Desenvolvido por Agrinteraz - Especialista em IA para o Agro.")

import streamlit as st
import pandas as pd
import joblib
import os

# 1. Configuração da Página
st.set_page_config(page_title="AgroIA - Sorocaba", page_icon="🌾")

# 2. Carregamento do Modelo (compatível com seu joblib.dump)
def carregar_modelo():
    caminho_atual = os.path.dirname(__file__)
    # O seu código do notebook salva como 'modelo_agro.pkl'
    caminho_modelo = os.path.join(caminho_atual, 'modelo_agro.pkl')
    return joblib.load(caminho_modelo)

modelo = carregar_modelo()

st.title("🌾 AgroIA: Monitoramento Regional")

# 3. Estrutura de Abas
tab1, tab2 = st.tabs(["🚜 Simulador", "🔬 Metodologia"])

with tab1:
    st.subheader("Calculadora de Produtividade Agrícola")
    
    # Parâmetros conforme o seu Passo 2 e 5 do Notebook
    cidade = st.selectbox("Cidade", ['Sorocaba (SP)', 'Itapetininga (SP)', 'Itapeva (SP)', 'Capão Bonito (SP)'])
    # Dados de médias históricas (Exemplos aproximados - ajuste com seus dados do IBGE/NASA)
    medias_chuva = {
        'Sorocaba (SP)': 850,
        'Itapetininga (SP)': 920,
        'Itapeva (SP)': 1050,
        'Capão Bonito (SP)': 1100
    }
    
    chuva_sugerida = medias_chuva.get(cidade, 800)
    
    st.info(f"💡 Em {cidade}, a média histórica de chuva para este ciclo é de aproximadamente **{chuva_sugerida}mm**.")
    
    # Agora o input de chuva pode usar essa média como valor padrão (value)
    chuva = st.number_input("Chuva Acumulada no Ciclo (mm)", 300, 1500, chuva_sugerida)
    
    # NDVI como Opção Avançada (conforme sua sugestão)
    with st.expander("🛠️ Opção Avançada: Índice de Satélite (NDVI)"):
        st.write("Ajuste o vigor vegetativo se tiver dados do Sentinel-2/ESA.")
        ndvi = st.slider("Vigor Vegetativo (NDVI)", 0.4, 0.9, 0.7)

    if st.button("🚀 Prever Produtividade"):
        try:
            # Criamos o DataFrame com os nomes EXATOS do seu Passo 4:
            # X = df_final[['ndvi_pico', 'chuva_acumulada']]
            dados = pd.DataFrame([[ndvi, chuva]], columns=['ndvi_pico', 'chuva_acumulada'])
            
            # Realiza a predição
            pred = modelo.predict(dados)[0]
            
            st.metric(f"Expectativa para {cidade}", f"{pred:.2f} kg/ha")
            st.write("Cálculo realizado com base em Random Forest Regressor treinado com dados ESA/NASA.")

            # Gráfico de Tendência Regional
            st.markdown("---")
            st.subheader("📈 Tendência Histórica")
            data_grafico = {
                'Ano': ['2020', '2021', '2022', '2023', '2024', '2025'],
                'Produtividade (kg/ha)': [4200, 4500, 4100, 4800, 5100, 4950]
            }
            st.line_chart(pd.DataFrame(data_grafico), x='Ano', y='Produtividade (kg/ha)')

        except Exception as e:
            st.error(f"Erro na predição: {e}")

with tab2:
    st.header("Metodologia Técnica")
    st.write(f"""
    Este modelo foi treinado utilizando dados de Sensoriamento Remoto e Climatologia:
    - **Fonte Satelital:** Google Earth Engine (Copernicus/Sentinel-2).
    - **Fonte Climática:** NASA POWER (Precipitação acumulada).
    - **Algoritmo:** Random Forest Regressor (Ensemble Learning).
    """)
    

# 4. Rodapé de Contato (Sugestão 3)
st.markdown("---")
st.subheader("💡 Consultoria Agrinteraz")
texto_wa = "Olá! Vi seu App AgroIA e gostaria de um diagnóstico personalizado."
# Lembre-se de colocar seu número real abaixo
link_wa = f"https://wa.me/5515981806430?text={texto_wa.replace(' ', '%20')}"
st.link_button("🟢 Falar com Especialista no WhatsApp", link_wa)

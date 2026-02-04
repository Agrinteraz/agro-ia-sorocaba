import streamlit as st
import pandas as pd
import joblib
import os

# Configuração da página (deve ser a primeira linha do Streamlit)
st.set_page_config(page_title="AgroIA - Sorocaba", page_icon="🌾", layout="wide")

# Função para carregar o modelo com segurança
def carregar_modelo():
    caminho_atual = os.path.dirname(__file__)
    caminho_modelo = os.path.join(caminho_atual, 'modelo_agro.pkl')
    return joblib.load(caminho_modelo)

modelo = carregar_modelo()

# Título Principal
st.title("🌾 AgroIA: Inteligência de Safra Regional")
st.markdown("---")

# Criando as Abas
tab_simulador, tab_tecnica = st.tabs(["🚜 Simulador de Produtividade", "🔬 Metodologia e Ciência"])

# --- ABA 1: SIMULADOR ---
with tab_simulador:
    st.subheader("Simulação de Safra em Tempo Real")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info("Ajuste os parâmetros abaixo:")
        cidade = st.selectbox("Selecione a Cidade", ['Sorocaba (SP)', 'Itapetininga (SP)', 'Itapeva (SP)', 'Capão Bonito (SP)'])
        ndvi = st.slider("Vigor Vegetativo (NDVI)", 0.4, 0.9, 0.7, help="Índice de saúde da planta captado por satélite.")
        chuva = st.number_input("Chuva Acumulada no Ciclo (mm)", 300, 1500, 800)
        
        btn_prever = st.button("🚀 Calcular Produtividade")

    with col2:
        if btn_prever:
            # Lógica de Previsão
            dados = pd.DataFrame([[ndvi, chuva]], columns=['ndvi_pico', 'chuva_acumulada'])
            pred = modelo.predict(dados)[0]
            
            st.metric(f"Expectativa para {cidade}", f"{pred:.2f} kg/ha")
            
            # Gráfico de Tendência (Sugestão 2 corrigida)
            st.markdown("#### Tendência Regional")
            data_grafico = {
                'Ano': ['2020', '2021', '2022', '2023', '2024', '2025'],
                'Produtividade (kg/ha)': [4200, 4500, 4100, 4800, 5100, 4950]
            }
            df_historico = pd.DataFrame(data_grafico)
            st.line_chart(df_historico, x='Ano', y='Produtividade (kg/ha)')
        else:
            st.write("👈 Configure os dados ao lado e clique em calcular para ver os resultados.")

# --- ABA 2: EXPLICAÇÃO TÉCNICA ---
with tab_tecnica:
    st.header("Documentação do Modelo")
    
    st.markdown("""
    O modelo **AgroIA** foi desenvolvido para apoiar a tomada de decisão de produtores no sudoeste paulista. 
    Diferente de cálculos genéricos, ele utiliza **Machine Learning** para correlacionar fatores biofísicos e climáticos.
    """)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("🛰️ Fontes de Dados")
        st.write("""
        - **Imagens de Satélite (Sentinel-2):** Extração de NDVI para medir a fotossíntese ativa.
        - **Dados Meteorológicos (NASA GPM):** Monitoramento de precipitação acumulada.
        - **Bases Locais:** Histórico de safras da região de Sorocaba.
        """)

    with col_b:
        st.subheader("🤖 O Algoritmo")
        st.write("""
        Utilizamos o **Random Forest Regressor**, um algoritmo que cria múltiplas árvores de decisão para 
        chegar a um resultado mais estável e preciso, reduzindo margens de erro causadas por anomalias climáticas.
        """)
        
    st.warning("⚠️ **Nota Técnica:** Este simulador é uma ferramenta de apoio e não substitui o acompanhamento de um engenheiro agrônomo em campo.")

# --- RODAPÉ DE CONTATO ---
st.markdown("---")
st.markdown("### 💡 Consultoria Agrinteraz")
st.write("Precisa de uma análise exclusiva para sua propriedade? Nossa equipe utiliza dados de sensores locais para maximizar seu resultado.")

# Espaço para o Botão do WhatsApp (Sugestão 3 em breve)
if st.button("Falar com um Especialista"):
    st.write("📞 Contato: (15) 981806430 | agrinteraz@gmail.com")

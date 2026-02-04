import streamlit as st
import pandas as pd
import joblib
import os

# 1. Configuração da Página
st.set_page_config(page_title="AgroIA - Sorocaba", page_icon="🌾")

# 2. Carregamento do Modelo
def carregar_modelo():
    caminho_atual = os.path.dirname(__file__)
    caminho_modelo = os.path.join(caminho_atual, 'modelo_agro.pkl')
    return joblib.load(caminho_modelo)

modelo = carregar_modelo()

st.title("🌾 AgroIA: Inteligência de Safra Agrinteraz")

# 3. Estrutura de Abas
tab1, tab2 = st.tabs(["🚜 Simulador", "🔬 Metodologia"])

with tab1:
    st.subheader("Simulador de Produtividade")
    
    # Seleção de Cidade e exibição da média histórica
    cidade = st.selectbox("Cidade", ['Sorocaba (SP)', 'Itapetininga (SP)', 'Itapeva (SP)', 'Capão Bonito (SP)'])
    
    medias_chuva = {
        'Sorocaba (SP)': 850,
        'Itapetininga (SP)': 920,
        'Itapeva (SP)': 1050,
        'Capão Bonito (SP)': 1100
    }
    chuva_sugerida = medias_chuva.get(cidade, 800)
    
    st.info(f"💡 Em {cidade}, a média histórica de chuva para este ciclo é de aproximadamente **{chuva_sugerida}mm**.")
    
    chuva = st.number_input("Chuva Acumulada no Ciclo (mm)", 300, 1500, chuva_sugerida)
    
    with st.expander("🛠️ Opção Avançada: Índice de Satélite (NDVI)"):
        st.write("Ajuste o vigor vegetativo conforme dados do Sentinel-2.")
        ndvi = st.slider("Vigor Vegetativo (NDVI)", 0.4, 0.9, 0.7)

    if st.button("🚀 Calcular e Gerar Diagnóstico"):
        try:
            # Predição
            dados = pd.DataFrame([[ndvi, chuva]], columns=['ndvi_pico', 'chuva_acumulada'])
            pred = modelo.predict(dados)[0]
            
            st.metric(f"Expectativa para {cidade}", f"{pred:.2f} kg/ha")
            
            # --- LÓGICA DE CONCLUSÃO DINÂMICA ---
            st.markdown("---")
            st.subheader("📝 Diagnóstico de Performance")
            
            # Dados históricos para comparação
            historico = {2020: 4200, 2021: 4500, 2022: 4100, 2023: 4800}
            superiores = [str(ano) for ano, media in historico.items() if pred > media]
            inferiores = [str(ano) for ano, media in historico.items() if pred <= media]
            
            conclusao = f"A produtividade calculada de **{pred:.2f} kg/ha** "
            
            if superiores:
                conclusao += f"é **maior** que a média da região nos anos de {', '.join(superiores)}. "
            if inferiores:
                conclusao += f"Por outro lado, projeta-se um resultado **menor** que o dos anos de {', '.join(inferiores)}."
            
            st.write(conclusao)
            
            # Dica visual
            if pred > 4500:
                st.success("✅ O cenário indica um potencial produtivo acima da média histórica recente.")
            else:
                st.warning("⚠️ O cenário sugere atenção, com produtividade abaixo dos picos históricos da região.")

            # Gráfico de Tendência
            st.markdown("---")
            st.subheader("📈 Gráfico de Tendência Histórica")
            st.write("Veja como a sua previsão se posiciona em relação aos anos anteriores:")
            data_grafico = {
                'Ano': ['2020', '2021', '2022', '2023', '2024', '2025'],
                'Produtividade (kg/ha)': [4200, 4500, 4100, 4800, 5100, 4950]
            }
            st.line_chart(pd.DataFrame(data_grafico), x='Ano', y='Produtividade (kg/ha)')

        except Exception as e:
            st.error(f"Erro no cálculo: {e}")

with tab2:
    st.header("Metodologia Técnica")
    st.write("""
    Este simulador utiliza **Inteligência Artificial (Random Forest)** treinada com dados reais de:
    - **NDVI:** Vigor da biomassa via satélite Sentinel-2 (ESA).
    - **Pluviometria:** Acumulado de chuvas via NASA POWER.
    
    A comparação histórica utiliza dados oficiais consolidados para o sudoeste paulista.
    """)

# Rodapé de Contato
st.markdown("---")
st.subheader("💡 Consultoria Agrinteraz")
st.write("Precisa de uma análise detalhada via satélite do seu talhão?")
link_wa = "https://wa.me/5515981806430?text=Olá!%20Gostaria%20de%20um%20diagnóstico%20detalhado%20da%20minha%20safra."
st.link_button("🟢 Falar com Especialista no WhatsApp", link_wa)

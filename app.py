import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

# Configuração da página
st.set_page_config(page_title="Escala de Serviço 1x3", page_icon="📅")

st.title("📅 Calculadora de Escala 1x3")
st.markdown("---")

# 1. Entrada da Data de Referência (Calendário nativo do navegador)
data_ref = st.date_input("Que dia você estava de serviço?", datetime.now())

st.sidebar.header("Opções de Visualização")
opcao = st.sidebar.radio(
    "Como deseja visualizar a escala?",
    ("Data Específica", "Período de Dias", "Mês Específico")
)

# Função de lógica (ajustada para trabalhar com objetos date)
def calcular_status(data_alvo, data_referencia):
    diff = (data_alvo - data_referencia).days
    return "🔴 SERVIÇO" if diff % 4 == 0 else "🟢 FOLGA"

# 2. Lógica das Opções
if opcao == "Data Específica":
    data_alvo = st.date_input("Qual data deseja consultar?", data_ref + timedelta(days=1))
    status = calcular_status(data_alvo, data_ref)
    # Exibição formatada em DD/MM/AAAA
    st.subheader(f"Resultado para {data_alvo.strftime('%d/%m/%Y')}:")
    st.info(f"Nesse dia você estará de: **{status}**")

elif opcao == "Período de Dias":
    qtd_dias = st.number_input("Quantos dias deseja gerar?", min_value=1, max_value=365, value=30)
    datas = []
    for i in range(qtd_dias):
        d = data_ref + timedelta(days=i)
        status = "🔴 SERVIÇO" if i % 4 == 0 else "🟢 FOLGA"
        # Formatação forçada para DD/MM/AAAA na tabela
        datas.append({
            "Data": d.strftime('%d/%m/%Y'), 
            "Dia": d.strftime('%a'), 
            "Status": status
        })
    
    df = pd.DataFrame(datas)
    st.table(df)

elif opcao == "Mês Específico":
    col1, col2 = st.columns(2)
    with col1:
        mes = st.selectbox("Mês", list(range(1, 13)), index=datetime.now().month - 1)
    with col2:
        ano = st.number_input("Ano", min_value=2020, max_value=2100, value=datetime.now().year)
    
    _, num_dias = calendar.monthrange(int(ano), int(mes))
    datas_mes = []
    for dia in range(1, num_dias + 1):
        d = datetime(int(ano), int(mes), dia).date()
        status = calcular_status(d, data_ref)
        datas_mes.append({
            "Data": d.strftime('%d/%m/%Y'), 
            "Dia": d.strftime('%a'), 
            "Status": status
        })
    
    st.table(pd.DataFrame(datas_mes))

st.markdown("---")
st.caption("Formato de data padrão: Dia/Mês/Ano")

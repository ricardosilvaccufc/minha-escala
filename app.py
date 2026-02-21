import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

# Configuração da página
st.set_page_config(page_title="Escala 1x3", page_icon="📅")

st.title("📅 Calculadora de Escala 1x3")
st.markdown("---")

DIAS_ABREV = {0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sáb", 6: "Dom"}

# 1. Entrada da Data de Referência
data_ref = st.date_input("Que dia você estava de serviço?", value=datetime.now(), format="DD/MM/YYYY")

st.sidebar.header("Opções de Visualização")
opcao = st.sidebar.radio("Como deseja visualizar a escala?", ("Data Específica", "Período de Dias", "Mês Específico"))

def calcular_status(data_alvo, data_referencia):
    diff = (data_alvo - data_referencia).days
    return "🔴 SERVIÇO" if diff % 4 == 0 else "🟢 FOLGA"

if opcao == "Data Específica":
    data_alvo = st.date_input("Qual data deseja consultar?", value=data_ref + timedelta(days=1), format="DD/MM/YYYY")
    status = calcular_status(data_alvo, data_ref)
    dia_sem = DIAS_ABREV[data_alvo.weekday()]
    st.subheader(f"Resultado para {data_alvo.strftime('%d/%m/%Y')} ({dia_sem}):")
    st.info(f"Nesse dia você estará de: **{status}**")

elif opcao == "Período de Dias":
    qtd_dias = st.number_input("Quantos dias deseja gerar?", min_value=1, max_value=365, value=30)
    datas = []
    total_servico = 0
    for i in range(qtd_dias):
        d = data_ref + timedelta(days=i)
        status = calcular_status(d, data_ref)
        if "SERVIÇO" in status: total_servico += 1
        datas.append({"Data": d.strftime('%d/%m/%Y'), "Dia": DIAS_ABREV[d.weekday()], "Status": status})
    
    st.dataframe(pd.DataFrame(datas), hide_index=True, use_container_width=True)
    st.metric("Total de Serviços no período", f"{total_servico} Plantões")

elif opcao == "Mês Específico":
    col1, col2 = st.columns(2)
    with col1:
        mes = st.selectbox("Mês", list(range(1, 13)), index=datetime.now().month - 1)
    with col2:
        ano = st.number_input("Ano", min_value=2024, max_value=2100, value=datetime.now().year)
    
    _, num_dias = calendar.monthrange(int(ano), int(mes))
    datas_mes = []
    total_servico_mes = 0
    for dia in range(1, num_dias + 1):
        d = datetime(int(ano), int(mes), dia).date()
        status = calcular_status(d, data_ref)
        if "SERVIÇO" in status: total_servico_mes += 1
        datas_mes.append({"Data": d.strftime('%d/%m/%Y'), "Dia": DIAS_ABREV[d.weekday()], "Status": status})
    
    st.dataframe(pd.DataFrame(datas_mes), hide_index=True, use_container_width=True)
    st.metric(f"Total de Serviços em {mes}/{ano}", f"{total_servico_mes} Plantões")

st.markdown("---")
st.write("© **Autor: Sergio Ricardo**")
st.write("📧 Contato: sergioricardo.ccufc@gmail.com")
st.caption("Escala 24x72h | Formato: Dia/Mês/Ano")

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

st.set_page_config(page_title="Escala 12x24/12x72", page_icon="⚖️")

st.title("⚖️ Calculadora Escala 12x24 / 12x72")
st.markdown("---")

DIAS_ABREV = {0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sáb", 6: "Dom"}

st.sidebar.header("⚙️ Opções de Visualização")
opcao = st.sidebar.radio("Como deseja visualizar?", ("Data Específica", "Período de Dias", "Mês Específico"))

st.sidebar.markdown("---")
st.sidebar.header("📌 Legenda")
st.sidebar.markdown("- **☀️ DIURNO**: 07h-19h\n- **🌙 NOTURNO**: 19h-07h\n- **🟢 FOLGA**: Descanso")

st.info("⚠️ Informe a data do seu **1º Serviço Diurno (07h-19h)**.")
data_ref = st.date_input("Data de Referência:", value=datetime.now(), format="DD/MM/YYYY")

def calcular_status_5dias(data_alvo, data_referencia):
    diff = (data_alvo - data_referencia).days
    posicao = diff % 5
    if posicao == 0: return "☀️ DIURNO (07h-19h) | 🟢 Folga Noturna"
    if posicao == 1: return "🌙 NOTURNO (19h-07h) | 🟢 Folga Diurna"
    if posicao == 2: return "🟢 FOLGA (Pós-Noturno)"
    if posicao == 3: return "🟢 FOLGA"
    if posicao == 4: return "🟢 FOLGA"
    return "Status indisponível"

if opcao == "Data Específica":
    data_alvo = st.date_input("Data para consulta:", value=datetime.now() + timedelta(days=1), format="DD/MM/YYYY")
    status = calcular_status_5dias(data_alvo, data_ref)
    dia_sem = DIAS_ABREV[data_alvo.weekday()]
    st.subheader(f"Resultado para {data_alvo.strftime('%d/%m/%Y')} ({dia_sem}):")
    st.success(f"Status: **{status}**")

elif opcao == "Período de Dias":
    qtd_dias = st.number_input("Quantos dias gerar?", min_value=1, max_value=365, value=20)
    datas = []
    serv_d, serv_n = 0, 0
    for i in range(qtd_dias):
        d = data_ref + timedelta(days=i)
        status = calcular_status_5dias(d, data_ref)
        if "DIURNO" in status: serv_d += 1
        if "NOTURNO" in status: serv_n += 1
        datas.append({"Data": d.strftime('%d/%m/%Y'), "Dia": DIAS_ABREV[d.weekday()], "Status": status})
    
    st.dataframe(pd.DataFrame(datas), hide_index=True, use_container_width=True)
    c1, c2 = st.columns(2)
    c1.metric("Serviços Diurnos", f"{serv_d}")
    c2.metric("Serviços Noturnos", f"{serv_n}")

elif opcao == "Mês Específico":
    col1, col2 = st.columns(2)
    with col1:
        mes = st.selectbox("Mês", list(range(1, 13)), index=datetime.now().month - 1)
    with col2:
        ano = st.number_input("Ano", min_value=2024, max_value=2100, value=datetime.now().year)
    
    _, num_dias = calendar.monthrange(int(ano), int(mes))
    datas_mes = []
    serv_d_m, serv_n_m = 0, 0
    for dia in range(1, num_dias + 1):
        d = datetime(int(ano), int(mes), dia).date()
        status = calcular_status_5dias(d, data_ref)
        if "DIURNO" in status: serv_d_m += 1
        if "NOTURNO" in status: serv_n_m += 1
        datas_mes.append({"Data": d.strftime('%d/%m/%Y'), "Dia": DIAS_ABREV[d.weekday()], "Status": status})
    
    st.dataframe(pd.DataFrame(datas_mes), hide_index=True, use_container_width=True)
    c1, c2 = st.columns(2)
    c1.metric("Serviços Diurnos", f"{serv_d_m}")
    c2.metric("Serviços Noturnos", f"{serv_n_m}")

st.markdown("---")
st.write("© **Autor: Sergio Ricardo**")
st.write("📧 Contato: sergioricardo.ccufc@gmail.com")
st.caption("Ciclo: 12h Dia -> 12h Noite -> 3 Folgas")

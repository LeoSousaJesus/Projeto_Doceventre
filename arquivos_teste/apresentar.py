import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("doceventre.csv", sep=",", decimal=" ")
df["Dia da Contratação"] = pd.to_datetime(df["Dia da Contratação"])
df = df.sort_values("Dia da Contratação")

df["Month"] = df["Dia da Contratação"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="Dia da Contratação", y="Valor", color="Descrição do Pacote", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x="Dia da Contratação", y="Descrição do Pacote", 
                color="Valor", title="Faturamento por pacote", 
                orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

valor_total = df_filtered.groupby("Endereço Contratante")[["Valor"]].sum().reset_index()
fig_cidade = px.bar(valor_total, x="Endereço Contratante", y="Valor", title="Faturamento por local")
col3.plotly_chart(fig_cidade, use_container_width=True)

fig_kind = px.pie(df_filtered, values="Valor", names="Descrição do Pacote", title="Faturamento por produto")
col4.plotly_chart(fig_kind, use_container_width=True)

# Converter a coluna 'Valor' para numérica e excluir dados NaN
df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
df = df.dropna(subset=["Valor"])

# Agrupar por mês e por Endereço Contratante e calcular a média mensal do Valor
monthly_average_by_location = df.groupby(["Month", "Endereço Contratante"])[["Valor"]].mean().reset_index()

# Criar o gráfico de barras interativo com plotly express
fig_monthly_average_location = px.bar(
    monthly_average_by_location, 
    x="Month", 
    y="Valor", 
    color="Endereço Contratante",
    title="Arrecadação Média Total por Mês por Local",
    labels={"Month": "Mês", "Valor": "Arrecadação Média", "Endereço Contratante": "Local"},
    barmode="group"
)

col5.plotly_chart(fig_monthly_average_location, use_container_width=True)



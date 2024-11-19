import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("doceventre.csv", sep=",", decimal=" ")
df["Dia da Contratação"] = pd.to_datetime(df["Dia da Contratação"])
df=df.sort_values("Dia da Contratação")

df["Month"] = df["Dia da Contratação"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

df_filtered = df[df["Month"] == month]

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="Dia da Contratação", y="Valor", color="Descrição do Pacote" ,title="Faturamento por dia")
col1.plotly_chart (fig_date, use_container_width=True)

fig_prod = px.bar(df_filtered, x="Dia da Contratação", y="Descrição do Pacote", 
                color="Valor" ,title="Faturamento por pacote", 
                orientation="h")
col2.plotly_chart (fig_prod, use_container_width=True)

valor_total = df_filtered.groupby("Endereço Contratante")[["Valor"]].sum().reset_index()
fig_cidade = px.bar(valor_total, x="Endereço Contratante", y="Valor", title="Faturamento por local")
col3.plotly_chart (fig_cidade, use_container_width=True)


fig_kind = px.pie(df_filtered, values="Valor" , names= "Descrição do Pacote", title="Faturamento por produto")
col4.plotly_chart (fig_kind, use_container_width=True)

faturamento_total = df_filtered.groupby("Descrição do Pacote")[["Valor"]].mean().reset_index()
fig_rating = px.bar(df_filtered, y= "Descrição do Pacote",x="Valor", title="Avaliação Total")
col5.plotly_chart (fig_rating, use_container_width=True )


import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Carregar os dados e processar as datas
df = pd.read_csv("doceventre.csv", sep=",", decimal=" ")
df["Dia da Contratação"] = pd.to_datetime(df["Dia da Contratação"])
df = df.sort_values("Dia da Contratação")

# Criar a coluna 'Month' correta
df["Month"] = df["Dia da Contratação"].apply(lambda x: str(x.year) + "-" + str(x.month))
month = st.sidebar.selectbox("Mês", df["Month"].unique())

# Filtrar os dados pelo mês selecionado
df_filtered = df[df["Month"] == month]

# Dividir o layout em colunas
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráfico de faturamento por dia
fig_date = px.bar(df_filtered, x="Dia da Contratação", y="Valor", color="Descrição do Pacote", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

# Gráfico de faturamento por pacote
fig_prod = px.bar(df_filtered, x="Dia da Contratação", y="Descrição do Pacote", 
                color="Valor", title="Faturamento por pacote", 
                orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

# Gráfico de faturamento por local
valor_total = df_filtered.groupby("Endereço Contratante")[["Valor"]].sum().reset_index()
fig_cidade = px.bar(valor_total, x="Endereço Contratante", y="Valor", title="Faturamento por local")
col3.plotly_chart(fig_cidade, use_container_width=True)

# Gráfico de pizza de faturamento por produto
fig_kind = px.pie(df_filtered, values="Valor", names="Descrição do Pacote", title="Faturamento por produto")
fig_kind.update_layout(showlegend=False)  # Ocultar a legenda
col4.plotly_chart(fig_kind, use_container_width=True)

# Garantir que os dados na coluna 'Endereço Contratante' estejam formatados corretamente
df["Endereço Contratante"] = df["Endereço Contratante"].str.strip().str.upper()

# Coordenadas das cidades
city_coords = {
    'TAGUATINGA': (-15.8359, -48.0493),
    'VICENTE PIRES': (-15.8208, -48.0351),
    'CEILÂNDIA': (-15.8104, -48.1096),
    'BRASÍLIA': (-15.7801, -47.9292),
    'SUDOESTE': (-15.7873, -47.8884),
    'LAGO NORTE': (-15.7249, -47.8295),
    'GUARÁ': (-15.8362, -47.9883),
    'ÁGUAS CLARAS': (-15.8327, -48.0317),
    'SANTA MARIA': (-16.0105, -48.0034),
    'NÚCLEO BANDEIRANTE': (-15.8710, -47.9648),
    'NOROESTE': (-15.7622, -47.8803),
    'JARDIM MANGUEIRAL': (-15.8678, -47.8994),
    'SAMAMBAIA': (-15.8798, -48.0835),
    'SOBRADINHO': (-15.6512, -47.7897),
    'FORMOSA': (-15.5411, -47.3363),
    'JARDIM INGA': (-16.0245, -48.0430),
    'SÃO SEBASTIÃO': (-15.9061, -47.7629),
    'LAGO SUL': (-15.8298, -47.8157),
    'GAMA': (-16.0205, -48.0628),
    'JARDIM BOTÂNICO': (-15.8908, -47.8363),
    'CIDADE OCIDENTAL': (-16.0733, -48.3384),
    'PARANOA': (-15.7750, -47.7756)
}

# Adicionar coordenadas ao DataFrame
df["Latitude"] = df["Endereço Contratante"].map(lambda x: city_coords.get(x, (None, None))[0])
df["Longitude"] = df["Endereço Contratante"].map(lambda x: city_coords.get(x, (None, None))[1])

# Converter a coluna 'Valor' para numérica e excluir dados NaN
df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
df = df.dropna(subset=["Valor", "Latitude", "Longitude"])

# Agrupar por mês e por Endereço Contratante e calcular a média mensal do Valor
monthly_average_by_location = df.groupby(["Month", "Endereço Contratante", "Latitude", "Longitude", "Descrição do Pacote"])[["Valor"]].mean().reset_index()

# Criar o mapa interativo com plotly
fig = px.scatter_mapbox(
    monthly_average_by_location,
    lat="Latitude",
    lon="Longitude",
    size="Valor",
    color="Descrição do Pacote",
    hover_name="Endereço Contratante",
    hover_data={"Valor": True, "Descrição do Pacote": True},
    title="Vendas Localidade",
    mapbox_style="open-street-map",
    zoom=10,
    height=600
)
fig.update_layout(showlegend=False)  # Ocultar a legenda

# Mostrar o gráfico no Streamlit
col5.plotly_chart(fig, use_container_width=True)


import pandas as pd
import plotly.express as px
import streamlit as st

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Police Incident Dashboard in San Francisco", page_icon=":police_car:", layout="wide")

# ---- READ CSV ----
@st.cache_data
def get_data_from_csv():
    df = pd.read_csv("SF_POLICE.csv")
    return df

df = get_data_from_csv()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

# Filtro por año
selected_year = st.sidebar.selectbox("Select Year", df["Incident Year"].unique())

# Filtro por resolución
selected_resolution = st.sidebar.selectbox("Select Resolution", df["Resolution"].unique())

# Filtro por distrito
selected_district = st.sidebar.selectbox("Select District", df["Police District"].unique())

# Filtrar el dataframe según los filtros seleccionados
filtered_df = df.loc[(df["Incident Year"] == selected_year) & (df["Resolution"] == selected_resolution) & (df["Police District"] == selected_district)].copy()

# ---- MAINPAGE ----
st.title(":police_car: Police Incident Dashboard")
st.markdown("##")

# TOP KPI's

# Gráfico 1: Incident by Day of Week [BAR CHART]
incidents_by_day = filtered_df["Incident Day of Week"].value_counts().reset_index()
incidents_by_day.columns = ["Day of Week", "Incident Count"]
fig_day_of_week = px.bar(incidents_by_day, x="Day of Week", y="Incident Count", title="Incidents by Day of Week")
fig_day_of_week.update_layout(xaxis={"categoryorder":"total descending"})

# Gráfico 2: Incident by Hour [BAR CHART]
filtered_df.loc[:, "Incident Hour"] = pd.to_datetime(filtered_df["Incident Time"]).dt.hour
incidents_by_hour = filtered_df["Incident Hour"].value_counts().reset_index()
incidents_by_hour.columns = ["Hour", "Incident Count"]
fig_hour_of_day = px.bar(incidents_by_hour, x="Hour", y="Incident Count", title="Incidents by Hour of Day")
fig_hour_of_day.update_layout(xaxis={"categoryorder":"total ascending"})

# Gráfico 3: Incident by Category [PIE CHART]
incidents_by_category = filtered_df["Incident Category"].value_counts().reset_index()
incidents_by_category.columns = ["Category", "Incident Count"]
fig_category = px.pie(incidents_by_category, values="Incident Count", names="Category", title="Incidents by Category")

# Gráfico 4: Incident by District [BAR CHART]
incidents_by_district = filtered_df["Police District"].value_counts().reset_index()
incidents_by_district.columns = ["District", "Incident Count"]
fig_district = px.bar(incidents_by_district, x="District", y="Incident Count", title="Incidents by Police District")
fig_district.update_layout(xaxis={"categoryorder":"total descending"})

# Gráfico 5: Incident by Neighborhood [BAR CHART]
incidents_by_neighborhood = filtered_df["Analysis Neighborhood"].value_counts().reset_index()
incidents_by_neighborhood.columns = ["Neighborhood", "Incident Count"]
fig_neighborhood = px.bar(incidents_by_neighborhood, x="Neighborhood", y="Incident Count", title="Incidents by Neighborhood")
fig_neighborhood.update_layout(xaxis={"categoryorder":"total descending"})

# Gráfico 6: Mapa de incidentes
fig_map = px.scatter_mapbox(filtered_df, lat='Latitude', lon='Longitude', hover_name='Incident Description',
                            title='San Francisco Incident Map')
fig_map.update_layout(mapbox_style='open-street-map')

# Mostrar los gráficos en la página principal
col1, col2 = st.columns(2)

col1.plotly_chart(fig_day_of_week, use_container_width=True)
col1.plotly_chart(fig_hour_of_day, use_container_width=True)
col1.plotly_chart(fig_category, use_container_width=True)

col2.plotly_chart(fig_district, use_container_width=True)
col2.plotly_chart(fig_neighborhood, use_container_width=True)
col2.plotly_chart(fig_map, use_container_width=True)

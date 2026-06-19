import streamlit as st

import numpy as np
import pandas as pd
import plotly.express as px
from utlis import load_data


#setting wide layout so graphs look better
st.set_page_config(
    page_title="UltraX Dashboard",
    layout="wide"
)

data = load_data()
data = data.drop(columns="Unnamed: 0")
data["date"] = pd.to_datetime(data["date"])
data = data.sort_values("date")

data["percent_max_speed"] = data["max_speed"] / data["max_max_speed_prev_total_days"]

#filtering out extreme speeds. Set at 44km, Usain Bolt top speed
data = data[data["max_speed"] < 44]



players_list = data["player_id"].unique()
metrics_list = ['duration',
    'total_distance',
    'mean_speed',
    'med_speed',
    'max_speed',
    'mean_acc',
    'max_acc',
    'max_decel',
    'mean_hr',
    'med_hr',
    'max_hr',
    'min_hr',
    'mean_mp',
    'med_mp',
    'max_mp',
    'mean_cadence',
    'med_cadence',
    'max_cadence',
    'avg_hrv',
    'max_hrv',
    'min_hrv',
    'std_hrv',
    'med_hrv',
    'percent_max_speed'
    ]

metrics_list = [i.replace("_", " ").title() for i in metrics_list]

selected_player = st.sidebar.selectbox(
    "Select Player",
    players_list
)

first_metric = st.sidebar.selectbox(
    "Select First Metric",
    metrics_list
)


second_metric = st.sidebar.selectbox(
    "Select Second Metric",
    [i for i in metrics_list if i != first_metric]
)

start_date, end_date = st.select_slider(
    "Date Slider",
    options=data["date"],
    value=[data["date"].min(), data["date"].max()]
)



player_data = data[(data["player_id"] == selected_player) & ((data["date"] >= start_date) & (data["date"] <= end_date))]


fig = px.scatter(player_data, 
                 first_metric.replace(" ", "_").lower(), 
                 second_metric.replace(" ", "_").lower(), 
                 title=f"{first_metric.replace("_", " ").title()} vs {second_metric.replace("_", " ").title()}",
                 trendline='ols')
fig.update_layout(xaxis_title = first_metric.replace("_", " ").title(),
                  yaxis_title = second_metric.replace("_", " ").title())
fig.update_layout(title_font=dict(size=40))

st.plotly_chart(fig, use_container_width=True)
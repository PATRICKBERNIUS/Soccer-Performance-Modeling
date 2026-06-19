import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


#setting wide layout so graphs look better
st.set_page_config(
    page_title="UltraX Dashboard",
    layout="wide"
)


@st.cache_data
def load_data():
    data = pd.read_csv("agg_data_for_clustering.csv")
    return data

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


#player = "E708k8gB"
#metric = "max_speed"


selected_player = st.sidebar.selectbox(
    "Select Player",
    players_list
)

# selected_metric = st.sidebar.selectbox(
#     "Select Metric",
#     metrics_list
# )

#player_data = data[data["player_id"] == selected_player]


start_date, end_date = st.select_slider(
    "Date Slider",
    options=data["date"],
    value=[data["date"].min(), data["date"].max()]
)




pivot_data = pd.melt(data, ["event_id", "player_id", "date"], metrics_list, "metric", "value")

player_data = pivot_data[(pivot_data["player_id"] == selected_player) & ((pivot_data["date"] >= start_date) & (pivot_data["date"] <= end_date))]








fig = px.line(player_data, 
              "date", 
              "value", 
              title=f"Player {selected_player} Metrics Over Time", 
              facet_col="metric", 
              facet_col_wrap=2, 
              height=5000, 
              facet_row_spacing=0.025,
              facet_col_spacing=0.06)

fig.update_yaxes(matches=None, showticklabels=True, title_text="")
fig.update_xaxes(matches=None, showticklabels=True)

fig.update_layout(title_font=dict(size=40), yaxis_title="Value")
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1].replace("_", " ").title()))

st.plotly_chart(fig, use_container_width=True)
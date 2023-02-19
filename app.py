import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
import plotly.graph_objects as go

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Running Dashboard", page_icon=":runner:", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(io=r"Laufzeiten.xlsx", engine='openpyxl', skiprows=0, usecols="A:D")
    # Add 'hour' column to dataframe
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")

# Filter Strecke
min_distance = min(df["Strecke"])
max_distance = max(df["Strecke"])
strecke = st.sidebar.slider("Strecke Slider", min_value=min_distance, max_value=max_distance, value=[min_distance, max_distance], step=0.5)


months = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
month_to_num = {month: i+1 for i, month in enumerate(months)}
df["Monat"] = df["Datum"].dt.month
# datum = st.sidebar.select_slider("Datum Slider", options=months)

# Filter Datum test
datum = st.sidebar.multiselect(
    "Select the month:",
    options=df["Datum"].dt.month.unique(),
    default=df["Datum"].dt.month.unique()
)

df_selection = df.query(
    "Strecke >= @strecke[0] & Strecke <= @strecke[1] & Datum.dt.month == @datum"
)



# ---- MAINPAGE ----
st.title(":runner: Running Dashboard")
st.markdown("##")


# TOP KPI's
total_distance = df_selection["Strecke"].sum()
number_of_runs = len(df_selection)
total_time = datetime.timedelta()
for i in df_selection["Zeit"]:
    (h, m, s) = str(i).split(':')
    d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    total_time += d

left_column, inter_cols_pace, right_column = st.columns((8,1,5))
with left_column:

    # Set the "Date" column as the index of the dataframe
    df2 = df_selection.copy()

    # Set the "Date" column as the index of the dataframe
    df2 = df2.set_index('Datum')

    # Resample the data to daily frequency and fill missing dates
    df_resampled = df2.resample('D').asfreq()

    # Fill missing values with default values
    df_resampled = df_resampled.fillna({'Strecke': 0,
                                        'Zeit': pd.Timedelta(0),
                                        'Geschwindigkeit': pd.Timedelta(0)})

    # Reset the index of the dataframe
    df_resampled = df_resampled.reset_index()

    fig_run_distance = px.line(df_resampled, x="Datum", y="Strecke", title='Running distance', template="plotly_white", markers=False)
    df_resampled_nonzero = df_resampled.where(df_resampled["Strecke"] > 0)
    fig_run_scatter = px.scatter(df_resampled_nonzero, x="Datum", y="Strecke", template="plotly_white")
    fig_run_distance_scatter = go.Figure(data=fig_run_distance.data + fig_run_scatter.data)
    st.plotly_chart(fig_run_distance_scatter, use_container_width=True)
    st.markdown("""---""")

    left_column_nest, middle_column_nest, right_column_nest = st.columns(3)

    left_column_nest.subheader("Total Distance:")
    left_column_nest.subheader(f"{total_distance:.2f} km")

    middle_column_nest.subheader("Total Time:")
    middle_column_nest.subheader(f"{total_time}")

    right_column_nest.subheader("Number of runs:")
    right_column_nest.subheader(f"{number_of_runs}")

with right_column:
    # height = (numRows + 1) * 35 + 3
    st.dataframe(df_selection, height = 500)


st.markdown("""---""")


# SALES BY PRODUCT LINE [BAR CHART]
# sales_by_product_line = (
#     df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
# )
# fig_product_sales = px.bar(
#     sales_by_product_line,
#     x="Total",
#     y=sales_by_product_line.index,
#     orientation="h",
#     title="<b>Sales by Product Line</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
#     template="plotly_white",
# )
# fig_product_sales.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     xaxis=(dict(showgrid=False))
# )
#
# # SALES BY HOUR [BAR CHART]
# sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
# fig_hourly_sales = px.bar(
#     sales_by_hour,
#     x=sales_by_hour.index,
#     y="Total",
#     title="<b>Sales by hour</b>",
#     color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
#     template="plotly_white",
# )
# fig_hourly_sales.update_layout(
#     xaxis=dict(tickmode="linear"),
#     plot_bgcolor="rgba(0,0,0,0)",
#     yaxis=(dict(showgrid=False)),
# )
#
#
# left_column, right_column = st.columns(2)
# left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
# right_column.plotly_chart(fig_product_sales, use_container_width=True)
#
#
# # ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


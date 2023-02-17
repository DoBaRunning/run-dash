import pandas as pd
import plotly.express as px
import streamlit as st


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Running Dashboard", page_icon=":runner:", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(io=r"C:\Users\tuejc6\PycharmProjects\Streamlit_dash\Laufzeiten.xlsx", engine='openpyxl', skiprows=0, usecols="A:D")
    # Add 'hour' column to dataframe
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()


# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
strecke = st.sidebar.multiselect(
    "Select the Strecke:",
    options=df["Strecke"].unique(),
    default=df["Strecke"].unique()
)

df_selection = df.query(
    "Strecke == @strecke"
)


# customer_type = st.sidebar.multiselect(
#     "Select the Customer Type:",
#     options=df["Customer_type"].unique(),
#     default=df["Customer_type"].unique(),
# )
#
# gender = st.sidebar.multiselect(
#     "Select the Gender:",
#     options=df["Gender"].unique(),
#     default=df["Gender"].unique()
# )
#
# df_selection = df.query(
#     "City == @city & Customer_type ==@customer_type & Gender == @gender"
# )



# ---- MAINPAGE ----
st.title(":runner: Running Dashboard")
st.markdown("##")

st.dataframe(df_selection)

# TOP KPI's
total_distance = df_selection["Strecke"].sum()
total_distance_int = int(df_selection["Strecke"].sum())

# total_time = df_selection["Zeit"].sum()
# average_rating = round(df_selection["Zeit"].mean(), 1)
# star_rating = ":star:" * int(round(average_rating, 0))
# average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Distance:")
    st.subheader(f"{total_distance} km")
with middle_column:
    st.subheader("Total Distance:")
    st.subheader(f"{total_distance_int} km")
with right_column:
    st.subheader("Total Distance:")
    st.subheader(f"{total_distance} km")
# with middle_column:
#     st.subheader("Average Rating:")
#     st.subheader(f"{average_rating} {star_rating}")
# with right_column:
#     st.subheader("Average Sales Per Transaction:")
#     st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# # SALES BY PRODUCT LINE [BAR CHART]
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
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)
#

# Filter Strecke old
# strecke = st.sidebar.multiselect(
#     "Select the Strecke:",
#     options=df["Strecke"].unique(),
#     default=df["Strecke"].unique()
# )



###
val = [None]* len(months) # this list will store info about which category is selected
for i, cat in enumerate(months):
    # create a checkbox for each category
    val[i] = st.sidebar.checkbox(cat, value=True) # value is the preselect value for first render

# filter data based on selection
df_flt = df[df.Datum.isin(months[val])].reset_index(drop=True)
###


df_selection = df.query(
    "Strecke >= @strecke[0] & Strecke <= @strecke[1] & Monat == @month_to_num[@datum]"
)

import plotly.express as px
import pandas as pd

# Create a sample dataframe
df = pd.DataFrame({'X': [1, 2, 3, 4, 5, 6], 'Y': [0, 0.5, 1.2, 0, 2.3, 0], 'Z': [0.5, 0, 1.1, 1.5, 0, 2.8]})

# Replace zero values with None
df_nonzero = df.where(df > 0)

# Create the figure
fig = px.line(df_nonzero, x='X', y=['Y', 'Z'], title='Line chart with markers for non-zero values only',
              line_shape='spline', render_mode='svg', color_discrete_sequence=px.colors.qualitative.Dark24,
              template='plotly_white', labels={'value': 'Y/Z'})

# Add markers for non-zero values only
fig.update_traces(mode='lines+markers', scatter=dict(symbol='circle', size=10,
                                                     line=dict(width=1, color='DarkSlateGray'),
                                                     color='white',
                                                     selector=dict(type='scatter', mode='lines')))
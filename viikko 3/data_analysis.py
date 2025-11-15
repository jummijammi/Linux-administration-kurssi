import streamlit as st
import pydeck as pdk
import pandas as pd
from db_config import get_meteorite_data
import numpy as np

st.title("Meteoriittien analyysi")

# Hae data MySQL:stä
df = get_meteorite_data()


df = df.dropna(subset=['reclat', 'reclong', 'mass_g'])


df['mass_size'] = np.log1p(df['mass_g']) * 1000  


mass_scaled = np.log1p(df['mass_g'])
mass_scaled = 255 * (mass_scaled - mass_scaled.min()) / (mass_scaled.max() - mass_scaled.min())
df['red'] = mass_scaled.astype(int)
df['blue'] = (255 - mass_scaled).astype(int)
df['color'] = df.apply(lambda row: [row['red'], 50, row['blue'], 180], axis=1)


layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[reclong, reclat]',
    get_radius='mass_size',
    get_fill_color='color',
    pickable=True,
    auto_highlight=True
)


tooltip = {
    "html": "<b>Name:</b> {name} <br/>"
            "<b>Class:</b> {recclass} <br/>"
            "<b>Mass (g):</b> {mass_g} <br/>"
            "<b>Year:</b> {year}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white",
        "fontSize": "12px",
        "padding": "5px",
    }
}


view_state = pdk.ViewState(
    latitude=df['reclat'].mean(),
    longitude=df['reclong'].mean(),
    zoom=2,
    pitch=0
)

r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
)

st.pydeck_chart(r)


st.subheader("Meteoriittien lista")
st.dataframe(df[['name', 'recclass', 'mass_g', 'year', 'reclat', 'reclong']])


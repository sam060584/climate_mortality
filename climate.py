import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
from PIL import Image
import openpyxl, xlrd
import plotly.express as px


st.set_option('deprecation.showPyplotGlobalUse', False)

deathData= pd.read_excel('data/Death_linked_heat_cold.xlsx')
mapData = pd.read_excel('data/matYearCountry.xls')
   
     


tab1, tab2, tab3 = st.tabs(['Introduction', 'Demographics', 'GDP and Temp'])

with tab1:
      image = Image.open('images/HeatVsCold.png')
      st.markdown("<h1 style='text-align: center;'>Are rising temperatures less deadly?</h1>", unsafe_allow_html=True)
      st.image(image, caption='Cold is far more deadly, for every death linked to heat, nine are tied to cold')

      hover = alt.selection_single(
        fields=["Year"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
      deathTrendHeat = (
                    alt.Chart(deathData, title="Death in millions over years cold vs heat")
                    .mark_line()
                    .encode(
                        x = 'Year',
                        y = 'Deacth in Millions(Heat)',
                        color=alt.value("#FFAA00")
                    )
      )

      deathTrendCold = (
                    alt.Chart(deathData, title="Death in millions over years cold vs heat")
                    .mark_line()
                    .encode(
                        x = 'Year',
                        y = 'Deacth in Millions(Cold)',
                        color = alt.value('#18A8D8')
                    )
      )

      tooltips = (
        alt.Chart(deathData)
        .mark_rule()
        .encode(
            x="Year",
            y = 'Deacth in Millions(Heat)',
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("Year", title = "Year"),
                alt.Tooltip("Deacth in Millions(Heat)", title="Death in Millions")
            ],
        )
        .add_selection(hover)
    )
    
     

      chart = (deathTrendHeat+deathTrendCold+tooltips).interactive()

      st.altair_chart(chart.interactive(), use_container_width=True)
                   


            

with tab2:
    st.markdown("<h1 style='text-align: center;'>Changes in Deaths linked to temperature</h1>", unsafe_allow_html=True)
    
    fig = px.scatter_mapbox(mapData, lat = 'lat', lon = 'lon', zoom = 1, color = "years_2080_2099", hover_name = 'Country')
    fig.update_layout(mapbox_style = "open-street-map")
    fig.update_layout(margin={"r":0, "t": 0, "l":0, "b":0})
    st.plotly_chart(fig)



       

with tab3:
    st.markdown("<h1 style='text-align: center;'>GDP and Temp impact on Mortality</h1>", unsafe_allow_html=True)
    values = mapData['Country'].tolist()
    
    c = alt.Chart(mapData).mark_circle().encode(
    x='years_2080_2099', y='Temperature', size='GDP', color='Country', tooltip=['Country', 'Temperature', 'GDP', 'years_2080_2099']).properties(
    width=1600,
    height=600
    )

    st.altair_chart(c, use_container_width=True)



import pandas as pd
import numpy as np
import dateutil
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import altair as alt
from vega_datasets import data
from plotly.subplots import make_subplots
import plotly.express as px
import json
from web.utils.utils import get_by_country_merged

def altair_global_cases_per_country(vax_data_by_man):
    "Bar Chart of Days"
    delta_days = []
    for row in vax_data_by_man['date']:
        delta_day = (row - min(vax_data_by_man['date'])).days
        delta_days.append(delta_day)
    vax_data_by_man = vax_data_by_man.assign(delta_days = delta_days)
    slider = alt.binding_range(min=0, max=max(vax_data_by_man['delta_days']), step = 1)

    selector = alt.selection_single(name = 'delta_days', fields = ['delta_days'],
                               bind=slider, init={'delta_days': 0})
    chart =  alt.Chart(vax_data_by_man, title = "Percent Vaccinated by Manufacturer over Time").mark_bar().encode(
        x='location',
        y=alt.Y('sum(percent_vaxes)', title = "Percent Vaccinated"),
        color=alt.Color('vaccine:N')
        ).properties(
        width=500,
        height=350
    ).add_selection(
    selector
    ).transform_filter(
    selector
    ).configure_facet(
    spacing=10
    )
    return chart.to_json()
    
  

def altair_global_time_series(timeseries_final):
    #Plot Altair 6; Global time series chart for daily new cases, recovered, and deaths - version 3 (more fancy selector)
    #declare data and initialization
    data = timeseries_final

    #specifying form of data; read: https://altair-viz.github.io/user_guide/data.html#long-form-vs-wide-form-data
    base = alt.Chart(data).transform_fold(
        ['daily new cases', 'daily new recovered', 'daily new deaths']
    ).properties(
        title='Global Time Series'
    )
    base.configure_title(
        fontSize=20,
        font='Courier',
        anchor='start',
        color='gray',
        align="center"
    )
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    # The basic line
    line = base.mark_line().encode(
        x='date:T',
        y=alt.Y('value:Q', axis=alt.Axis(title='# of cases')),
        color='key:N',

    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = base.mark_point().encode(
        x='date:T',
        opacity=alt.value(0),
        tooltip=[alt.Tooltip('yearmonthdate(date)', title="Date")]
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value:Q', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(data).mark_rule(color='gray').encode(
        x='date:T',

    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data
    chart = alt.layer(
        line, selectors, points, rules, text
    ).properties(
        width=1300, height=500
    )
    chart_json = chart.to_json()
    return chart_json

#Plot Altair 7 geographical analysis; ref : https://github.com/altair-viz/altair/issues/2044


def altair_geo_analysis(final_df):
    world_source = final_df

    source = alt.topo_feature(data.world_110m.url, "countries")
    background = alt.Chart(source).mark_geoshape(fill="white")

    foreground = (
        alt.Chart(source)
        .mark_geoshape(stroke="black", strokeWidth=0.15)
        .encode(
            color=alt.Color(
                "confirmed:N", scale=alt.Scale(scheme="redpurple"), legend=None,
            ),
            tooltip=[
                alt.Tooltip("Country/Region:N", title="Country"),
                alt.Tooltip("confirmed:Q", title="confirmed cases"),
            ],

        ).transform_lookup(
            lookup="id",
            from_=alt.LookupData(world_source, "id", [
                                 "confirmed", "Country/Region"]),
        )
    )

    final_map = (
        (background + foreground)
        .configure_view(strokeWidth=0)
        .properties(width=700, height=400, title='Total Confirmed Cases/Country')
        .project("naturalEarth1")
    )
    final_map_json = final_map.to_json()
    return final_map_json



def altair_per_country_time_series(vax_data_man):
    "returns json for time series vaccinations"
    input_dropdown = alt.binding_select(options=['Germany','Iceland','Italy',
                                             'Czechia', 'Latvia', 'Lithuania', 'Chile', 'United States'])
    selection = alt.selection_single(fields=['location'], bind=input_dropdown, name='location')
    color = alt.condition(selection,
                    alt.Color('vaccine:N'),
                    alt.value('lightgray'))

    chart = alt.Chart(vax_data_man, title = "Vaccination by Manufacturer").mark_line().encode(
    x=alt.X('date:T'),
    y=alt.Y('percent_vaxes:Q'),
    color = color,
    tooltip='date:T'
        ).add_selection(
    selection
    ).transform_filter(
    selection
    ).properties(
    width=500,
    height=350
    )
    return chart.to_json()
    # #Plot Altair 6a; per_country time series chart for daily new cases, recovered, and deaths - version 3 (more fancy selector)
    # # I use US data

    # #declare data and initialization
    # data = get_by_country_merged(
    #     total_confirmed, total_death, total_recovered, country_name)
    # #column name: date	value_confirmed	daily_new_confirmed	value_death	daily_new_death	value_recovered	daily_new_recovered

    # #specifying form of data; read: https://altair-viz.github.io/user_guide/data.html#long-form-vs-wide-form-data
    # base = alt.Chart(data).transform_fold(
    #     ['daily_new_confirmed', 'daily_new_recovered', 'daily_new_death']
    # )

    # # Create a selection that chooses the nearest point & selects based on x-value
    # nearest = alt.selection(type='single', nearest=True, on='mouseover',
    #                         fields=['date'], empty='none')

    # # The basic line
    # line = base.mark_line().encode(
    #     x='date:T',
    #     y=alt.Y('value:Q', axis=alt.Axis(title='# of cases')),
    #     color='key:N',

    # )

    # # Transparent selectors across the chart. This is what tells us
    # # the x-value of the cursor
    # selectors = base.mark_point().encode(
    #     x='date:T',
    #     opacity=alt.value(0),
    #     tooltip=[alt.Tooltip('yearmonthdate(date)', title="Date")]
    # ).add_selection(
    #     nearest
    # )

    # # Draw points on the line, and highlight based on selection
    # points = line.mark_point().encode(
    #     opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    # )

    # # Draw text labels near the points, and highlight based on selection
    # text = line.mark_text(align='left', dx=5, dy=-5).encode(
    #     text=alt.condition(nearest, 'value:Q', alt.value(' '))
    # )

    # # Draw a rule at the location of the selection
    # rules = alt.Chart(data).mark_rule(color='gray').encode(
    #     x='date:T',

    # ).transform_filter(
    #     nearest
    # )

    # # Put the five layers into a chart and bind the data
    # chart = alt.layer(
    #     line, selectors, points, rules, text
    # ).properties(width=1300, height=400, title=f'{country_name} daily cases')
    # chart_json = chart.to_json()
    # return chart_json



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
#### Graphs for Home Page

#Graph 1: Internation vaccination
def make_global_vax(all_data, countries):
    scale = alt.Scale(
      range=['floralwhite', 'forestgreen'],
      type='linear', domain = [0, 100]
    )
    chart = alt.Chart(all_data).mark_geoshape()\
        .encode(color=alt.Color('total_vaccinations_per_hundred:Q', title = "Percent Vaccinated", scale = scale), 
        tooltip=["Country", "people_fully_vaccinated_per_hundred"])\
        .transform_lookup(
        lookup='id',
        from_=alt.LookupData(countries, key='id',
                             fields=["type", "properties", "geometry"])
    )\
        .project('naturalEarth1')\
        .properties(
        width=1000,
        height=600
    )
    return chart.to_json()
#     "Makes international chloropleth"
#     sphere = alt.sphere()
#     graticule = alt.graticule()
#     scale = alt.Scale(
#       range=['floralwhite', 'darkgreen'],
#       type='linear'
#     )
#   # # Layering and configuring the components
#     chart = alt.layer(
#         alt.Chart(sphere).mark_geoshape(),
#         alt.Chart(graticule).mark_geoshape(stroke='white', strokeWidth=0.5),
#     alt.Chart(all_data, title = "Percent Vaccinated in the World").mark_geoshape().encode(
#         color=alt.Color('people_fully_vaccinated_per_hundred:Q', scale = scale, title = "Percent Fully Vaccinated"),
#         tooltip=["Country", "people_fully_vaccinated_per_hundred"]
#     ).transform_lookup(
#       lookup='id',
#       from_=alt.LookupData(countries, key='id',
#                              fields=["type", "properties", "geometry"])).properties(
#       width=700,
#       height=400
#     )
#     ).project(
#       'naturalEarth1'
#     ).properties(width=600, height=400).configure_view(stroke=None)
#     return chart.to_json()



#Graphs for Vaccination by manufacturer
def altair_global_cases_per_country(vax_data_by_man):
    "Bar Chart of Days"
    domain = ['Pfizer/BioNTech', "Moderna", "Johnson&Johnson", 'Oxford/AstraZeneca', 'Sinovac']
    range_ = ['indianred', 'skyblue', 'turquoise', 'mediumvioletred', 'palevioletred']
    delta_days = []
    for row in vax_data_by_man['date']:
        delta_day = (row - min(vax_data_by_man['date'])).days
        delta_days.append(delta_day)
    vax_data_by_man = vax_data_by_man.assign(delta_days = delta_days)
    slider = alt.binding_range(min=0, max=max(vax_data_by_man['delta_days']), step = 1,  name = 'Select Days since December 24, 2020')

    selector = alt.selection_single(name = 'delta_days', fields = ['delta_days'],
                               bind=slider, init={'delta_days': 0})
    chart =  alt.Chart(vax_data_by_man).mark_bar().encode(
        x=alt.X('location', title = "Location"),
        y=alt.Y('sum(percent_vaxes)', title = "Percent Vaccinated"),
        color=alt.Color('vaccine:N', title = 'Vaccine', scale = alt.Scale(domain = domain, range = range_))
        ).properties(
        width=1000,
        height=600
    ).add_selection(
    selector
    ).transform_filter(
    selector
    ).configure_facet(
    spacing=10
    )
    return chart.to_json()

def altair_per_country_time_series(vax_data_man):
    "returns json for time series vaccinations"
    input_dropdown = alt.binding_select(options=['Germany','Iceland','Italy',
                                             'Czechia', 'Latvia', 'Lithuania', 'Chile', 'United States', 'Romania'], name = 'Select Country ')
    selection = alt.selection_single(fields=['location'], init={'location':'United States'}, bind=input_dropdown)
    domain = ['Pfizer/BioNTech', "Moderna", "Johnson&Johnson", 'Oxford/AstraZeneca', 'Sinovac']
    range_ = ['indianred', 'skyblue', 'turquoise', 'mediumvioletred', 'fuchsia']
    # color = alt.condition(selection,
    #                 alt.Color('vaccine:N'),
    #                 alt.value('lightgray'))

    chart = alt.Chart(vax_data_man).mark_line().encode(
    x=alt.X('date:T', title= "Date"),
    y=alt.Y('percent_vaxes:Q', title = 'Percent of Population Vaccinated'),
    color = alt.Color('vaccine:N', title = 'Vaccine', scale = alt.Scale(domain = domain, range = range_)),
    tooltip='date:T'
        ).add_selection(
    selection
    ).transform_filter(
    selection
    ).properties(
    width=1000,
    height=600
    )
    return chart.to_json()
  
#Graphs for Global cases
def date_deaths(df):
    alt.data_transformers.disable_max_rows()
    input_dropdown = alt.binding_select(options=['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'])
    selection = alt.selection_single(fields=['continent'], bind=input_dropdown, name='Displayed ')
    color = alt.condition(selection,
                        alt.Color('continent:N', legend=None),
                        alt.value('lightgray'))

    k = alt.Chart(df, title = "New Deaths in Time").mark_point().encode(
    alt.X('date:T', title = 'Date'),
       alt.Y('new_deaths_smoothed_per_million:Q', title = 'New Deaths'),
       color = color,
        tooltip='Name:N'
    ).add_selection(
        selection
    ).properties(
        width=700,
        height=400
        ).interactive()
    return k.to_json()
def date_vaccinations(df):
    alt.data_transformers.disable_max_rows()
    input_dropdown = alt.binding_select(options=['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'])
    selection = alt.selection_single(fields=['continent'], bind=input_dropdown, name='Displayed ')
    color = alt.condition(selection,
                        alt.Color('continent:N', legend=None),
                        alt.value('lightgray'))

    k = alt.Chart(df).mark_point().encode(
    alt.X('date:T', title = 'Date'),
       alt.Y('new_vaccinations_smoothed_per_million:Q', title = 'New Vaccinations'),
       color = color,
        tooltip='Name:N'
    ).add_selection(
        selection
    ).properties(
        width=700,
        height=400
        ).interactive()
    return k.to_json()

def vaccinations_deaths(df):
    alt.data_transformers.disable_max_rows()
    input_dropdown = alt.binding_select(options=['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'])
    selection = alt.selection_single(fields=['continent'], bind=input_dropdown, name='Displayed ')
    color = alt.condition(selection,
                        alt.Color('continent:N', legend=None),
                        alt.value('lightgray'))

    k = alt.Chart(df, title = "Vaccinations vs Deaths").mark_point().encode(
    alt.Y('new_deaths_smoothed_per_million:Q', title = 'New Deaths'),
       alt.X('new_vaccinations_smoothed_per_million:Q', title = 'New Vaccinations', scale=alt.Scale(domain=[0, 17000])),
       color = color,
        tooltip='Name:N'
    ).add_selection(
        selection
    ).properties(
    width=700,
    height=400
    ).interactive()
    return k.to_json()

def hdi_vaccinations(df):
    alt.data_transformers.disable_max_rows()
    input_dropdown = alt.binding_select(options=['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'])
    selection = alt.selection_single(fields=['continent'], bind=input_dropdown, name='Displayed ')
    color = alt.condition(selection,
                        alt.Color('continent:N', legend=None),
                        alt.value('lightgray'))

    k = alt.Chart(df).mark_point().encode(
    alt.Y('new_vaccinations_smoothed_per_million:Q', title = 'New Deaths '),
       alt.X('human_development_index', title = 'New Vaccinations'),
       color = color,
        tooltip='Name:N'
    ).add_selection(
        selection
    ).properties(
      width=700,
      height=400
    ).interactive()
    return k.to_json()


### State Covid data ###
def state_vaccinations_per_hundred(state):
  input_dropdown = alt.binding_select(options=list(state['location'].unique()), name = "Select Location")
  selection1 = alt.selection_single(fields=['location'], bind=input_dropdown, name='location', init={'location':'California'})
  #alt.binding_checkbox(fields=['location']) #, bind=input_dropdown, name='location' 
  #selection2 = alt.selection_single(fields=['location'], bind=input_dropdown, name='location')
  alt.data_transformers.disable_max_rows()
  state_bubble = state#pd.read_csv("us_state_vaccinations.csv",encoding='latin-1')

  chart = alt.Chart(state_bubble).mark_circle(size=100).encode(
      x=alt.X('monthdate(date):T', title='date'),
      y=alt.Y('people_fully_vaccinated_per_hundred:Q',title = 'Percent Fully Vaccinated'),
      # size='Elapsed_Time',
      # href='url:N',
      tooltip=["location", "people_fully_vaccinated_per_hundred"]
  ).properties().add_selection(
    selection1
).transform_filter(
    selection1
).properties(
    width=1000,
    height=600)
  return chart.to_json()

def state_map(state):
    state['location'] = state['location'].replace(['New York State'],'New York')
    newest = max(state['date'])
    recent = state[state['date'] == newest]
    avg_data = recent[recent.location != 'American Samoa']
    avg_data = avg_data[avg_data.location != 'Bureau of Prisons']
    avg_data = avg_data[avg_data.location != 'Dept of Defense']
    avg_data = avg_data[avg_data.location != 'Federated States of Micronesia']
    avg_data = avg_data[avg_data.location != 'Guam']
    avg_data = avg_data[avg_data.location != 'Indian Health Svc']
    avg_data = avg_data[avg_data.location != 'Long Term Care']
    avg_data = avg_data[avg_data.location != 'Marshall Islands']
    avg_data = avg_data[avg_data.location != 'Northern Mariana Islands']
  # avg_data = avg_data[avg_data.location != 'Puerto Rico']
    avg_data = avg_data[avg_data.location != 'Republic of Palau']
    avg_data = avg_data[avg_data.location != 'Veterans Health']
    avg_data = avg_data[avg_data.location != 'Virgin Islands']
    avg_data = avg_data[avg_data.location != 'United States']
    avg_data = avg_data.groupby('location').mean()
    avg_data['id'] = np.arange(len(avg_data)) + 1
    avg_data['date'] = newest
    example = pd.read_csv('https://raw.githubusercontent.com/vega/vega/master/docs/data/population_engineers_hurricanes.csv')
    result = pd.merge(left=avg_data, right=example, how='left', left_on='location', right_on='state')
    source = alt.topo_feature(data.us_10m.url, 'states')
    capitals = data.us_state_capitals.url
    map = alt.Chart(source).mark_geoshape().encode(
            color=alt.condition('datum.people_fully_vaccinated_per_hundred !== null','people_fully_vaccinated_per_hundred:Q', alt.value('lightgray'), title = "Percent Fully Vaccinated")
        ,tooltip =
        [alt.Tooltip('state:N'),
          alt.Tooltip('people_fully_vaccinated_per_hundred:Q'), alt.Tooltip('date:O'),
        ]).transform_lookup(
        lookup='id',
        from_=alt.LookupData(result, 'id_y', ['people_fully_vaccinated_per_hundred','state','date'])).properties(
        width=1000,
        height=600).project(
        type='albersUsa')
    background = alt.Chart(source).mark_geoshape(
      fill='lightgray',
      stroke='white'
    ).project('albersUsa')

    return map.to_json()



def state_vaccinations_vs_distribution(state):
    alt.data_transformers.disable_max_rows()
    genres = ['Maryland', 'California']
    genre_dropdown = alt.binding_select(options=genres)
    genre_select = alt.selection_single(fields=['location'], bind=genre_dropdown, name="location")
    base = alt.Chart(state).encode(x=alt.X('monthdate(date):O', title='date'))
    bar = base.mark_bar().encode(y='total_vaccinations:Q')
    filter_genres = base.add_selection(
        genre_select
        ).transform_filter(
      genre_select
        ).properties(title="Dropdown Filtering")
    rule = alt.Chart(state).mark_rule(color='red').encode(x=alt.X('monthdate(date):O', title='date'),
      y='total_distributed:Q'
        )
    final = (bar + rule).properties(title='State Total Vaccinations Administered vs State Vaccine Distribution',width=600).add_selection(genre_select).transform_filter(
      genre_select
  )
    return final.to_json()




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

    
    # add charts for Global Cases and Deaths Page
def country_deaths(df):
    alt.data_transformers.enable('default', max_rows=None)
    k =alt.Chart(df).mark_bar().encode(
    alt.X('location:N', sort = '-y'),
    alt.Y('new_deaths_per_million:Q'),
    color = 'location'
    ).interactive()
    return k.to_json()

def hdi_hospital(df):
    alt.data_transformers.enable('default', max_rows=None)
    k =alt.Chart(df).mark_bar().encode(
        x = 'human_development_index',
        y = 'hospital_beds_per_thousand',
        color = 'location'
    ).interactive()
    return k.to_json()

def continent_deaths(df):
    alt.data_transformers.enable('default', max_rows=None)
    k =alt.Chart(df).mark_bar().encode(
    x = 'continent',
    y = 'total_deaths_per_million',
    # y= alt.Y('total_deaths_per_million:N', sort='-x')
    color = 'continent'
    ).interactive()
    return k.to_json()


def continent_new_cases(df):
    alt.data_transformers.enable('default', max_rows=None)
    k =alt.Chart(df).mark_bar().encode(
    x = 'continent',
    y = 'new_cases_per_million',
    color = 'continent'
        ).interactive()
    return k.to_json()


def hdi_new_cases(df):
    alt.data_transformers.enable('default', max_rows=None)
    k =alt.Chart(df).mark_point().encode(
    alt.X('human_development_index:Q',
    scale=alt.Scale(zero=False)),
    y = 'new_cases_per_million',
    color = 'continent'
        ).interactive()
    return k.to_json()

def vax_cases(df):
    
    k =alt.Chart(df).mark_point().encode(
        alt.Y('total_cases:Q'),
       alt.X('new_vaccinations_smoothed_per_million:Q',
            ),  color = 'continent'
        ).interactive()
    return k.to_json()


### New graph for continent page ###
def date_deaths_cases_vaccinations(df):
    #url='https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
    #df = pd.read_csv(url)
    df = df.dropna(subset=['total_deaths', 'total_tests'])

    df = df.sort_values('date')
    vf = df[df['date'] > '2020-12-05']
    vf

    val = 0
    dates = df['date'].tolist()
    count = 0
    list_day = []
    for i in range(df.shape[0]):
      if dates[i] != val:
        val = dates[i]
        list_day.append(count)
        count += 1
      else:
        list_day.append(count)

    df['days_after_2-13-21'] = list_day
    df = df[df['days_after_2-13-21'] % 7 == 0]
    cf = df[df['date'] > '2020-12-05']



    input_dropdown = alt.binding_select(options=['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'], name = 'Select Continent ')
    selection = alt.selection_single(fields=['continent'], bind=input_dropdown, name='Displayed ')
    color = alt.condition(selection,
                        alt.Color('continent:N'),
                        alt.value('lightgray'))

    l = alt.Chart(df).mark_line().encode(
    alt.X('date:T', title = 'Date'),
       alt.Y('mean(new_deaths_smoothed_per_million):Q', title = 'New Deaths per Million'),
       color = color,
        tooltip='Name:N'
    ).add_selection(
        selection
    ).properties(width=400, height=400)

    m = alt.Chart(df).mark_line().encode(
    alt.X('date:T', title = 'Date'),
       alt.Y('mean(new_cases_smoothed_per_million):Q', title = 'New Cases per Million'),
       color = color,
        tooltip='Name:N'
    ).add_selection(
        selection
    ).properties(width=400, height=400)

    n = alt.Chart(cf).mark_line().encode(
    alt.X('date:T', title = 'Date'),
       alt.Y('mean(new_vaccinations_smoothed_per_million):Q', title = 'New Vaccinations per Million'),
       color = color,
        tooltip='Name:N'
    ).add_selection(
        selection
    ).properties(width=400, height=400)
    charts =  l | m | n
    #charts
    return charts.to_json()



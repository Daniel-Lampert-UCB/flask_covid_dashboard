from altair import Chart, X, Y, Axis, Data, DataFormat
import pandas as pd
import numpy as np
from flask import render_template, url_for, flash, redirect, request, make_response, jsonify, abort
from web import app
from web.utils import utils, altair_plot, plotly_plot
import json

# Loading raw data and clean it



#loading data
total_confirmed, total_death, total_recovered, df_pop = utils.load_data()


(grouped_total_confirmed, grouped_total_recovered,
 grouped_total_death, timeseries_final, country_names) = utils.preprocessed_data(total_confirmed, total_death, total_recovered)

final_df = utils.merge_data(grouped_total_confirmed,
                            grouped_total_recovered, grouped_total_death, df_pop)

#defined by daniel
# Load all data
us_covid_vaccinations, vaccinations_by_manufacturer, owid_covid_latest, vaccinations = utils.pull_data()
#pre-process vacinations by manufacturer
vax_cases_by_man = utils.prepprocess_data_vaccinations_by_man(vaccinations_by_manufacturer)
#Get most recent date to find total vaccines in world
total_vaccines = utils.get_total_vaccines(vaccinations)
#total cases in world
total_cases = utils.total_cases(owid_covid_latest)
#Total deaths in world
deaths = utils.total_death(owid_covid_latest)
# read in owid data
owid = utils.clean_case_data(owid_covid_latest)
owid_date = utils.date_correct_owid(owid_covid_latest)



#for chart_js map

@app.route("/")
@app.route("/global-vaccinations")
def plot_plotly_global():
    #ploting
    plot_global_cases_per_country = plotly_plot.plotly_global_cases_per_country(
        final_df)
    plot_global_time_series = plotly_plot.plotly_global_timeseries(
        timeseries_final)
    plot_geo_analysis = plotly_plot.plotly_geo_analysis(final_df)
    context = {"total_all_confirmed": int(total_cases),
               "total_death": int(deaths), "total_all_vaccines": int(total_vaccines),
            'plot_global_cases_per_country': plot_global_cases_per_country,
            'plot_global_time_series': plot_global_time_series,'plot_geo_analysis': plot_geo_analysis}
    return render_template('plotly.html', context=context)



@app.route("/vaccinations-by-manufacturer")
def plot_altair_global():
    # total confirmed cases globally
    # total_all_confirmed = total_confirmed[total_confirmed.columns[-1]].sum()
    # total_all_recovered = total_recovered[total_recovered.columns[-1]].sum()
    # total_all_deaths = total_death[total_death.columns[-1]].sum()
    #ploting
    plot_global_cases_per_country = altair_plot.altair_global_cases_per_country(vax_cases_by_man)
    # plot_global_time_series = altair_plot.altair_global_time_series(
    #     timeseries_final)
    time_series = altair_plot.altair_per_country_time_series(vax_cases_by_man)
    context = {'plot_global_cases_per_country': plot_global_cases_per_country,
                'plot_geo_analysis': time_series, 'plot_global_cases_per_country': plot_global_cases_per_country}
    return render_template('altair.html', context=context)

    
@app.route("/cases-deaths-vaccines")
def plot_chartjs():
    #time_series = altair_plot.altair_per_country_time_series(vax_cases_by_man)
    deaths_vax = altair_plot.vaccinations_deaths(owid_date)
    date_vaccines = altair_plot.date_vaccinations(owid_date)
    date_deaths = altair_plot.date_deaths(owid_date)
    context = {'date_deaths': date_deaths, 'date_vaccines':date_vaccines, 'death_vax': deaths_vax}
    return render_template('chartjs.html', context=context)

@app.route("/state-vaccines")
def plot_states():
    state_vax = altair_plot.state_vaccinations_per_hundred(us_covid_vaccinations)
    map_ = altair_plot.state_map(us_covid_vaccinations)
    context = {'state_vax':state_vax, 'map':map_}
    return render_template('states.html', context=context)



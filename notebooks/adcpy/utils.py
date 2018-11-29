

import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4
import os
from adcpy import adcirc
from adcpy import swan
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from IPython.display import HTML
import plotly.graph_objs as go
import plotly.offline as po
import pandas as pd

def output_files(root_dir):
    f61 = os.path.join(root_dir,'fort.61.nc')
    f62 = os.path.join(root_dir,'fort.62.nc')
    f63 = os.path.join(root_dir,'fort.63.nc')
    f64 = os.path.join(root_dir,'fort.64.nc')
    f73 = os.path.join(root_dir,'fort.73.nc')
    f74 = os.path.join(root_dir,'fort.74.nc')
    max_f63 = os.path.join(root_dir,'maxele.63.nc')
    max_wv63 = os.path.join(root_dir,'maxwvel.63.nc')
    max_v63  = os.path.join(root_dir,'maxvel.63.nc')
    minpr63  = os.path.join(root_dir,'minpr.63.nc')
    swan_hs = os.path.join(root_dir,'swan_HS.63.nc')
    max_hs = os.path.join(root_dir,'swan_HS_max.63.nc')
    swan_dir = os.path.join(root_dir,'swan_DIR.63.nc')
    max_dir = os.path.join(root_dir,'swan_DIR_max.63.nc')
    files = [f61,f62,f63,f64,f73,f74,max_f63,max_wv63,max_v63,minpr63,swan_hs,max_hs,swan_dir,max_dir]
    return files

def timeseries(nc_data,start,freq,station,name):
    data = nc_data['zeta'][:,station]#106378]
    table = pd.DataFrame(data)
    date  = pd.date_range(start=start,periods=int(len(table)),freq=freq)
    table.insert(0,'Date Time',date)
    table = table.rename(columns={0:name})
    return table

def plot_timeseries(table,start,end,station):
    pred = pd.read_csv('https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date='+start+'&end_date='+end+'&datum=MSL&station='+station+'&time_zone=GMT&units=metric&interval=6&format=csv')
    obs  = pd.read_csv('https://tidesandcurrents.noaa.gov/api/datagetter?product=water_level&application=NOS.COOPS.TAC.WL&begin_date='+start+'&end_date='+end+'&datum=MSL&station='+station+'&time_zone=GMT&units=metric&format=csv')
    trace = go.Scatter(x = table['Date Time'],y = table[' Prediction'],
                name = 'ADCIRC',mode = 'lines',
                line = dict(
                    color = ('rgb(204, 0, 153)')))
    trace2 = go.Scatter(x = pred['Date Time'],y = pred[' Prediction'],
                    name = 'NOAA Prediction',mode = 'lines',
                    line = dict(
                        color = ('rgb(100, 100, 153)')))
    trace3 = go.Scatter(x = obs['Date Time'],y = obs[' Water Level'],
                    name = 'NOAA Observation',mode = 'lines',
                    line = dict(
                        color = ('rgb(100, 100, 53)')))
    data = [trace,trace2,trace3]
    return data
def plot_tidal(table,start,end,station):
    pred = pd.read_csv('https://tidesandcurrents.noaa.gov/api/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date='+start+'&end_date='+end+'&datum=MSL&station='+station+'&time_zone=GMT&units=metric&interval=6&format=csv')
    obs  = pd.read_csv('https://tidesandcurrents.noaa.gov/api/datagetter?product=water_level&application=NOS.COOPS.TAC.WL&begin_date='+start+'&end_date='+end+'&datum=MSL&station='+station+'&time_zone=GMT&units=metric&format=csv')
    table = table.set_index(pd.DatetimeIndex(table['Date Time']))
    pred = pred.set_index(pd.DatetimeIndex(pred['Date Time']))
    trace = go.Scatter(x = table['Date Time'],y = table[' Prediction'],
                name = 'ADCIRC',mode = 'lines',
                line = dict(
                    color = ('rgb(204, 0, 153)')))
    trace2 = go.Scatter(x = pred['Date Time'],y = pred[' Prediction'],
                    name = 'NOAA Prediction',mode = 'lines',
                    line = dict(
                        color = ('rgb(100, 100, 153)')))
    trace3 = go.Scatter(x = obs['Date Time'],y = obs[' Water Level'],
                    name = 'NOAA Observation',mode = 'lines',
                    line = dict(
                        color = ('rgb(100, 100, 53)')))
    data = [trace,trace2]
    return data

def layout(title,xaxis,yaxis):
    layout = go.Layout(dict(title=title),xaxis = dict(title = xaxis),
                   yaxis = dict(title = yaxis),legend= dict(orientation="h"),
                   font = dict(color = 'rgb(0,0,0)'),paper_bgcolor = 'rgb(255,255,255)',
                   plot_bgcolor = 'rgb(255,255,255)')
    return layout


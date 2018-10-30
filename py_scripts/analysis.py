
import matplotlib.pyplot as plt
from adcirc import adcirc
import os
import pandas as pd
import netCDF4 as nc4
from datetime import datetime
import matplotlib.pyplot as plt
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import numpy as np
import random


def table_station(path,file,start,freq,station,attribute,name):
    nc_file = nc4.Dataset(os.path.join(path,file))
    data = nc_file[attribute][:,station]
    table = pd.DataFrame(data)
    date  = pd.date_range(start=start,periods=int(len(table)),freq=freq)
    table.insert(0,'Date Time',date)
    table = table.rename(columns={0:name})
    return table


def noaa_data(path,file):
    data = pd.read_csv(os.path.join(path,file))
    return data



def calc_bias(model_data,name,obs_data,pred_data):
    n = len(pred_data)
    bias,e,SI,ak_bias,noaa_bias = [],[],[],[],[]
    for i in range(len(model_data)):
        ei= model_data[name][i] - pred_data[' Prediction'][i]
        e.append(ei)
        e_ave = np.average(ei)
        SI.append(np.sqrt((1/n)*(ei-e_ave)**2)/((1/n)*abs(pred_data[' Prediction'][i])))
        bias.append(((1/n)*ei)/((1/n)*abs(pred_data[' Prediction'][i])))
        ak_bias.append(obs_data[' Water Level'][i] - model_data[name][i])
        noaa_bias.append(obs_data[' Water Level'][i] - pred_data[' Prediction'][i])
    SI2 = pd.DataFrame(SI)
    bias2 = pd.DataFrame(bias)
    bias2 = bias2.replace([np.inf, -np.inf], np.nan)
    ak_bias2 = pd.DataFrame(ak_bias)
    noaa_bias= pd.DataFrame(noaa_bias)
    return bias2,ak_bias2,SI2,noaa_bias

def plot(model_data,name,info,pred_data):
    data = []
    i=0
    contents = [model_data,pred_data]
    for content in contents:

        c_list = ['rgb(51, 204, 51)','rgb(0, 255, 204)',
              'rgb(0, 204, 255)','rgb(102, 255, 255)',
              'rgb(0, 102, 153)','rgb(0, 0, 255)',
              'rgb(51, 51, 255)','rgb(102, 0, 255)',
              'rgb(153, 153, 255)','rgb(204, 0, 255)',
              'rgb(255, 51, 204)','rgb(204, 0, 0)',
              'rgb(255, 153, 0)','rgb(204, 255, 51)',
              'rgb(0, 153, 0)']
        for x in range(1):
            y=random.randint(1,14)
            color = c_list[y]
        trace = go.Scatter(
                x = content['Date Time'],
                y = content[name],
                mode = 'lines',
                name = info[i],
                line = dict(
                        color = color)
                            )
        data.append(trace)
        i+=1
    return data

def plot_bias(model_data,bias,bias2,info):
    data = []
    i=0
    contents = [bias,bias2]
    for content in contents:

        c_list = ['rgb(51, 204, 51)','rgb(0, 255, 204)',
              'rgb(0, 204, 255)','rgb(102, 255, 255)',
              'rgb(0, 102, 153)','rgb(0, 0, 255)',
              'rgb(51, 51, 255)','rgb(102, 0, 255)',
              'rgb(153, 153, 255)','rgb(204, 0, 255)',
              'rgb(255, 51, 204)','rgb(204, 0, 0)',
              'rgb(255, 153, 0)','rgb(204, 255, 51)',
              'rgb(0, 153, 0)']
        for x in range(1):
            y=random.randint(1,14)
            color = c_list[y]
        trace = go.Scatter(
                x = model_data['Date Time'],
                y = content[0],
                mode = 'lines',
                name = info[i],
                line = dict(
                        color = color,
                        dash  = 'dash')
                            )
        data.append(trace)
        i+=1
    return data



















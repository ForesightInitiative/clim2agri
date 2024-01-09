#import requests
from netCDF4 import Dataset
#import wget
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
#import matplotlib.pyplot as plt
#from bs4 import BeautifulSoup
#import zipfile
from rclone_python import rclone


def find_closest_index(array, target):
    closest_index = None
    min_distance = float('inf')
    
    for i, num in enumerate(array):
        distance = abs(num - target)
        if distance < min_distance:
            min_distance = distance
            closest_index = i
            
    return closest_index


def generate_month_year_range(initial_date, final_date):
    result = []
    current_date = initial_date
    
    while current_date <= final_date:
        result.append(current_date.strftime("%m-%Y"))
        current_date += timedelta(days=32)
        current_date = current_date.replace(day=1)  # Move to the first day of the next month
    
    return result

def generate_day_of_year_range(initial_date, final_date):
    result = []
    current_date = initial_date
    
    while current_date <= final_date:
        result.append(current_date.strftime("%j-%Y"))
        current_date += timedelta(days=1)
    
    return result


var_mswx = {'LWd':'downward_longwave_radiation',
            'SWd':'downward_shortwave_radiation',
            'P':'precipitation',
            'Pres':'surface_pressure',
            'RelHum':'relative_humidity',
            'SpecHum':'specific_humidity',
            'Temp':'air_temperature',
            'Tmax':'air_temperature',
            'Tmin':'air_temperature',
            'Wind':'wind_speed'}
var_mswx_df = {'lw_dwn,MJ/m2/day':'downward_longwave_radiation',
            'sw_dwn,MJ/m2/day':'downward_shortwave_radiation',
            'rainfall,mm/day':'precipitation',
            'srfc_pressure,Pa':'surface_pressure',
            'rh,':'relative_humidity',
            'specific_humidity,':'specific_humidity',
            't2m_mean,C':'air_temperature',
            't2m_max,C':'air_temperature',
            't2m_min,C':'air_temperature',
            'windspeed,m/s':'wind_speed'}
def mswx(ini_date, fin_date, lat, lon):
    os.mkdir('MSWX')
    doy_year_range = generate_day_of_year_range(ini_date, fin_date)
    array_df = []    
    for doy_year in doy_year_range:
        [doy,year] = doy_year.split('-')
        doy = doy.zfill(3)
        aux_var = []
        for var in var_mswx.keys():
            try:
                rclone.copy(f'GoogleDrive:/MSWX_V100/Past/{var}/Daily/{year}{doy}.nc', 'MSWX', ignore_existing=True, args=['--drive-shared-with-me'])
            except:
                rclone.copy(f'GoogleDrive:/MSWX_V100/NRT/{var}/Daily/{year}{doy}.nc', 'MSWX', ignore_existing=True, args=['--drive-shared-with-me'])

            filename = f'MSWX/{year}{doy}.nc'

            mswx_nc = Dataset(filename)
            os.remove(filename)
            #mswx_time = pd.to_datetime(datetime(1900, 1, 1,0,0,0) + timedelta(days=int(mswx_nc['time'][:])))

            closest_index_lat = find_closest_index(mswx_nc['lat'][:], lat)
            closest_index_lon = find_closest_index(mswx_nc['lon'][:], lon)
            aux_var.append(np.squeeze(mswx_nc[var_mswx[var]][:][0,closest_index_lat,closest_index_lon]))

        array_df.append(aux_var)
            
    #df_mswx = pd.DataFrame(array_df,columns = ['date','pp']) 
    #df_mswx.set_index(['date'],inplace = True)  
    os.rmdir('MSWX')
    df_mswx = pd.DataFrame(np.squeeze(array_df),columns=var_mswx_df.keys())
    df_mswx['date']=np.arange(ini_date,fin_date + timedelta(days=1),np.timedelta64(1, "D"))
    df_mswx.set_index('date',inplace = True)
    df_mswx['radiation,MJ/m2/day'] = df_mswx['lw_dwn,MJ/m2/day'] + df_mswx['sw_dwn,MJ/m2/day']
    df_mswx['rh,'] = df_mswx['rh,']/100

    return df_mswx
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

def mswep(ini_date, fin_date, lat, lon):
    os.mkdir('MSWEP')
    doy_year_range = generate_day_of_year_range(ini_date, fin_date)
    array_df = []    
    for doy_year in doy_year_range:
        [doy,year] = doy_year.split('-')
        doy = doy.zfill(3)
        try:
            rclone.copy(f'GoogleDrive:/MSWEP_V280/Past/Daily/{year}{doy}.nc', 'MSWEP', ignore_existing=True, args=['--drive-shared-with-me'])
        except:
            rclone.copy(f'GoogleDrive:/MSWEP_V280/NRT/Daily/{year}{doy}.nc', 'MSWEP', ignore_existing=True, args=['--drive-shared-with-me'])

        filename = f'MSWEP/{year}{doy}.nc'

        mswep_nc = Dataset(filename)
        os.remove(filename)
        mswep_time = pd.to_datetime(datetime(1900, 1, 1,0,0,0) + timedelta(days=int(mswep_nc['time'][:])))

        closest_index_lat = find_closest_index(mswep_nc['lat'][:], lat)
        closest_index_lon = find_closest_index(mswep_nc['lon'][:], lon)

        array_df.append([mswep_time,np.squeeze(np.array(mswep_nc['precipitation'][:][0,closest_index_lat,closest_index_lon]))])
            
    df_mswep = pd.DataFrame(array_df,columns = ['date','rainfall,mm/day']) 
    df_mswep.set_index(['date'],inplace = True)  
    os.rmdir('MSWEP')
    #df_final = df.loc[ini_date:fin_date]
        #df = pd.DataFrame([mswep_time,np.squeeze(np.array(mswep_nc['precipitation'][0,closest_index_lat,closest_index_lon]))], 
        #         index = ['date','pp']).transpose().set_index('date')
        #array_df.append(df)
    return df_mswep
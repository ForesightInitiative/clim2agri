#import requests
from netCDF4 import Dataset
import wget
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
#import matplotlib.pyplot as plt
#from bs4 import BeautifulSoup
#import zipfile
#from rclone_python import rclone


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

def chirps(ini_date, fin_date, lat, lon):
    month_year_range = generate_month_year_range(ini_date, fin_date)
    array_df = []    
    for month_year in month_year_range:
        [month,year] = month_year.split('-')
        base_link = f'https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/by_month/chirps-v2.0.{year}.{month}.days_p05.nc'

        filename = wget.download(base_link)

        chirps_nc = Dataset(filename)
        os.remove(filename)
        chirps_time = pd.to_datetime([datetime(1980, 1, 1,0,0,0) + timedelta(days=int(days)) for days in chirps_nc['time'][:]])

        closest_index_lat = find_closest_index(chirps_nc['latitude'][:], lat)
        closest_index_lon = find_closest_index(chirps_nc['longitude'][:], lon)

        df = pd.DataFrame([chirps_time,np.squeeze(np.array(chirps_nc['precip'][:,closest_index_lat,closest_index_lon]))], 
                index = ['date','rainfall,mm/day']).transpose().set_index('date')
        array_df.append(df)
        
    df_final = pd.concat(array_df).loc[ini_date:fin_date]
    return df_final
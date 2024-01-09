import requests
from netCDF4 import Dataset
import wget
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
#import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
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


def persiann(ini_date, fin_date, lat, lon):
    month_year_range = generate_month_year_range(ini_date, fin_date)
    array_df = []
    for i, month_year in enumerate(month_year_range):
        [month,year] = month_year.split('-')
        #print(year)
        url_files = f'https://www.ncei.noaa.gov/data/precipitation-persiann/access/{year}/'
        url_base_download = f'https://www.ncei.noaa.gov/data/precipitation-persiann/access/{year}/'
        
        response = requests.get(url_files)
        soup= BeautifulSoup(response.content,features="html.parser")
        list_links = soup.find_all('a')[5:]

        for link in list_links:
            link = link.get_text()
            _, _, date, _ = link.split('_')
            year_file = date[0:4]
            month_file = date[4:6]
            day_file = date[6:8]

            if month == month_file:
                #print(month)
                url_download = url_base_download + link
                filename = wget.download(url_download)
                #print(filename)
                persiann_nc = Dataset(filename)
                os.remove(filename)

                persiann_time = pd.to_datetime(datetime(1979, 1, 1,0,0,0) + timedelta(days=int(persiann_nc['time'][:][0])))

                closest_index_lat = find_closest_index(persiann_nc['lat'][:], lat)
                closest_index_lon = find_closest_index(persiann_nc['lon'][:], lon)

                array_df.append([persiann_time,np.squeeze(np.array(persiann_nc['precipitation'][:][0,closest_index_lon,closest_index_lat]))])
            
    df = pd.DataFrame(array_df,columns = ['date','rainfall,mm/day']) 
    df.set_index(['date'],inplace = True)  
    df_final = df.loc[ini_date:fin_date]
    return df_final
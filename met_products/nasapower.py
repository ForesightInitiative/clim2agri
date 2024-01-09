#import requests
#from netCDF4 import Dataset
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

def nasapower(ini_date,fin_date, lat, lon):

    dates = f'start={ini_date.year}{ini_date.month}{ini_date.day}&end={fin_date.year}{str(fin_date.month).zfill(2)}{str(fin_date.day).zfill(2)}&'
    loc = f'latitude={lat}&longitude={lon}&'
    com = 'community=ag&'
    parameters = 'parameters=T2M%2CT2M_MIN%2CT2M_MAX%2CTDEW%2CU2M%2CV2M%2CPRECTOTCORR%2CALLSKY_SFC_LW_DWN%2CALLSKY_SFC_SW_DWN'
    others = '&format=csv&header=true&time-standard=utc'
    api_link = 'https://power.larc.nasa.gov/api/temporal/daily/point?'+dates+loc+com+parameters+others

    filename = wget.download(api_link)
    date_array = np.arange(ini_date, fin_date+timedelta(days=1), timedelta(days=1)).astype(datetime)
    df = pd.read_csv(filename,skiprows = 17)
    os.remove(filename)
    df['date'] = date_array
    df.set_index('date',inplace = True)
    df['radiation,MJ/m2/day'] = df['ALLSKY_SFC_LW_DWN']+df['ALLSKY_SFC_SW_DWN']
    
    
    df.drop(columns = ['YEAR','DOY'],inplace = True)
    df.rename(columns={"PRECTOTCORR": "rainfall,mm/day", 
                       "T2M_MAX": "t2m_max,C",
                       "ALLSKY_SFC_SW_DWN":'sw_down,MJ/m2/day',
                        "T2M_MIN":"t2m_min,C",
                        "U2M":"u2m,m/s",
                        "V2M":"v2m,m/s",
                        "T2M":"t2m_mean,C",
                        "ALLSKY_SFC_LW_DWN":"lw_down,MJ/m2/day",
                        "T2MDEW":"t2m_dew,C",
                        },inplace = True)

    df['windspeed,m/s'] = np.sqrt(df['u2m,m/s']**2+df['v2m,m/s']**2                )
    return df

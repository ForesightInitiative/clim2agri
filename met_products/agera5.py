#import requests
from netCDF4 import Dataset
#import wget
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
#import matplotlib.pyplot as plt
#from bs4 import BeautifulSoup
import zipfile
#from rclone_python import rclone
import cdsapi


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

def agera5(ini_date, fin_date, lat, lon):
    delta = 0.5
    os.mkdir('AgEra5')
    month_year_range = generate_month_year_range(ini_date, fin_date)
    array_df = []    
    for month_year in month_year_range:
        [month,year] = month_year.split('-')
        c = cdsapi.Client()

        c.retrieve(
        'sis-agrometeorological-indicators',
        {
            'format': 'zip',
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'month': month,
            'variable': '2m_temperature',
            'statistic': '24_hour_mean',
            'area': [
                lat - delta, lon - delta, lat + delta,
                lon + delta,
            ],
            'year': year,
        },
        f'AgEra5/temperature_{year}_{month}.zip')
        
    for filename in os.listdir('AgEra5'):
        if filename.endswith('.zip'):
            with zipfile.ZipFile(f'AgEra5/{filename}', 'r') as zip_ref:
                zip_ref.extractall('AgEra5')
            os.remove('AgEra5/'+filename)
    array_df = []

    for filename in os.listdir('AgEra5'):
        if filename.endswith('.nc'):
            agera5_nc = Dataset('AgEra5/'+filename)
            os.remove('AgEra5/'+filename)

            agera5_time = pd.to_datetime(datetime(1900, 1, 1,0,0,0) + timedelta(days=int(agera5_nc['time'][:][0])))

            closest_index_lat = find_closest_index(agera5_nc['lat'][:], lat)
            closest_index_lon = find_closest_index(agera5_nc['lon'][:], lon)

            array_df.append([agera5_time,np.squeeze((agera5_nc['Temperature_Air_2m_Mean_24h'][:][0,closest_index_lat,closest_index_lon]))])
    df = pd.DataFrame(array_df,columns = ['date','T2m_mean']) 
    df.set_index(['date'],inplace = True)  
    df.sort_index(inplace = True)
    df_final_temp_mean = df.loc[ini_date:fin_date]

    array_df = []    
    for month_year in month_year_range:
        [month,year] = month_year.split('-')
        c = cdsapi.Client()

        c.retrieve(
        'sis-agrometeorological-indicators',
        {
            'format': 'zip',
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'month': month,
            'variable': '2m_temperature',
            'statistic': '24_hour_minimum',
            'area': [
                lat - delta, lon - delta, lat + delta,
                lon + delta,
            ],
            'year': year,
        },
        f'AgEra5/temperature_{year}_{month}.zip')
        
    for filename in os.listdir('AgEra5'):
        if filename.endswith('.zip'):
            with zipfile.ZipFile(f'AgEra5/{filename}', 'r') as zip_ref:
                zip_ref.extractall('AgEra5')
            os.remove('AgEra5/'+filename)

    array_df = []

    for filename in os.listdir('AgEra5'):
        if filename.endswith('.nc'):
            agera5_nc = Dataset('AgEra5/'+filename)
            os.remove('AgEra5/'+filename)

            agera5_time = pd.to_datetime(datetime(1900, 1, 1,0,0,0) + timedelta(days=int(agera5_nc['time'][:][0])))

            closest_index_lat = find_closest_index(agera5_nc['lat'][:], lat)
            closest_index_lon = find_closest_index(agera5_nc['lon'][:], lon)

            array_df.append([agera5_time,np.squeeze((agera5_nc['Temperature_Air_2m_Min_24h'][:][0,closest_index_lat,closest_index_lon]))])
    df = pd.DataFrame(array_df,columns = ['date','T2m_min']) 
    df.set_index(['date'],inplace = True)  
    df.sort_index(inplace = True)
    df_final_temp_min = df.loc[ini_date:fin_date]

    array_df = []    
    for month_year in month_year_range:
        [month,year] = month_year.split('-')
        c = cdsapi.Client()

        c.retrieve(
        'sis-agrometeorological-indicators',
        {
            'format': 'zip',
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'month': month,
            'variable': '2m_temperature',
            'statistic': '24_hour_maximum',
            'area': [
                lat - delta, lon - delta, lat + delta,
                lon + delta,
            ],
            'year': year,
        },
        f'AgEra5/temperature_{year}_{month}.zip')
        
    for filename in os.listdir('AgEra5'):
        if filename.endswith('.zip'):
            with zipfile.ZipFile(f'AgEra5/{filename}', 'r') as zip_ref:
                zip_ref.extractall('AgEra5')
            os.remove('AgEra5/'+filename)

    array_df = []

    for filename in os.listdir('AgEra5'):
        if filename.endswith('.nc'):
            agera5_nc = Dataset('AgEra5/'+filename)
            os.remove('AgEra5/'+filename)

            agera5_time = pd.to_datetime(datetime(1900, 1, 1,0,0,0) + timedelta(days=int(agera5_nc['time'][:][0])))

            closest_index_lat = find_closest_index(agera5_nc['lat'][:], lat)
            closest_index_lon = find_closest_index(agera5_nc['lon'][:], lon)

            array_df.append([agera5_time,np.squeeze((agera5_nc['Temperature_Air_2m_Max_24h'][:][0,closest_index_lat,closest_index_lon]))])
    df = pd.DataFrame(array_df,columns = ['date','T2m_max']) 
    df.set_index(['date'],inplace = True)  
    df.sort_index(inplace = True)
    df_final_temp_max = df.loc[ini_date:fin_date]

    array_df = []    
    for month_year in month_year_range:
        [month,year] = month_year.split('-')
        c = cdsapi.Client()

        c.retrieve(
        'sis-agrometeorological-indicators',
        {
            'format': 'zip',
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'month': month,
            'variable': 'solar_radiation_flux',
            'area': [
                lat - delta, lon - delta, lat + delta,
                lon + delta,
            ],
            'year': year,
        },
        f'AgEra5/temperature_{year}_{month}.zip')
        
    for filename in os.listdir('AgEra5'):
        if filename.endswith('.zip'):
            with zipfile.ZipFile(f'AgEra5/{filename}', 'r') as zip_ref:
                zip_ref.extractall('AgEra5')
            os.remove('AgEra5/'+filename)

    array_df = []

    for filename in os.listdir('AgEra5'):
        if filename.endswith('.nc'):
            agera5_nc = Dataset('AgEra5/'+filename)
            os.remove('AgEra5/'+filename)

            agera5_time = pd.to_datetime(datetime(1900, 1, 1,0,0,0) + timedelta(days=int(agera5_nc['time'][:][0])))

            closest_index_lat = find_closest_index(agera5_nc['lat'][:], lat)
            closest_index_lon = find_closest_index(agera5_nc['lon'][:], lon)

            array_df.append([agera5_time,np.squeeze((agera5_nc['Solar_Radiation_Flux'][:][0,closest_index_lat,closest_index_lon]))])
    df = pd.DataFrame(array_df,columns = ['date','Radiation']) 
    df.set_index(['date'],inplace = True)  
    df.sort_index(inplace = True)
    df_final_rad = df.loc[ini_date:fin_date]

    array_df = []    
    for month_year in month_year_range:
        [month,year] = month_year.split('-')
        c = cdsapi.Client()

        c.retrieve(
        'sis-agrometeorological-indicators',
        {
            'format': 'zip',
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'month': month,
            'variable': 'precipitation_flux',
            'area': [
                lat - delta, lon - delta, lat + delta,
                lon + delta,
            ],
            'year': year,
        },
        f'AgEra5/temperature_{year}_{month}.zip')
        
    for filename in os.listdir('AgEra5'):
        if filename.endswith('.zip'):
            with zipfile.ZipFile(f'AgEra5/{filename}', 'r') as zip_ref:
                zip_ref.extractall('AgEra5')
            os.remove('AgEra5/'+filename)

    array_df = []

    for filename in os.listdir('AgEra5'):
        if filename.endswith('.nc'):
            agera5_nc = Dataset('AgEra5/'+filename)
            os.remove('AgEra5/'+filename)

            agera5_time = pd.to_datetime(datetime(1900, 1, 1,0,0,0) + timedelta(days=int(agera5_nc['time'][:][0])))

            closest_index_lat = find_closest_index(agera5_nc['lat'][:], lat)
            closest_index_lon = find_closest_index(agera5_nc['lon'][:], lon)

            array_df.append([agera5_time,np.squeeze((agera5_nc['Precipitation_Flux'][:][0,closest_index_lat,closest_index_lon]))])
    df = pd.DataFrame(array_df,columns = ['date','Precipitation']) 
    df.set_index(['date'],inplace = True)  
    df.sort_index(inplace = True)
    df_final_precipitation = df.loc[ini_date:fin_date]

    array_df = []    
    for month_year in month_year_range:
        [month,year] = month_year.split('-')
        c = cdsapi.Client()

        c.retrieve(
        'sis-agrometeorological-indicators',
        {
            'format': 'zip',
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'month': month,
            'variable': '10m_wind_speed',
            'statistic': '24_hour_mean',
            'area': [
                lat - delta, lon - delta, lat + delta,
                lon + delta,
            ],
            'year': year,
        },
        f'AgEra5/temperature_{year}_{month}.zip')
        
    for filename in os.listdir('AgEra5'):
        if filename.endswith('.zip'):
            with zipfile.ZipFile(f'AgEra5/{filename}', 'r') as zip_ref:
                zip_ref.extractall('AgEra5')
            os.remove('AgEra5/'+filename)

    array_df = []

    for filename in os.listdir('AgEra5'):
        if filename.endswith('.nc'):
            agera5_nc = Dataset('AgEra5/'+filename)
            os.remove('AgEra5/'+filename)

            agera5_time = pd.to_datetime(datetime(1900, 1, 1,0,0,0) + timedelta(days=int(agera5_nc['time'][:][0])))

            closest_index_lat = find_closest_index(agera5_nc['lat'][:], lat)
            closest_index_lon = find_closest_index(agera5_nc['lon'][:], lon)

            array_df.append([agera5_time,np.squeeze((agera5_nc['Wind_Speed_10m_Mean'][:][0,closest_index_lat,closest_index_lon]))])
    df = pd.DataFrame(array_df,columns = ['date','Windspeed']) 
    df.set_index(['date'],inplace = True)  
    df.sort_index(inplace = True)
    df_final_windspeed = df.loc[ini_date:fin_date]

    array_df = []    
    for month_year in month_year_range:
        [month,year] = month_year.split('-')
        c = cdsapi.Client()

        c.retrieve(
        'sis-agrometeorological-indicators',
        {
            'format': 'zip',
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'month': month,
            'variable': 'vapour_pressure',
            'statistic': '24_hour_mean',
            'area': [
                lat - delta, lon - delta, lat + delta,
                lon + delta,
            ],
            'year': year,
        },
        f'AgEra5/temperature_{year}_{month}.zip')
        
    for filename in os.listdir('AgEra5'):
        if filename.endswith('.zip'):
            with zipfile.ZipFile(f'AgEra5/{filename}', 'r') as zip_ref:
                zip_ref.extractall('AgEra5')
            os.remove('AgEra5/'+filename)

    array_df = []

    for filename in os.listdir('AgEra5'):
        if filename.endswith('.nc'):
            agera5_nc = Dataset('AgEra5/'+filename)
            os.remove('AgEra5/'+filename)

            agera5_time = pd.to_datetime(datetime(1900, 1, 1,0,0,0) + timedelta(days=int(agera5_nc['time'][:][0])))

            closest_index_lat = find_closest_index(agera5_nc['lat'][:], lat)
            closest_index_lon = find_closest_index(agera5_nc['lon'][:], lon)

            array_df.append([agera5_time,np.squeeze((agera5_nc['Vapour_Pressure_Mean'][:][0,closest_index_lat,closest_index_lon]))])
    df = pd.DataFrame(array_df,columns = ['date','vp']) 
    df.set_index(['date'],inplace = True)  
    df.sort_index(inplace = True)
    df_final_vp = df.loc[ini_date:fin_date]
    os.rmdir('AgEra5')
    df_final_agera5 = pd.concat([df_final_temp_mean,df_final_temp_min, df_final_temp_max,df_final_rad,df_final_precipitation,df_final_windspeed,df_final_vp],axis = 1)
    def e_sat(T):
        T = T - 273.15
        return 0.6112*np.exp(17.67*T/(T+243.5))*1000/100

    def compute_HR(vp,T):
        return vp/e_sat(T)
    
    df_final_agera5["HR"] = compute_HR(df_final_agera5["vp"],df_final_agera5["T2m_mean"])

    df_final_agera5["T2m_mean"] = df_final_agera5["T2m_mean"] - 273.15
    df_final_agera5["T2m_min"] = df_final_agera5["T2m_min"] - 273.15
    df_final_agera5["T2m_max"] = df_final_agera5["T2m_max"] - 273.15
    
    df_final_agera5.rename(columns = {"T2m_mean":"t2m_mean,C",	
                                      "T2m_min":"t2m_min,C",
                                      "T2m_max":"t2m_max,C",
                                      "Radiation":"radiation,MJ/m2/day",
                                      "Precipitation":"rainfall,mm/day",
                                      "Windspeed":"windspeed,m/s",
                                      "vp":"vapor_pressure,kPa",
                                      "HR":"hr,"},inplace = True)

    return df_final_agera5
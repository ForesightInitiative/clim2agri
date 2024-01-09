#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime
import pandas as pd
import numpy as np

from met_products.agera5 import agera5
from met_products.chirps import chirps
from met_products.imerg import imerg
from met_products.nasapower import nasapower
from met_products.persiann import persiann
from met_products.mswep import mswep
from met_products.mswx import mswx


# In[2]:



# In[3]:


dict_ = {'1':'Tmin',
            '2':'Tmax',
            '3':'Tmean',
            '4':'Rainfall',
            '5':'Radiation',
            '6':'Windspeed',
            '7':'Relative Humidity',
            '8':'Vapor Pressure'}

dict_var = {'1':'t2m_min,C',
            '2':'t2m_max,C',
            '3':'t2m_mean,C',
            '4':'rainfall,mm/day',
            '5':'radiation,MJ/m2/day',
            '6':'windspeed,m/s',
            '7':'rh',
            '8':'vapor_pressure,kPa'}

dict_gridded_product_var = {'NASAPOWER': ['Tmin','Tmax','Tmean','Rainfall','Radiation','Windspeed'],
                            'Chirps': ['Rainfall'],
                            'AgEra5': ['Tmin','Tmax','Tmean','Rainfall','Radiation','Windspeed','Relative Humidity','Vapor Pressure'],
                            'Persiann': ['Rainfall'],
                            'Imerg': ['Rainfall'],
                            'MSWEP': ['Rainfall'],
                            'MSWX': ['Tmin','Tmax','Tmean','Rainfall','Radiation','Windspeed', 'Relative Humidity']}
dict_var_gridded_products = {
                                'Tmin': ['AgEra5','MSWX','NASAPOWER'],
                                'Tmax': ['AgEra5','MSWX','NASAPOWER'],
                                'Tmean':['AgEra5','MSWX','NASAPOWER'],
                                'Rainfall': ['AgEra5','Chirps','Imerg','MSWEP','MSWX','NASAPOWER','Persiann'],
                                'Radiation': ['AgEra5','MSWX','NASAPOWER'],
                                'Windspeed': ['AgEra5','MSWX','NASAPOWER'],
                                'Relative Humidity': ['AgEra5','MSWX'],
                                'Vapor Pressure': ['AgEra5']
                            }


# In[24]:


def var_and_cropmodel(ini_date,fin_date,lat,lon):    
    input_var = input('The available variables are the following: \n\
                        1.- Tmin \n\
                        2.- Tmax \n\
                        3.- Tmean \n\
                        4.- Rainfall \n\
                        5.- Radiation \n\
                        6.- Windspeed \n\
                        7.- Relative Humidity \n\
                        8.- Vapor Presure \n')
    
    str_input = 'Which gridded product you would like to extract that variable from?'
    for index, item in enumerate(dict_var_gridded_products[dict_[input_var]], start=1):
        #print(f"{index}.- {item}")
        str_input = str_input + f"{index}.- {item} \n"

    input_gp = input(str_input)
    gp = dict_var_gridded_products[dict_[input_var]][int(input_gp)-1]

    if gp == 'AgEra5':
        df = agera5(ini_date,fin_date,lat,lon)
    elif gp == 'Chirps':
        df = chirps(ini_date,fin_date,lat,lon)
    elif gp == 'Imerg':
        df = imerg(ini_date,fin_date,lat,lon)
    elif gp == 'MSWEP':
        df = mswep(ini_date,fin_date,lat,lon)
    elif gp == 'MSWX':
        df = mswx(ini_date,fin_date,lat,lon)
    elif gp == 'NASAPOWER':
        df = nasapower(ini_date,fin_date,lat,lon)
    elif gp == 'Persiann':
        df = persiann(ini_date,fin_date,lat,lon)
    return df, input_var


# In[7]:


def create_empty_csv():

    df_aux = pd.DataFrame(columns=[ 'Date',
                                    't2m_min,C',
                                    't2m_max,C',
                                    't2m_mean,C',
                                    'rainfall,mm/day',
                                    'radiation,MJ/m2/day',
                                    'windspeed,m/s',
                                    'rh',
                                    'vapor_pressure,kPa',
                                    'ETo,mm',
                                    '[CO2],ppm'])
    #df_aux.set_index('Date',inplace = True)

    df_aux.to_csv('weather_variables.csv')

    return print('----- A new file named: weather_variables.csv has been created -----')


# In[19]:


def download_variable(ini_date,fin_date,lat,lon):
    ini_date = datetime.strptime(ini_date,'%Y-%m-%d')
    fin_date = datetime.strptime(fin_date,'%Y-%m-%d')
    df, input_var = var_and_cropmodel(ini_date,fin_date,lat,lon)
    var = [np.round(aux_var,2) for aux_var in df[dict_var[input_var]].values]
    df_aux = pd.read_csv('weather_variables.csv',index_col = 0)
    df_aux[dict_var[input_var]] = var
    df_aux['Date'] = df.index
    #df_aux.set_index('Date',inplace = True)
    df_aux.to_csv('weather_variables.csv')
    return print(f'------ {dict_var[input_var]} Downloaded Successfully! -----')    


# # Aquacrop

def build_AQUACROP_input_file(lat,lon):
    df_aux = pd.read_csv('weather_variables.csv',index_col=0)
    df_aux['Date'] = pd.to_datetime(df_aux['Date'])
    df_aux.set_index('Date',inplace = True)


    day = np.array(df_aux.index.day,dtype = str)
    month = np.array(df_aux.index.month,dtype = str)
    year = np.array(df_aux.index.year,dtype = str)


    df_crop_model = pd.DataFrame(np.transpose(np.array([day,month,year,
                                                        df_aux['t2m_min,C'],
                                                        df_aux['t2m_max,C'],
                                                        df_aux['rainfall,mm/day'],
                                                        df_aux['ETo,mm']])),columns=['Day','Month','Year','Tmin(C)','Tmax(C)','Prcp(mm)','Eto(mm)'])

    file_name = "AQUACROP_input_file.txt"
    df_crop_model.to_csv(file_name,sep = '\t', index = False)
    return print('----- File has been built successfully! -----')

# # Cropsyst


def build_CROPSYST_input_file(lat,lon):
    df_aux = pd.read_csv('weather_variables.csv',index_col=0)
    df_aux['Date'] = pd.to_datetime(df_aux['Date'])
    df_aux.set_index('Date',inplace = True)

    doy = np.array([dt.timetuple().tm_yday for dt in df_aux.index],dtype = str)
    #var = np.round(df_aux[dict_var[input_var]].values,2)

    df_crop_model = pd.DataFrame(np.transpose([doy,
                                                df_aux['rainfall,mm/day'],
                                                df_aux['t2m_max,C'],
                                                df_aux['t2m_min,C'],
                                                df_aux['radiation,MJ/m2/day']]))

    file_name = "CROPSYST_input_file.txt"
    df_crop_model.to_csv(file_name,sep = ' ', index = False, header= False)
    return print('----- File has been built successfully! -----')


# # EPIC



def build_EPIC_input_file(lat,lon):
    df_aux = pd.read_csv('weather_variables.csv',index_col=0)
    df_aux['Date'] = pd.to_datetime(df_aux['Date'])
    df_aux.set_index('Date',inplace = True)
    
    day = np.array(df_aux.index.day,dtype = str)
    month = np.array(df_aux.index.month,dtype = str)
    year = np.array(df_aux.index.year,dtype = str)
    #var = np.round(df[dict_var[input_var]].values,2)

    df_crop_model = pd.DataFrame(np.transpose(np.array([year,month,day,
                                                        df_aux['radiation,MJ/m2/day'],
                                                        df_aux['t2m_max,C'],
                                                        df_aux['t2m_min,C'],
                                                        df_aux['rainfall,mm/day'],
                                                        df_aux['rh'],
                                                        df_aux['windspeed,m/s']
                                                        ])))
    file_name = "EPIC_input_file.txt"

# Write the header lines to the file
    with open(file_name, 'w') as file:
        file.write(f"## Weather file name\n")
        file.write(f"## Number of years followed by the beginning year e.g. if the data starts\n")
        file.write(f"## year 2023 and there are 10 years of data then: 102023\n")
    df_crop_model.to_csv(file_name, sep='\t', index=False, header=False, mode='a')
    return print('----- File has been built successfully! -----')


# # DSSAT



def build_DSSAT_input_file(lat,lon):    
    df_aux = pd.read_csv('weather_variables.csv',index_col=0)
    df_aux['Date'] = pd.to_datetime(df_aux['Date'])
    df_aux.set_index('Date',inplace = True)

    doy = np.array([dt.timetuple().tm_yday for dt in df_aux.index],dtype = str)
    year = np.array(df_aux.index.year,dtype = str)
    #var = np.round(df[dict_var[input_var]].values,2)

    date_doy = []
    for y, d in zip(year,doy):
        date_doy.append(y[-2::]+d.zfill(3))
    date_doy = np.array(date_doy,dtype = str)

    df_crop_model = pd.DataFrame(np.transpose(np.array([date_doy,
                                                        df_aux['radiation,MJ/m2/day'],
                                                        df_aux['t2m_max,C'],
                                                        df_aux['t2m_min,C'],
                                                        df_aux['rainfall,mm/day']])))

    file_name = "DSSAT_input_file.txt"
    tav = np.round(np.mean(df_aux['t2m_mean,C']),2)
    amp = np.round(np.max(df_aux.resample('1M').mean()['t2m_mean,C'])-np.min(df_aux.resample('1M').mean()['t2m_mean,C']),2)
    # Write the header lines to the file
    with open(file_name, 'w') as file:
        file.write(f"*WEATHER DATA: NAME OF STATION\n")
        file.write(f"@\t INSI\t LAT\t LONG\t ELEV\t TAV\t AMP\t REFHT\t WNDHT\n")
        file.write(f"\t XXXX\t {lat}\t {lon}\t ...\t {tav}\t {amp}\t ...\t ...\n")
        file.write(f"#DATE\t SRAD\t TMAX\t TMIN\t RAIN\n")

    df_crop_model.to_csv(file_name, sep='\t', index=False, header=None, mode='a')
    return print('----- File has been built successfully! -----')

# # STICS

# In[23]:


def build_STICS_input_file(lat,lon):
    df_aux = pd.read_csv('weather_variables.csv',index_col=0)
    df_aux['Date'] = pd.to_datetime(df_aux['Date'])
    df_aux.set_index('Date',inplace = True)
    
    date_doy = np.array([dt.timetuple().tm_yday for dt in df_aux.index],dtype = str)
    year = np.array(df_aux.index.year,dtype = str)
    day = np.array(df_aux.index.day,dtype = str)
    month = np.array(df_aux.index.month,dtype = str)
    #var = np.round(df_aux[dict_var[input_var]].values,2)
    station = ['station']*len(year)
#minimum temperature, maximum temperature, radiation, potential evapotranspiration, precipitation, wind speed, relative humidity, and CO2 concentration
    df_crop_model = pd.DataFrame(np.transpose(np.array([station,year, month, day, date_doy,
                                                        df_aux['t2m_min,C'],
                                                        df_aux['t2m_max,C'],
                                                        df_aux['radiation,MJ/m2/day'],
                                                        df_aux['ETo,mm'],
                                                        df_aux['rainfall,mm/day'],
                                                        df_aux['windspeed,m/s'],
                                                        df_aux['rh'],
                                                        df_aux['[CO2],ppm']])))
    file_name = "STICS_input_file.txt"
    df_crop_model.to_csv(file_name, sep='\t', index=False, header=False)
    return print('----- File has been built successfully! -----')


# # Orizav3


def build_ORIZA_input_file(lat,lon):
    df_aux = pd.read_csv('weather_variables.csv',index_col=0)
    df_aux['Date'] = pd.to_datetime(df_aux['Date'])
    df_aux.set_index('Date',inplace = True)

    file_name = "ORIZAv3_input_file.txt"

# Write the header lines to the file
    with open(file_name, 'w') as file:
        file.write(f"*-----------------------------------------------------------\n")
        file.write(f"* Station Name : \n")
        file.write(f"* Author :                 -99.: nil value\n")
        file.write(f"* Source :\n")
        file.write(f"* Comments  : \n")
        file.write(f"* Longitude : {lon}        Latitude: {lat}     Altitude:\n")
        file.write(f"* Column Daily Value\n")
        file.write(f"* 1  Station number\n")
        file.write(f"* 2  Year\n")
        file.write(f"* 3  Day\n")
        file.write(f"* 4  irradiance            KJ m-2 d-1\n")
        file.write(f"* 5  min temperature               oC\n")
        file.write(f"* 6  max temperature               oC\n")
        file.write(f"* 7  vapor pressure               kPa\n")
        file.write(f"* 8  mean wind speed            m s-1\n")
        file.write(f"* 9  precipitation             mm d-1\n")
        file.write(f"*-----------------------------------------------------------\n")
        file.write(f"{lon},{lat},ALT,A,B \n")

    doy = np.array([dt.timetuple().tm_yday for dt in df_aux.index],dtype = str)
    year = np.array(df_aux.index.year,dtype = str)
        #var = np.round(df[dict_var[input_var]].values,2)
        #if input_var == 5:
        #    var = var*1000
    station = ['1']*len(doy)
        
    df_crop_model = pd.DataFrame(np.transpose(np.array([station,year, doy, 
                                                        df_aux['radiation,MJ/m2/day'],
                                                        df_aux['t2m_min,C'],
                                                        df_aux['t2m_max,C'],
                                                        df_aux['vapor_pressure,kPa'],
                                                        df_aux['windspeed,m/s'],
                                                        df_aux['rainfall,mm/day']])))

    df_crop_model.to_csv(file_name, sep=',', index=False, header=False, mode='a')
    return print('----- File has been built successfully! -----')


# # APSIM


def build_APSIM_input_file(lat,lon):
    df_aux = pd.read_csv('weather_variables.csv',index_col=0)
    df_aux['Date'] = pd.to_datetime(df_aux['Date'])
    df_aux.set_index('Date',inplace = True)

    file_name = "APSIM_input_file.txt"
    tav = np.round(np.mean(df_aux['t2m_mean,C']),2)
    amp = np.round(np.max(df_aux.resample('1M').mean()['t2m_mean,C'])-np.min(df_aux.resample('1M').mean()['t2m_mean,C']),2)
# Write the header lines to the file
    with open(file_name, 'w') as file:
        file.write(f"site = somewhere \n")
        file.write(f"latitude = {lat} \n")
        file.write(f"latitude = {lon} \n")
        file.write(f"tav =  {tav} \n")
        file.write(f"amp =  {amp} \n")
        file.write(f"year\t day\t radn\t maxt\t mint\t rain\n")
        file.write(f"()\t ()\t (MJ/m2)\t (oC)\t (oC)\t (mm)\n")

    doy = np.array([dt.timetuple().tm_yday for dt in df_aux.index],dtype = str)
    year = np.array(df_aux.index.year,dtype = str)
        #var = np.round(df[dict_var[input_var]].values,2)
        #if input_var == 5:
        #    var = var*1000
        
    df_crop_model = pd.DataFrame(np.transpose(np.array([year, doy, 
                                                        df_aux['radiation,MJ/m2/day'],
                                                        df_aux['t2m_max,C'],
                                                        df_aux['t2m_min,C'],
                                                        df_aux['rainfall,mm/day']])))

    df_crop_model.to_csv(file_name, sep='\t', index=False, header=False, mode='a')
    return print('----- File has been built successfully! -----')


# # WOFOST

# In[32]:


def build_WOFOST_input_file(lat,lon):
    df_aux = pd.read_csv('weather_variables.csv',index_col=0)
    df_aux['Date'] = pd.to_datetime(df_aux['Date'])
    df_aux.set_index('Date',inplace = True)

    file_name = "WOFOST_input_file.txt"

# Write the header lines to the file
    with open(file_name, 'w') as file:
        file.write(f"*---------------------------------------------------------------------------*\n")
        file.write(f"* Station name: \n")
        file.write(f"* Year: \n")
        file.write(f"* Author: \n")
        file.write(f"* Source: \n")
        file.write(f"* (...)\n")
        file.write(f"*\n")
        file.write(f"** WCCDESCRIPTION=\n")
        file.write(f"** WCCFORMAT=\n")
        file.write(f"** WCCYEARNR=\n")
        #file.write(f"8536 LISBOA/PORTELA\n")
        file.write(f"*---------------------------------------------------------------------------*\n")
        file.write(f"{lon}\t {lat}\t ALT\t A\t B\n")

    doy = np.array([dt.timetuple().tm_yday for dt in df_aux.index],dtype = str)
    year = np.array(df_aux.index.year,dtype = str)
        #var = np.round(df[dict_var[input_var]].values,2)
        #if input_var == 5:
        #    var = var*1000
    station = ['1']*len(doy)

    df_crop_model = pd.DataFrame(np.transpose(np.array([station, year, doy, 
                                                        df_aux['radiation,MJ/m2/day'],
                                                        df_aux['t2m_min,C'],
                                                        df_aux['t2m_max,C'],
                                                        df_aux['vapor_pressure,kPa'],
                                                        df_aux['windspeed,m/s'],
                                                        df_aux['rainfall,mm/day']])))

    df_crop_model.to_csv(file_name, sep='\t', index=False, header=False, mode='a')
    return print('----- File has been built successfully! -----')


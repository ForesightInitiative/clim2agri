import requests
from netCDF4 import Dataset
#import wget
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


'''
from subprocess import Popen
from getpass import getpass
import platform
import os
import shutil

urs = 'urs.earthdata.nasa.gov'    # Earthdata URL to call for authentication
prompts = ['Enter NASA Earthdata Login Username \n(or create an account at urs.earthdata.nasa.gov): ',
           'Enter NASA Earthdata Login Password: ']

homeDir = os.path.expanduser("~") + os.sep +'CIMMYT/clim2agri'#os.path.expanduser("~") + os.sep

with open(homeDir + '.netrc', 'w') as file:
    file.write('machine {} login {} password {}'.format(urs, getpass(prompt=prompts[0]), getpass(prompt=prompts[1])))
    file.close()
with open(homeDir + '.urs_cookies', 'w') as file:
    file.write('')
    file.close()
with open(homeDir + '.dodsrc', 'w') as file:
    file.write('HTTP.COOKIEJAR={}.urs_cookies\n'.format(homeDir))
    file.write('HTTP.NETRC={}.netrc'.format(homeDir))
    file.close()

print('Saved .netrc, .urs_cookies, and .dodsrc to:', homeDir)

# Set appropriate permissions for Linux/macOS
if platform.system() != "Windows":
    Popen('chmod og-rw ~/.netrc', shell=True)
else:
    # Copy dodsrc to working directory in Windows  
    shutil.copy2(homeDir + '.dodsrc', os.getcwd())
    print('Copied .dodsrc to:', os.getcwd())
'''
    

def imerg(ini_date, fin_date, lat, lon):
    month_year_range = generate_month_year_range(ini_date, fin_date)
    days_array = [str(day).zfill(2) for day in range(1,32)]
    array_df = []    
    for i, month_year in enumerate(month_year_range):
        [month,year] = month_year.split('-')

        if i == 0:
            days = [str(day).zfill(2) for day in range(ini_date.day,32)]
        elif i == len(month_year_range)-1:
            days = [str(day).zfill(2) for day in range(1,fin_date.day+1)]
        else:
            dats = days_array

        for day in days:
            try:
                url = f'https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGDL.06/{year}/{month}/3B-DAY-L.MS.MRG.3IMERG.{year}{month}{day}-S000000-E235959.V06.nc4.nc4?HQprecipitation,time,lon,lat'

    #'https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3/GPM_3IMERGDL.06/2020/09/3B-DAY-L.MS.MRG.3IMERG.20200901-S000000-E235959.V06.nc4.html'
                # Set the FILENAME string to the data file name, the LABEL keyword value, or any customized name. 
                filename = f'IMERG_LATE_{year}_{month}_{day}.nc'

                result = requests.get(url)
                
                try:
                    result.raise_for_status()
                    f = open(filename,'wb')
                    f.write(result.content)
                    f.close()
                    #print('contents of URL written to '+filename)
                except:
                    print('requests.get() returned an error code '+str(result.status_code))


                imerg_nc = Dataset(filename)
                os.remove(filename)
                #imerg_time = pd.to_datetime(datetime(1970, 1, 1,0,0,0) + timedelta(days=int(days)) for days in imerg_nc['time'][:])

                imerg_time = pd.to_datetime(datetime(1970, 1, 1,0,0,0) + timedelta(days=int(imerg_nc['time'][:][0])))

                closest_index_lat = find_closest_index(imerg_nc['lat'][:], lat)
                closest_index_lon = find_closest_index(imerg_nc['lon'][:], lon)

                #df = pd.DataFrame([imerg_time,np.squeeze(np.array(imerg_nc['HQprecipitation'][:][0,closest_index_lon,closest_index_lat]))], 
                #         index = ['date','pp']).transpose().set_index('date')
                array_df.append([imerg_time,np.squeeze(np.array(imerg_nc['HQprecipitation'][:][0,closest_index_lon,closest_index_lat]))])
                #array_df.append(df)
            except:
                pass

    df = pd.DataFrame(array_df,columns = ['date','rainfall,mm/day']) 
    df.set_index(['date'],inplace = True)  
    df_final = df.loc[ini_date:fin_date]
    return df_final
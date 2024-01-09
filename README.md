![cgiar_cimmyt_logo](https://github.com/Fran-GS-96/clim2agri_test/assets/98550294/ffefef1f-3722-479e-a74d-b566f54384ee)

# clim2agri

## Table of Content

- [Configuring the Environment](#configuring-the-environment)
- [Access to Gridded Products](#access-to-gridded-products)
- [How to… ?](#how-to-)


##  Configuring the Environment 

In this section we show how to configure a python virtual environment in order to be able to run the code without any problem. For what follows you will need to have installed Python 3, and the pip package. The list of instructions are:

* Download:

Download and then decompress the folder.

* Create Virtual Environment:
  
Open the terminal and access the folder you have just decompressed. This can be accomplished with the ‘cd’ command followed by the path to the folder.

In order to create the virtual environment you should write the following command, where ‘name_of_env’ is an arbitrary name for the environment you are creating.

> python3 -m venv name_of_env

* Create Jupyter Kernel:
  
Depending on how you open jupyter notebook files it might be necessary to create a jupyter kernel as follows. We recommend running this code anyway.

> source name_of_env/bin/activate
> ipython kernel install --name name_of_env --user

* Installing necessary packages:
  
 Now we need to install all the needed packages for the code to run, which can be done with the following command.

> pip install -r requirements.txt

Now that the virtual environment is configured, you can open the jupyter notebook and start using it.

## Access to Gridded Products

You can already start using the jupyter notebook to download variables from some meteorological gridded products and to create input files. However, in order to download data from some products you need to follow some additional steps for which we will encourage you to follow from each product website.

* IMERG
  
In this case you need to create an account on the EarthData website. Afterwards, you should run the code ‘imerg.py,’ which is located in the compressed file. The code will ask you to provide your username and password. After running this code some folders will be created in your directory in order to access Imerg data.

* MSWEP and MSWX
  
Both MSWEP and MSWX require for you to create an account on their website so that they can share a drive folder with their data. Be aware that you need to follow the instructions in their website to have access through python and download the data through the Jupyter Notebook we provide.

The video referenced in the instructions is the following https://www.youtube.com/watch?v=vPs9K_VC-lg 

* AgERA5

In order to download data from AgERA5, first you will need to create an account on https://cds.climate.copernicus.eu/cdsapp#!/home and then create an API key so that you can have access through their API. All the instructions can be found on their website.


## How to… ? 

The jupyter notebook was made with the objective of being self-explanatory and without the need of running any other additional codes. Therefore, we consider the best way to learn how to use it is by following the steps provided in the jupyter notebook. Nevertheless, here we summarize the steps you need to accomplish in order to download data and/or create input files.
Creating weather_variables.csv File
This is the first step and is crucial. Without the weather_variables.csv file, you will not be able to run any of the codes below. In order to create this file there is a built-in function which is:

> create_empty_csv()

Once you run the line above, a new and empty .csv file will be created in your directory. Be aware that if you already have such a file and you run this function, then all the data that you might have will be erased.

The motivation for creating this file is twofold. The first one is to a place to save and for the user to see the data that is being downloaded. Plus, a .csv file is relatively easy to work with and perform additional analysis. The second motivation is that you might want to add data from other sources e.g. local meteorological stations, data from other reanalysis, etc. This can be done by simply pasting the data in the weather_variables.csv file; the only caveat is that the units of the variables should match the units shown in the corresponding column.
Downloading Data
To download data you just need to run the line:

> download_variable(ini_date,fin_date,lat,lon)

Where ini_date, and fin_date correspond to the initial and final date of the period you want to download the data, and lat and lon are the coordinates of the point of interest. 

After running the line above, a message will be deployed on your screen asking you to choose the variable you want to download. Once you select the variable, another message will appear asking you from which meteorological product you want to extract the particular variable you chose. Recall the data will be saved in the weather_variables.csv file.

You can download as many variables and from as many gridded meteorological products as you want, you just need to repeat the sequence just mentioned.
Creating Input Files
This is a straightforward step, you just need to run one of the following lines depending on the input file you want to generate. 

> build_APSIM_input_file(lat,lon)

> build_AQUACROP_input_file(lat,lon)

> build_CROPSYST_input_file(lat,lon)

> build_DSSAT_input_file(lat,lon)

> build_EPIC_input_file(lat,lon)

> build_ORIZA_input_file(lat,lon)

> build_STICS_input_file(lat,lon)

> build_WOFOST_input_file(lat,lon)

The input file generated will be a file containing the name of the crop model and with .txt extension. Therefore, you will need to change the name of the file and the extension before using it in the respective crop model.

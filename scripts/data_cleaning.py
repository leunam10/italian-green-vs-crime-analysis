"""

This script is used to clean the raw data and to produce the final csv files that are used for the analysis.
After the dataframes are cleaned some useful column are added:

- the GPS coordinates of the cities

"""

import pandas as pd 
import argparse
from geopy.geocoders import Nominatim
import os

pd.set_option("future.no_silent_downcasting", True)
######################################################################################################################################

# Argument Definition 
parser = argparse.ArgumentParser(
    prog = "Data cleaning script",
    description = "This script is used to clean the raw data and to produce the final csv files that are used for the analysis"
)

parser.add_argument("--dataset", choices = ["park", "crime"], help = "Type the dataset to clean [park/crime]")
parser.add_argument("--savefile", choices = ["yes", "no"], default="no", help = "if to save the cleaned file in the output directory [yes/no]")

args = parser.parse_args()
dataset = args.dataset
savefile = True if args.savefile == "yes" else False

######################################################################################################################################


## Functions ##
def park_clean_function(dataset_name, path_in):

    """
    
    This function is used to clean the raw park excel file and save distinct csv files

    """

    # read the raw park dataset: each sheet is a dataframe    
    # !! do not change the sheet_name, they are different because of wrong syntax among the sheets of the file !!
    df10_1 = pd.read_excel(os.path.join(path_in, dataset_name), sheet_name="Tav. 10.1  - verde urbano")
    df10_2 = pd.read_excel(os.path.join(path_in, dataset_name), sheet_name="Tav 10.2 - verde urbano ")
    df13_1 = pd.read_excel(os.path.join(path_in, dataset_name), sheet_name="Tav 13.1 - verde urbano ")
    df13_2 = pd.read_excel(os.path.join(path_in, dataset_name), sheet_name="Tav 13.2 - verde urbano ")

    df_list = [df10_1, df10_2, df13_1, df13_2]

    print("")
    # list where the cleaned df are saved
    df_clean_list = []
    # cycle over all the dataframes to clean
    for df in df_list:
        
        print(f"Dataset: {df.columns[0]}")
        print("Columns renaming")
        # change the name of the columns
        df.rename(columns={df.columns[0] : "cities",
                               "Unnamed: 1": "2011",
                               "Unnamed: 2": "2012",
                               "Unnamed: 3": "2013",
                               "Unnamed: 4": "2014",
                               "Unnamed: 5": "2015",
                               "Unnamed: 6": "2016",
                               "Unnamed: 7": "2017",
                               "Unnamed: 8": "2018",
                               "Unnamed: 9": "2019",
                               "Unnamed: 10": "2020",
                               "Unnamed: 11": "2021"}, inplace=True)
        print("Drop NaN")
        # remove NaN
        df.dropna(inplace=True)

        print("Cleaning header")
        # remove first row --> additional header (not useful after renaming)
        df.drop(index=1, inplace=True)

        print("Reset index")
        # reset index
        df.reset_index(drop=True, inplace=True)
        
        # removing white spaces from the name of the cities
        print("Stripping of the cities name")
        df["cities"] = df["cities"].str.strip()

        print("Cleaning specific values")
        # renaming some cities in the "cities" column
        df.replace({"cities" : {"Bolzano - Bozen " : "Bolzano",
                                "Bolzano - Bozen" : "Bolzano",
                                "Reggio nell'Emilia " : "Reggio Emilia",
                                "Reggio nell'Emilia" : "Reggio Emilia",
                                "Isernia (a)" : "Isernia",
                                "Isernia (b)" : "Isernia",
                                "Matera  (a)" : "Matera",
                                "Matera  (b)" : "Matera",
                                "Trapani (b)" : "Trapani",
                                "Matera (b)" : "Matera",
                                "Nord (*)" : "Nord",
                                "Nord (*)" : "Nord",
                                "Nord-ovest (*)" : "Nord-ovest",
                                "Nord-Ovest (*)" : "Nord-ovest",
                                "Nord-est (*)" : "Nord-est",
                                "Nord-Est (*)" : "Nord-est",
                                "Centro (*)" : "Centro",
                                "Centro (*)" : "Centro",
                                "Mezzogiorno (*)" : "Mezzogiorno",
                                "Mezzogiorno (*)" : "Mezzogiorno",
                                "Sud (*)" : "Sud",
                                "Sud (*)" : "Sud",
                                "Isole (*)" : "Isole",
                                "Isole (*)" : "Isole",
                                "Capoluoghi di città metropolitana " : "capoluoghi_di_citta_metropolitana",
                                "Capoluoghi di provincia (*)" : "capoluoghi_di_provincia",
                                "Capoluoghi di provincia (*)" : "capoluoghi_di_provincia",
                                "Italia (*)" : "Italia"}}, inplace=True)
        
        # replace not acceptable string (e.g. ….) with zeros
        print("Replacing non-acceptable strings")
        df["2011"] = df["2011"].replace("….",0)
        df["2012"] = df["2012"].replace("….",0)
        df["2013"] = df["2013"].replace("….",0)
        df["2014"] = df["2014"].replace("….",0)
        df["2015"] = df["2015"].replace("….",0)
        df["2016"] = df["2016"].replace("….",0)
        df["2017"] = df["2017"].replace("….",0)
        df["2018"] = df["2018"].replace("….",0)
        
        df_clean_list.append(df)
        print("")
    return df_clean_list

def crime_clean_function(dataset_name, path_in):
    
    """
    
    This function is used to clean the raw crime csv file and save it into a files

    """

    # read the raw dataset
    df = pd.read_csv(os.path.join(path_in, dataset_name))
    
    # removing columns
    df.drop(["ITTER107", "TIPO_DATO35", 
             "Tipo dato", "Flag Codes", 
             "Flags", "Seleziona periodo"], axis=1, inplace=True)

    # renaming columns
    df.rename(columns={"Territorio" : "cities",
                       "REATI_PS" : "crime_code",
                       "Tipo di delitto" : "felony",
                       "TIME" : "year",
                       "Value" : "count"}, inplace=True)


    return df

## Initialize Nominatim API
geolocator = Nominatim(user_agent="geo_city_park_and_crime")
def get_coordinates(city):
    try:
        location = geolocator.geocode(city)
        return location.latitude, location.longitude
    except:
        return None, None

def add_columns_to_park_df(df_list, path_out, savefile):

    for df in df_list:
        cities = df["cities"]
        for city in cities:
            lat, lon = get_coordinates(city)
            print(city, lat, lon)
        quit()
        
    if(savefile):
        print("Saving csv files")
        # save dataframe with the Density of urban green areas in provincial/metropolitan city capitals (Percentage incidence on the municipal area)
        df_list[0].to_csv(os.path.join(path_out, "urban_green_area_city_capitals_2011_2021_density.csv"), index=False)
        df_list[1].to_csv(os.path.join(path_out, "urban_green_area_city_capitals_2011_2021_m2.csv"), index=False)
        df_list[2].to_csv(os.path.join(path_out, "availability_of_usable_urban_green_space_city_capitals_2011_2021_m2_per_inhabitant.csv"), index=False)
        df_list[3].to_csv(os.path.join(path_out, "availability_of_usable_urban_green_space_city_capitals_2011_2021_m2.csv"), index=False)


def add_columns_to_crime_df(df, path_out, savefile):
    if(savefile):
        df.to_csv(os.path.join(path_out, "individuals_reported_and_arrested_or_detained_by_police_forces_2004_2022_ISTAT.csv"), index=False)
    


## Main ##

if(__name__ == "__main__"):
    # path where are saved the raw data
    path_in = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "data/raw"))

    # path where the cleaned data are saved
    path_out = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "data/clean"))
    # check if the 'clean' folder exists if not create the folder
    if(not os.path.isdir(path_out)):
        os.mkdir(path_out)

    # Change this filename if you have renamed the input files 
    park_dataset_filename = "urban_green_2011_2021_ISTAT.xlsx"
    crime_dataset_filename = "individuals_reported_and_arrested_or_detained_by_police_forces_2004_2022_ISTAT.csv"

    if(dataset == "park"):
        df_list = park_clean_function(park_dataset_filename, path_in)
        add_columns_to_park_df(df_list, path_out, savefile)
    elif(dataset == "crime"):
        df = crime_clean_function(crime_dataset_filename, path_in)
        add_columns_to_crime_df(df, path_out, savefile)



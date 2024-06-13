"""

This script is used to clean the raw data and to produce the final csv files that are used for the analysis

"""


import pandas as pd 
import argparse
import os


######################################################################################################################################

# Argument Definition 
parser = argparse.ArgumentParser(
    prog = "Data cleaning script",
    description = "This script is used to clean the raw data and to produce the final csv files that are used for the analysis"
)

parser.add_argument("--dataset", help = "Type the dataset to clean [park/crime]")
parser.add_argument("--savefile", default="yes", help = "if to save the cleaned file in the output directory [yes/no]")

args = parser.parse_args()
dataset = args.dataset
savefile = True if args.savefile == "yes" else False

######################################################################################################################################


## Functions ##
def park_clean_function(dataset_name, path_in, path_out, savefile):

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
                                "Nord (*)" : "North",
                                "Nord-ovest (*)" : "North-west",
                                "Nord-est (*)" : "North-east",
                                "Centro (*)" : "Center",
                                "Mezzogiorno (*)" : "Mezzogiorno",
                                "Sud (*)" : "South",
                                "Isole (*)" : "Island",
                                "Capoluoghi di città metropolitana " : "capital_cities",
                                "Capoluoghi di provincia (*)" : "provincial_capitals",
                                "Italia (*)" : "Italy"}}, inplace=True)
        
        # removing white spaces from the name of the cities
        print("Stripping of the cities name")
        df["cities"] = df["cities"].str.strip()
        print("")



    print("Saving csv files")
    if(savefile):
        # save dataframe with the Density of urban green areas in provincial/metropolitan city capitals (Percentage incidence on the municipal area)
        df_list[0].to_csv(os.path.join(path_out, "urban_green_area_density_in_city_capitals_2011_2021.csv"))
        df_list[1].to_csv(os.path.join(path_out, "urban_green_area_city_capitals_2011_2021_m2.csv"))
        df_list[2].to_csv(os.path.join(path_out, "availability_of_usable_urban_green_space_city_capitals_2011_2021_m2_per_inhabitant.csv"))
        df_list[3].to_csv(os.path.join(path_out, "availability_of_usable_urban_green_space_city_capitals_2011_2021_m2.csv"))


def crime_clean_function(dataset_name, path_in, path_out, savefile):
    
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

    if(savefile):
        df.to_csv(os.path.join(path_out, "individuals_reported_and_arrested_or_detained_by_police_forces_2004_2022_ISTAT_clean.csv"))

## Main ##

# path where are saved the raw data
path_in = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "data/raw"))

# path where the cleaned data are saved
path_out = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "data/clean"))

if(dataset == "park"):
    park_clean_function("urban_green_2011_2021_ISTAT.xlsx", path_in, path_out, savefile)
elif(dataset == "crime"):
    crime_clean_function("individuals_reported_and_arrested_or_detained_by_police_forces_2004_2022_ISTAT.csv", path_in, path_out, savefile)



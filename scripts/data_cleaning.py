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
def park_clean_function(path_in, path_out, savefile):

    """
    
    This function takes clean the raw park excel file and save distinct csv files

    """

    # read the raw park dataset: each sheet is a dataframe    
    # !! do not change the sheet_name, they are different because of wrong syntax among the sheets of the file !!
    df10_1 = pd.read_excel(os.path.join(path_in, "VERDE_URBANO_2011_2021_ISTAT.xlsx"), sheet_name="Tav. 10.1  - verde urbano")
    df10_2 = pd.read_excel(os.path.join(path_in, "VERDE_URBANO_2011_2021_ISTAT.xlsx"), sheet_name="Tav 10.2 - verde urbano ")
    df13_1 = pd.read_excel(os.path.join(path_in, "VERDE_URBANO_2011_2021_ISTAT.xlsx"), sheet_name="Tav 13.1 - verde urbano ")
    df13_2 = pd.read_excel(os.path.join(path_in, "VERDE_URBANO_2011_2021_ISTAT.xlsx"), sheet_name="Tav 13.2 - verde urbano ")

    # cleaning 'Tav. 10.1  - verde urbano' sheet
    # change the name of the columns
    df10_1.rename(columns={df10_1.columns[0] : "cities",
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
    # remove NaN
    df10_1.dropna(inplace=True)

    # remove first row --> additional header (not useful after renaming)
    df10_1.drop(index=1, inplace=True)
    
    # reset index
    df10_1.reset_index(drop=True, inplace=True)

    # renaming some cities in the "cities" column
    df10_1.replace({"cities" : {"Nord (*)" : "North",
                                "Nord-ovest (*)" : "North-west",
                                "Nord-est (*)" : "North-east",
                                "Centro (*)" : "Center",
                                "Mezzogiorno (*)" : "Mezzogiorno",
                                "Sud (*)" : "Sud",
                                "Isole (*)" : "Island",
                                "Capoluoghi di città metropolitana " : "capital_cities",
                                "Capoluoghi di provincia (*)" : "provincial_capitals",
                                "Italia (*)" : "Italy"}}, inplace=True)
    
    # cleaning 'Tav 10.2 - verde urbano '
    # change the name of the columns
    df10_2.rename(columns={df10_2.columns[0] : "cities",
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
 
    # remove NaN
    df10_2.dropna(inplace=True)

    # remove first row --> additional header (not useful after renaming)
    df10_2.drop(index=1, inplace=True)
    
    # reset index
    df10_2.reset_index(drop=True, inplace=True)

    # renaming some cities in the "cities" column
    df10_2.replace({"cities" : {"Nord (*)" : "North",
                                "Nord-ovest (*)" : "North-west",
                                "Nord-est (*)" : "North-east",
                                "Centro (*)" : "Center",
                                "Mezzogiorno (*)" : "Mezzogiorno",
                                "Sud (*)" : "Sud",
                                "Isole (*)" : "Island",
                                "Capoluoghi di città metropolitana " : "capital_cities",
                                "Capoluoghi di provincia (*)" : "provincial_capitals",
                                "Italia (*)" : "Italy"}}, inplace=True)

    # cleaning 'Tav 13.1 - verde urbano '
    # change the name of the columns
    df13_1.rename(columns={df13_1.columns[0] : "cities",
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
                           "Unnamed: 11": "2021"})

    # remove NaN
    df13_1.dropna(inplace=True)

    # remove first row --> additional header (not useful after renaming)
    df13_1.drop(index=1, inplace=True)
    
    # reset index
    df13_1.reset_index(drop=True, inplace=True)

    # renaming some cities in the "cities" column
    df13_1.replace({"cities" : {"Nord (*)" : "North",
                                "Nord-ovest (*)" : "North-west",
                                "Nord-est (*)" : "North-east",
                                "Centro (*)" : "Center",
                                "Mezzogiorno (*)" : "Mezzogiorno",
                                "Sud (*)" : "Sud",
                                "Isole (*)" : "Island",
                                "Capoluoghi di città metropolitana " : "capital_cities",
                                "Capoluoghi di provincia (*)" : "provincial_capitals",
                                "Italia (*)" : "Italy"}}, inplace=True)
#
    # cleaning 'Tav 13.2 - verde urbano '
    # change the name of the columns
    df13_2.rename(columns={df13_2.columns[0] : "cities",
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

    # remove NaN
    df13_2.dropna(inplace=True)

    # remove first row --> additional header (not useful after renaming)
    df13_2.drop(index=1, inplace=True)
    
    # reset index
    df13_2.reset_index(drop=True, inplace=True)

    # renaming some cities in the "cities" column
    df13_2.replace({"cities" : {"Nord (*) " : "North",
                                "Nord-Ovest (*) " : "North-west",
                                "Nord-Est (*) " : "North-east",
                                "Centro (*) " : "Center",
                                "Mezzogiorno (*) " : "Mezzogiorno",
                                "Sud (*) " : "Sud",
                                "Isole (*) " : "Island",
                                "Capoluoghi di città metropolitana " : "capital_cities",
                                "Capoluoghi di provincia (*) " : "provincial_capitals",
                                "Italia (*)" : "Italy"}}, inplace=True)

    if(savefile):
        # save dataframe with the Density of urban green areas in provincial/metropolitan city capitals (Percentage incidence on the municipal area)
        df10_1.to_csv(os.path.join(path_out, "urban_green_area_density_in_city_capitals.csv"))
        df10_2.to_csv(os.path.join(path_out, "test2.csv"))
        df13_1.to_csv(os.path.join(path_out, "test3.csv"))
        df13_2.to_csv(os.path.join(path_out, "test4.csv"))


def crime_clean_function(path_in, path_out, savefile):
    pass


## Main ##

# path where are saved the raw data
path_in = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "data/raw"))

# path where the cleaned data are saved
path_out = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "data"))

if(dataset == "park"):
    park_clean_function(path_in, path_out, savefile)
elif(dataset == "crime"):
    crime_clean_function(path_in, path_out, savefile)



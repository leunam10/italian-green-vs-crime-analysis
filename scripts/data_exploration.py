"""

This scipt is used to visualize the crime and park data. This is used as a first exploritory analysis to enhance possible relation or outliers

"""


import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sn
import argparse
import os

######################################################################################################################################
# CLI argument
parser = argparse.ArgumentParser(
    prog = "Data cleaning script",
    description = "This script is used to to visualize the crime and park data"
)

parser.add_argument("--dataset", choices = ["park", "crime", "both"], help="Type the dataset to clean [park/crime/both]")
parser.add_argument("--savefigure", choices = ["yes", "no"], default="no",  help = "if to save the figures in the output directory [yes/no]")

args = parser.parse_args()
dataset = args.dataset
savefigure = True if args.savefigure == "yes" else False

######################################################################################################################################

def green_park_barplot(dataset, year, figsize=(15,10), savefigure=False):
    """
    This function plots the green park availability for each city for a specific year as a barplot.
    """

    fig, ax = plt.subplots(figsize = figsize)
    dataset.plot.bar(x="cities", y=str(year),
                     edgecolor="k",
                     ax=ax)
    plt.show()



########
# MAIN #
########

# path where are stored the pre-processed park and crime datasets
path_in =  os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "data/clean"))

# path where the figures are saved if savefigure is True
path_figure =  os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "figures"))
# check if the 'figures' folder exists if not create the folder
if(not os.path.isdir(path_figure)):
    os.mkdir(path_figure)

################################################################################################################################################
# default input filenames [change here if the output are different from default]
urban_green_availability_m2_filename = "availability_of_usable_urban_green_space_city_capitals_2011_2021_m2.csv"
urban_green_availability_m2_per_inhabitant_filename = "availability_of_usable_urban_green_space_city_capitals_2011_2021_m2_per_inhabitant.csv"
urban_green_area_m2_filename = "urban_green_area_city_capitals_2011_2021_m2.csv"
urban_green_area_density_filename = "urban_green_area_city_capitals_2011_2021_density.csv"
crime_filename = "individuals_reported_and_arrested_or_detained_by_police_forces_2004_2022_ISTAT.csv"
################################################################################################################################################


# loading datasets
if(dataset == "park"):
    urban_green_availability_m2_df = pd.read_csv(os.path.join(path_in, urban_green_availability_m2_filename))
    urban_green_availability_m2_per_inhabitant_df = pd.read_csv(os.path.join(path_in, urban_green_availability_m2_per_inhabitant_filename))
    urban_green_area_m2_df = pd.read_csv(os.path.join(path_in, urban_green_area_m2_filename))
    urban_green_area_density = pd.read_csv(os.path.join(path_in, urban_green_area_density_filename))
elif(dataset == "crime"):
    crime_df = pd.read_csv(os.path.join(path_in, crime_filename))
elif(dataset == "both"):
    crime_df = pd.read_csv(os.path.join(path_in, crime_filename))
    urban_green_availability_m2_df = pd.read_csv(os.path.join(path_in, urban_green_availability_m2_filename))
    urban_green_availability_m2_per_inhabitant_df = pd.read_csv(os.path.join(path_in, urban_green_availability_m2_per_inhabitant_filename))
    urban_green_area_m2_df = pd.read_csv(os.path.join(path_in, urban_green_area_m2_filename))
    urban_green_area_density = pd.read_csv(os.path.join(path_in, urban_green_area_density_filename))


## PARK EXPLORATION ##
if(dataset == "park"):
    green_park_barplot(urban_green_availability_m2_df, 2020, figsize=(15,10), savefigure=savefigure)



## CRIME EXPLORATION ##

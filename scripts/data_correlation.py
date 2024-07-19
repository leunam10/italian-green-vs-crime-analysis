"""

This script is used to perform a statistical correlation analysis between the park and the crime dataset. 
The goal is to find a relation between the park presence and the felonies committed: specifically we 
expect to have a decrease of the felonies corresponding to an increase of the park count.

We can perform this analysis for all the italian provinces at once or for a specific province. At same 
time we can see if there are some specific felony that is more influenced by the precence of green areas.

"""


import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

# Argument Definition 
parser = argparse.ArgumentParser(
    prog = "Data correlation script",
    description = "This script is used study the statistical correlation between the park and crime datasets"
)

parser.add_argument("--park_path", default = "default", help = "Path where the park cleaned datasets are")
parser.add_argument("--crime_path", default = "default", help = "Path where the crime cleaned dataset is")
parser.add_argument("--park_dataset", choices = ["availability_m2", "availability_m2_per_inhabitant", "area_m2", "area_density"], default="availability_m2_per_inhabitant", help = "Type of park dataset")
parser.add_argument("--park_city", default = "all", help = "which city of the park dataset to consider (if all consider all the provinces as one)")
parser.add_argument("--crime_city", default = "all", help = "which city of the crime dataset to consider (if all consider all the provinces as one)")
parser.add_argument("--crime_felony", default = "all", help = "which felony of the crime dataset to consider (if all consider all the total felonies without distinguish the type)")
parser.add_argument("--normalization", choices = ["yes", "no"], default = "yes", help = "If to apply a min\max normalization to the data [yes or no]")

args = parser.parse_args()
park_path = args.park_path
crime_path = args.crime_path
park_dataset = args.park_dataset
park_city = args.park_city
crime_city = args.crime_city
crime_felony = args.crime_felony
normalization = True if args.normalization == "yes" else False


def park_crime_data_selection(park_df, crime_df, city, felony, normalization=True):
    
    """
    
    This function select the park and the crime dataframe by city and or felony

    """

    park_crime_dict = {"year" : [],
                       "city" : [],
                       "felony" : [],
                       "park_count" : [],
                       "crime_count": [],
                       "park_count_norm" : [],
                       "crime_count_norm" : []
                       }

    for year in park_df.columns:
        if(year!="cities"):
            park_crime_dict["city"].append(city)
            park_crime_dict["year"].append(str(year))
            park_crime_dict["felony"].append(felony)
            
            if(city == "all"):
                park_crime_dict["park_count"].append(park_df[str(year)].sum())
            else:
                park_crime_dict["park_count"].append(park_df.loc[park_df["cities"]==city][str(year)].iloc[0])

            if(felony == "all"):
                if(city == "all"):
                    park_crime_dict["crime_count"].append(crime_df.loc[crime_df["year"]==int(year)]["count"].sum())
                else:
                    park_crime_dict["crime_count"].append(crime_df.loc[(crime_df["cities"]==city) & (crime_df["year"]==int(year))]["count"].sum())
            else:
                if(city == "all"):
                    park_crime_dict["crime_count"].append(crime_df.loc[(crime_df["felony"]==felony) & (crime_df["year"]==int(year))]["count"].sum())
                else:
                    park_crime_dict["crime_count"].append(crime_df.loc[(crime_df["cities"]==city) & (crime_df["felony"]==felony) & (crime_df["year"]==int(year))]["count"].sum())

    if(normalization):
        for i in range(len(park_crime_dict["park_count"])):
            park_crime_dict["park_count_norm"].append((park_crime_dict["park_count"][i]-min(park_crime_dict["park_count"])) / (max(park_crime_dict["park_count"])-min(park_crime_dict["park_count"])))
            park_crime_dict["crime_count_norm"].append((park_crime_dict["crime_count"][i]-min(park_crime_dict["crime_count"])) / (max(park_crime_dict["crime_count"])-min(park_crime_dict["crime_count"])))


    park_crime_df = pd.DataFrame(park_crime_dict)

    return park_crime_df

def correlation_plot(park_df, crime_df, city, felony, method="pearson", normalization=True):

    """
    
    """
    corr_dict = {"city" : [],
                 "felony" : [],
                 "corr" : []}
    
    if(city == "each" and felony == "all"):
        for city in park_df["cities"].unique():
            park_crime_df = park_crime_data_selection(park_df, crime_df, city, "all")
            
            corr_dict["city"].append(city)
            corr_dict["felony"].append(felony)
            if(normalization):
                corr_dict["corr"].append(park_crime_df[["park_count_norm", "crime_count_norm"]].corr(method=method)["park_count_norm"]["crime_count_norm"])
            else:        
                corr_dict["corr"].append(park_crime_df[["park_count", "crime_count"]].corr(method=method)["park_count"]["crime_count"])

j
    corr_df = pd.DataFrame(corr_dict)
    return corr_df

if(__name__ == "__main__"):

    # filename of the cleaned dataset   
    if(park_dataset == "availability_m2"):
        park_filename = "availability_of_usable_urban_green_space_city_capitals_2011_2021_m2.csv"
    elif(park_dataset == "availability_m2_per_inhabitant"):
        park_filename = "availability_of_usable_urban_green_space_city_capitals_2011_2021_m2_per_inhabitant.csv"
    elif(park_dataset == "area_m2"):
        park_filename = "urban_green_area_city_capitals_2011_2021_m2.csv"
    elif(park_dataset == "area_density"):
        park_filename = "urban_green_area_city_capitals_2011_2021_density.csv"

    crime_filename = "individuals_reported_and_arrested_or_detained_by_police_forces_2004_2022_ISTAT.csv"


    # paths definition
    if(park_path == "default"):
        park_path_in = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "data/parks_and_crime/clean"))
    else:
        park_path_in =  os.path.join(os.path.abspath(""), os.path.join("..", park_path))

    if(crime_path == "default"):
        crime_path_in =  os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "data/parks_and_crime/clean"))
    else:
        crime_path_in =  os.path.join(os.path.abspath(""), os.path.join("..", crime_path))

    # load dataset as pd dataframe
    park_df = pd.read_csv(os.path.join(park_path_in, park_filename))
    crime_df = pd.read_csv(os.path.join(crime_path_in, crime_filename))


    correlation_plot(park_df, crime_df, "each", "all")
    quit()
        
#    for felony in crime_df["felony"].unique():
#        if(felony != "totale"):
#            park_crime_df = park_crime_data_selection(park_df, crime_df, "all", felony)
#            corr = park_crime_df[["park_count_norm", "crime_count_norm"]].corr()["park_count_norm"]["crime_count_norm"]
#            print(felony, corr)

for city in park_df["cities"].unique():
    for felony in crime_df["felony"].unique():
        
        park_crime_df = park_crime_data_selection(park_df, crime_df, "all", felony)
        corr = park_crime_df[["park_count_norm", "crime_count_norm"]].corr()["park_count_norm"]["crime_count_norm"]
        print(city, felony, corr)
   

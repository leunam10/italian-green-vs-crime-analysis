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

parser.add_argument("--city", default = "default", help = "which city to consider in the correlation")
parser.add_argument("--felony", default = "default", help = "which felony to consider for the correlation")
parser.add_argument("--park_path", default = "default", help = "Path where the park cleaned datasets are")
parser.add_argument("--crime_path", default = "default", help = "Path where the crime cleaned dataset is")
parser.add_argument("--path_out", default = "default", help = "path where files will be saved")
parser.add_argument("--park_dataset", choices = ["availability_m2", "availability_m2_per_inhabitant", "area_m2", "area_density"], default="availability_m2_per_inhabitant", help = "Type of park dataset")
parser.add_argument("--park_city", default = "all", help = "which city of the park dataset to consider (if all consider all the provinces as one)")
parser.add_argument("--crime_city", default = "all", help = "which city of the crime dataset to consider (if all consider all the provinces as one)")
parser.add_argument("--crime_felony", default = "all", help = "which felony of the crime dataset to consider (if all consider all the total felonies without distinguish the type)")
parser.add_argument("--normalization", choices = ["yes", "no"], default = "yes", help = "If to apply a min\max normalization to the data [yes or no]")
parser.add_argument("--save_corr", choices=["yes", "no"], default = "yes", help = "If to save of not the correlation file to use it")
parser.add_argument("--load_corr", choices=["yes", "no"], default = "yes", help = "If to load a previously computed correlation file")
parser.add_argument("--corr_filename", default = "corr_df.csv", help = "choose the name of the correlation output file")
parser.add_argument("--corr_fig_filename", default = "correlation", help = "choose the name of the correlation figure")

args = parser.parse_args()
city = args.city
felony = args.felony
park_path = args.park_path
crime_path = args.crime_path
path_out = args.path_out
park_dataset = args.park_dataset
park_city = args.park_city
crime_city = args.crime_city
crime_felony = args.crime_felony
normalization = True if args.normalization == "yes" else False
save_corr = True if args.save_corr == "yes" else False
load_corr = True if args.load_corr == "yes" else False
corr_filename = args.corr_filename
corr_fig_filename = args.corr_fig_filename

if(save_corr):
    load_corr = False


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

def compute_correlation(park_df, crime_df, city, felony, method="pearson", normalization=True):

    """
    
    This function returns the correlation dataframe for different combinations of city and felonies

    """
    
    corr_dict = {"city" : [],
                 "felony" : [],
                 "corr" : []}
    
    if(city == "each"):
        for city in park_df["cities"].unique():

            corr_dict["city"].append(city)
            corr_dict["felony"].append(felony)

            park_crime_df = park_crime_data_selection(park_df, crime_df, city, felony)
            
            if(normalization):
                corr_dict["corr"].append(park_crime_df[["park_count_norm", "crime_count_norm"]].corr(method=method)["park_count_norm"]["crime_count_norm"])
            else:        
                corr_dict["corr"].append(park_crime_df[["park_count", "crime_count"]].corr(method=method)["park_count"]["crime_count"])

    elif(felony == "each"):
        for felony in crime_df["felony"].unique():
            if(felony != "totale"):
    
                corr_dict["city"].append(city)
                corr_dict["felony"].append(felony)
    
                park_crime_df = park_crime_data_selection(park_df, crime_df, city, felony)
                if(normalization):
                    corr_dict["corr"].append(park_crime_df[["park_count_norm", "crime_count_norm"]].corr(method=method)["park_count_norm"]["crime_count_norm"])
                else:
                    corr_dict["corr"].append(park_crime_df[["park_count", "crime_count"]].corr(method=method)["park_count"]["crime_count"])

    elif(city == "each" and felony == "each"):
        for city in park_df["cities"].unique():
            for felony in crime_df["felony"].unique():
                corr_dict["city"].append(city)
                corr_dict["felony"].append(felony)

                park_crime_df = park_crime_data_selection(park_df, crime_df, city, felony)

                if(normalization): 
                    corr_dict["corr"].append(park_crime_df[["park_count_norm", "crime_count_norm"]].corr(method=method)["park_count_norm"]["crime_count_norm"])
                else:
                    corr_dict["corr"].append(park_crime_df[["park_count", "crime_count"]].corr(method=method)["park_count"]["crime_count"])

    elif(city == "all" and felony == "all"):
        corr_dict["city"].append(city)
        corr_dict["felony"].append(felony)
        park_crime_df = park_crime_data_selection(park_df, crime_df, city, felony)

        if(normalization):
            corr_dict["corr"].append(park_crime_df[["park_count_norm", "crime_count_norm"]].corr(method=method)["park_count_norm"]["crime_count_norm"])
        else:
            corr_dict["corr"].append(park_crime_df[["park_count", "crime_count"]].corr(method=method)["park_count"]["crime_count"])


    corr_df = pd.DataFrame(corr_dict)

    return corr_df


def plot_correlation(corr_df,
                     city,
                     felony,
                     pdf=False, 
                     figname="correlation", 
                     path_out=os.path.join(os.path.abspath(""), os.path.join("..", "figures")),
                     figsize=(20,20)):

    """

    This function plots the correlation coefficient as a bar plot

    """

    # check if the figure folder exists. If not create it
    if(not os.path.isdir(path_out)):
        os.mkdir(path_out)

    threshold_1 = 0.6
    threshold_2 = 0.8
    threshold_3 = 0.9

    colors = []
    for value in corr_df["corr"]:
        if(value >= threshold_1 and value < threshold_2 or value <= -threshold_1 and value > -threshold_2):
            colors.append("green")
        elif(value >= threshold_2 and value < threshold_3 or value <= -threshold_2 and value > -threshold_3):
            colors.append("orange")
        elif(value >= threshold_3 or value <= -threshold_3):
            colors.append("red")
        else:
            colors.append("grey")

    fig, ax = plt.subplots(figsize=figsize)

    if(city == "all" and felony == "all"):
        ax.set_title("Correlation between the aggragation of all cities and all felonies")
        x = "city"
    elif(city == "each" and felony != "all" or felony != "each"):
        ax.set_title("Correlation for all the cities and "+felony)
        x = "city"
    elif(city != "all" and city != "each" or felony == "each"):
        ax.set_title("Correlation between all the felonies for "+city)
        x = "felony"
    elif(city == "each" and felony == "all"):
        ax.set_title("Correlation for each of the cities with the aggregation of the felonies")
        x = "city"
    elif(city == "all" and felony == "each"):
        ax.set_title("Correlation for each of the felony with the aggregation of the cities")
        x = "felony"

    corr_df.plot.barh(x=x, y="corr", 
                      edgecolor="k", color=colors, 
                      grid=True, 
                      legend=False, 
                      ax=ax)

    ax.set_xlim([-1.1, 1.1])
    ax.set_xlabel("Correlation coefficient")
    ax.set_ylabel("Cities")
    ax.set_axisbelow(True)

    plt.savefig(os.path.join(path_out, figname+".png"))
    if(pdf):
        plt.savefig(os.path.join(path_out, figname+".pdf"))

    plt.close()

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

    if(path_out == "default"):
        path_out_final = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join("..", "output"))
    else:
        path_out_finale =  os.path.join(os.path.abspath(""), os.path.join("..", path_out))


    if(load_corr):
        if(path_out == "default"):  
            corr_df = pd.read_csv(os.path.join("../output", corr_filename))
        else:
            corr_df = pd.read_csv(os.path.join(path_out, corr_filename))

    else:
        # load dataset as pd dataframe
        park_df = pd.read_csv(os.path.join(park_path_in, park_filename))
        crime_df = pd.read_csv(os.path.join(crime_path_in, crime_filename))

        corr_df = compute_correlation(park_df, crime_df, city, felony)

    if(save_corr):
        if(not os.path.isdir(path_out_final)):
            os.mkdir(path_out_final)
        corr_df.to_csv(os.path.join(path_out_final, corr_filename))

    #plot_correlation(corr_df, city, felony, figname=corr_fig_filename)    
   
    if(city == "each" and felony == "all"):
        for city in corr_df["city"].unique():
            plot_correlation(corr_df, city, felony, figname="corr_"+city+"_all_felonies")    

    if(felony == "each" and city == "all"):
        for felony in corr_df["felony"].unique():
            plot_correlation(corr_df, city, felony, figname="corr_"+felony+"_all_cities")    

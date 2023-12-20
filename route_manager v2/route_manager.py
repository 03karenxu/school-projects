#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 8 14:44:33 2023
Based on: https://www.kaggle.com/datasets/arbazmohammad/world-airports-and-airlines-datasets
Sample input: --AIRLINES="airlines.yaml" --AIRPORTS="airports.yaml" --ROUTES="routes.yaml" --QUESTION="q1" --GRAPH_TYPE="bar"
@author: rivera
@author: karenx
"""

import sys
import csv
import yaml
import pandas as pd
import matplotlib.pyplot as plt

def diff(val1: str, val2: str) -> float:
    """Returns the absolute value of val1 - val2
    """
    return abs(float(val1) - float(val2))


def addstr(str1: str, str2: str) -> str:
    """Documentation
    """
    return str1 + "-" + str2


def get_args() -> list:
    """Returns a list of strings where each element is an input argument.
            Parameters
            ----------
                None

            Returns
            -------
                list[str]
                    List of strings where each string is an argument.
    """
    temp = []
    input = sys.argv

    if len(input) != 6:
        print("Insufficient number of arguments. Sample input:")
        print("--AIRLINES=\"airlines.yaml\" --AIRPORTS=\"airports.yaml\" --ROUTES=\"routes.yaml\" --QUESTION=\"q1\" --GRAPH_TYPE=\"bar\"")
        sys.exit(1)  # Exit with an error code

    else:
        airlines = get_info(input[1])
        airports = get_info(input[2])
        routes = get_info(input[3])
        question = get_info(input[4])
        graph_type = get_info(input[5])
    
        temp.append(airlines)
        temp.append(airports)
        temp.append(routes)
        temp.append(question)
        temp.append(graph_type)
    
    return temp


def get_info(input_str: str) -> str:
    """Returns only the useful information from the input argument.
            Parameters
            ----------
                input_str : str, required
                    The argument as given.

            Returns
            -------
                str
                    The information extracted from the argument.
    """
    info = input_str.split("=")
    return info[1]
 
  
def yaml_to_pandas(filename: str, data_type: str) -> pd.DataFrame:
    """Takes the info from a YAML file and loads it to a pandas dataframe.
            Parameters
            ----------
                filename : str, required
                    The filename
                data_type: str, required
                    Type of data stored in file

            Returns
            -------
                pd.Dataframe
                The dataframe created from the YAML file.
    """
    f = open(filename, "r")
    data = yaml.load(f, Loader = yaml.Loader)
    list_data = data.get(data_type)
    df = pd.DataFrame.from_dict(list_data)
    f.close()
    
    return df


def merge_df(airlines_df: pd.DataFrame, 
             airports_df: pd.DataFrame, 
             routes_df: pd.DataFrame) -> pd.DataFrame:
    """Returns the top 20 airlines that offer the greatest number of 
    routes with destination country as Canada.
            Parameters
            ----------
                airlines_df : pandas dataframe, required
                    A pandas dataframe containing airline information.
                airports_df : pandas dataframe, required
                    A pandas dataframe containing airport information.
                routes_df : pandas dataframe, required
                    A pandas dataframe containing route information.

            Returns
            -------
                pandas dataframe
                    A pandas dataframe merging all 3 input dataframes.
    """
    merged1_df = pd.merge(airlines_df,
                          routes_df,
                          left_on = "airline_id",
                          right_on = "route_airline_id")
    
    merged2_df = pd.merge(merged1_df,
                          airports_df,
                          left_on = "route_to_airport_id",
                          right_on = "airport_id")
    
    return merged2_df


def df_to_list(df: pd.DataFrame, key_name: str) -> list:
    """Returns a specific column in a pandas dataframe as a list
            Parameters
            ----------
                df : pandas dataframe
                    Dataframe containing desired information
                key_name : str
                    name of column to be returned as a list

            Returns
            -------
                list
                    a list containing each element in the specified column
    """    
    result_dict = df.to_dict()
    result_list = []
    for key in result_dict[key_name]:
        result_list.append(result_dict[key_name][key])
    return result_list


def q1(airlines_df: pd.DataFrame, 
       airports_df: pd.DataFrame, 
       routes_df: pd.DataFrame) -> pd.DataFrame:
    """Returns the top 20 airlines that offer the greatest number of 
    routes with destination country as Canada.
            Parameters
            ----------
                airlines_df : pandas dataframe, required
                    A pandas dataframe containing airline information.
                airports_df : pandas dataframe, required
                    A pandas dataframe containing airport information.
                routes_df : pandas dataframe, required
                    A pandas dataframe containing route information.

            Returns
            -------
                pandas dataframe
                    A pandas dataframe containing the result.
    """
    merged_df = merge_df(airlines_df, airports_df, routes_df)
    
    merged_df.drop(["airline_id",
                    "airport_id",
                    "route_airline_id",
                    "route_to_airport_id",
                    "route_from_aiport_id",
                    "airline_country",
                    "airport_city",
                    "airport_icao_unique_code",
                    "airport_name", "airport_altitude"],
                   inplace = True,
                   axis = 1)
    
    canadian = merged_df[merged_df["airport_country"] == "Canada"]
    
    grouped = canadian.groupby(["airline_name","airline_icao_unique_code"],
                               as_index = False).size()
    
    answer = grouped.sort_values(by=["size", "airline_name"],
                                        ascending = [False, True]).head(20)
    
    return answer

def q2(airports_df: pd.DataFrame, routes_df: pd.DataFrame) -> pd.DataFrame:
    """Returns the top 30 countries with least appearances as 
    destination country on the routes data
            Parameters
            ----------
                airports_df : pandas dataframe, required
                    A pandas dataframe containing airport information.
                routes_df : pandas dataframe, required
                    A pandas dataframe containing route information.

            Returns
            -------
                pandas dataframe
                    A pandas dataframe containing the result.
    """
    merged_df = pd.merge(airports_df,
                         routes_df,
                         left_on = "airport_id",
                         right_on = "route_to_airport_id")
    
    merged_df.drop(["airport_id",
                    "route_to_airport_id",
                    "airport_city",
                    "airport_icao_unique_code",
                    "airport_name",
                    "airport_altitude",
                    "route_from_aiport_id",
                    "route_airline_id"], inplace = True, axis = 1)
    
    merged_df["airport_country"] = merged_df["airport_country"].str.replace(" ",
                                                                            "_")
    
    grouped = merged_df.groupby("airport_country", as_index = False).size()
    
    answer = grouped.sort_values(by=["size", "airport_country"]).head(30)
    
    answer["airport_country"] = answer["airport_country"].str.replace("_", " ")
    
    return answer


def q3(airports_df: pd.DataFrame, routes_df: pd.DataFrame) -> None:
    """Returns the top 10 destination airports.
            Parameters
            ----------
                airports_df : pandas dataframe, required
                    A pandas dataframe containing airport information.
                routes_df : pandas dataframe, required
                    A pandas dataframe containing route information.

            Returns
            -------
                pandas dataframe
                    A pandas dataframe containing the result.
    """
    merged_df = pd.merge(airports_df,
                         routes_df,
                         left_on = "airport_id",
                         right_on = "route_to_airport_id")
    
    merged_df.drop(["airport_id",
                    "route_to_airport_id",
                    "airport_altitude",
                    "route_from_aiport_id",
                    "route_airline_id"],
                   inplace = True,
                   axis = 1)
    
    merged_df["airport_name"] = merged_df["airport_name"].str.replace(" ", "_")
    
    grouped = merged_df.groupby(["airport_name",
                                 "airport_city",
                                 "airport_country",
                                 "airport_icao_unique_code"],
                                as_index = False).size()
    
    answer = grouped.sort_values(by=["size", "airport_name"],
                                 ascending = [False, True]).head(10)
    
    answer["airport_name"] = answer["airport_name"].str.replace("_", " ")
    
    return answer

def q4(airports_df: pd.DataFrame, routes_df: pd.DataFrame) -> None:
    """Returns the top 15 destination cities.
            Parameters
            ----------
                airports_df : pandas dataframe, required
                    A pandas dataframe containing airport information.
                routes_df : pandas dataframe, required
                    A pandas dataframe containing route information.

            Returns
            -------
                pandas dataframe
                    A pandas dataframe containing the result.
    """
    merged_df = pd.merge(airports_df,
                         routes_df,
                         left_on = "airport_id",
                         right_on = "route_to_airport_id")
    
    merged_df.drop(["airport_id",
                    "route_to_airport_id",
                    "route_from_aiport_id",
                    "route_airline_id",
                    "airport_name",
                    "airport_altitude",
                    "airport_icao_unique_code"],
                   inplace = True,
                   axis = 1)
    
    merged_df["airport_city"] = merged_df["airport_city"].str.replace(" ", "_")
    
    grouped = merged_df.groupby(["airport_city", "airport_country"],
                                as_index = False).size()
    
    answer = grouped.sort_values(by=["size", "airport_city"],
                                 ascending = [False, True]).head(15)
    
    answer["airport_city"] = answer["airport_city"].str.replace("_", " ")
    
    return answer


def q5(airports_df: pd.DataFrame, routes_df: pd.DataFrame) -> None:
    """Returns the top 10 unique Canadian routes with most difference between
       the destination altitude and the origin altitude?
            Parameters
            ----------
                airports_df : pandas dataframe, required
                    A pandas dataframe containing airport information.
                routes_df : pandas dataframe, required
                    A pandas dataframe containing route information.

            Returns
            -------
                pandas dataframe
                    A pandas dataframe containing the result.
    """
    merged_df = pd.merge(airports_df,
                         routes_df,
                         left_on = "airport_id",
                         right_on = "route_to_airport_id")
    
    merged_df = pd.merge(airports_df,
                         merged_df,
                         left_on = "airport_id",
                         right_on = "route_from_aiport_id")
    
    merged_df = merged_df.rename(columns=
                      {"airport_icao_unique_code_x":"src_icao",
                       "airport_altitude_x":"src_altitude",
                       "airport_icao_unique_code_y":"dest_icao",
                       "airport_altitude_y":"dest_altitude"})
    
    merged_df["altitude_diff"] = merged_df.apply(lambda x:
                                                 diff(x["dest_altitude"],
                                                      x["src_altitude"]),
                                                 axis=1)
    
    canadian = merged_df[merged_df["airport_country_x"] == "Canada"]
    canadian = canadian[canadian["airport_country_y"] == "Canada"]
    
    answer = canadian.sort_values(by=["altitude_diff"],
                                 ascending = False).head(10)
    
    answer["route"] = answer.apply(lambda x:addstr(x["src_icao"],
                                                   x["dest_icao"]), axis=1)
    
    answer.drop(["src_icao",
                 "dest_icao",
                 "route_to_airport_id",
                 "airport_id_x",
                 "airport_id_y",
                 "route_from_aiport_id",
                 "dest_altitude",
                 "src_altitude",
                 "airport_country_x",
                 "airport_country_y",
                 "route_airline_id"], inplace = True, axis = 1)
    
    return answer

def q1_csv(df: pd.DataFrame) -> None:
    """Writes the data to q1.csv
            Parameters
            ----------
                df : pandas dataframe
                    dataframe containing answer to q1

            Returns
            -------
                None
    """  
    airlines = df_to_list(df, "airline_name")
    icao = df_to_list(df, "airline_icao_unique_code")
    size = df_to_list(df, "size")
    
    f = open("q1.csv", "w")
    
    f.write("subject,statistic\n")
    for i in range(len(airlines)):
        line = airlines[i] + " (" + icao[i] + "),"+ str(size[i]) + "\n"
        f.write(line)
        
    f.close()


def q2_csv(df: pd.DataFrame) -> None:
    """Writes the data to q2.csv
            Parameters
            ----------
                df : pandas dataframe
                    dataframe containing answer to q2

            Returns
            -------
                None
    """      
    countries = df_to_list(df, "airport_country")
    size = df_to_list(df, "size")
    
    f = open("q2.csv", "w")
    
    f.write("subject,statistic\n")
    for i in range(len(countries)):
        line = countries[i] + ","+ str(size[i]) + "\n"
        f.write(line)
        
    f.close()


def q3_csv(df: pd.DataFrame) -> None:
    """Writes the data to q3.csv
            Parameters
            ----------
                df : pandas dataframe
                    dataframe containing answer to q3

            Returns
            -------
                None
    """  
    names = df_to_list(df, "airport_name")
    icao = df_to_list(df, "airport_icao_unique_code")
    cities = df_to_list(df, "airport_city")
    countries = df_to_list(df, "airport_country")
    size = df_to_list(df, "size")
    
    f = open("q3.csv", "w")
    
    writer = csv.writer(f)
    
    f.write("subject,statistic\n")
    for i in range(len(names)):
        subject = names[i]+" ("+icao[i]+"), "+cities[i]+", "+countries[i]
        writer.writerow([subject, str(size[i])])
        
    f.close()

    
def q4_csv(df: pd.DataFrame) -> None:
    """Writes the data to q4.csv
            Parameters
            ----------
                df : pandas dataframe
                    dataframe containing answer to q4

            Returns
            -------
                None
    """  
    cities = df_to_list(df, "airport_city")
    countries = df_to_list(df, "airport_country")
    size = df_to_list(df, "size")
    
    f = open("q4.csv", "w")
    
    writer = csv.writer(f)
    
    f.write("subject,statistic\n")
    for i in range(len(cities)):
        subject = cities[i]+", "+countries[i]
        writer.writerow([subject, str(size[i])])
        
    f.close()
    

def q5_csv(df: pd.DataFrame) -> None:
    """Writes the data to q5.csv
            Parameters
            ----------
                df : pandas dataframe
                    dataframe containing answer to q5

            Returns
            -------
                None
    """  
    routes = df_to_list(df, "route")
    diffs = df_to_list(df, "altitude_diff")
    
    f = open("q5.csv", "w")
    
    f.write("subject,statistic\n")
    for i in range(len(routes)):
        f.write(routes[i]+","+str(diffs[i])+"\n")
        
    f.close()
    
    
def pie(df: pd.DataFrame,
        filename: str,
        my_title: str,
        to_plot: str,
        as_labels : str) -> None:
    """Outputs a pie chart to a pdf given a pandas dataframe.
            Parameters
            ----------
                df : pandas dataframe
                    dataframe containing data to be output to graph
                filename : str
                    name of pdf file to be written to
                my_title : str
                    title of pie chart
                to_plot : str
                    name of column to be plotted
                labels : str
                    name of column to be used as labels

            Returns
            -------
                None
    """
    my_labels = df_to_list(df, as_labels)
    data = df_to_list(df, to_plot)
    num_elements = len(my_labels)
    
    if num_elements > 20:
        cols = 2
        bbox = (2.25, 0.4)
    else:
        cols = 1
        bbox = (2,0.5)
    
    f = open(filename, "w")
    
    plt.pie(data, labels = my_labels, textprops = {'fontsize' : 4.5})
    plt.title(my_title)
    plt.savefig(filename)
    
    f.close()

def bar(df: pd.DataFrame,
        filename: str,
        my_title: str,
        categories: str,
        values: str,
        x_label: str,
        y_label: str) -> None:
    """Outputs a bar graph to a pdf given a pandas dataframe.
            Parameters
            ----------
                df : pandas dataframe
                    dataframe containing data to be output to graph
                filename : str
                    name of pdf file to be written to
                my_title : str
                    title of bar graph
                categories : str
                    name of column to be used for x-axis
                values : str
                    name of column to be used for y-axis
                x_label : str
                    title of x-axis
                y_label
                    title of y-axis

            Returns
            -------
                None
    """
    x_axis = df_to_list(df, categories)
    y_axis = df_to_list(df, values)
    
    f = open(filename, "w")

    plt.bar(x_axis, y_axis)
    plt.subplots_adjust(bottom = 0.4)
    plt.xticks(rotation = 'vertical', fontsize = "x-small")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(my_title)
    plt.savefig(filename)
    
    f.close()    
    
def main():
    """Main entry point of the program."""
    args = get_args()
    
    airlines_df = yaml_to_pandas(args[0], "airlines")
    airports_df = yaml_to_pandas(args[1], "airports")
    routes_df = yaml_to_pandas(args[2], "routes")

    # case 1:
    if args[3] == "q1":
        result = q1(airlines_df, airports_df, routes_df)
        q1_csv(result)
        
        if args[4] == "pie":
            pie(result,
                "q1.pdf",
                "Top 20 Airlines with Routes to Canada",
                "size",
                "airline_name")
        elif args[4] == "bar":
            bar(result,
                "q1.pdf",
                "Top 20 Airlines with Routes to Canada",
                "airline_name",
                "size",
                "Airlines",
                "# Routes to Canada")
    
    # case 2:
    elif args[3] == "q2":
        result = q2(airports_df, routes_df)
        q2_csv(result)
        
        if args[4] == "pie":
            pie(result, "q2.pdf",
                "Top 30 Countries with Least\nAppearances as Destinations",
                "size",
                "airport_country")          
        elif args[4] == "bar":
            bar(result,
                "q2.pdf",
                "Top 30 Countries with Least Appearances as Destinations",
                "airport_country",
                "size",
                "Destination Countries",
                "# Times Appeared as Destination")
    # case 3:   
    elif args[3] == "q3":
        result = q3(airports_df, routes_df)
        q3_csv(result)
        
        if args[4] == "pie":
            pie(result,
                "q3.pdf",
                "Top 10 Destination Airports",
                "size",
                "airport_name")
        elif args[4] == "bar":
            bar(result,
                "q3.pdf",
                "Top 10 Destination Airports",
                "airport_name",
                "size",
                "Airports",
                "# Times Appeared as Destination") 
    
    # case 4:
    elif args[3] == "q4":
        result = q4(airports_df, routes_df)
        q4_csv(result)
        
        if args[4] == "pie":
            pie(result,
                "q4.pdf",
                "Top 15 Destination Cities",
                "size",
                "airport_city")
        elif args[4] == "bar":
            bar(result,
                "q4.pdf",
                "Top 15 Destination Cities",
                "airport_city",
                "size",
                "Cities",
                "# Times Appeared as Destination")        
    else:
        result = q5(airports_df, routes_df)
        q5_csv(result)
        if args[4] == "pie":
            pie(result,
                "q5.pdf",
                "Top 10 Canadian Routes with\n the Most Difference in Altitude",
                "altitude_diff",
                "route")
        elif args[4] == "bar":
            bar(result,
                "q5.pdf",
                "Top 10 Canadian Routes with\n the Most Difference in Altitude",
                "route",
                "altitude_diff",
                "Routes",
                "Altitiude Difference")


if __name__ == '__main__':
    main()

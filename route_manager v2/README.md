**README**

**Date completed: March 7th, 2023**
Assignment for software engingeering course. Exercise in python data analysis using pandas, and how matplotlib can be used to generate graphs. 

Requires 3 yaml files in the same directory, containing the route, airline, and airport information. Files must be formatted as the given example files are.

**TO RUN:**

    $ python route_manager.py --AIRLINES="<yaml file>" --AIRPORTS="<yaml file>" --ROUTES="<yaml file>" --QUESTION="<q1-q5>" --GRAPH_TYPE="<bar/pie>"

Note: <> denotes a placeholder. Eg. Replace <yaml file> with routes.yaml
* QUESTION accepts qi, 1 <= i <= 5
* GRAPH_TYPE accepts either pie or bar

**OUTPUT:**

For each question, outputs 2 files:
* a qi.csv file containing a table with the result statistics
* a qi.pdf file containing a graph (of specified type) representing the result statistics.

1) What are the top 20 airlines with routes to Canada?
2) What are the top 30 countries with least appearances as destinations?
3) What are the top 10 destination airports?
4) What are the top 15 destination cities?
5) What are the top 10 Canadian routes with the most difference in altitude from source to destination?

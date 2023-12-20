README.txt

Assignment for a software engineering course. Exercise in c programming and csv data analysis. 

Requires a csv file in the same directory which contains a list of airline routes, formatted as the example csv file "airline-routes-data.csv" is formatted.

To compile:

    $ gcc route_manager.c -o route_manager

To run:

    Program can be run in one of the following ways:

    Note: <> denotes a placeholder, eg. Replace <airline code> with ETH for Ethiopian Airlines

    1) $ ./route_manager --DATA="<csv file>" --AIRLINE="<airline code>" --DEST_COUNTRY="<country name>"`

    2) $ ./route_manager --DATA="<csv file>" --SRC_COUNTRY="<country name>" --DEST_CITY="<city name>" --DEST_COUNTRY="<country name>"
    
    3) $ ./route_manager --DATA="<csv file>" --SRC_CITY="<city name>" --SRC_COUNTRY="<country name>" --DEST_CITY="<city name>" --DEST_COUNTRY="<country name>"

Output:

    Writes a txt file (output.txt) to the same directory with airline routes based on the input given:

    In case 1): Gives all routes to the destination country offered by the given airline

    It specifies:
        - the origin (airport icao, city and country)
        - the destination (airport name, icao, and city).
    
    In case 2): Gives all routes from the source country to the destination city.

    It specifies:
        - the airline offering the route (name and code)
        - the source airport from which it departs (airport name, icao, and city).

    In case 3): Gives all routes from the source city to the destination city.

    It specifies:
        - the airline offering the route (name and code)
        - the route (in form source icao-destination icao)

    If no routes can be found given the input, the output.txt filecontains only "NO RESULTS FOUND."
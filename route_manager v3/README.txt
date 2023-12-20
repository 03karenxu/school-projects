README.txt

To compile:

    $ make

To run:

    Note: <> denotes a placeholder. Eg. <yaml file> is replaced by routes-airlines-airports.yaml (yaml file
    must be of same format as given yaml file).

    $ ./route_manager --DATA="<yaml file>" --QUESTION=<num> --N=<num>

    The question number corresponds to three questions that the program can answer:

    1) What are the top N airlines that offer the greatest number of routes with the destination country as Canada?

    2) What are the top N countries with the least appearances as the destination country in the routes data?

    3) What are the top N destination airports?

    Where N is the number specified in the input.

README.txt

To run:

    Note: <> denotes a placeholder. Eg. Replace <yaml file> with routes.yaml
        - QUESTION accepts qi, 1 <= i <= 5
        - GRAPH_TYPE accepts either pie, or bar

    > python route_manager.py --AIRLINES="<yaml file>" --AIRPORTS="<yaml file>" --ROUTES="<yaml file>" --QUESTION="<q1-q5>" --GRAPH_TYPE="<bar/pie>"

Output:

    For each question, outputs 2 files:
        - a qi.csv file containing a table with the result statistics
        - a qi.pdf file containing a graph (of specified type) representing the result statistics.

    q1) What are the top 20 airlines with routes to Canada?
    q2) What are the top 30 countries with least appearances as destinations?
    q3) What are the top 10 destination airports?
    q4) What are the top 15 destination cities?
    q5) What are the top 10 Canadian routes with the most difference in altitude
        from source to destination?
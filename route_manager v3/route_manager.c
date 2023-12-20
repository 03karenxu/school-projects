/** @file route_manager.c
 *  @brief A small program to analyze airline routes data.
 *  @author Mike Z.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Jose O.
 *  @author Saasha J.
 *  @author Victoria L.
 *  @author Karen Xu
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list.h"

// TODO: Make sure to adjust this based on the input files given
#define MAX_LINE_LEN 80

/**
 * @brief Serves as an incremental counter for navigating the list.
 *
 * @param p The pointer of the node to print.
 * @param arg The pointer of the index.
 *
 */
void inccounter(node_t *p, void *arg)
{
    int *ip = (int *)arg;
    (*ip)++;
}

/**
 * @brief Allows to print out the content of a node.
 *
 * @param p The pointer of the node to print.
 * @param arg The format of the string.
 *
 */
void print_node(node_t *p, void *arg)
{
    char *fmt = (char *)arg;
    if (p->next != NULL) {
	printf(fmt, p->subject, p->statistic, p->next->subject);
    }
}

/**
 * @brief Allows to print each node in the list.
 *
 * @param l The first node in the list
 *
 */
void analysis(node_t *l)
{
    int len = 0;

    apply(l, inccounter, &len);
    printf("Number of words: %d\n", len);

    apply(l, print_node, "%s, %i\n");
}

/**
 * @brief opens a yaml file
 * 
 * @param ifp, the file to be read
 * @return FILE*
 * 
 */
FILE* open_file(char *filename) {
    FILE* ifp = fopen(filename, "r");
    if (ifp != NULL) {
        return ifp;
    } else {
        return NULL;
    }
}

/**
 * @brief opens a yaml file
 * 
 * @param ifp, the file to be read
 * @return FILE*
 * 
 */
void output(node_t* list, int amount) {
    node_t *curr = NULL;
    int count = 0;
    char line[MAX_LINE_LEN];
    
    FILE* ofp = fopen("output.csv", "w");
    fputs("subject,statistic\n", ofp);
    
    curr = list;
    while (curr != NULL && count < amount) {
	sprintf(line,"\"%s\",%i\n", curr->subject, curr->statistic);
	fputs(line, ofp);
	count++;
	curr = curr->next;
    }
    
    fclose(ofp);
}

/**
 * @brief returns only the useful information of a line
 * 
 * @param line - the full line as given in the yaml file
 * @return 
 * 
 */
char* get_info(char *line) {
    char* info = strtok(line, ":\n");
    info = strtok(NULL, ":\n");
    if (info[0] == ' ' ) info++;
    if (strcmp(info, "' Sheffield'") == 0){
	info = "Sheffield";
    } else if (strcmp(info, "' Santiago Island'") == 0){
	info = "Santiago Island";
    }

    return info;
}


/**
 * @brief returns only the useful information of a line
 * 
 * @param line - the full line as given in the yaml file
 * @return 
 * 
 */
char* get_arg(char *argv[], int arg_index){
    char* arg = strtok(argv[arg_index], "=");
    arg = strtok(NULL, "=");
    return arg;
}


/**
 * @brief determines whether a node is in the list or not.
 * 
 * @param list - pointer to the first node in the list to be searched
	  searched - subject to search for in list
 * @return pointer to the searched node if found, null otherwise
 * 
 */
node_t* find_in_list(node_t *list, char *searched){
    node_t *curr = list;
    while (curr!= NULL) {
	if (strcmp(curr->subject, searched) == 0) {
	    return curr;
	}
	curr = curr->next;
    }
    
    return NULL;
}

/**
 * @brief What are the top N airlines that offer the greatest number of routes
          with destination country as Canada?
 * 
 * @param airline_name - name of route airline
          airline_icao_unique_code - icao code of route airline
	  to_airport_country - route destination country
	  list - pointer to first node in linked list
 * @return pointer to first node in result list
 * 
 */
node_t* q1(char *airline_name,
        char *airline_icao_unique_code,
        char *to_airport_country,
	node_t* list) {

	char *subject = NULL;
	subject = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
	sprintf(subject,"%s (%s)", airline_name, airline_icao_unique_code);
	    
	if (strcmp(to_airport_country,"Canada") == 0) {
	    if (find_in_list(list, subject) != NULL) {
		find_in_list(list,subject)->statistic++;
	    } else {
		list = add_front(list, new_node(subject, 1));
	    }
	    
	}
	free(subject);
	return list;
}

/**
 * @brief What are the top N countries with least appearances as destination
	  country on the routes data?
 * 
 * @param to_airport_country - route destination country
	  list - pointer to first node in list
 * @return pointer to first node in result list
 * 
 */
node_t* q2(char *to_airport_country, node_t* list) {

	char *subject = NULL;
	subject = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
	sprintf(subject,"%s", to_airport_country);
	    
	if (find_in_list(list, subject) != NULL) {
	    find_in_list(list,subject)->statistic++;
	} else {
	    list = add_front(list, new_node(subject, 1));
	}
	free(subject);
	return list;
}


/**
 * @brief What are the top N destination airports?
 * 
 * @param to_airport_name - route destination airport name
	  to_airport_icao_unique_code - route destination icao code
	  to_airport_city - route destination city
	  to_airport_country - route destination country
	  list - pointer to first node in list
 * @return pointer to first node in result list
 * 
 */
node_t* q3(char *to_airport_name,
	   char *to_airport_icao_unique_code,
	   char *to_airport_city,
	   char *to_airport_country,
	   node_t* list) {

	char *subject = NULL;
	subject = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
	sprintf(subject,
	        "%s (%s), %s, %s",
		to_airport_name,
		to_airport_icao_unique_code,
		to_airport_city,
		to_airport_country);
	    
	if (find_in_list(list, subject) != NULL) {
	    find_in_list(list,subject)->statistic++;
	} else {
	    list = add_front(list, new_node(subject, 1));
	}
	free(subject);
	return list;
}


/**
 * @brief sorts a linked list in either ascending or descending order
 * 
 * @param list - pointer to first node in the original list
	  question - number of the question given as a command line argument
 * @return pointer to the first node in the sorted list
 * 
 */
node_t* sort_data(node_t *list, int question){
    node_t *sorted_list = NULL;
    node_t *curr = NULL;
    
    for (curr=list; curr!=NULL; curr=curr->next) {
	if (question == 2) {
	    sorted_list = add_inorder_desc(sorted_list,
					   new_node(curr->subject,
						    curr->statistic));
	} else {
	    sorted_list = add_inorder(sorted_list,
				  new_node(curr->subject, curr->statistic));
	}
    }

    return sorted_list;
}

/**
 * @brief processes the given route data based on which question is asked
 * 
 * @param airline_name - name of the route airline
          airline_icao_unique_code - icao code of the route airline
	  airline_country - country of route airline
	  from_airport_name - name of route's source airport
	  from_airport_city - city of route's source airport
	  from_airport_country - country of route's source airport
	  from_airport_icao_unique_code - icao code of route's source airport
	  from_airport_altitude - altitude of route's source airport
	  to_airport_name - name of route's destination airport
	  to_airport_city - city of route's destination airport
	  to_airport_country - country of route's destination airport
	  to_airport_icao_unique_code - icao code of route's destination airport
	  to_airport_altitude - altitude of route's destination airport
	  question - question number asked
	  list - pointer to first node in list
	  
 * @return pointer to first node in linked list with the result information
 * 
 */
node_t* process_data(char *airline_name,
                  char *airline_icao_unique_code,
                  char *airline_country,
                  char *from_airport_name,
                  char *from_airport_city,
                  char *from_airport_country,
                  char *from_airport_icao_unique_code,
                  char *from_airport_altitude,
                  char *to_airport_name,
                  char *to_airport_city,
                  char *to_airport_country,
                  char *to_airport_icao_unique_code,
                  char *to_airport_altitude,
                  int question,
		  node_t *list) {
        
          
    if (question == 1) {
        list = q1(airline_name,
		  airline_icao_unique_code,
		  to_airport_country,
		  list);
    } else if (question == 2) {
        list = q2(to_airport_country, list);
    } else {
        list = q3(to_airport_name,
		  to_airport_icao_unique_code,
		  to_airport_city,
		  to_airport_country,
		  list);
    }
    
    return list;
}


/**
 * @brief reads a yaml file
 * 
 * @param filename, the file to be read
 * @return 
 * 
 */
node_t* read_file(char *filename, int question, node_t *list) {
    
    FILE* ifp = open_file(filename);
     
    char *line = NULL;
    line = (char *)malloc(sizeof(char) * MAX_LINE_LEN);

    char *airline_name;
    char *airline_icao_unique_code;
    char *airline_country;
    char *from_airport_name;
    char *from_airport_city;
    char *from_airport_country;
    char *from_airport_icao_unique_code;
    char *from_airport_altitude;
    char *to_airport_name;
    char *to_airport_city;
    char *to_airport_country;
    char *to_airport_icao_unique_code;
    char *to_airport_altitude;
    
    fgets(line, MAX_LINE_LEN, ifp);
    
    char line2[MAX_LINE_LEN];
    char line3[MAX_LINE_LEN];
    char line4[MAX_LINE_LEN];
    char line5[MAX_LINE_LEN];
    char line6[MAX_LINE_LEN];
    char line7[MAX_LINE_LEN];
    char line8[MAX_LINE_LEN];
    char line9[MAX_LINE_LEN];
    char line10[MAX_LINE_LEN];
    char line11[MAX_LINE_LEN];
    char line12[MAX_LINE_LEN];
    char line13[MAX_LINE_LEN];

    while (fgets(line, MAX_LINE_LEN, ifp) != NULL) {

        if (line[0] == '-') {
            airline_name = get_info(line);
            
            fgets(line2, MAX_LINE_LEN, ifp);
            airline_icao_unique_code = get_info(line2);
            
            fgets(line3, MAX_LINE_LEN, ifp);
            airline_country = get_info(line3);
            
            fgets(line4, MAX_LINE_LEN, ifp);
            from_airport_name = get_info(line4);
            
            fgets(line5, MAX_LINE_LEN, ifp);
            from_airport_city = get_info(line5);
            
            fgets(line6, MAX_LINE_LEN, ifp);
            from_airport_country = get_info(line6);
            
            fgets(line7, MAX_LINE_LEN, ifp);
            from_airport_icao_unique_code = get_info(line7);
            
            fgets(line8, MAX_LINE_LEN, ifp);
            from_airport_altitude= get_info(line8);
            
            fgets(line9, MAX_LINE_LEN, ifp);
            to_airport_name = get_info(line9);
            
            fgets(line10, MAX_LINE_LEN, ifp);
            to_airport_city = get_info(line10);
            
            fgets(line11, MAX_LINE_LEN, ifp);
            to_airport_country = get_info(line11);
            
            fgets(line12, MAX_LINE_LEN, ifp);
            to_airport_icao_unique_code = get_info(line12);
            
            fgets(line13, MAX_LINE_LEN, ifp);
            to_airport_altitude= get_info(line13);
            
            list = process_data(airline_name,
				airline_icao_unique_code,
				airline_country,
				from_airport_name,
				from_airport_city,
				from_airport_country,
				from_airport_icao_unique_code,
				from_airport_altitude,
				to_airport_name,
				to_airport_city,
				to_airport_country,
				to_airport_icao_unique_code,
				to_airport_altitude,
				question,
				list);
				
        }
	
        
    }
    
    free(line);

    return list;   
}


/**
 * @brief The main function and entry point of the program.
 *
 * @param argc The number of arguments passed to the program.
 * @param argv The list of arguments passed to the program.
 * @return int 0: No errors; 1: Errors produced.
 *
 */
int main(int argc, char *argv[])
{   
    node_t *list = NULL;
    char *filename = get_arg(argv, 1);
    int question = atoi(strtok(get_arg(argv, 2), "="));
    int amount = atoi(strtok(get_arg(argv, 3), "="));
    
    list = read_file(filename, question, list);
    list = sort_data(list, question);
    
    output(list, amount);

    node_t *temp_n = NULL;
    for (; list != NULL; list = temp_n)
    {
        temp_n = list->next;
        free(list->subject);
        free(list);
    }
     
}
/** @file route_manager.c
 *  @brief A pipes & filters program that uses conditionals, loops, and string processing tools in C to process airline routes.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Jose O.
 *  @author Saasha J.
 *  @author Victoria L.
 *  @author Karen Xu
 *
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_STRING_LENGTH 100
#define MAX_LINE_LENGTH 200
#define MAX_AIRLINE_NAMES 100

// store command-line arguments
struct Arg {
    char data[MAX_STRING_LENGTH];
    char airline[MAX_STRING_LENGTH];
    char src_city[MAX_STRING_LENGTH];
    char src_country[MAX_STRING_LENGTH];
    char dest_city[MAX_STRING_LENGTH];
    char dest_country[MAX_STRING_LENGTH];
} input;

// store fields from the input file
struct Fields {
    char airline_name[MAX_STRING_LENGTH];
    char airline_icao[MAX_STRING_LENGTH];
    char airline_country[MAX_STRING_LENGTH];
    char src_airport[MAX_STRING_LENGTH];
    char src_city[MAX_STRING_LENGTH];
    char src_country[MAX_STRING_LENGTH];
    char src_airport_icao[MAX_STRING_LENGTH];
    float src_altitude;
    char dest_airport[MAX_STRING_LENGTH];
    char dest_city[MAX_STRING_LENGTH];
    char dest_country[MAX_STRING_LENGTH];
    char dest_airport_icao[MAX_STRING_LENGTH];
    float dest_altitude;
} fline;

char airline_name[MAX_AIRLINE_NAMES][MAX_STRING_LENGTH];

// extract information from command-line arguments
char* obtainInfo(int index, char *argv[])
{
    char* info = strtok(argv[index], "=");
    info = strtok(NULL, "=");
    return (info);
}

// obtain command-line arguments
struct Arg obtainArg(int argc, char *argv[])
{
    struct Arg input;

    char* data = obtainInfo(1, argv);
    strcpy(input.data, data);

    if (argc == 4)
    {
        char* airline = obtainInfo(2, argv);
        strcpy(input.airline, airline);

        char* dest_country = obtainInfo(3, argv);
        strcpy(input.dest_country, dest_country);

    }

    if (argc == 5)
    {
        char* src_country = obtainInfo(2, argv);
        strcpy(input.src_country, src_country);

        char* dest_city = obtainInfo(3, argv);
        strcpy(input.dest_city, dest_city);

        char* dest_country = obtainInfo(4, argv);
        strcpy(input.dest_country, dest_country);

    }

    if (argc == 6)
    {
        char* src_city = obtainInfo(2, argv);
        strcpy(input.src_city, src_city);

        char* src_country = obtainInfo(3, argv);
        strcpy(input.src_country, src_country);

        char* dest_city = obtainInfo(4, argv);
        strcpy(input.dest_city, dest_city);

        char* dest_country = obtainInfo(5, argv);
        strcpy(input.dest_country, dest_country);

    }

    return input;
}

// open file for reading
FILE* openFile(char* filename) {

    FILE* ifp = fopen(filename, "r");
    if (ifp != NULL) {
        return ifp;
    } else {
        return NULL;
    }
}

// open output file
FILE* outputFile() {
    FILE *ofp = fopen("output.txt", "w");

    fclose(ofp);
    return ofp;
}

// process a line from the input file
char* processLine(struct Arg input, char* line, int argc) {
    struct Fields fline;
    
    char *token = strtok(line, ",");
    strncpy(fline.airline_name, token, MAX_STRING_LENGTH);

    token = strtok(NULL, ",");
    if (token != NULL){
        strncpy(fline.airline_icao, token, MAX_STRING_LENGTH);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        strncpy(fline.airline_country, token, MAX_STRING_LENGTH);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        strncpy(fline.src_airport, token, MAX_STRING_LENGTH);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        strncpy(fline.src_city, token, MAX_STRING_LENGTH);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        strncpy(fline.src_country, token, MAX_STRING_LENGTH);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        strncpy(fline.src_airport_icao, token, MAX_STRING_LENGTH);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        fline.src_altitude = atof(token);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        strncpy(fline.dest_airport, token, MAX_STRING_LENGTH);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        strncpy(fline.dest_city, token, MAX_STRING_LENGTH);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        strncpy(fline.dest_country, token, MAX_STRING_LENGTH);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        strncpy(fline.dest_airport_icao, token, MAX_STRING_LENGTH);
    }

    token = strtok(NULL, ",");
    if (token != NULL){
        fline.dest_altitude = atof(token);
    }

    char* target = (char*)malloc(200 * sizeof(char));

    if (argc == 4) {
        if (strcmp(input.airline, fline.airline_icao) == 0 && strcmp(input.dest_country, fline.dest_country) == 0) {
            strncpy(airline_name[0], fline.airline_name, MAX_STRING_LENGTH); 
            sprintf(target, "FROM: %s, %s, %s TO: %s (%s), %s\n", fline.src_airport_icao, fline.src_city, fline.src_country, fline.dest_airport, fline.dest_airport_icao, fline.dest_city);
            return target;
        }
    }

    if (argc == 5) {
        if (strcmp(input.src_country, fline.src_country) ==0 && strcmp(input.dest_city, fline.dest_city)==0 && strcmp(input.dest_country, fline.dest_country) == 0) {
            sprintf(target, "AIRLINE: %s (%s) ORIGIN: %s (%s), %s\n", fline.airline_name, fline.airline_icao, fline.src_airport, fline.src_airport_icao, fline.src_city);
            return target;
        }
    }

    if (argc == 6) {
        if (strcmp(input.src_city, fline.src_city) ==0 && strcmp(input.src_country, fline.src_country) ==0 && strcmp(input.dest_city, fline.dest_city)==0 && strcmp(input.dest_country, fline.dest_country) == 0) {
            sprintf(target, "AIRLINE: %s (%s) ROUTE: %s-%s\n", fline.airline_name, fline.airline_icao, fline.src_airport_icao, fline.dest_airport_icao);
            return target;
        }
    }

    return NULL;
}

// read the input file and write results to the output file
void readFile(struct Arg input, char* filename, int argc) {


    FILE* ifp = openFile(filename);
    FILE* ofp = fopen("output.txt", "w");

    char line[MAX_LINE_LENGTH];
    fgets(line, MAX_LINE_LENGTH, ifp);
    char* result;
    char matches[MAX_STRING_LENGTH][MAX_STRING_LENGTH];
    int i = 0;
    
    while (fgets(line, MAX_LINE_LENGTH, ifp) != NULL) {
        result = processLine(input,line, argc);
        if (result!=NULL) {
            strcpy(matches[i], result);
            free(result);
            i++;
        }

    }

    if (i == 0) {
        fputs("NO RESULTS FOUND.", ofp);
    } else {
        if (argc == 4){

            char header1[MAX_STRING_LENGTH];
            int j = 0;
            sprintf(header1, "FLIGHTS TO %s BY %s (%s):\n", input.dest_country, airline_name[0], input.airline);
            fputs(header1, ofp);
            while (j < i){
                fputs(matches[j], ofp);
                j++;
            }
        }
        if (argc == 5){
            char header2[MAX_STRING_LENGTH];
            int k = 0;
            sprintf(header2, "FLIGHTS FROM %s TO %s, %s:\n", input.src_country, input.dest_city, input.dest_country);
            fputs(header2, ofp);
            while (k < i) {
                fputs(matches[k], ofp);
                k++;
            }
        }

        if (argc == 6) {
            char header3[MAX_STRING_LENGTH];
            int l = 0;
            sprintf(header3, "FLIGHTS FROM %s, %s TO %s, %s:\n", input.src_city, input.src_country, input.dest_city, input.dest_country);
            fputs(header3, ofp);
            while (l<i) {
                fputs(matches[l], ofp);
                l++;
            }
        }
    }


    fclose(ifp);
    fclose(ofp);
    
}

/**
 * Function: main
 * --------------
 * @brief The main function and entry point of the program.
 *
 * @param argc The number of arguments passed to the program.
 * @param argv The list of arguments passed to the program.
 * @return int 0: No errors; 1: Errors produced.
 *
 */

int main(int argc, char *argv[])
{
  char* output_str;
  struct Arg input = obtainArg(argc, argv);
  readFile(input, input.data, argc);

}
    

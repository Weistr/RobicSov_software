#include <stdio.h>
#include <stdlib.h>
#include "search.h"

int kociembaSolve(int argc, char *argv)
{
    printf("\npgmstart\n");
    if (argc > 1) {
        char patternized[64];
        char* facelets = argv;
        /*
        if (argc > 2) {
            patternize(facelets, argv[2], patternized);
            facelets = patternized;
        }*/
        char *sol = solution(
            facelets,
            24,
            1000,
            0,
            "cache"
        );
        if (sol == NULL) {
            puts("Unsolvable cube!");
            return 2;
        }
        puts(sol);
        free(sol);
        return 0;
    } else {
        return 1;
    }    
}

int main(int argc, char **argv)
{
    printf("please enter the cube state\n");
    char inStr[128]={0};
    scanf("%s",&inStr);\
    printf("get:");
    for (int i = 0; i < 60; i++)
    {
        printf("%c",inStr[i]);
    }
    kociembaSolve(2,"UUUUUUUUUBBBRRRRRRRRRFFFFFFDDDDDDDDDFFFLLLLLLLLLBBBBBB");
}

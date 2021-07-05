#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
    char password[50];
    char passwordKey[50];
    scanf("%s", password);
    
    if (strlen(password) > 9 && password[5] == '.')
    {
        int passwordLength = strlen(password);
        srand(passwordLength);
        for(int i = 0; i < passwordLength; i++)
        {
            passwordKey[i] = password[i] + rand() % passwordLength - passwordLength/2;
        }
        passwordKey[passwordLength] = 0;
        puts(passwordKey);
    }
    else
    {
        printf("Password is invalid! Password length is at least 10 and 6th character is \".\"");
    }
}
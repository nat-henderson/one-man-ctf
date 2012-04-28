#include <stdio.h>
#include <stdlib.h>
#include <sys/utsname.h>


typedef char* (*strFunc)();
struct utsname unameData;
struct methodlist {
	strFunc public[3];
	strFunc private;
};

char* myrandom() {
	char* result;
	asprintf(&result, "%d",rand());
	return result;
}

char* helloWorld() {
	return "Hello, World";
}

char* printInfo() {
	char* result;
	uname(&unameData);
	asprintf(&result,"%s",unameData.sysname);
	return result;
}

char* readPassword() {
	printf("running password\n");
	FILE* file = fopen("../level08/password.txt","r");
	printf("file open\n");
	char* passwd = (char*)malloc(sizeof(char) * 50); 
	fscanf(file, "%s",passwd);
	return passwd;
}

int main(int argv, char** argc) {
	if(argv == 1) {
		printf("Usage: enter a number from 0 to 2 (inclusive)\n");
		printf("to run one of our basic functions\n");
	} else {
		int val = atoi(argc[1]);
		
		struct methodlist m;
		m.public[0] = helloWorld;
		m.public[1] = myrandom;
		m.public[2] = printInfo;
		m.private = readPassword;

		printf("%s\n",m.public[val]());
	}
	return 0;
}


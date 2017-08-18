#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int modify(FILE *in, char *entry) {
	char buff[80];
	int entryLen = strlen(entry);
	for (int i = 0 ; i < entryLen ; i++)
		buff[i] = entry[i];
	buff[entryLen++] = ':';
	while (entryLen < 79) {
		buff[entryLen++] = ' ';
	}
	buff[79] = '\n';
	fwrite(buff, 1, 80, in);

	return 0;
}

int main(int argc, char *argv[]) {
	FILE *in;

	if(argc!=3) {
		fprintf(stderr, "Usage: %s <out_filename> <input>\n", argv[0]);
    	exit(1);
    } else {
    	if ((in= fopen(argv[1], "w"))==NULL) {
    	fprintf(stderr, "Couldn't write to '%s'\n", argv[1]);
        exit(1);
    	}
    	modify(in, argv[2]);
		fclose(in);
    }
	return 0;
}

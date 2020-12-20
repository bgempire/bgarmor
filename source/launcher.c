#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_BUFFER_LENGTH 512
#define COMMAND_BUFFER_LENGTH 2048
#define COMMON_FILE_PATH "./launcher/common.txt"

#ifdef _WIN32
	#define COMMAND_PREFIX "ECHO OFF && "
#elif defined(__unix__)
	#define COMMAND_PREFIX ""
#endif

typedef struct {
	char pythonExecutable[LINE_BUFFER_LENGTH];
	char launcherScript[LINE_BUFFER_LENGTH];
} Common;

void copyStringChunk(char* source, char* target, const char from, const char to) {
	int started = 0;

	while (*source != from && *source != '\0')
		source++;

	if (*source == from)
		started = 1;

	while (started && *source != '\0') {
		*target = *source;
		target++;
		source++;

		if (*source == to) {
			*target = *source;
			target++;
			*target = '\0';
			started = 0;
		}
	}
}

void getPathFromCommon(Common* common) {
	FILE* filePointer = fopen(COMMON_FILE_PATH, "r");
	char buffer[LINE_BUFFER_LENGTH];

	while(fgets(buffer, LINE_BUFFER_LENGTH, filePointer)) {

		if (strstr(buffer, "PYTHON_EXECUTABLE") != NULL) {
			copyStringChunk(buffer, common->pythonExecutable, '"', '"');
		}
		else if (strstr(buffer, "LAUNCHER_SCRIPT") != NULL) {
			copyStringChunk(buffer, common->launcherScript, '"', '"');
		}
	}
	fclose(filePointer);
}

int main() {
	Common common;
	char command[COMMAND_BUFFER_LENGTH];
	
	getPathFromCommon(&common);
	printf("Python path: %s\nLauncher script path: %s\n\n", common.pythonExecutable, common.launcherScript);
	
	strcat(command, COMMAND_PREFIX);
	strcat(command, common.pythonExecutable);
	strcat(command, " ");
	strcat(command, common.launcherScript);
	
	system(command);
}

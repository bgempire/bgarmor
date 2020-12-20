#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_BUFFER_LENGTH 512
#define COMMAND_BUFFER_LENGTH 2048

#ifdef _WIN32
	#define COMMON_FILE_PATH "./launcher/Windows/common.txt"
	#define COMMAND_PREFIX "ECHO OFF && "
	#define DEFAULT_QUOTE "\""
#elif defined(__unix__)
	#define COMMON_FILE_PATH "./launcher/Linux/common.txt"
	#define COMMAND_PREFIX ""
	#define DEFAULT_QUOTE "'"
#endif

const char* DEFAULT_LAUNCHER_SCRIPT = "./launcher/launcher_min.py";
const char* FALLBACK_LAUNCHER_SCRIPT = "./launcher/launcher.py";

typedef struct {
	char pythonExecutable[LINE_BUFFER_LENGTH];
	char launcherScript[LINE_BUFFER_LENGTH];
} Common;

void copyStringChunk(char* source, char* target, const char from, const char to) {
	int started = 0;
	
	while (*source != from && *source != '\0') {
		source++;
		if (*source == from) {
			started = 1;
			source++;
			break;
		}
	}
	while (started && *source != '\0' && *source != to) {
		*target = *source;
		target++;
		source++;

		if (*source == to) {
			*target = '\0';
			started = 0;
		}
	}
}

void getPathFromCommon(Common* common) {
	FILE* filePointer = fopen(COMMON_FILE_PATH, "r");
	char buffer[LINE_BUFFER_LENGTH];

	while(fgets(buffer, LINE_BUFFER_LENGTH, filePointer) != NULL) {
		if (strstr(buffer, "PYTHON_EXECUTABLE") != NULL)
			copyStringChunk(buffer, common->pythonExecutable, '"', '"');
	}
	fclose(filePointer);
	filePointer = NULL;
	filePointer = fopen(DEFAULT_LAUNCHER_SCRIPT, "r");
	
	if (filePointer) {
		strcpy(common->launcherScript, DEFAULT_LAUNCHER_SCRIPT);
		fclose(filePointer);
	}
	else {
		strcpy(common->launcherScript, FALLBACK_LAUNCHER_SCRIPT);
	}
}

int main() {
	Common common;
	char command[COMMAND_BUFFER_LENGTH];
	
	// Cleanup strings
	strcpy(common.launcherScript, "");
	strcpy(common.pythonExecutable, "");
	
	getPathFromCommon(&common);
	printf("Python path: %s\nLauncher script path: %s\n\n", common.pythonExecutable, common.launcherScript);
	
	strcat(command, COMMAND_PREFIX);
	strcat(command, DEFAULT_QUOTE);
	strcat(command, common.pythonExecutable);
	strcat(command, DEFAULT_QUOTE);
	strcat(command, " ");
	strcat(command, DEFAULT_QUOTE);
	strcat(command, common.launcherScript);
	strcat(command, DEFAULT_QUOTE);
	
	system(command);
}

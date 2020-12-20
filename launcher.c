#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_BUFFER_LENGTH 512
#define COMMAND_BUFFER_LENGTH 2048
#define DEFAULT_LAUNCHER_SCRIPT "./launcher/launcher_min.py"
#define FALLBACK_LAUNCHER_SCRIPT "./launcher/launcher.py"

#ifdef _WIN32
	#define COMMON_FILE_PATH "./launcher/Windows/common.txt"
	#define COMMAND_PREFIX "ECHO OFF && "
#elif defined(__unix__)
	#define COMMON_FILE_PATH "./launcher/Linux/common.txt"
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
	
	if (strcmp(common->launcherScript, "\"\"") == 0) {
		if (filePointer = open(DEFAULT_LAUNCHER_SCRIPT, "r") != NULL) {
			strcpy(common->launcherScript, DEFAULT_LAUNCHER_SCRIPT);
		}
		else {
			strcpy(common->launcherScript, FALLBACK_LAUNCHER_SCRIPT);
		}
		fclose(filePointer);
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
	strcat(command, common.pythonExecutable);
	strcat(command, " ");
	strcat(command, common.launcherScript);
	
	system(command);
}

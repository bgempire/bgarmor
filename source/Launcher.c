#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_BUFFER_LENGTH 512
#define COMMAND_BUFFER_LENGTH 2048

#ifdef _WIN32
    #ifdef _WIN32_WINNT
        #undef _WIN32_WINNT
    #endif
    #define _WIN32_WINNT 0x0500
    #include <windows.h>
    const char* COMMON_FILE_PATH = "./launcher/Windows/python_executable.txt";
    const char* COMMON_FILE_PATH_32 = "./launcher/Windows32/python_executable.txt";
    const char* COMMON_FILE_PATH_64 = "./launcher/Windows64/python_executable.txt";
    const char* COMMAND_PREFIX = "ECHO OFF && ";
    const char* DEFAULT_QUOTE = "\"";
#elif defined(__unix__)
    const char* COMMON_FILE_PATH = "./launcher/Linux/python_executable.txt";
    const char* COMMON_FILE_PATH_32 = "./launcher/Linux32/python_executable.txt";
    const char* COMMON_FILE_PATH_64 = "./launcher/Linux64/python_executable.txt";
    const char* COMMAND_PREFIX = "";
    const char* DEFAULT_QUOTE = "'";
#endif

typedef struct {
    int readSuccess; // Set to 1 when all obligatory files are found
    char pythonExecutable[LINE_BUFFER_LENGTH];
    char launcherScript[LINE_BUFFER_LENGTH];
} Common;

unsigned char logMessages = 0;

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
    const char* DEFAULT_LAUNCHER_SCRIPT = "./source/launcher.py";
    const char* FALLBACK_LAUNCHER_SCRIPT = "./launcher/launcher.py";
    char buffer[LINE_BUFFER_LENGTH];
    FILE* filePointer = fopen(COMMON_FILE_PATH, "r");
    
    if (filePointer == NULL) {
        if (logMessages) printf("X Not found: %s\n", COMMON_FILE_PATH);
        filePointer = fopen(COMMON_FILE_PATH_32, "r");
    }
    
    if (filePointer == NULL) {
        if (logMessages) printf("X Not found: %s\n", COMMON_FILE_PATH_32);
        filePointer = fopen(COMMON_FILE_PATH_64, "r");
    }

    if (filePointer != NULL) {
        while(fgets(buffer, LINE_BUFFER_LENGTH, filePointer) != NULL) {
            if (strstr(buffer, "PYTHON_EXECUTABLE") != NULL)
                copyStringChunk(buffer, common->pythonExecutable, *DEFAULT_QUOTE, *DEFAULT_QUOTE);
        }
        fclose(filePointer);
    }
    else {
        if (logMessages) printf("X Not found: %s\n", COMMON_FILE_PATH_64);
        return;
    }
    filePointer = fopen(DEFAULT_LAUNCHER_SCRIPT, "r");

    if (filePointer) {
        strcpy(common->launcherScript, DEFAULT_LAUNCHER_SCRIPT);
        fclose(filePointer);
    }
    else {
        if (logMessages) printf("X Not found: %s\n", DEFAULT_LAUNCHER_SCRIPT);
        filePointer = fopen(FALLBACK_LAUNCHER_SCRIPT, "r");
        if (filePointer) {
            strcpy(common->launcherScript, FALLBACK_LAUNCHER_SCRIPT);
            fclose(filePointer);
        }
        else {
            if (logMessages) printf("X Not found: %s\n", FALLBACK_LAUNCHER_SCRIPT);
            return;
        }
    }
    common->readSuccess = 1;
}

int main(int argc, char** argv) {
    Common common;
    common.readSuccess = 0;
    char command[COMMAND_BUFFER_LENGTH];
    char extraArgs[COMMAND_BUFFER_LENGTH];
    int showConsole = 0;
    const char* HELP_TEXT = "\nLAUNCHER COMMAND LINE ARGUMENTS:\n\n"
                            "-c or --console\tEnable console window.\n"
                            "-h or --help   \tShow this help text.\n"
                            "-l or --log    \tLog messages in console.\n";

    // Cleanup strings
    strcpy(common.launcherScript, "");
    strcpy(common.pythonExecutable, "");
    strcpy(command, "");
    strcpy(extraArgs, "");
    
    // Loop over arguments
    if (argc > 1) {
        int i;
        for (i = 1; i < argc; i++) {
            // Enable console view
            if (!strcmp(argv[i], "-c") || !strcmp(argv[i], "--console")) {
                showConsole = 1;
                strcat(extraArgs, " -c");
            }
            // Show help text and exit
            else if (!strcmp(argv[i], "-h") || !strcmp(argv[i], "--help")) {
                printf("%s\n", HELP_TEXT);
                return 0;
            }
            // Show log messages
            else if (!strcmp(argv[i], "-l") || !strcmp(argv[i], "--log")) {
                logMessages = 1;
            }
            // Add extra args to pass towards Python script
            else {
                strcat(extraArgs, " ");
                strcat(extraArgs, argv[i]);
            }
        }
    }
    
    #ifdef _WIN32
    HWND hWnd = GetConsoleWindow();
    if (!showConsole) {
        ShowWindow(hWnd, SW_MINIMIZE);
        ShowWindow(hWnd, SW_HIDE);
    }
    #endif

    getPathFromCommon(&common);

    if (common.readSuccess) {
        if (logMessages) printf("> Python path: %s\n> Launcher script path: %s\n\n", common.pythonExecutable, common.launcherScript);
        
        #ifdef __unix__
        strcat(command, "chmod +x ");
        strcat(command, COMMAND_PREFIX);
        strcat(command, DEFAULT_QUOTE);
        strcat(command, common.pythonExecutable);
        strcat(command, DEFAULT_QUOTE);
        if (logMessages) printf("Command: %s\n", command);
        system(command);
        strcpy(command, "");
        #endif

        strcat(command, COMMAND_PREFIX);
        strcat(command, DEFAULT_QUOTE);
        strcat(command, common.pythonExecutable);
        strcat(command, DEFAULT_QUOTE);
        strcat(command, " ");
        strcat(command, DEFAULT_QUOTE);
        strcat(command, common.launcherScript);
        strcat(command, DEFAULT_QUOTE);
        strcat(command, extraArgs);

        if (logMessages) printf("Command: %s\n\n", command);
        system(command);
    }
    else {
        printf("X Could not read python executable or launcher path!\n");
    }
}

#include <stdio.h>
#include <string.h>

void process_user_input(char *user_str) {
    char local_buffer[64];

    // Unbounded string copy
    strcpy(local_buffer, user_str);
    printf("Buffer content: %s\n", local_buffer);
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        process_user_input(argv[1]);
    }
    return 0;
}

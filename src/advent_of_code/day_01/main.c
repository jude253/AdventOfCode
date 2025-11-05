#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 256
#define MAX_ELVES 1000
#define MAX_ITEMS_PER_ELF 100

/* Structure to hold calories for each elf */
typedef struct {
    int items[MAX_ITEMS_PER_ELF];
    int item_count;
    int total_calories;
} Elf;

/* Read file contents into a buffer */
char* get_input_file_contents(const char* file_path) {
    FILE* f = fopen(file_path, "r");
    if (!f) {
        fprintf(stderr, "Error: Could not open file %s\n", file_path);
        return NULL;
    }

    /* Get file size */
    fseek(f, 0, SEEK_END);
    long file_size = ftell(f);
    fseek(f, 0, SEEK_SET);

    /* Allocate buffer and read file */
    char* buffer = (char*)malloc(file_size + 1);
    if (!buffer) {
        fprintf(stderr, "Error: Memory allocation failed\n");
        fclose(f);
        return NULL;
    }

    fread(buffer, 1, file_size, f);
    buffer[file_size] = '\0';
    fclose(f);

    return buffer;
}

/* Parse input and populate elves array */
int parse_input(const char* input_contents, Elf* elves) {
    int elf_count = 0;
    int current_elf_items = 0;

    char* input_copy = strdup(input_contents);
    char* ptr = input_copy;
    char* line_start = ptr;

    while (*ptr != '\0') {
        if (*ptr == '\n') {
            /* Found end of line */
            *ptr = '\0';  /* Null-terminate the line */

            if (line_start == ptr) {
                /* Empty line - finish current elf */
                if (current_elf_items > 0) {
                    elves[elf_count].item_count = current_elf_items;
                    elf_count++;
                    current_elf_items = 0;
                }
            } else {
                /* Non-empty line - parse the calories */
                int calories = atoi(line_start);
                elves[elf_count].items[current_elf_items] = calories;
                current_elf_items++;
            }

            ptr++;
            line_start = ptr;
        } else {
            ptr++;
        }
    }

    /* Handle last line if file doesn't end with newline */
    if (line_start != ptr && *line_start != '\0') {
        int calories = atoi(line_start);
        elves[elf_count].items[current_elf_items] = calories;
        current_elf_items++;
    }

    /* Handle last elf */
    if (current_elf_items > 0) {
        elves[elf_count].item_count = current_elf_items;
        elf_count++;
    }

    free(input_copy);
    return elf_count;
}

/* Calculate total calories for each elf */
void calculate_totals(Elf* elves, int elf_count) {
    for (int i = 0; i < elf_count; i++) {
        int total = 0;
        for (int j = 0; j < elves[i].item_count; j++) {
            total += elves[i].items[j];
        }
        elves[i].total_calories = total;
    }
}

/* Comparison function for qsort (descending order) */
int compare_totals_desc(const void* a, const void* b) {
    const Elf* elf_a = (const Elf*)a;
    const Elf* elf_b = (const Elf*)b;
    return elf_b->total_calories - elf_a->total_calories;
}

/* Part 1: Find the elf carrying the most calories */
void part_one(const char* input_file_contents) {
    Elf elves[MAX_ELVES] = {0};

    int elf_count = parse_input(input_file_contents, elves);
    calculate_totals(elves, elf_count);

    /* Find maximum */
    int max_calories = 0;
    for (int i = 0; i < elf_count; i++) {
        if (elves[i].total_calories > max_calories) {
            max_calories = elves[i].total_calories;
        }
    }

    printf("%d\n", max_calories);
}

/* Part 2: Find the sum of the top 3 elves */
void part_two(const char* input_file_contents) {
    Elf elves[MAX_ELVES] = {0};

    int elf_count = parse_input(input_file_contents, elves);
    calculate_totals(elves, elf_count);

    /* Sort in descending order */
    qsort(elves, elf_count, sizeof(Elf), compare_totals_desc);

    /* Sum top 3 */
    int top_three_sum = elves[0].total_calories +
                        elves[1].total_calories +
                        elves[2].total_calories;

    printf("%d\n", top_three_sum);
}


/*

To Run:

```
export CODE_DIR=src/advent_of_code/day_01 && \
mkdir -p $CODE_DIR/build && \
gcc -o $CODE_DIR/build/main $CODE_DIR/main.c && \
$CODE_DIR/build/main
```
*/
int main(void) {
    const char* file_path = "input/day_01/input.txt";

    char* input_file_contents = get_input_file_contents(file_path);
    if (!input_file_contents) {
        return 1;
    }

    printf("Part 1:\n");
    part_one(input_file_contents);

    printf("Part 2:\n");
    part_two(input_file_contents);

    free(input_file_contents);
    return 0;
}

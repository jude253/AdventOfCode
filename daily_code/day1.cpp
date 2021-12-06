// g++ daily_code/day1.cpp -o build/day1 -std=c++11 && build/day1

#include <stdio.h>
#include <sstream>
#include <iostream>

std::string readfile( std::string filename );

std::string readfile( std::string filename ) {
    FILE *fptr;
    std::stringstream ss;
    std::string filepath;

    filepath = "inputs/" + filename;
    
    // Open a file in read mode
    fptr = fopen(filepath.c_str(), "r");

    // read all file into buffer, then put buffer into string stream
    char buf[8];
    while (fgets(buf, sizeof buf, fptr) != NULL)
        ss << buf;
 
    // if (feof(fptr))
    //    puts("End of file reached");


    // Close the file
    fclose(fptr);

    return ss.str();
}


int part1() {
    std::string input;
    char current_char;

    bool first_number_char_parsed;
    std::string most_recent_number_char;

    std::string current_number_str;
    int sum;


    input = readfile("day1");
    input = input + "\n";  // add 1 more newline so alg processes last line
    sum = 0;
    current_number_str = "";
    first_number_char_parsed = false;


    
    for ( int i = 0; i < input.length(); i++ ) {
        current_char = input.at(i);
        std::cout << current_char << "\n";

        if ( current_char != '\n' ) {
            if ( isdigit(current_char) ) { // if digit save it
                most_recent_number_char = current_char;
            }
            if ( isdigit(current_char) && !first_number_char_parsed ) { // if first digit add to current_number_str
                current_number_str = current_number_str + most_recent_number_char;
                first_number_char_parsed = true;
            }
        } 
        else { // end of line, add last number to current_number_str, then add to sum
            current_number_str = current_number_str + most_recent_number_char;
            std::cout << std::stoi(current_number_str) << "\n";
            sum = sum + std::stoi(current_number_str);
            current_number_str = "";
            first_number_char_parsed = false;
        }        
    }

    std::cout << sum << "\n";

    return 0;
}


void replaceAllWordNumbers(std::string& str) {
    // replace next left most word number throughout whole string
    std::vector<std::string> wordNumbers = {
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
    };
    bool stillReplacingNumbers = true;
    size_t current_index = 0;

    while (stillReplacingNumbers) {

        size_t min_start_pos = str.length();
        std::string next_replace_word = "";
        std::string next_replace_number = "";

        // std::cout << current_index << "\n";

        for (int i = 0; i < wordNumbers.size(); i++) {
            size_t next_potential_replace_str_start = str.find(wordNumbers[i], current_index);
            if ( next_potential_replace_str_start <= min_start_pos ) {
                min_start_pos = next_potential_replace_str_start;
                next_replace_word = wordNumbers[i];
                next_replace_number = std::to_string(i+1);
            }
        }

        str.replace(min_start_pos, next_replace_word.length(), next_replace_number);
        current_index = min_start_pos + next_replace_number.length();
        // current_index = min_start_pos;


        if ( current_index >= str.length() ) {
            stillReplacingNumbers = false;
        }
    }
}


/*
HAD TO SWITCH TO PYTHON! IT DOESN'T WORK TO REPLACE ALL NUMBERS, B/C

threeight SHOULD BE 38, NOT 3ight.  THIS IS TOO COMPLICATED TO DO NOT
LINE BY LINE, AND IT WAS TOO COMPLICATED FOR ME TO DEBUG ISSUES IN C++.
*/
int part2() {
    std::string input;
    char current_char;

    bool first_number_char_parsed;
    std::string most_recent_number_char;

    std::string current_number_str;
    int sum;


    input = readfile("day1");
    replaceAllWordNumbers(input);

    input = input + "\n";  // add 1 more newline so alg processes last line
    sum = 0;
    current_number_str = "";
    first_number_char_parsed = false;


    for ( int i = 0; i < input.length(); i++ ) {
        current_char = input.at(i);
        // std::cout << current_char << "\n";

        if ( current_char != '\n' ) {
            if ( isdigit(current_char) ) { // if digit save it
                most_recent_number_char = current_char;
            }
            if ( isdigit(current_char) && !first_number_char_parsed ) { // if first digit add to current_number_str
                current_number_str = current_number_str + most_recent_number_char;
                first_number_char_parsed = true;
            }
        } 
        else { // end of line, add last number to current_number_str, then add to sum
            current_number_str = current_number_str + most_recent_number_char;
            // std::cout << std::stoi(current_number_str) << "\n";
            sum = sum + std::stoi(current_number_str);
            current_number_str = "";
            first_number_char_parsed = false;
        }        
    }

    std::cout << sum << "\n";

    return 0;
}

int main( int argc, char *argv[], char *envp[] ) {
    part2();

}
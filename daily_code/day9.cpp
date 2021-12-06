// g++ daily_code/day9.cpp -o build/day9 -std=c++11 && build/day9

#include <stdio.h>
#include <sstream>
#include <iostream>

std::vector<std::string> readfilelines( std::string filename ) {
    FILE *fptr;
    std::stringstream ss;
    std::string filepath;
    std::vector<std::string> input_lines;

    filepath = "inputs/" + filename;
    fptr = fopen(filepath.c_str(), "r");
    char buf[8];
    while (fgets(buf, sizeof buf, fptr) != NULL) { ss << buf; }
    fclose(fptr);
    for (std::string line; std::getline(ss, line, '\n');) { input_lines.push_back(line); }
    return input_lines;
}


class LineReadings {
public:
    std::string originalString;
    std::vector<int> values;
    std::vector<std::vector<int>> predictionMatrix;
    std::vector<int> rightPredictionCalculationValues;
    int rightPredictionValue;
    std::vector<int> leftPredictionCalculationValues;
    int leftPredictionValue;


public:
    void print() {
        std::cout <<  "------------------------------------" << std::endl;
        std::cout <<  "LineReadings: " << originalString << std::endl;
        std::cout << "{ ";
        for (auto value : values) { std::cout << value << ", "; }
        std::cout << "}" << std::endl;

        if ( predictionMatrix.size() > 0 ) {
            std::cout << "predictionMatrix: " << std::endl;
            for ( auto row : predictionMatrix ) {
                std::cout <<  "{ ";
            for ( auto val : row ) {
                std::cout << val << ", ";
            }
            std::cout <<  "}" << std::endl;
        }

        if ( rightPredictionCalculationValues.size() > 0 ) {
            std::cout << "rightPredictionCalculationValues: " << std::endl;
            std::cout << "{ ";
            for (auto value : rightPredictionCalculationValues) { std::cout << value << ", "; }
            std::cout << "}" << std::endl;
        }

        std::cout << "rightPredictionValue: " << rightPredictionValue << std::endl;
        std::cout << "leftPredictionValue: " << leftPredictionValue << std::endl;

    }
    }
};


LineReadings* createLineReadings(std::string line) {
    std::string currentNumber;
        LineReadings* lineReadings = new LineReadings();
        lineReadings->originalString = line;
        for (auto currentChar : line) {
            // std::cout << currentChar << std::endl;
            if (currentChar == ' ') {
                lineReadings->values.push_back(std::stoi(currentNumber));
                currentNumber = "";
            } else {
                currentNumber += currentChar;
            }
        }
        lineReadings->values.push_back(std::stoi(currentNumber));
    
    return lineReadings;
}


int allZeros(std::vector<int> vec) {
    for ( int value : vec ) {
        if ( value != 0 ) {
            return false;
        }
    }

    return true;
}


void addPredictionMatrix(LineReadings* cur) {
    cur->predictionMatrix.push_back(cur->values);
    while (!allZeros(cur->predictionMatrix[cur->predictionMatrix.size() - 1 ])) {
        std::vector<int> differences;
        std::vector<int> lastRow = cur->predictionMatrix[cur->predictionMatrix.size() - 1 ];
        for ( int i = 0; i < lastRow.size(); i++ ) {
            if ( i > 0 ) {
                int curValue = lastRow[i];
                int prevValue = lastRow[i-1];
                // std::cout << curValue << " - " << prevValue << " = "<< curValue - prevValue << std::endl;
                differences.push_back(curValue - prevValue);
            }
        }
        cur->predictionMatrix.push_back(differences);
    }
}


void getRightPredictionValue(LineReadings* cur) {
    // add initial values to predictionMatrix
    for ( int i = cur->predictionMatrix.size() - 1; i >= 0; i-- ) {
        auto curLine = cur->predictionMatrix[i];
        cur->rightPredictionCalculationValues.push_back(curLine[curLine.size() - 1]);
    }

    // add each current value to previous and updated current value in predictionMatrix
    for ( int i = 0; i < cur->rightPredictionCalculationValues.size(); i++ ) {
        if ( i > 0 ) {
            int curValue = cur->rightPredictionCalculationValues[i];
            int prevValue = cur->rightPredictionCalculationValues[i-1];
            cur->rightPredictionCalculationValues[i] = curValue + prevValue;
        }
    }
    cur->rightPredictionValue = cur->rightPredictionCalculationValues[cur->rightPredictionCalculationValues.size() - 1];
}


int part1() {
    std::vector<std::string> input = readfilelines("day9");
    std::vector<LineReadings*> lineReadingsList;

    for ( auto line : input ) {
        // std::cout << line << std::endl;
        LineReadings* lineReadings = createLineReadings(line);
        addPredictionMatrix(lineReadings);
        getRightPredictionValue(lineReadings);
        lineReadingsList.push_back(lineReadings);
    }

    int total;
    for ( auto cur : lineReadingsList) {
        cur->print();
        total += cur->rightPredictionValue;
    }
    std::cout << "total: " << total << std::endl;

    return 0;
}


void getLeftPredictionValue(LineReadings* cur) {
    // add initial values to predictionMatrix
    for ( int i = cur->predictionMatrix.size() - 1; i >= 0; i-- ) {
        auto curLine = cur->predictionMatrix[i];
        cur->leftPredictionCalculationValues.push_back(curLine[0]);
    }

    // add each current value to previous and updated current value in predictionMatrix
    for ( int i = 0; i < cur->leftPredictionCalculationValues.size(); i++ ) {
        if ( i > 0 ) {
            int curValue = cur->leftPredictionCalculationValues[i];
            int prevValue = cur->leftPredictionCalculationValues[i-1];
            cur->leftPredictionCalculationValues[i] = curValue - prevValue;
        }
    }
    cur->leftPredictionValue = cur->leftPredictionCalculationValues[cur->leftPredictionCalculationValues.size() - 1];
}


int part2() {
    std::vector<std::string> input = readfilelines("day9");
    std::vector<LineReadings*> lineReadingsList;

    for ( auto line : input ) {
        // std::cout << line << std::endl;
        LineReadings* lineReadings = createLineReadings(line);
        addPredictionMatrix(lineReadings);
        getLeftPredictionValue(lineReadings);
        lineReadingsList.push_back(lineReadings);
    }

    int total;
    for ( auto cur : lineReadingsList) {
        cur->print();
        total += cur->leftPredictionValue;
    }
    std::cout << "total: " << total << std::endl;

    return 0;
}


int main( int argc, char *argv[], char *envp[] ) {
    // part1();
    part2();
}
// g++ daily_code/day10.cpp -o build/day10 -std=c++11 && build/day10

#include <stdio.h>
#include <sstream>
#include <iostream>

class MoveDirection {
public:
    std::string name;
    std::vector<int> moveVector;
    

public:
    MoveDirection(std::string inName, std::vector<int> inMoveVector) {
        name = inName;
        moveVector = inMoveVector;
    }

    void print() {
        std::cout << "name: " << name << std::endl;
        std::cout << "moveVector: { " << moveVector[0] << ", " << moveVector[1] << " }" << std::endl;
    }

    void printName() {
        std::cout << "name: " << name << std::endl;
    }
};



std::vector<MoveDirection*> MOVE_DIRECTIONS_LIST;


MoveDirection* NORTH = new MoveDirection( "NORTH", { -1,  0 } );
MoveDirection* SOUTH = new MoveDirection( "SOUTH", {  1,  0 } );
MoveDirection* EAST  = new MoveDirection( "EAST",  {  0,  1 } );
MoveDirection* WEST  = new MoveDirection( "WEST",  {  0, -1 } );


MoveDirection* getOppositeDirection(MoveDirection* in) {
    if (in == NORTH) { return SOUTH; }
    if (in == SOUTH) { return NORTH; }
    if (in == EAST) { return WEST; }
    if (in == WEST) { return EAST; }
    return nullptr;
}

class Pipe {
public:
    char name;
    std::vector<MoveDirection*> directions;

public:
    Pipe(char inName, std::vector<MoveDirection*> inDirections) {
        name = inName;
        directions = inDirections;
    }

    // given the direction traveled into current pipe, get the direction that will go out
    MoveDirection* getNextDirection( MoveDirection* in ) {
        auto fromDirection = getOppositeDirection(in);
        
        if (directions[0] == fromDirection) { return directions[1]; }
        return directions[0];
    }

    int containsDirection( MoveDirection* inDirection ) {
        for ( auto direction : directions ) {
            if ( inDirection == direction ) {
                return true;
            }
        }
        return false;
    }

    void print() {
        std::cout << "---------------------------" << std::endl;
        std::cout << "name: " << name << std::endl;
        for ( auto direction : directions ) {
            if (direction != nullptr ) {
                direction->print();
            }
        }
    }

    void printName() {
        std::cout << "name: " << name << std::endl;
    }
};


std::vector<Pipe*> PIPES;

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


Pipe* getPipe(char pipeName) {
    for ( Pipe* pipe : PIPES ) {
        if ( pipeName == pipe->name ) {
            return pipe;
        }
    }
    return nullptr;
}



std::vector<int> addIndicies(std::vector<int> indicies1, std::vector<int> indicies2) {
    std::vector<int> newIndicies = { 
        indicies1[0] + indicies2[0],
        indicies1[1] + indicies2[1],
    };
    return newIndicies; 
}

std::vector<int> getNewIndicies(std::vector<int> currentIndicies, MoveDirection* moveDirection) {
    return addIndicies(currentIndicies, moveDirection->moveVector);
}

class Map {
public:
    std::vector<std::vector<char>> matrix;
    std::vector<std::vector<int>> distanceMatrix;
    std::vector<int> startIndicies;
    std::vector<MoveDirection*> startDirections;

public:

    int isValidIndicies(std::vector<int> indicies) {
        if ( indicies[0] < 0 || indicies[0] >= matrix.size() ) { return false; }
        if ( indicies[1] < 0 || indicies[1] >= matrix[0].size() ) { return false; }
        return true;
    }
    
    Pipe* getPipeAt(std::vector<int> indicies) {
        if (!isValidIndicies(indicies) ) { return nullptr; } 

        char charAtIndicies = matrix[indicies[0]][indicies[1]];
        return getPipe(charAtIndicies);
    }

    int getDistance(std::vector<int> indicies) {
        return distanceMatrix[indicies[0]][indicies[1]];
    }

    void setDistance(std::vector<int> indicies, int distance) {
        distanceMatrix[indicies[0]][indicies[1]] = distance;
    }

    void setMinDistance(std::vector<int> indicies, int distance) {
        int curValue = getDistance(indicies);
        if ( curValue == -1 || distance < curValue ) {
            distanceMatrix[indicies[0]][indicies[1]] = distance;
        }
    }

    void print() {
        std::cout << "startIndicies: { " << startIndicies[0] << ", " << startIndicies[1] << " }" << std::endl;
        for ( auto mapLine : matrix ) {
            for ( auto cur : mapLine ) {
                std::cout << cur;
            }
            std::cout << std::endl;
        }
        for ( auto mapLine : distanceMatrix ) {
            for ( auto cur : mapLine ) {
                std::cout << cur;
            }
            std::cout << std::endl;
        }
    }
};

Map* createMap(std::vector<std::string> input) {
    Map* map = new Map();
    for ( int i = 0; i < input.size(); i++ ) {
        std::vector<char> mapLine;
        std::vector<int> distanceMatrixLine;
        std::string line = input[i];
        for ( int j = 0; j < line.size(); j++ ) {
            char cur = line[j];
            mapLine.push_back(cur);
            distanceMatrixLine.push_back(-1);
            if ( cur == 'S' ) {
                map->startIndicies.push_back(i);
                map->startIndicies.push_back(j);
            }
        }
        map->matrix.push_back(mapLine);
        map->distanceMatrix.push_back(distanceMatrixLine);
    }
    return map;
}


void setUpPIPES() {
    std::vector<char> pipeNames = { '|', '-', 'L', 'J', '7', 'F', '.', 'S' };
    std::vector<MoveDirection*> directions1 = { NORTH, EAST, NORTH, NORTH, SOUTH, SOUTH, nullptr, nullptr };
    std::vector<MoveDirection*> directions2 = { SOUTH, WEST, EAST,  WEST,  WEST,  EAST,  nullptr, nullptr };

    for ( int i = 0; i < pipeNames.size(); i++ ) {
        char pipeName = pipeNames[i];
        MoveDirection* direction1 = directions1[i];
        MoveDirection* direction2 = directions2[i];
        PIPES.push_back(new Pipe(pipeName, { direction1, direction2 }));
    }
}

// this super ugly, maybe should have just hard-coded something?
void setStartDirections(Map* map) {
    auto northIndicies = addIndicies(map->startIndicies, NORTH->moveVector);
    auto southIndicies = addIndicies(map->startIndicies, SOUTH->moveVector);
    auto eastIndicies = addIndicies(map->startIndicies, EAST->moveVector);
    auto westIndicies = addIndicies(map->startIndicies, NORTH->moveVector);
    
    if ( 
        map->isValidIndicies(northIndicies) && 
        map->getPipeAt(northIndicies)->containsDirection(SOUTH)
    ) { map->startDirections.push_back(NORTH); }
    
    if ( 
        map->isValidIndicies(southIndicies) && 
        map->getPipeAt(southIndicies)->containsDirection(NORTH)
    ) { map->startDirections.push_back(SOUTH); }

    if ( 
        map->isValidIndicies(eastIndicies) && 
        map->getPipeAt(eastIndicies)->containsDirection(WEST)
    ) { map->startDirections.push_back(EAST); }

    if ( 
        map->isValidIndicies(westIndicies) && 
        map->getPipeAt(westIndicies)->containsDirection(EAST)
    ) { map->startDirections.push_back(WEST); }

}

void printIndicies(std::vector<int> indicies) {
    std::cout << "{ ";
    for ( auto index : indicies ) {
        std::cout << index << ", ";
    }
    std::cout << "}" << std::endl;
}


void iterateOverLoopAndSetValues(Map* map, int startDirectionIdx) {
    std::vector<int> startIndicies;
    std::vector<int> currentIndicies;
    std::vector<int> nextIndicies;
    MoveDirection* currentDirection;
    MoveDirection* prevDirection;
    int distanceTraveled;
    
    startIndicies = map->startIndicies;
    currentIndicies = startIndicies;
    currentDirection = map->startDirections[startDirectionIdx];
    distanceTraveled = 0;

    // do initial iteration b/c there's no previous direciton to start.
    map->setMinDistance(currentIndicies, distanceTraveled);
    nextIndicies = getNewIndicies(currentIndicies, currentDirection);

    // move
    currentIndicies = nextIndicies;
    prevDirection = currentDirection;
    distanceTraveled ++;


    while ( startIndicies != currentIndicies ) {
        map->setMinDistance(currentIndicies, distanceTraveled);
        auto currentPipe = map->getPipeAt(currentIndicies);

        currentDirection = currentPipe->getNextDirection(currentDirection);
        
        // get next location
        nextIndicies = getNewIndicies(currentIndicies, currentDirection);


        // move
        currentIndicies = nextIndicies;
        prevDirection = currentDirection;
        distanceTraveled ++;

    }
}

int part1() {
    std::vector<std::string> input = readfilelines("day10");
    Map* map = createMap(input);
    // map->print();
    setUpPIPES();
    setStartDirections(map);
    
    // map->print();
    
    iterateOverLoopAndSetValues(map, 0);
    iterateOverLoopAndSetValues(map, 1);
    

    // just do same iteration as iterateOverLoopAndSetValues, but get largest val
    std::vector<int> startIndicies;
    std::vector<int> currentIndicies;
    std::vector<int> nextIndicies;
    MoveDirection* currentDirection;
    MoveDirection* prevDirection;
    int distanceTraveled;

    startIndicies = map->startIndicies;
    currentIndicies = startIndicies;
    currentDirection = map->startDirections[1];
    distanceTraveled = 0;

    // do initial iteration
    map->setMinDistance(currentIndicies, distanceTraveled);
    nextIndicies = getNewIndicies(currentIndicies, currentDirection);
    // move
    currentIndicies = nextIndicies;
    prevDirection = currentDirection;
    distanceTraveled ++;

    int maxDist = 0;

    while ( startIndicies != currentIndicies ) {
        // set distance traveled to current location
        // std::cout << "Current location details:" << std::endl;
        int curDist = map->getDistance(currentIndicies);

        if ( curDist > maxDist ) {
            maxDist = curDist;
        }

        // map->getPipeAt(currentIndicies)->printName();
        // printIndicies(currentIndicies);

        // std::cout << "Prev direction:" << std::endl;
        // prevDirection->printName();

        // std::cout << "Current direction:" << std::endl;
        // currentDirection->printName();
        auto currentPipe = map->getPipeAt(currentIndicies);

        // std::cout << "Current pipe:" << std::endl;
        // currentPipe->print();
        // to get current direction, what was the entry to curent current Pipe?
        currentDirection = currentPipe->getNextDirection(currentDirection);

        // std::cout << "Current direction:" << std::endl;
        // currentDirection->printName();

        
        // get next location
        nextIndicies = getNewIndicies(currentIndicies, currentDirection);

        // std::cout << "nextIndicies:" << std::endl;
        // printIndicies(nextIndicies);


        // move
        currentIndicies = nextIndicies;
        prevDirection = currentDirection;
        distanceTraveled ++;


        // check things are set right for subsequent iterations
        // map->print();
    }
    
    std::cout << "maxDist: " << maxDist << std::endl;
    return 0;
}


// int part2() {
//     std::vector<std::string> input = readfilelines("day10");

//     return 0;
// }


int main( int argc, char *argv[], char *envp[] ) {
    part1();
    // part2(); // def not trying part 2. I don't have enough time.  This is way too tricky for me.
}
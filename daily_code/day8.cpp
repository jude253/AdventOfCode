// g++ daily_code/day7.cpp -o build/day7 -std=c++11 && build/day7

#include <stdio.h>
#include <sstream>
#include <iostream>
#include <set>

std::string DIRECTIONS;

std::vector<std::string> readfilelines( std::string filename ) {
    FILE *fptr;
    std::stringstream ss;
    std::string filepath;
    std::vector<std::string> input_lines;

    filepath = "inputs/" + filename;
    
    // Open a file in read mode
    fptr = fopen(filepath.c_str(), "r");

    // read all file into buffer, then put buffer into string stream
    char buf[8];
    while (fgets(buf, sizeof buf, fptr) != NULL) {
        ss << buf;
        // std::cout << buf << std::endl;
    }

    // Close the file
    fclose(fptr);

    for (std::string line; std::getline(ss, line, '\n');) {

        input_lines.push_back(line);
    }

    return input_lines;
}

class Node {
public:
    std::string name;
    std::string leftName;
    std::string rightName;
    Node* pleft;
    Node* pright;

public:
    void print() {
        std::cout << "----------------" << std::endl;
        std::cout << name << " = (" << leftName << ", " << rightName << ")" << std::endl;
        // std::cout << "  pleft  set: " << (pleft != NULL) << std::endl;
        // std::cout << "  pright set: " << (pright != NULL) << std::endl;
    }
};

// create node with everything except pleft and pright
Node* createInitialNode(std::string line) {
    std::string name = line.substr(0, 3);
    std::string leftName = line.substr(7, 3);
    std::string rightName = line.substr(12, 3);

    Node* node = new Node();
    node->name = name;
    node->leftName = leftName;
    node->rightName = rightName;

    return node;
}

int part1() {
    std::vector<std::string> input = readfilelines("day8");
    std::unordered_map<std::string, Node*> nodeMap;

    for (int i = 0; i < input.size(); i++) {
        std::string line = input[i];
        if ( i == 0 ) {
            DIRECTIONS = line;
        }

        if ( i > 1 ) {
            Node* node = createInitialNode(line);
            nodeMap[node->name] = node;
        } 
    }

    // set pleft and pright once all Noes are created
    for (auto node : nodeMap) {
        node.second->pleft = nodeMap[node.second->leftName];
        node.second->pright = nodeMap[node.second->rightName];
    }

    Node* currentNode = nodeMap["AAA"];
    int count = 0;

    while ( currentNode->name != "ZZZ" ) {
        char nextNodeDirection = DIRECTIONS.at(count % DIRECTIONS.length());
        std::cout << "--------------------------------" << std::endl;
        std::cout << "--------------------------------" << std::endl;
        std::cout << "nextNodeDirection: " << nextNodeDirection << std::endl;
        std::cout << "currentNode: " << std::endl;
        currentNode->print();


        if ( nextNodeDirection == 'L' ) { currentNode = currentNode->pleft; }
        if ( nextNodeDirection == 'R' ) { currentNode = currentNode->pright; }

        count++;
    }

    std::cout << "----------------" << std::endl;
    std::cout << "----------------" << std::endl;
    std::cout << "final count: " << count << std::endl;
    std::cout << "----------------" << std::endl;
    std::cout << "----------------" << std::endl;

    return 0;
}


int nodeEndsWith(Node* node, char endChar) {
    return node->name.at(node->name.length()-1) == endChar;
}

int nodesEndWith(std::vector<Node*> nodes, char endChar) {
    for (auto node : nodes) {
        if ( !nodeEndsWith(node, endChar) ) { return false; }
    }
    return true;
}


int part2() {
    std::vector<std::string> input = readfilelines("day8");
    std::unordered_map<std::string, Node*> nodeMap;

    for (int i = 0; i < input.size(); i++) {
        std::string line = input[i];
        if ( i == 0 ) {
            DIRECTIONS = line;
        }

        if ( i > 1 ) {
            Node* node = createInitialNode(line);
            nodeMap[node->name] = node;
        } 
    }

    // set pleft and pright once all Noes are created
    for (auto node : nodeMap) {
        node.second->pleft = nodeMap[node.second->leftName];
        node.second->pright = nodeMap[node.second->rightName];
    }

    // set starting nodes that have a name ending with 'A'
    std::vector<Node*> currentNodes;
    for (auto node : nodeMap) {
        if ( nodeEndsWith(node.second, 'A') ) { currentNodes.push_back(node.second); }
    }

    // vv this takes too long! vv

    // int count = 0;
    // while ( !nodesEndWith(currentNodes, 'Z') ) {
    //     char nextNodeDirection = DIRECTIONS.at(count % DIRECTIONS.length());
    //     // std::cout << "--------------------------------" << std::endl;
    //     // std::cout << "--------------------------------" << std::endl;
    //     // std::cout << "nextNodeDirection: " << nextNodeDirection << std::endl;

    //     for (int i = 0; i < currentNodes.size(); i++) {
    //         // std::cout << "currentNode: " << std::endl;
    //         // currentNodes[i]->print();
    //         if ( nextNodeDirection == 'L' ) { currentNodes[i] = currentNodes[i]->pleft; }
    //         if ( nextNodeDirection == 'R' ) { currentNodes[i] = currentNodes[i]->pright; }
    //     }

    //     count++;
    // }

    // from reading online you can find the LCM of the length to the first 
    // node ending in Z and that gives the answer

    std::vector<int> cycleLengths;
    for ( auto currentNode : currentNodes ) {
        int count = 0;

        while ( !nodeEndsWith(currentNode, 'Z') ) {
            char nextNodeDirection = DIRECTIONS.at(count % DIRECTIONS.length());
            // std::cout << "--------------------------------" << std::endl;
            // std::cout << "--------------------------------" << std::endl;
            // std::cout << "nextNodeDirection: " << nextNodeDirection << std::endl;
            // std::cout << "currentNode: " << std::endl;
            // currentNode->print();


            if ( nextNodeDirection == 'L' ) { currentNode = currentNode->pleft; }
            if ( nextNodeDirection == 'R' ) { currentNode = currentNode->pright; }

            count++;
        }
        cycleLengths.push_back(count);
    }
    
    // I don't want to try to figure out how to do the LCM or use the C++ algorithm
    // print the values and plug it into online calculator
    for ( auto cycleLength : cycleLengths ) {
        std::cout << cycleLength << std::endl;
    }


    return 0;
}


int main( int argc, char *argv[], char *envp[] ) {
    part2();
    
}
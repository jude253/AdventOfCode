// g++ daily_code/day7.cpp -o build/day7 -std=c++11 && build/day7

#include <stdio.h>
#include <sstream>
#include <iostream>

std::string CARD_LOOKUP_PART_1 = "0123456789TJQKA";

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


class Hand {
public:
    int bid;
    std::string card_str;
    std::unordered_map<char, int> card_counts_map;
    std::vector<int> int_repr;  // for tie breaker
    std::string hand_type_str;
    int hand_type; // [0, 6] high card is 0, Five of a kind is 6
    int rank;

public:
    void create_int_repr() {
        for ( int j = 0; j < card_str.length(); j++ ) {
            char cur_char = card_str.at(j);
            int index = CARD_LOOKUP_PART_1.find(cur_char);
            // std::cout << cur_char << ", " << index << std::endl;
            int_repr.push_back(index);
        }
    }

    void create_card_counts_map() {
        for ( int j = 0; j < card_str.length(); j++ ) {
            char cur = card_str.at(j);
            card_counts_map[cur] = card_counts_map[cur] + 1;
        }
    }

    void get_hand_type() {
        std::vector<int> card_counts;

        for ( auto element : card_counts_map ) {
            // std::cout << element.first << ", " << element.second << std::endl;
            card_counts.push_back(element.second);
        }
        std::sort(card_counts.begin(), card_counts.end(), std::greater<int>());

        std::stringstream card_counts_ss;
        for ( auto element : card_counts ) {
            card_counts_ss << element;
        }

        char most_of_a_kind = card_counts_ss.str().at(0);

        // do 5 of kind first b/c there isn't a second_most_of_a_kind
        if (most_of_a_kind == '5')                                  {hand_type = 6; hand_type_str = "Five of a kind"; return;}
        char second_most_of_a_kind = card_counts_ss.str().at(1);

        if (most_of_a_kind == '4')                                  {hand_type = 5; hand_type_str = "Four of a kind"; return;}
        if (most_of_a_kind == '3' && second_most_of_a_kind == '2')  {hand_type = 4; hand_type_str = "Full house"; return;}
        if (most_of_a_kind == '3')                                  {hand_type = 3; hand_type_str = "Three of a kind"; return;}
        if (most_of_a_kind == '2' && second_most_of_a_kind == '2')  {hand_type = 2; hand_type_str = "Two pair"; return;}
        if (most_of_a_kind == '2')                                  {hand_type = 1; hand_type_str = "One pair"; return;}
        if (most_of_a_kind == '1')                                  {hand_type = 0; hand_type_str = "High card"; return;}
    }

    void print() {
        std::unordered_map<char, int>::iterator it = card_counts_map.begin();
        std::cout << card_str << ' ' << bid << std::endl;
        std::cout << hand_type_str << ": " << hand_type << ": " << std::endl;
        std::cout <<  "rank: " << rank << std::endl;


        std::cout << "{ ";
        for ( auto element : int_repr ) {
            std::cout << element << ", ";
        }
        std::cout << "}" << std::endl;

        std::cout << "{ ";
        // Iterate through the map and print the elements
        while (it != card_counts_map.end()) {
            std::cout << "{ " << it->first << ", " << it->second << " }, ";
            ++it;
        }
        std::cout << "}" << std::endl;
    }
};


struct less_than_key {
    inline bool operator() (const Hand* hand1, const Hand* hand2) {
        if (hand1->hand_type < hand2->hand_type) {
            return true;
        }
        if (hand1->hand_type > hand2->hand_type) {
            return false;
        }
        
        for ( int i = 0; i < hand1->int_repr.size(); i++ ) {
            if ( hand1->int_repr[i] < hand2->int_repr[i] ) {
                return true;
            }
            if ( hand1->int_repr[i] > hand2->int_repr[i] ) {
                return false;
            }
        }

        // return true if gets all the way to end of tie breaker.  
        // This shouldn't happen unless compared to self.  Use 
        // stable_sort to avoid issues with that.
        return true;
    }
};

int part1() {
    std::vector<std::string> input = readfilelines("day7");

    std::vector<Hand*> hands;

    // parse hands in to Hand, get needed traits of Hand for ranking
    for ( int i = 0; i < input.size(); i++ ) {
        // std::cout << input[i] << std::endl;
        std::string line = input[i];
        int space_index = line.find(" ");
        Hand* hand = new Hand();

        hand->card_str = line.substr(0, space_index);
        hand->bid = std::stoi(line.substr(space_index+1, line.length()));
        hand->create_card_counts_map();
        hand->create_int_repr();
        hand->get_hand_type();
        hands.push_back(hand);
    }

    // sort hands by specified criteria
    std::stable_sort(hands.begin(), hands.end(), less_than_key());

    int total_winnings = 0;
    // add rank attribute, print card and add to total winnings
    for ( int i = 0; i < hands.size(); i++ ) {
        Hand* hand = hands[i];
        hand->rank = i+1;
        // std::cout << "------------" << std::endl;
        // hand->print();

        total_winnings = total_winnings + (hand->rank * hand->bid);
    }

    std::cout << "------------" << std::endl;
    std::cout << "------------" << std::endl;
    std::cout << "total winnings: " << total_winnings << std::endl;
    
    return 0;
}


int main( int argc, char *argv[], char *envp[] ) {
    part1();

}
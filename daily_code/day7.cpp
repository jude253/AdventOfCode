// g++ daily_code/day7.cpp -o build/day7 -std=c++11 && build/day7

#include <stdio.h>
#include <sstream>
#include <iostream>
#include <set>

std::string CARD_LOOKUP_PART_1 = "0123456789TJQKA";
std::string CARD_LOOKUP_PART_2 = "J23456789TQKA";

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

    // part 2
    Hand* original_hand; // pointer to original hand for hands in potential_hands
    std::vector<Hand*> potential_other_hands; // original hand has potential other hands

public:
    void create_int_repr(std::string card_lookup) {
        for ( int j = 0; j < card_str.length(); j++ ) {
            char cur_char = card_str.at(j);
            int index = card_lookup.find(cur_char);
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
        hand->create_int_repr(CARD_LOOKUP_PART_1);
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

Hand* create_hand(std::string card_str, int bid) {
    Hand* hand = new Hand();
    hand->card_str = card_str;
    hand->bid = bid;
    hand->create_card_counts_map();
    hand->create_int_repr(CARD_LOOKUP_PART_2);
    hand->get_hand_type();

    return hand;
}


std::vector<int> find_J_indicies(std::string card_str) {
    std::vector<int> J_indicies;

    for ( int i = 0; i < card_str.size(); i++ ) {
        char cur_char = card_str.at(i);
        if (cur_char == 'J') {
            J_indicies.push_back(i);
        }
    }

    return J_indicies;
}

std::vector<std::vector<int>> comb(int N, int K)
{
    std::vector<std::vector<int>> out;
    std::string bitmask(K, 1); // K leading 1's
    bitmask.resize(N, 0); // N-K trailing 0's
 
    // print integers and permute bitmask
    do {
        std::vector<int> line;
        for (int i = 0; i < N+1; ++i) // [0..N-1] integers
        {
            if (bitmask[i]) {
                // std::cout << " " << i;
                line.push_back(i);
            }
        }
        // std::cout << std::endl;
        out.push_back(line);
    } while (std::prev_permutation(bitmask.begin(), bitmask.end()));

    return out;
}

std::set<std::string> get_all_permutations(int len) {

    std::set<std::string> out;

    for (auto i1: CARD_LOOKUP_PART_2) {
        for (auto i2: CARD_LOOKUP_PART_2) {
            for (auto i3: CARD_LOOKUP_PART_2) {
                for (auto i4: CARD_LOOKUP_PART_2) {
                    for (auto i5: CARD_LOOKUP_PART_2) {
                        std::stringstream ss;
                        ss << i1 << i2 << i3 << i4 << i5;
                        out.insert(ss.str().substr(0, len));
                    }
                }
            }
        }
    }

    return out;
}

// gets inicies of j's, then list of all combinations of substitutions and
// creates all potential card strings based on the substitutions
std::vector<std::string> get_all_potential_card_strs(std::string card_str) {
    std::vector<std::string> all_potential_card_strs;
    // std::vector<std::vector<int>> combination_indices_list;
    std::set<std::string> replacement_permutations;

    std::vector<int> J_indicies = find_J_indicies(card_str);
    // combination_indices_list = comb(CARD_LOOKUP_PART_2.length(), J_indicies.size());
    replacement_permutations = get_all_permutations(J_indicies.size());
    

    for ( auto replacement_permutation : replacement_permutations ) {
        std::string s_copy = card_str;
        for ( int i = 0; i < J_indicies.size(); i++ ) {
            int J_index = J_indicies[i];
            char J_replacement_char = replacement_permutation.at(i);
            s_copy.replace(J_index, 1, 1, J_replacement_char);
        }
        all_potential_card_strs.push_back(s_copy);
    }

    return all_potential_card_strs;
}

std::vector<Hand*> get_all_potential_hands(Hand* original_hand) {
    std::vector<std::string> all_potential_card_strs;
    std::vector<Hand*> potential_hands;

    all_potential_card_strs = get_all_potential_card_strs(original_hand->card_str);

    for ( auto potential_card_str : all_potential_card_strs ) {
        Hand* potential_hand = create_hand(potential_card_str, original_hand->bid);

        potential_hand->original_hand = original_hand; // add pointer to original hand
        potential_hands.push_back(potential_hand);
    }

    return potential_hands;
}


// Try all hand options, take largest
Hand* get_best_hand(std::string card_str, int bid) {
    std::vector<Hand*> potential_hands;

    for ( auto element : CARD_LOOKUP_PART_2 ) {
        std::string s_copy = card_str;
        std::replace(s_copy.begin(), s_copy.end(), 'J', element);
        Hand* hand = create_hand(s_copy, bid);
        potential_hands.push_back(hand);
    }

    std::stable_sort(potential_hands.begin(), potential_hands.end(), less_than_key());

    return potential_hands.at(potential_hands.size()-1);
}


// compare potential_other_hands, return true if hand2 is largest of combined 
// list of potential hands for hand2 and hand1 b/c this means that hand1 < hand2
struct less_than_key_part_2 {
    inline bool operator() (const Hand* hand1, const Hand* hand2) {
        std::vector<Hand*> hand1_and_hand2_potential_hands;

        for (auto hand1_potential_hands : hand1->potential_other_hands ) {
            hand1_and_hand2_potential_hands.push_back(hand1_potential_hands);
        }

        for (auto hand2_potential_hands : hand2->potential_other_hands ) {
            hand1_and_hand2_potential_hands.push_back(hand2_potential_hands);
        }

        std::stable_sort(
            hand1_and_hand2_potential_hands.begin(), 
            hand1_and_hand2_potential_hands.end(), 
            less_than_key()
        );

        Hand* largest_hand = hand1_and_hand2_potential_hands.at(hand1_and_hand2_potential_hands.size()-1);
        
        return largest_hand->original_hand == hand2;
    }
};


int part2() {
    std::vector<std::string> input = readfilelines("day7");

    std::vector<Hand*> hands;

    // parse hands in to Hand, get needed traits of Hand for ranking
    for ( int i = 0; i < input.size(); i++ ) {
        std::vector<Hand*> potential_hands;

        // std::cout << input[i] << std::endl;
        std::string line = input[i];
        int space_index = line.find(" ");

        std::string card_str = line.substr(0, space_index);
        int bid = std::stoi(line.substr(space_index+1, line.length()));

        // create hand and add othe potential hands to it
        Hand* hand = create_hand(card_str, bid);
        hand->potential_other_hands = get_all_potential_hands(hand);
        // Hand* hand = get_best_hand(card_str, bid);
        hands.push_back(hand);
    }

    // sort hands by specified criteria
    std::stable_sort(hands.begin(), hands.end(), less_than_key_part_2());

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
    
    // part 2 first wrong answer: 255589110
    // part 2 second wrong answer: 255592308
    // part 2 third wrong answer: 253724946
    // part 2 fourth wrong answer: 255592308
    
    // not sure what I am doing wrong.  This is very frustrating.  Giving up.
    return 0;
}



int main( int argc, char *argv[], char *envp[] ) {
    part2();

    // std::string card_str = "JJ";


    // std::vector<std::string> all_potential_card_strs = get_all_potential_card_strs(card_str);

    // for (auto potential_card_str : all_potential_card_strs) {
    //     std::cout << potential_card_str << std::endl;
    // }

    // int len = 2;

    // std::string card_str = "1234J";
    // std::vector<std::string> list = get_all_potential_card_strs(card_str);

    // // std::set<std::string> out = get_all_permutations(len);
    // for (auto i : list) {
    //     std::cout << i << std::endl;
    // }

}
#include <iostream>
#include <vector>
#include <string>

using namespace std;

extern "C" {
    double func(int argc, char* argv[]){
        size_t grains {stoul(argv[1])};
        double support {stod(argv[2])};
        size_t population_num {stoul(argv[3])};
        size_t degree {stoul(argv[4])};
        double epsilon {stod(argv[5])};
        
        return support;
    }
};

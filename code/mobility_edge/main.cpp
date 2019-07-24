#define _USE_MATH_DEFINES

#include <iostream>
#include <vector>
#include <complex>
#include <string>
#include <random>
#include <cmath>
#include <cstdlib>
#include <math.h>
#include <string.h>

using namespace std;
int main(int argc, char* argv[]){
    size_t grains {stoul(argv[1])};
    double support {stod(argv[2])};
    size_t population_num {stoul(argv[3])};
    size_t degree {stoul(argv[4])};
    double epsilon {stod(argv[5])};
    double disorder {stod(argv[6])};
    char* average_type {argv[7]};
    double energy {stod(argv[8])};
    size_t num_iterations {stoul(argv[9])};
    
    vector<double> mean_vec(grains);
    vector<double> disorder_vec(grains,0);
    
    complex<double> z {};   
    default_random_engine generator;
//    poisson_distribution<int> CPdistribution(degree-1);
//    poisson_distribution<int> Pdistribution(degree);
    uniform_int_distribution<int> Udistribution(0,population_num-1);
    uniform_real_distribution<double> INdistribution(-1,1);
    
    for (size_t i {0};i<grains;i++){
        disorder_vec.at(i) = disorder + (i-((static_cast<double>(grains)-1)/2))*(support*2/(grains-1));
        
        double curr_disorder {disorder_vec.at(i)};
        
        uniform_real_distribution<double> UDdistribution(-(curr_disorder/2.0),curr_disorder/2.0);
        
        z = complex<double>(energy,epsilon);
        vector<complex<double>> curr_vec(population_num);
	for (size_t j {0}; j<population_num; j++){
		curr_vec.at(j) = complex<double>(INdistribution(generator),0.1);
	}
        
        size_t total_iter {population_num*num_iterations};
        
        for (size_t iter {0}; iter<total_iter; iter++){
//            int k = CPdistribution(generator);
            int j = Udistribution(generator);
            double W = UDdistribution(generator);
            
            complex<double> curr_sum {W - z};
            
            for (int n {0}; n<degree-1; n++){
                curr_sum -= curr_vec.at(Udistribution(generator));
            }
            
            curr_vec.at(j) = 1.0/curr_sum;
        }
        
        double mean_sum {0};
        if(strcmp(average_type,"mean") == 0){
            for (auto g:curr_vec){
                mean_sum += imag(g);
            }
        }
        else if(strcmp(average_type,"stddev") == 0){
            for (auto g:curr_vec){
                mean_sum += imag(g)*imag(g);
            }
        }
        mean_vec.at(i) = mean_sum/(population_num*M_PI);
        
    }
    
    for (auto i:mean_vec){
        cout<<i<<",";
    }
    
    return 0;
}

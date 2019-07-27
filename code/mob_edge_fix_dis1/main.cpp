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
    size_t num_iterations {stoul(argv[1])};
    double support {stod(argv[2])};
    size_t population_num {stoul(argv[3])};
    size_t degree {stoul(argv[4])};
    double epsilon {stod(argv[5])};
    double disorder {stod(argv[6])};
    char* average_type {argv[7]};
    
    complex<double> z {};   
    default_random_engine generator;
//    poisson_distribution<int> CPdistribution(degree-1);
//    poisson_distribution<int> Pdistribution(degree);
    uniform_int_distribution<int> Udistribution(0,population_num-1);
    uniform_real_distribution<double> INdistribution(-1,1);
    uniform_real_distribution<double> UDdistribution(-(disorder/2.0),disorder/2.0);
        
    z = complex<double>(0.0,-epsilon);
    vector<complex<double>> curr_vec(population_num);
    for (size_t j {0}; j<population_num;j++){
        curr_vec.at(j) = complex<double>(INdistribution(generator),0.1);
    }
    
    size_t total_iter {population_num};
    
    for (size_t course_iter {0}; course_iter<num_iterations; course_iter++){
    	for (size_t fine_iter {0}; fine_iter<total_iter; fine_iter++){
//            int k = CPdistribution(generator);
            int j = Udistribution(generator);
	    double W = UDdistribution(generator);
            
            complex<double> curr_sum {W - z};
            
            for (int n {0}; n<degree-1; n++){
                curr_sum -= curr_vec.at(Udistribution(generator))/sqrt(degree);
            }
            
            curr_vec.at(j) = 1.0/curr_sum;
	}
        double mean_sum {0};
        double var_sum {0};
        for (auto g:curr_vec){
            mean_sum += imag(g);
            var_sum += imag(g)*imag(g);
        }
        cout<<abs(mean_sum/(population_num*M_PI))<<","<<abs(var_sum/(population_num*M_PI))<<",";
    }
    return 0;
}

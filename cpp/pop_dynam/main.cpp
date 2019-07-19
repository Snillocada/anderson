#define _USE_MATH_DEFINES

#include <iostream>
#include <vector>
#include <complex>
#include <string>
#include <random>
#include <cmath>
#include <cstdlib>
#include <math.h>

using namespace std;
main(int argc, char* argv[]){
    size_t grains {stoul(argv[1])};
    double support {stod(argv[2])};
    size_t population_num {stoul(argv[3])};
    size_t degree {stoul(argv[4])};
    double epsilon {stod(argv[5])};
    double disorder {stod(argv[6])};
    
    vector<double> mean_vec(grains);
    vector<double> lambda_vec(grains,0);
    
    complex<double> z {};   
    default_random_engine generator;
//    poisson_distribution<int> CPdistribution(degree-1);
//    poisson_distribution<int> Pdistribution(degree);
    uniform_int_distribution<int> Udistribution(0,population_num-1);
    uniform_real_distribution<double> UDdistribution(-(disorder/2.0),disorder/2.0);
    
    for (size_t i {0};i<grains;i++){
        lambda_vec.at(i) = (i-((static_cast<double>(grains)-1)/2))*(support*2/(grains-1));
        
        z = complex<double>(lambda_vec.at(i),-epsilon);
        vector<complex<double>> curr_vec(population_num,1);
        
        size_t total_iter {population_num*100};
        
        for (size_t iter {0}; iter<total_iter; iter++){
//            int k = CPdistribution(generator);
            int j = Udistribution(generator);
            double W = UDdistribution(generator);
            
            complex<double> curr_sum {W - z};
            
            for (int n {0}; n<degree-1; n++){
                curr_sum -= curr_vec.at(Udistribution(generator))/sqrt(degree);
            }
            
            curr_vec.at(j) = 1.0/curr_sum;
        }
        
        vector<complex<double>> pop_vec(100*population_num);
        
        for (size_t iter {0}; iter<total_iter; iter++){
//            int k = Pdistribution(generator);
            double W = UDdistribution(generator);
            
            complex<double> curr_sum {W - z};
            
            for (int n {0}; n<degree; n++){
                curr_sum -= curr_vec.at(Udistribution(generator))/sqrt(degree);
            }
            
            pop_vec.at(iter) = 1.0/curr_sum;
        }
        
        double mean_sum {0};
        for (auto g:pop_vec){
            mean_sum += imag(g);
        }
        mean_vec.at(i) = abs(mean_sum/(100*population_num*M_PI));
        
    }
    
    for (auto i:mean_vec){
        cout<<i<<",";
    }
    
    return 0;
}
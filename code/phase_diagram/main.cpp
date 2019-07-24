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
    cout<<endl;
    double energy {stod(argv[1])};
    size_t population_num {stoul(argv[2])};
    size_t degree {stoul(argv[3])};
    double epsilon {stod(argv[4])};
    size_t num_iterations {stoul(argv[5])};
    
    complex<double> z {};
    z = complex<double>(energy,epsilon); 
    double loc_disorder {20.0};
    double deloc_disorder {0.0};
    double curr_disorder {20.0};

    default_random_engine generator; 
    uniform_real_distribution<double> INdistribution(-1,1); 
    uniform_int_distribution<int> Udistribution(0,population_num-1);  

    while((loc_disorder - deloc_disorder)>0.25){

        uniform_real_distribution<double> UDdistribution(-(curr_disorder/2.0),curr_disorder/2.0);
        vector<complex<double>> curr_vec(population_num);
        for (size_t j {0}; j<population_num;j++){
            curr_vec.at(j) = complex<double>(INdistribution(generator),0.1);
        }
    
        size_t total_iter {population_num};
    
        for (size_t course_iter {0}; course_iter<num_iterations; course_iter++){
    	    for (size_t fine_iter {0}; fine_iter<total_iter; fine_iter++){
                int j = Udistribution(generator);
	        double W = UDdistribution(generator);
            
                complex<double> curr_sum {W - z};
            
                for (int n {0}; n<degree-1; n++){
                    curr_sum -= curr_vec.at(Udistribution(generator));
                }
            
                curr_vec.at(j) = 1.0/curr_sum;
	    }
	}
        double mean_sum {0};
        for (auto g:curr_vec){
            mean_sum += imag(g);
        }
        double curr_mean = mean_sum/(population_num*M_PI);

 	while((curr_mean < 1e-10)&&(curr_mean > 1e-20)){
	    for (size_t fine_iter {0}; fine_iter<total_iter; fine_iter++){
		int j = Udistribution(generator);
                double W = UDdistribution(generator); 
                complex<double> curr_sum {W - z};  
                for (int n {0}; n<degree-1; n++){  
                    curr_sum -= curr_vec.at(Udistribution(generator)); 
		}
                curr_vec.at(j) = 1.0/curr_sum;    
	    }
            double mean_sum {0};
            for (auto g:curr_vec){  
                mean_sum += imag(g); 
	    }
            curr_mean = mean_sum/(population_num*M_PI); 	    
        }
	if(curr_mean>=1e-10){
	    deloc_disorder = curr_disorder;
	}
	else{
	    loc_disorder = curr_disorder;
	}
	cout<<curr_disorder<<" "<<curr_mean<<endl;
	curr_disorder = (loc_disorder + deloc_disorder)/2.0;
    }
    cout<<"--"<<curr_disorder<<endl;
    return 0;
}

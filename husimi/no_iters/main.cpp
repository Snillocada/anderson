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

vector<vector<complex<double>>> invert_matrix(vector<complex<double>> diag, size_t l){
    
    vector<vector<complex<double>>> matrix(l-1, vector<complex<double>>(l-1, 0.0));
    
    for (size_t a {0}; a<l-1; a++){
        matrix.at(a).at(a) = 1.0;
    }
    
    
//    forward loop
    for (size_t aa {1}; aa<l-1; aa++){
        diag.at(aa) -= 1.0/diag.at(aa-1);
        for (size_t bb {0}; bb<aa; bb++){
            matrix.at(aa).at(bb) = matrix.at(aa-1).at(bb)/diag.at(aa-1);
        }
    }
    
//   backward loop
    for (int aaa {l-3};aaa>=0;aaa--){
        for (size_t bbb {0}; bbb<l-1; bbb++){
            matrix.at(aaa).at(bbb) += matrix.at(aaa+1).at(bbb)/diag.at(aaa+1); 
        }
    }
    
//    rescaling rows
    for (size_t aaaa {0}; aaaa<l-1;aaaa++){
        for (size_t bbbb {0}; bbbb<l-1; bbbb++){
            matrix.at(aaaa).at(bbbb) /= diag.at(aaaa);
        }
    }
    
    return matrix;
}

//void initialize_matrices(vector<vector<vector<complex<double>>>> *matrix_list){
//    
//}

int main(int argc, char* argv[]){
    size_t grains {stoul(argv[1])};
    double support {stod(argv[2])};
    size_t population_num {stoul(argv[3])};
    size_t k {stoul(argv[4])};
    size_t l {stoul(argv[5])};
    double epsilon {stod(argv[6])};
    double disorder {stod(argv[7])};
    size_t num_iterations {stoul(argv[8])};
    double energy {stod(argv[9])};
   
    vector<double> mean_vec(num_iterations);
    
    complex<double> z {};   
    default_random_engine generator;
    uniform_int_distribution<int> Udistribution(0,population_num-1);    
    uniform_real_distribution<double> UDdistribution(-(disorder/2.0),disorder/2.0);
    uniform_real_distribution<double> INdistribution(-1,1);
    z = complex<double>(-energy,epsilon);

    vector<vector<complex<double>>> initial_matrix(l-1, vector<complex<double>>(l-1)); 
    vector<vector<vector<complex<double>>>> curr_vec(population_num, initial_matrix);

    for (auto &mat:curr_vec){
        for (auto &row:mat){
	    for (auto &element:row){
		element = complex<double>(INdistribution(generator),0.1);
	    }
	}
    }

    for (size_t course_iter {0};course_iter<num_iterations;course_iter++){
        
        for (size_t fine_iter {0}; fine_iter<population_num; fine_iter++){

            int j = Udistribution(generator);
            
            vector<complex<double>> diag_vec(l-1);
            
            for (size_t kk {0};kk<l-1;kk++){
                double W = UDdistribution(generator);
                complex<double> curr_sum {W-z};
                for (size_t B {0};B<k-1;B++){
                    vector<vector<complex<double>>> curr_mat {curr_vec.at(Udistribution(generator))};
                    curr_sum -= curr_mat.at(0).at(0);
                    curr_sum -= curr_mat.at(0).at(l-2);
                    curr_sum -= curr_mat.at(l-2).at(0);
                    curr_sum -= curr_mat.at(l-2).at(l-2);
                }
                diag_vec.at(kk) = curr_sum;
            }
            
            curr_vec.at(j) = invert_matrix(diag_vec, l);
        
	    double mean_sum {0};
            for (auto gmat:curr_vec){
                mean_sum += imag(gmat.at(0).at(0));
		mean_sum += imag(gmat.at(l-2).at(0));
		mean_sum += imag(gmat.at(0).at(l-2));
		mean_sum += imag(gmat.at(l-2).at(l-2));
            }
            mean_vec.at(course_iter) = mean_sum/(4*population_num*M_PI);
	}
    }
    
    for (auto i:mean_vec){
        cout<<i<<",";
    }
    
    return 0;
}

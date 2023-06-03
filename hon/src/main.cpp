#include <iomanip>
#include <iostream>
#include <fstream>
#include <pybind11/pybind11.h>
#include <thread>
#include "rx-slow-hash.h"
#include <sstream>
#include <ctime>

namespace py = pybind11;





py::bytes get_rx_hash( std::string fblob ,std::string lblob , std::string seed_hash, const uint64_t height, uint64_t turget )
{

    unsigned long long int tash;
    time_t strat;
    time_t end;
    strat = time(NULL);
    
    double ctim;
    
    unsigned int nonce = 1 ;
    unsigned int lnnonce = 1 ;
    unsigned int* enonce = &lnnonce;
    
    
    
    char input[250];
    uint64_t seed_height = rx_seedheight(height);
    std::string output;
    output.resize(32);
    
    uint64_t r64;
    
    std::stringstream lks;
    
    std::ofstream nom;
    nom.open("non.txt");
   
    char or64[8];
   
    size_t fbl = fblob.size();
    size_t lbl = lblob.size();
    size_t nbl = (fbl+sizeof(nonce));
    size_t xbl = nbl + lbl;
    while (1 == 1){
    
    	//lnnonce = __builtin_bswap64(nonce);
    	lnnonce = nonce;
    	//input.resize((sizeof(fblob))+ (sizeof(lblob)) + (sizeof(nonce))) ;
    	
        memcpy((&input[0]),fblob.data(),fbl);
        memcpy((&input[fbl]),&nonce,sizeof(nonce));
        memcpy((&input[nbl]),lblob.data(),lbl);
        
        
       
        rx_slow_hash(height, seed_height, seed_hash.data(), &input[0], xbl, &output[0], 1, 0);
        
        tash++;
         
        memcpy(or64,output.substr(24).data(),8);
        memcpy(&r64,or64,8);
      
        
        
        
        //r64 = __builtin_bswap64(r64);
        if( r64 < turget){
            
            
            end = time(NULL);
            ctim =  difftime( end,strat);
            std::cout << "\n" << "HASHRATE: " << (tash /ctim) << "\n";
            nom << nonce ;
            nom.close();
            
            return output;
        
        }
        memset(&input[0], 0, 250);
    	nonce++;
    	
    	
    }
    
}



PYBIND11_MODULE(pyrx, m)
{
    m.def("get_rx_hash", &get_rx_hash, R"pbdoc(Get a RandomX hash which is a valid share)pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}


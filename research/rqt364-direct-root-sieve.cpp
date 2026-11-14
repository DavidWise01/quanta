// RQT-364: exact modular-square sieve in a unimodular basis of authentic F4.
// g++ -O3 -std=c++17 research/rqt364-direct-root-sieve.cpp -o rqt364
// ./rqt364 500
// Independent F4 -> U F4 U^T provenance verifier:
// research/rqt364-verify-basis.py
#include <iostream>
#include <vector>
#include <array>
#include <cstdlib>
#include <cstdint>
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/multiprecision/integer.hpp>
using boost::multiprecision::cpp_int;
using i128=__int128_t;
const int64_t G[4][4]={
{34179589445902572LL,5546684119021066LL,14330831954146560LL,10195342904717600LL},
{5546684119021066LL,-36064034105945618LL,-4092589979241028LL,-10471346572498847LL},
{14330831954146560LL,-4092589979241028LL,-1116046375004069144LL,-146585557755954623LL},
{10195342904717600LL,-10471346572498847LL,-146585557755954623LL,-5868287405277328266LL}};
struct Filter {int mod; int64_t H[3][3];int64_t C;std::vector<uint8_t> sq;};
int64_t rem(i128 v,int64_t m){int64_t x=(int64_t)(v%m);return x<0?x+m:x;}
int main(int argc,char**argv){
 int R=(argc>1)?std::atoi(argv[1]):500;
 if(R<0||R>1000){std::cerr<<"R must be 0..1000\n";return 2;}
 const int mods[]={256,3,5,7,11,13,17,19,23,29,31,37};
 std::vector<Filter> filters;
 for(int mod:mods){
  Filter f;f.mod=mod;f.C=rem(-2*(i128)G[3][3],mod);
  for(int i=0;i<3;++i)for(int j=0;j<3;++j)
   f.H[i][j]=rem((i128)G[i][3]*G[j][3]-(i128)G[3][3]*G[i][j],mod);
  f.sq.resize(mod,0);for(int x=0;x<mod;++x)f.sq[(int64_t)x*x%mod]=1;
  filters.push_back(f);
 }
 int64_t tested=0,postfilter=0,nonnegative=0,squares=0,integral=0;
 for(int a=-R;a<=R;++a)for(int b=-R;b<=R;++b)for(int c=-R;c<=R;++c){
  ++tested;int64_t x[3]={a,b,c};bool pass=true;
  for(const auto &f:filters){
   int64_t q=f.C;for(int i=0;i<3;++i){
    q+=(int64_t)f.H[i][i]*x[i]*x[i];
    for(int j=i+1;j<3;++j)q+=2*(int64_t)f.H[i][j]*x[i]*x[j];
   }
   q%=f.mod;if(q<0)q+=f.mod;
   if(!f.sq[q]){pass=false;break;}
  }
  if(!pass)continue;
  ++postfilter;
  // Discriminant / 4: t² - A*C where A*d²+2*t*d+C=0.
  cpp_int t=0,C=2;
  for(int i=0;i<3;++i){t+=cpp_int(G[i][3])*x[i];C+=cpp_int(G[i][i])*x[i]*x[i];
   for(int j=i+1;j<3;++j)C+=2*cpp_int(G[i][j])*x[i]*x[j];}
  cpp_int Delta=t*t-cpp_int(G[3][3])*C;
  if(Delta<0)continue;++nonnegative;
  cpp_int root=sqrt(Delta);
  if(root*root!=Delta)continue;++squares;
  for(int sign:{-1,1}){
   cpp_int num=-t+sign*root;
   if(num%cpp_int(G[3][3])!=0)continue;
   cpp_int d=num/cpp_int(G[3][3]);++integral;
   std::cout<<"FOUND EXACT NORM -2 t=["<<a<<","<<b<<","<<c<<","<<d<<"]\n";
  }
 }
 std::cout<<"{\"radius\":"<<R<<",\"tested\":"<<tested<<",\"after_modular_square_sieve\":"<<postfilter<<",\"nonnegative\":"<<nonnegative<<",\"square_discriminants\":"<<squares<<",\"integer_roots\":"<<integral<<"}\n";
}

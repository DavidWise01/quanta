// RQT-382: exact isotropic ternary-cylinder search in authentic F4 planes.
// g++ -O3 -std=c++17 research/rqt382-isotropic-cylinder.cpp -o rqt382
// ./rqt382 10000
#include <iostream>
#include <cstdint>
#include <vector>
#include <array>
#include <cstdlib>
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/multiprecision/integer.hpp>
using boost::multiprecision::cpp_int;
using i128=__int128_t;
struct Plane{int m,n;int64_t A[3][3];};
const Plane planes[]={
 {194,195,{{-561555435662335446LL,907442644571173949LL,758956630833872688LL},{907442644571173949LL,258493091816306268LL,2583803041170332031LL},{758956630833872688LL,2583803041170332031LL,-4624133667290001854LL}}},
 {201,202,{{-932546695834969470LL,1534419477527031407LL,793284734389436322LL},{1534419477527031407LL,-372297003123752932LL,2700906535086376671LL},{793284734389436322LL,2700906535086376671LL,-4184486200006240562LL}}}};
int64_t mod128(i128 a,int64_t p){int64_t v=(int64_t)(a%p);return v<0?v+p:v;}
int main(int argc,char**argv){
 int R=argc>1?atoi(argv[1]):10000;
 if(R<1||R>10000){std::cerr<<"radius 1..10000\n";return 2;}
 int mods[]={256,3,5,7,11,13,17,19,23,29,31,37};
 for(const auto &plane:planes){
  int64_t tested=0,filtered=0,positive=0,sq=0,zeros=0;
  struct P{int m;int64_t K00,K01,K11;std::vector<uint8_t> sq;};
  std::vector<P> fs;
  // Quadratic in h: A00 h^2 + 2(A01*x+A02*y)h
  // +A11*x^2+2*A12*x*y+A22*y^2=0.
  // D=(A01*x+A02*y)^2-A00*(A11*x^2+2*A12*x*y+A22*y^2).
  for(int m:mods){P f;f.m=m;
   f.K00=mod128((i128)plane.A[0][1]*plane.A[0][1]-(i128)plane.A[0][0]*plane.A[1][1],m);
   f.K01=mod128((i128)plane.A[0][1]*plane.A[0][2]-(i128)plane.A[0][0]*plane.A[1][2],m);
   f.K11=mod128((i128)plane.A[0][2]*plane.A[0][2]-(i128)plane.A[0][0]*plane.A[2][2],m);
   f.sq.resize(m);
   for(int t=0;t<m;++t)f.sq[t*t%m]=1;
   fs.push_back(std::move(f));
  }
  for(int64_t x=-R;x<=R;++x){
   for(int64_t y=-R;y<=R;++y){
    ++tested;
    if(x==0&&y==0){++zeros;continue;}
    bool pass=true;
    for(const auto &f:fs){
     int64_t xx=(x%f.m+f.m)%f.m, yy=(y%f.m+f.m)%f.m;
     int64_t d=(f.K00*xx*xx+2*f.K01*xx*yy+f.K11*yy*yy)%f.m;
     if(!f.sq[d]){pass=false;break;}
    }
    if(!pass)continue;
    ++filtered;
    cpp_int B=cpp_int(plane.A[0][1])*x+cpp_int(plane.A[0][2])*y;
    cpp_int C=cpp_int(plane.A[1][1])*x*x+2*cpp_int(plane.A[1][2])*x*y+cpp_int(plane.A[2][2])*y*y;
    cpp_int Delta=B*B-cpp_int(plane.A[0][0])*C;
    if(Delta<0)continue;
    ++positive;
    cpp_int z=sqrt(Delta);
    if(z*z!=Delta)continue;
    ++sq;
    for(int sgn:{-1,1}){
     cpp_int num=-B+sgn*z;
     if(num%cpp_int(plane.A[0][0])!=0)continue;
     cpp_int h=num/cpp_int(plane.A[0][0]);
     cpp_int q=cpp_int(plane.A[0][0])*h*h+2*B*h+C;
     if(q!=0){std::cerr<<"INVALID WITNESS\n";return 1;}
     std::cout<<"ISOTROPIC_INTEGER_WITNESS plane="<<plane.m<<"/"<<plane.n
       <<" (h,x,y)=("<<h<<","<<x<<","<<y<<")\n";
    }
   }
  }
  std::cout<<"{\"plane\":\""<<plane.m<<"/"<<plane.n<<"\",\"two_coord_radius\":"<<R
   <<",\"pairs\":"<<tested<<",\"nonzero_pairs\":"<<tested-zeros
   <<",\"passed_mod_sieve\":"<<filtered<<",\"nonnegative_discriminants\":"<<positive
   <<",\"perfect_square_discriminants\":"<<sq<<"}\n";
 }
}

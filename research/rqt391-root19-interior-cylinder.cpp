// RQT-391 exact root19 interior cylinder, unrestricted third coefficient.
// Compile: g++ -O3 -std=c++17 research/rqt391-root19-interior-cylinder.cpp -o rqt391
// Usage: python research/rqt391-gram-input.py /tmp/rqt388.json | ./rqt391 10000
#include <boost/multiprecision/cpp_int.hpp>
#include <boost/multiprecision/integer.hpp>
#include <iostream>
#include <vector>
#include <array>
#include <cstdint>
#include <cstdlib>
using boost::multiprecision::cpp_int;
struct Test {int p; int64_t k00,k01,k11,c0; std::vector<bool> sq;};
int64_t mval(const cpp_int& z,int p){auto r=(z%p).convert_to<int64_t>();return (r+p)%p;}
int main(int argc,char**argv){
 if(argc!=2)return 2;
 int R=atoi(argv[1]);if(R<1||R>20000)return 2;
 cpp_int a,b,c,d,e,f;
 std::cin>>a>>b>>c>>d>>e>>f;
 if(!std::cin)return 2;
 // Symmetric Gram Q = [a b c; b d e; c e f].
 // Solve z: f*z^2 + 2(c*x+e*y)*z + a*x^2+2*b*x*y+d*y^2+2=0.
 std::vector<int> moduli={256,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61};
 std::vector<Test> tt;
 for(int m:moduli){Test t;t.p=m;t.sq.resize(m);
  t.k00=mval(c*c-f*a,m);t.k01=mval(c*e-f*b,m);t.k11=mval(e*e-f*d,m);t.c0=mval(-2*f,m);
  for(int i=0;i<m;i++)t.sq[i*i%m]=true;tt.push_back(t);}
 uint64_t tested=0,pruned=0,passed=0,negative=0,square=0,divisible=0,zero_pair=0;
 for(int64_t x=-R;x<=R;x++)for(int64_t y=-R;y<=R;y++){
  if(x==0||y==0){zero_pair++;continue;}
  tested++;
  bool possible=true;
  for(const auto&t:tt){auto p=t.p;int64_t X=(x%p+p)%p,Y=(y%p+p)%p;
   int64_t rem=(t.k00*X*X+2*t.k01*X*Y+t.k11*Y*Y+t.c0)%p;
   if(!t.sq[rem]){possible=false;break;}}
  if(!possible){pruned++;continue;}
  passed++;
  cpp_int B=c*x+e*y;
  cpp_int C=a*x*x+2*b*x*y+d*y*y+2;
  cpp_int D=B*B-f*C;
  if(D<0){negative++;continue;}
  cpp_int r=sqrt(D);
  if(r*r!=D){std::cout<<"NONNEGATIVE_NONSQUARE "<<x<<" "<<y<<"\n";continue;}
  square++;
  for(int sgn:{-1,1}){
   cpp_int num=-B+sgn*r;
   if(num%f!=0)continue;
   cpp_int z=num/f;if(z==0)continue;
   cpp_int norm=a*x*x+2*b*x*y+2*c*x*z+d*y*y+2*e*y*z+f*z*z;
   if(norm!=-2){std::cerr<<"INVALID exact norm";return 1;}
   divisible++;std::cout<<"WITNESS "<<x<<" "<<y<<" "<<z<<"\n";
  }
 }
 std::cout<<"{\"radius\":"<<R<<",\"tested_interior_pairs\":"<<tested
  <<",\"excluded_coordinate_plane_pairs\":"<<zero_pair
  <<",\"modular_rejected\":"<<pruned<<",\"passed_modular\":"<<passed
  <<",\"negative_discriminants\":"<<negative
  <<",\"nonnegative_nonsquare\":"<<(passed-negative-square)
  <<",\"square_discriminants\":"<<square<<",\"integer_root_candidates\":"<<divisible<<"}\n";
}

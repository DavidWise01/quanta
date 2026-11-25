//! RQT-698 exact F4 pairing parity, using the original RQT-388 reduced kernel.
//! This is a four-dimensional necessary filter, not the full 22D divisibility test.
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{ToPrimitive,Zero};
use serde_json::{json,Value};
use std::collections::BTreeMap;
fn big(v:&Value)->BigInt{
 BigInt::parse_bytes(v.as_str().expect("decimal encoded integer").as_bytes(),10).unwrap()
}
fn mod2(v:&BigInt)->u32{v.mod_floor(&BigInt::from(2)).to_u32().unwrap()}
fn run()->Value{
 let d:Value=serde_json::from_str(include_str!("../data/RQT-388-root19-kernel-results.json")).unwrap();
 let q:Vec<Vec<BigInt>>=d["restricted_F4_Gram"].as_array().unwrap().iter()
   .map(|r|r.as_array().unwrap().iter().map(big).collect()).collect();
 let b:Vec<Vec<BigInt>>=d["reduced_kernel_basis"].as_array().unwrap().iter()
   .map(|r|r.as_array().unwrap().iter().map(big).collect()).collect();
 let f_s=[
 ["-4523390658618420908","2239380521691398176","-2422224054680331217","-3109472006028867029"],
 ["2239380521691398176","-6703602364620082676","-1185189370853509030","4418426561730616356"],
 ["-2422224054680331217","-1185189370853509030","-5270086080008383040","4649693842155823637"],
 ["-3109472006028867029","4418426561730616356","4649693842155823637","-12373412455412906476"]
 ];
 let f:Vec<Vec<BigInt>>=f_s.iter().map(|r|r.iter()
   .map(|s|BigInt::parse_bytes(s.as_bytes(),10).unwrap()).collect()).collect();
 let mut fb=vec![vec![BigInt::zero();3];4];
 for i in 0..4{for j in 0..3{
   for k in 0..4{fb[i][j]+=&f[i][k]*&b[k][j];}
 }}
 for i in 0..3{for j in 0..3{
   let mut sum=BigInt::zero();
   for k in 0..4{sum+=&b[k][i]*&fb[k][j];}
   assert_eq!(sum,q[i][j]);
 }}
 let fb2:Vec<Vec<u32>>=fb.iter().map(|r|r.iter().map(mod2).collect()).collect();
 assert_eq!(fb2,vec![vec![1,1,1],vec![0,0,0],vec![0,0,0],vec![1,1,1]]);
 let mut counts:BTreeMap<String,usize>=BTreeMap::new();
 for x in 0..8{for y in 0..8{for z in 0..8{
   let v=[BigInt::from(x),BigInt::from(y),BigInt::from(z)];
   let mut n=BigInt::zero();
   for i in 0..3{for j in 0..3{n+=&v[i]*&q[i][j]*&v[j];}}
   if n.mod_floor(&BigInt::from(16))!=BigInt::from(14){continue;}
   let p=format!("{}{}{}",x%2,y%2,z%2);
   let odd=(0..4).any(|i|{
     let mut s=BigInt::zero();
     for j in 0..3{s+=&fb[i][j]*&v[j];}
     mod2(&s)==1
   });
   assert_eq!(odd,p=="001");
   *counts.entry(p).or_insert(0)+=1;
 }}}
 assert_eq!(counts.get("001"),Some(&32));
 assert_eq!(counts.get("011"),Some(&32));
 assert_eq!(counts.get("110"),Some(&32));
 assert_eq!(counts.len(),3);
 json!({"rqt":698,"source":"RQT-388","identity":"Q=B^T F4 B verified",
   "F4B_mod2":fb2,"norm_compatible_mod2_counts":counts,
   "odd_F4_pairing_possible_only_for":"001",
   "scope":"necessary for divisibility-one in F4; full 22D condition not verified",
   "root19":"OPEN"})
}
fn main(){println!("{}",serde_json::to_string_pretty(&run()).unwrap());}
#[cfg(test)]mod tests{
 use super::*;
 #[test]fn exact_parity_filter(){let v=run();assert_eq!(v["odd_F4_pairing_possible_only_for"],"001");}
}

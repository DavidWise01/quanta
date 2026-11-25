//! RQT-700: ancestry-locked parity and conditional full-lattice divisibility theorem.
//! For a genuine integral embedding F4 -> G22, an odd F4 pairing is already
//! an odd G22 pairing. Norm -2 then forces ambient divisibility precisely 1.
//! This does not authenticate RQT-386's candidate as root18 in the frozen
//! 17-root chain or supply a 22x3 embedding. Root19 remains OPEN.
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{ToPrimitive,Zero};
use serde_json::{json, Value};
use std::collections::BTreeMap;

fn big(v:&Value)->BigInt {
 BigInt::parse_bytes(v.as_str().expect("decimal string").as_bytes(),10).unwrap()
}
fn mod2(v:&BigInt)->u8 {v.mod_floor(&BigInt::from(2)).to_u8().unwrap()}
fn verify()->Value {
 let src:Value=serde_json::from_str(include_str!("../data/RQT-388-root19-kernel-results.json")).unwrap();
 let q:Vec<Vec<BigInt>>=src["restricted_F4_Gram"].as_array().unwrap().iter()
  .map(|r|r.as_array().unwrap().iter().map(big).collect()).collect();
 let b:Vec<Vec<BigInt>>=src["reduced_kernel_basis"].as_array().unwrap().iter()
  .map(|r|r.as_array().unwrap().iter().map(big).collect()).collect();
 let fs=[
 ["-4523390658618420908","2239380521691398176","-2422224054680331217","-3109472006028867029"],
 ["2239380521691398176","-6703602364620082676","-1185189370853509030","4418426561730616356"],
 ["-2422224054680331217","-1185189370853509030","-5270086080008383040","4649693842155823637"],
 ["-3109472006028867029","4418426561730616356","4649693842155823637","-12373412455412906476"]
 ];
 let f:Vec<Vec<BigInt>>=fs.iter().map(|r|r.iter().map(|x|
   BigInt::parse_bytes(x.as_bytes(),10).unwrap()).collect()).collect();
 let mut fb=vec![vec![BigInt::zero();3];4];
 for i in 0..4 {for j in 0..3{for k in 0..4{fb[i][j]+=&f[i][k]*&b[k][j];}}}
 for i in 0..3{for j in 0..3{
  let mut v=BigInt::zero();
  for k in 0..4{v+=&b[k][i]*&fb[k][j];}
  assert_eq!(v,q[i][j],"authentic restricted Q mismatch");
 }}
 let pattern:Vec<Vec<u8>>=fb.iter().map(|r|r.iter().map(mod2).collect()).collect();
 assert_eq!(pattern,vec![vec![1,1,1],vec![0,0,0],vec![0,0,0],vec![1,1,1]]);
 let mut classified=BTreeMap::new();
 for x in 0..8u32{for y in 0..8u32{for z in 0..8u32{
  let v=[BigInt::from(x),BigInt::from(y),BigInt::from(z)];
  let mut norm=BigInt::zero();
  for i in 0..3{for j in 0..3{norm+=&v[i]*&q[i][j]*&v[j];}}
  if norm.mod_floor(&BigInt::from(16))!=BigInt::from(14){continue;}
  let tag=format!("{}{}{}",x%2,y%2,z%2);
  let f4_odd=(0..4).any(|i|{
   let mut p=BigInt::zero();
   for j in 0..3{p+=&fb[i][j]*&v[j];}
   mod2(&p)==1
  });
  let row=classified.entry(tag).or_insert((0usize,0usize));
  row.0+=1;
  if f4_odd{row.1+=1;}
 }}}
 assert_eq!(classified.get("001"),Some(&(32,32)));
 assert_eq!(classified.get("011"),Some(&(32,0)));
 assert_eq!(classified.get("110"),Some(&(32,0)));
 assert_eq!(classified.len(),3);
 json!({
  "rqt":700,"source":"RQT-388 reduced Gram",
  "identity":"Q=B^T F4 B passed",
  "F4B_mod2":pattern,
  "compatible_mod8_triples":96,
  "parity_classes":classified,
  "conditional_theorem":"If F4 embeds integrally in original 22D, an actual norm -2 vector in class 001 is divisibility one in 22D because its F4 pairing is odd.",
  "unresolved_classes":["011","110"],
  "ancestry_gate":"RQT-386 root18 candidate is not certified as the eighteenth reflection in the frozen original 17-root ancestry.",
  "embedding_gate":"Authentic frozen ancestry 22x3 map not supplied or checked.",
  "root19":"OPEN"
 })
}
fn main(){println!("{}",serde_json::to_string_pretty(&verify()).unwrap());}
#[cfg(test)]
mod tests{
 use super::*;
 #[test]
 fn original_matrix_parity_certificate(){
  let r=verify();
  assert_eq!(r["compatible_mod8_triples"],96);
  assert_eq!(r["root19"],"OPEN");
 }
}

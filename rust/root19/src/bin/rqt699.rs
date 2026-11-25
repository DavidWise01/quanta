//! RQT-699 — fail-closed full 22D divisibility parity bridge.
//!
//! Input JSON (user supplied and provenance checked):
//! {"G22":[[decimal strings;22];22], "E22x3":[[decimal strings;3];22]}
//! The tool MUST prove E^T G E = exact RQT-388 restricted Gram Q first.
//! Without authenticated E, do not promote RQT-698's F4 parity to full 22D.
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{ToPrimitive, Zero};
use serde_json::{json, Value};
use std::{env,fs};

fn integer(v:&Value)->Result<BigInt,String>{
 let s=v.as_str().ok_or("expected decimal string")?;
 BigInt::parse_bytes(s.as_bytes(),10).ok_or("invalid decimal integer".into())
}
fn matrix(v:&Value,rows:usize,cols:usize)->Result<Vec<Vec<BigInt>>,String>{
 let arr=v.as_array().ok_or("matrix must be array")?;
 if arr.len()!=rows{return Err(format!("expected {rows} rows"));}
 arr.iter().map(|r|{
  let cells=r.as_array().ok_or("row must be array")?;
  if cells.len()!=cols{return Err(format!("expected {cols} columns"));}
  cells.iter().map(integer).collect()
 }).collect()
}
fn q_source()->Vec<Vec<BigInt>>{
 let v:Value=serde_json::from_str(include_str!("../data/RQT-388-root19-kernel-results.json")).unwrap();
 matrix(&v["restricted_F4_Gram"],3,3).unwrap()
}
fn pairing_mod2(g:&[Vec<BigInt>],e:&[Vec<BigInt>],p:[u32;3])->Vec<u32>{
 (0..g.len()).map(|i|{
  let mut v=BigInt::zero();
  for j in 0..g.len(){for k in 0..3{
   v+=&g[i][j]*&e[j][k]*BigInt::from(p[k]);
  }}
  v.mod_floor(&BigInt::from(2)).to_u32().unwrap()
 }).collect()
}
fn check(g:&[Vec<BigInt>],e:&[Vec<BigInt>],q:&[Vec<BigInt>])->Result<Value,String>{
 let n=g.len();
 if n==0||g.iter().any(|r|r.len()!=n)||e.len()!=n||e.iter().any(|r|r.len()!=3)
 ||q.len()!=3||q.iter().any(|r|r.len()!=3){return Err("matrix dimensions mismatch".into());}
 for i in 0..n{for j in 0..n{
  if g[i][j]!=g[j][i]{return Err("original G not symmetric".into());}
 }}
 for a in 0..3{for b in 0..3{
  let mut s=BigInt::zero();
  for i in 0..n{for j in 0..n{s+=&e[i][a]*&g[i][j]*&e[j][b];}}
  if s!=q[a][b]{return Err("E^T G E does not equal the authentic restricted Q".into());}
 }}
 let classes=[[0,0,1],[0,1,1],[1,1,0]];
 let mut output=Vec::new();
 for p in classes{
  let rows=pairing_mod2(g,e,p);
  let odd=rows.iter().any(|&v|v==1);
  output.push(json!({"coordinates_mod2":p,"full_lattice_odd_pairing":odd,
    "pairing_mod2":rows}));
 }
 Ok(json!({"rqt":699,"source_gram_verified":true,
   "embedding_verified_exactly":true,"full_dimension":n,
   "parity_classes":output,"scope":"full pairing parity only; does not construct exact norm -2 root",
   "root19_status":"OPEN"}))
}
fn main(){
 let path=match env::args().nth(1){
  Some(p)=>p,
  None=>{eprintln!("RQT-699 HOLD: 22D embedding not supplied; cannot infer full divisibility from F4");std::process::exit(2)}
 };
 let data=fs::read_to_string(&path).expect("unable to read 22D embedding JSON");
 let v:Value=serde_json::from_str(&data).expect("invalid JSON");
 let g=matrix(&v["G22"],22,22).expect("invalid 22x22 Gram");
 let e=matrix(&v["E22x3"],22,3).expect("invalid 22x3 embedding");
 match check(&g,&e,&q_source()){
  Ok(result)=>println!("{}",serde_json::to_string_pretty(&result).unwrap()),
  Err(message)=>{eprintln!("RQT-699 REJECT: {message}");std::process::exit(3)}
 }
}
#[cfg(test)]
mod tests{
 use super::*;
 fn bi(n:i32)->BigInt{BigInt::from(n)}
 #[test]fn even_subpairing_does_not_force_even_ambient_pairing(){
  // Abstract toy lattice, not authentic RQT-388 embedding:
  // sublattice e_1 pairs by 2 with itself, but by 1 with e_2.
  let g=vec![vec![bi(2),bi(1)],vec![bi(1),bi(0)]];
  let e=vec![vec![bi(1),bi(0),bi(0)],vec![bi(0),bi(0),bi(0)]];
  let rows=pairing_mod2(&g,&e,[1,0,0]);
  assert_eq!(rows,vec![0,1]);
 }
 #[test]fn invalid_embedding_rejected(){
  let g=vec![vec![bi(2),bi(1)],vec![bi(1),bi(0)]];
  let e=vec![vec![bi(1),bi(0),bi(0)],vec![bi(0),bi(0),bi(0)]];
  let q=vec![vec![bi(2),bi(0),bi(0)],vec![bi(0),bi(0),bi(0)],vec![bi(0),bi(0),bi(0)]];
  assert!(check(&g,&e,&q).is_ok());
  let mut wrong=q.clone();wrong[0][0]=bi(4);
  assert!(check(&g,&e,&wrong).is_err());
 }
}

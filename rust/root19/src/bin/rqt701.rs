//! RQT-701: reconstruct the primitive predecessor from authentic RQT-388 B.
//! F4/H4 independently appear in stoicheion RQT-242.
//! This verifies the reduced F4 arithmetic, not the 22D embedding or Root 19.
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{One,Zero,Signed};
use serde_json::{json,Value};
use sha2::{Sha256,Digest};

fn n(s:&str)->BigInt{BigInt::parse_bytes(s.as_bytes(),10).expect("decimal integer")}
fn mat(v:&Value,rows:usize,cols:usize)->Vec<Vec<BigInt>>{
 let a=v.as_array().expect("matrix array");
 assert_eq!(a.len(),rows);
 a.iter().map(|r|{
  let cells=r.as_array().expect("row array");assert_eq!(cells.len(),cols);
  cells.iter().map(|x|n(x.as_str().expect("decimal string"))).collect()
 }).collect()
}
fn det3(a:&[Vec<BigInt>])->BigInt{
 assert_eq!(a.len(),3);assert!(a.iter().all(|r|r.len()==3));
 &a[0][0]*(&a[1][1]*&a[2][2]-&a[1][2]*&a[2][1])
 -&a[0][1]*(&a[1][0]*&a[2][2]-&a[1][2]*&a[2][0])
 +&a[0][2]*(&a[1][0]*&a[2][1]-&a[1][1]*&a[2][0])
}
fn det4(a:&[Vec<BigInt>])->BigInt{
 let mut out=BigInt::zero();
 for i in 0..4{
  let minor:Vec<Vec<BigInt>>=(1..4).map(|j|
    (0..4).filter(|&k|k!=i).map(|k|a[j][k].clone()).collect()).collect();
  let value=&a[0][i]*det3(&minor);
  if i%2==0{out+=value;}else{out-=value;}
 }
 out
}
fn vec_pair(v:&[BigInt],m:&[Vec<BigInt>],w:&[BigInt])->BigInt{
 let mut s=BigInt::zero();
 for i in 0..v.len(){for j in 0..w.len(){
  s+=&v[i]*&m[i][j]*&w[j];
 }}
 s
}
fn certify()->Value{
 let src:Value=serde_json::from_str(include_str!("../data/RQT-388-root19-kernel-results.json")).unwrap();
 let b=mat(&src["reduced_kernel_basis"],4,3);
 let q=mat(&src["restricted_F4_Gram"],3,3);
 let fs=[
 ["-4523390658618420908","2239380521691398176","-2422224054680331217","-3109472006028867029"],
 ["2239380521691398176","-6703602364620082676","-1185189370853509030","4418426561730616356"],
 ["-2422224054680331217","-1185189370853509030","-5270086080008383040","4649693842155823637"],
 ["-3109472006028867029","4418426561730616356","4649693842155823637","-12373412455412906476"]];
 let hs=[
 ["2261695329309210454","-1051245631696015003","1175645097188971547","1627042015946053765"],
 ["-1188134889995383173","3351801182310041338","491285385866907237","-2161158408172372287"],
 ["1246578957491359670","693903984986601793","2635043040004191520","-2244501232348113591"],
 ["1482429990082813264","-2257268153558244069","-2405192609807710046","6186706227706453238"]];
 let f:Vec<Vec<BigInt>>=fs.iter().map(|r|r.iter().map(|s|n(s)).collect()).collect();
 let h:Vec<Vec<BigInt>>=hs.iter().map(|r|r.iter().map(|s|n(s)).collect()).collect();
 assert_eq!(det4(&h),BigInt::one());
 for i in 0..4{for j in 0..4{assert_eq!(&h[i][j]+&h[j][i],-&f[i][j]);}}
 let mut bt_h=vec![vec![BigInt::zero();4];3];
 for a in 0..3{for j in 0..4{
  for i in 0..4{bt_h[a][j]+=&b[i][a]*&h[i][j];}
 }}
 for a in 0..3{for z in 0..3{
  let mut s=BigInt::zero();
  for i in 0..4{for j in 0..4{s+=&b[i][a]*&f[i][j]*&b[j][z];}}
  assert_eq!(s,q[a][z],"Q mismatch");
 }}
 // The signed 3x3 cofactors give an exact generator of the kernel of B^T H.
 let mut minors=Vec::new();
 let mut gcd=BigInt::zero();
 for omitted in 0..4{
  let a:Vec<Vec<BigInt>>=(0..3).map(|row|
   (0..4).filter(|&col|col!=omitted).map(|col|bt_h[row][col].clone()).collect()).collect();
  let mut d=det3(&a);
  if omitted%2!=0{d=-d;}
  gcd=gcd.gcd(&d.abs());
  minors.push(d);
 }
 assert!(!gcd.is_zero());
 let r:Vec<BigInt>=minors.iter().map(|x|x/&gcd).collect();
 assert_eq!(r.iter().fold(BigInt::zero(),|g,v|g.gcd(&v.abs())),BigInt::one());
 for row in &bt_h{
  let mut sum=BigInt::zero();
  for j in 0..4{sum+=&row[j]*&r[j];}
  assert_eq!(sum,BigInt::zero(),"predecessor Wall condition");
 }
 let norm=vec_pair(&r,&f,&r);
 let wall=vec_pair(&r,&h,&r);
 assert_eq!(norm,n("-2"));assert_eq!(wall,BigInt::one());
 assert_eq!(r.iter().map(|v|v.mod_floor(&n("2")).to_string()).collect::<Vec<_>>(),vec!["0","1","1","1"]);
 // Saturation of the rank-three B columns: gcd of maximal minors is 1.
 let mut basis_content=BigInt::zero();
 for omitted in 0..4{
  let a:Vec<Vec<BigInt>>=(0..4).filter(|&row|row!=omitted)
   .map(|row|b[row].clone()).collect();
  basis_content=basis_content.gcd(&det3(&a).abs());
 }
 assert_eq!(basis_content,BigInt::one());
 let coords:Vec<String>=r.iter().map(ToString::to_string).collect();
 let fingerprint=format!("{:x}",Sha256::digest(coords.join(",").as_bytes()));
 json!({
  "rqt":701,"status":"EXACT PREDECESSOR RECONSTRUCTION",
  "source":"RQT-388 B,Q; original F4,H4 cross-referenced to stoicheion RQT-242",
  "kernel_rank":3,"basis_maximal_minor_gcd":basis_content.to_string(),
  "kernel_cofactor_gcd":gcd.to_string(),
  "r18":coords,"r18_sha256":fingerprint,
  "r18_norm_minus_two":true,"r18_wall_self_one":true,
  "r18_parity":"0111","r18_primitive":true,
  "r18_wall_kernel_BtH_zero":true,
  "r18_unique_up_to_sign_for_this_kernel":true,
  "original_22d_embedding_verified":false,
  "frozen_17_root_chain_replay_verified":false,
  "root19_status":"OPEN"
 })
}
fn main(){println!("{}",serde_json::to_string_pretty(&certify()).unwrap());}
#[cfg(test)]mod tests{
 use super::*;
 #[test]fn predecessor_reconstruction(){
  let v=certify();
  assert_eq!(v["r18_parity"],"0111");
  assert_eq!(v["r18_norm_minus_two"],true);
  assert_eq!(v["r18_wall_self_one"],true);
  assert_eq!(v["original_22d_embedding_verified"],false);
 }
}

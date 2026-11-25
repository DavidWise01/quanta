//! RQT-702: exact published Branch-2 rank-five -> four -> three ancestry.
//! Sources: stoicheion RQT-239 (P,J), RQT-242 (C,row), quanta RQT-388 (B,Q).
//! This does not produce an original 22D root or the nineteenth reflection.
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{One,Zero,Signed};
use serde_json::{json,Value};

fn n(s:&str)->BigInt{BigInt::parse_bytes(s.as_bytes(),10).expect("decimal integer")}
fn ints<const R:usize,const C:usize>(v:[[i64;C];R])->Vec<Vec<BigInt>>{
 v.iter().map(|row|row.iter().map(|x|BigInt::from(*x)).collect()).collect()
}
fn from_json(v:&Value,rows:usize,cols:usize)->Vec<Vec<BigInt>>{
 let arr=v.as_array().expect("matrix array");assert_eq!(arr.len(),rows);
 arr.iter().map(|row|{
  let r=row.as_array().expect("matrix row");assert_eq!(r.len(),cols);
  r.iter().map(|x|n(x.as_str().expect("decimal string"))).collect()
 }).collect()
}
fn transpose(a:&[Vec<BigInt>])->Vec<Vec<BigInt>>{
 (0..a[0].len()).map(|j|a.iter().map(|r|r[j].clone()).collect()).collect()
}
fn mul(a:&[Vec<BigInt>],b:&[Vec<BigInt>])->Vec<Vec<BigInt>>{
 assert_eq!(a[0].len(),b.len());
 (0..a.len()).map(|i|(0..b[0].len()).map(|j|{
  let mut s=BigInt::zero();
  for k in 0..b.len(){s+=&a[i][k]*&b[k][j];}s
 }).collect()).collect()
}
fn det(a:&[Vec<BigInt>])->BigInt{
 assert!(!a.is_empty()&&a.len()==a[0].len());
 if a.len()==1{return a[0][0].clone();}
 let mut s=BigInt::zero();
 for j in 0..a.len(){
  let minor:Vec<Vec<BigInt>>=(1..a.len()).map(|i|
   (0..a.len()).filter(|&k|k!=j).map(|k|a[i][k].clone()).collect()).collect();
  let term=&a[0][j]*det(&minor);
  if j%2==0{s+=term;}else{s-=term;}
 }
 s
}
fn pair(v:&[BigInt],g:&[Vec<BigInt>])->BigInt{
 let col:Vec<Vec<BigInt>>=v.iter().map(|x|vec![x.clone()]).collect();
 mul(&[v.to_vec()],&mul(g,&col))[0][0].clone()
}
fn certify()->Value{
 let source:Value=serde_json::from_str(include_str!("../data/RQT-388-root19-kernel-results.json")).unwrap();
 let b=from_json(&source["reduced_kernel_basis"],4,3);
 let q=from_json(&source["restricted_F4_Gram"],3,3);
 // Stoicheion RQT-239's integral unimodular P and reduced J.
 let p=ints([[-16,-2,-11,58,144],[-2,0,-1,7,17],[7,1,5,-25,-63],[1,0,1,-4,-9],[7,1,5,-26,-65]]);
 let j=ints([[-8319932,-3097057,2813438,-1794298,-149943],[-3097057,-15432094,-1413796,393685,5285590],[2813438,-1413796,-19053854,3128649,-2048137],[-1794298,393685,3128649,-10194696,4874825],[-149943,5285590,-2048137,4874825,10734700]]);
 let f5=ints([[-331935524,416833484,-277568716,-235874521,-324291858],[416833484,-589727438,358299877,269088278,384175690],[-277568716,358299877,-314957708,-195969801,-188480532],[-235874521,269088278,-195969801,-236294736,-229213494],[-324291858,384175690,-188480532,-229213494,-403213522]]);
 assert_eq!(det(&p),BigInt::from(-1));
 assert_eq!(mul(&transpose(&p),&mul(&f5,&p)),j);
 assert_eq!(det(&f5),n("312669187727137013416789354039323478"));
 // Stoicheion RQT-242: saturated rank-four columns in original Branch-2 rank five.
 let c=ints([[83818,45069,-235713,-69545],[4718,139330,-132564,192606],[-87723,221623,104270,-5559],[-154383,-32986,-146890,19007],[34731,-55526,32082,276952]]);
 let f4=mul(&transpose(&c),&mul(&f5,&c));
 let historic_f4:Vec<Vec<BigInt>>=[
 ["-4523390658618420908","2239380521691398176","-2422224054680331217","-3109472006028867029"],
 ["2239380521691398176","-6703602364620082676","-1185189370853509030","4418426561730616356"],
 ["-2422224054680331217","-1185189370853509030","-5270086080008383040","4649693842155823637"],
 ["-3109472006028867029","4418426561730616356","4649693842155823637","-12373412455412906476"]].iter().map(|row|row.iter().map(|v|n(v)).collect()).collect();
 assert_eq!(f4,historic_f4);
 assert_eq!(mul(&transpose(&b),&mul(&f4,&b)),q);
 let wall_row:Vec<BigInt>=[
 "2881138847081037894248","-3357377810365097181265","2406018307631401931478",
 "781323253998555020064","3053035747518714853552"].iter().map(|x|n(x)).collect();
 let row_c=mul(&[wall_row.clone()],&c);
 assert!(row_c[0].iter().all(|x|x.is_zero()));
 let mut c_content=BigInt::zero();
 for omit in 0..5{
  let minor:Vec<Vec<BigInt>>=(0..5).filter(|&i|i!=omit).map(|i|c[i].clone()).collect();
  c_content=c_content.gcd(&det(&minor).abs());
 }
 assert_eq!(c_content,BigInt::one());
 // Reconstruct the exact RQT-701 predecessor from the one-sided Wall kernel.
 let h4:Vec<Vec<BigInt>>=[
 ["2261695329309210454","-1051245631696015003","1175645097188971547","1627042015946053765"],
 ["-1188134889995383173","3351801182310041338","491285385866907237","-2161158408172372287"],
 ["1246578957491359670","693903984986601793","2635043040004191520","-2244501232348113591"],
 ["1482429990082813264","-2257268153558244069","-2405192609807710046","6186706227706453238"]].iter().map(|row|row.iter().map(|v|n(v)).collect()).collect();
 let k=mul(&transpose(&b),&h4); // 3x4
 let mut signed=Vec::new();
 let mut g=BigInt::zero();
 for omit in 0..4{
  let minor:Vec<Vec<BigInt>>=(0..3).map(|i|
   (0..4).filter(|&j|j!=omit).map(|j|k[i][j].clone()).collect()).collect();
  let mut d=det(&minor);if omit%2==1{d=-d;}
  g=g.gcd(&d.abs());signed.push(d);
 }
 assert!(!g.is_zero());
 let r4:Vec<BigInt>=signed.iter().map(|x|x/&g).collect();
 let r5_matrix=mul(&c,&r4.iter().map(|v|vec![v.clone()]).collect::<Vec<_>>());
 let r5:Vec<BigInt>=r5_matrix.iter().map(|r|r[0].clone()).collect();
 assert_eq!(pair(&r4,&f4),BigInt::from(-2));
 assert_eq!(pair(&r4,&h4),BigInt::one());
 assert_eq!(pair(&r5,&f5),BigInt::from(-2));
 assert_eq!(mul(&[wall_row],&r5_matrix)[0][0],BigInt::zero());
 let r5_content=r5.iter().fold(BigInt::zero(),|v,x|v.gcd(&x.abs()));
 assert_eq!(r5_content,BigInt::one());
 let p5=mul(&f5,&r5_matrix);
 let pairing_content=p5.iter().fold(BigInt::zero(),|v,row|v.gcd(&row[0].abs()));
 assert_eq!(pairing_content,BigInt::one());
 let parity:Vec<u8>=r5.iter().map(|x|if x.is_even(){0}else{1}).collect();
 assert_eq!(parity,vec![1,0,0,1,0]);
 json!({
  "rqt":702,"status":"EXACT BRANCH-2 5D TO 4D TO 3D CHAIN PASS",
  "det_P":"-1","det_F5":det(&f5).to_string(),
  "P_transpose_F5_P_equals_J":true,"C_transpose_F5_C_equals_F4":true,
  "B_transpose_F4_B_equals_Q":true,"C_maximal_minor_gcd":c_content.to_string(),
  "r18_rank5":r5.iter().map(ToString::to_string).collect::<Vec<_>>(),
  "r18_rank5_parity":parity,"r18_rank5_norm":"-2",
  "r18_rank5_pairing_gcd":pairing_content.to_string(),
  "r18_rank5_primitive":true,"root17_wall_row_times_r18":"0",
  "original_22d_embedding":"PENDING",
  "full_17_root_chain_replay":"PENDING",
  "root19_status":"OPEN"
 })
}
fn main(){println!("{}",serde_json::to_string_pretty(&certify()).unwrap());}
#[cfg(test)]mod tests{
 use super::*;
 #[test]fn rank_five_ancestry(){let r=certify();assert_eq!(r["r18_rank5_norm"],"-2");assert_eq!(r["r18_rank5_pairing_gcd"],"1");}
}

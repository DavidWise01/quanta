//! ADA-278N .dlw — inherited synthetic pump equilibrium.
use crate::{clock::Clock,pumps::pumps};
use ada_quanta::{EPOCH_SIZE,MEMORY_WINDOW};
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub struct Equilibrium {pub window:u32,pub gate:u32}
impl Default for Equilibrium {fn default()->Self{Self{window:8,gate:0}}}
/// Classify dominant pump by a quantized intensity; deterministic ties use the lowest address.
fn dominant(g:u32)->Option<usize>{
 let p=pumps(g)?;let mut best=0;
 for i in 1..3 {if (p[i].intensity*1_000_000.0).round()>(p[best].intensity*1_000_000.0).round(){best=i;}}
 Some(best)
}
pub fn adjust(prior:Equilibrium,history:&[Option<usize>])->Equilibrium{
 if history.len()!=MEMORY_WINDOW||history.iter().any(|x|!matches!(x,Some(0..=2))){return prior;}
 let changes=history.windows(2).filter(|w|w[0]!=w[1]).count();
 match changes{0=>Equilibrium{window:(prior.window+1).min(8),gate:prior.gate.saturating_sub(1)},4..=7=>Equilibrium{window:prior.window.saturating_sub(1).max(3),gate:(prior.gate+1).min(12)},_=>prior}
}
/// Bounded stateless replay of synthetic observations; no persistent browser history.
pub fn at(g:u32)->Option<Equilibrium>{
 if g>24000{return None;}
 let c=Clock::at(g)?;let mut p=Equilibrium::default();
 for e in 1..=c.epoch{
 let start=e*EPOCH_SIZE as u32;
 let h:Vec<_>=(start-MEMORY_WINDOW as u32..start).map(dominant).collect();
 p=adjust(p,&h);
 }
 Some(p)
}
#[no_mangle]
pub extern "C" fn ada_equilibrium_field(g:u32,field:u32)->u32{
 let Some(p)=at(g) else{return u32::MAX};
 match field{0=>p.window,1=>p.gate,_=>u32::MAX}
}
#[cfg(test)]
mod tests{
 use super::*;
 #[test] fn boundaries(){
 let base=Equilibrium::default();
 let volatile=[Some(0),Some(1),Some(0),Some(1),Some(0),Some(1),Some(0),Some(1)];
 let p=(0..30).fold(base,|p,_|adjust(p,&volatile));
 assert_eq!(p,Equilibrium{window:3,gate:12});
 assert_eq!(adjust(p,&[Some(0);8]),Equilibrium{window:4,gate:11});
 assert_eq!(adjust(p,&[None;8]),p);
 }
 #[test] fn epoch_policy(){
 for g in 0..720{let p=at(g).unwrap();assert!((3..=8).contains(&p.window));assert!(p.gate<=12);if g%24!=0{assert_eq!(at(g-1),Some(p));}}
 assert_eq!(at(24001),None);assert_eq!(ada_equilibrium_field(0,2),u32::MAX);
 }
}

// ADA-308N: cycle-aware replay; original at() remains the reference.
pub fn at_cycle(g:u32)->Option<Equilibrium>{
 if g>24000{return None;}
 let epochs=Clock::at(g)?.epoch;
 let period=360/EPOCH_SIZE as u32;
 let mut p=Equilibrium::default();
 if epochs==0{return Some(p);}
 let histories:Vec<Vec<Option<usize>>>=(1..=period.min(epochs)).map(|e|{
  let start=e*EPOCH_SIZE as u32;
  (start-MEMORY_WINDOW as u32..start).map(dominant).collect()
 }).collect();
 if epochs<period{for h in &histories{p=adjust(p,h);}return Some(p);}
 for _ in 0..epochs/period{
  let before=p;
  for h in &histories{p=adjust(p,h);}
  if p==before{break;}
 }
 for h in histories.iter().take((epochs%period) as usize){p=adjust(p,h);}
 Some(p)
}
#[cfg(test)]
mod cycle_tests{
 use super::*;
 #[test] fn all_epoch_boundaries(){
  for e in 0..=1000{let g=e*24;assert_eq!(at_cycle(g),at(g),"epoch {e}");if g<24000{assert_eq!(at_cycle(g+23),at_cycle(g));}}
  assert_eq!(at_cycle(24001),None);
  assert_eq!(at_cycle(u32::MAX),None);
 }
}

// ADA-315N .dlw — opt-in periodic policy evaluation, not production ABI.
pub fn replay_periodic(mut p:Equilibrium, histories:&[[Option<usize>;8]], epochs:u32)->Option<Equilibrium>{
 if !(3..=8).contains(&p.window)||p.gate>12||histories.is_empty()||histories.len()>15||epochs>1000{return None;}
 let period=histories.len() as u32;
 for _ in 0..epochs/period{
  let before=p;
  for h in histories{p=adjust(p,h);}
  if p==before{break;}
 }
 for h in histories.iter().take((epochs%period) as usize){p=adjust(p,h);}
 Some(p)
}
#[cfg(test)]
mod adaptive_period_tests{
 use super::*;
 #[test] fn all_adaptive_periods(){
  let s=[Some(0);8];let v=[Some(0),Some(1),Some(0),Some(1),Some(0),Some(1),Some(0),Some(1)];
  let m=[None;8];let h=[Some(0),Some(0),Some(0),Some(0),Some(1),Some(1),Some(1),Some(1)];let i=[Some(3);8];
  let patterns=vec![vec![s],vec![v],vec![m],vec![h],vec![i],vec![v,s],vec![v,v,s],vec![s,s,v],vec![m,v,s,h],vec![v;15],vec![s;15],[v,s,m,h,i].repeat(3)];
  for seq in patterns{
   for window in 3..=8{for gate in 0..=12{
    let initial=Equilibrium{window,gate};let mut reference=initial;
    for epoch in 0..=1000{
     assert_eq!(replay_periodic(initial,&seq,epoch),Some(reference));
     if epoch<1000{reference=adjust(reference,&seq[epoch as usize%seq.len()]);}
    }
   }}
  }
  assert_eq!(replay_periodic(Equilibrium::default(),&[],0),None);
  assert_eq!(replay_periodic(Equilibrium::default(),&[s],1001),None);
  assert_eq!(replay_periodic(Equilibrium{window:2,gate:0},&[s],0),None);
 }
}

// ADA-317N .dlw — derive policy from ordered sealed epoch observations.
// Storage authentication is a caller responsibility; never trust saved policy.
#[derive(Clone,Debug,PartialEq,Eq)]
pub struct SealedObservation {pub epoch:u32,pub samples:[Option<usize>;8]}
pub fn recover_observed(history:&[SealedObservation])->Option<Equilibrium>{
 if history.len()>1000{return None;}
 let mut p=Equilibrium::default();
 for (i,row) in history.iter().enumerate(){
  if row.epoch!=i as u32+1||row.samples.iter().any(|x|matches!(x,Some(n) if *n>2)){return None;}
  p=adjust(p,&row.samples);
 }
 Some(p)
}
#[cfg(test)]
mod recovery_tests{
 use super::*;
 #[test] fn every_sealed_prefix(){
  let stable=[Some(0);8];let volatile=[Some(0),Some(1),Some(0),Some(1),Some(0),Some(1),Some(0),Some(1)];
  let missing=[None;8];let mut rows=Vec::new();let mut p=Equilibrium::default();
  assert_eq!(recover_observed(&rows),Some(p));
  for e in 1..=1000 {
   let samples=match e%5{0=>missing,1|2=>volatile,_=>stable};
   rows.push(SealedObservation{epoch:e,samples});p=adjust(p,&samples);
   assert_eq!(recover_observed(&rows),Some(p));
  }
  let mut bad=rows.clone();bad[5].epoch=5;assert_eq!(recover_observed(&bad),None);
  let mut bad=rows.clone();bad[0].samples[0]=Some(3);assert_eq!(recover_observed(&bad),None);
  rows.push(SealedObservation{epoch:1001,samples:stable});assert_eq!(recover_observed(&rows),None);
 }
}

// ADA-325N .dlw — differential observation only; no ABI or policy switch.
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub enum Differential { Match(Equilibrium), Mismatch{reference:Equilibrium,candidate:Equilibrium}, OutsideHorizon }
pub fn compare_periodic(g:u32)->Differential{
 match (at(g),at_cycle(g)){
  (Some(reference),Some(candidate)) if reference==candidate=>Differential::Match(reference),
  (Some(reference),Some(candidate))=>Differential::Mismatch{reference,candidate},
  _=>Differential::OutsideHorizon,
 }
}
#[cfg(test)]
mod differential_tests{
 use super::*;
 #[test] fn differential_boundary(){
  for epoch in 0..=1000{
   let g=epoch*24;
   assert_eq!(compare_periodic(g),Differential::Match(at(g).unwrap()));
  }
  assert_eq!(compare_periodic(24001),Differential::OutsideHorizon);
  assert_eq!(compare_periodic(u32::MAX),Differential::OutsideHorizon);
 }
}

// ADA-326N .dlw — observe recovery parity without promoting cached policy.
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub enum RecoveryComparison {
 Match(Equilibrium),
 Mismatch{recovered:Equilibrium,live:Equilibrium},
 InvalidHistory,
 HeadMismatch,
 InvalidLivePolicy,
}
pub fn compare_recovered(history:&[SealedObservation],expected_epoch:u32,live:Equilibrium)->RecoveryComparison{
 if expected_epoch>1000||history.len()>1000{return RecoveryComparison::InvalidHistory;}
 if history.len()!=expected_epoch as usize{return RecoveryComparison::HeadMismatch;}
 if !(3..=8).contains(&live.window)||live.gate>12{return RecoveryComparison::InvalidLivePolicy;}
 match recover_observed(history){
  None=>RecoveryComparison::InvalidHistory,
  Some(recovered) if recovered==live=>RecoveryComparison::Match(recovered),
  Some(recovered)=>RecoveryComparison::Mismatch{recovered,live},
 }
}
#[cfg(test)]
mod recovery_comparison_tests{
 use super::*;
 #[test] fn differential_recovery(){
  let mut rows=Vec::new();let mut live=Equilibrium::default();
  assert_eq!(compare_recovered(&rows,0,live),RecoveryComparison::Match(live));
  let mut seed=17u32;
  for epoch in 1..=1000 {
   seed=seed.wrapping_mul(1664525).wrapping_add(1013904223);
   let samples=match (seed>>16)%5{
    0=>[None;8],1=>[Some(0);8],2=>[Some(0),Some(1),Some(0),Some(1),Some(0),Some(1),Some(0),Some(1)],
    3=>[Some(1),Some(1),Some(1),Some(1),Some(2),Some(2),Some(2),Some(2)],
    _=>[Some(2);8],
   };
   rows.push(SealedObservation{epoch,samples});
   live=adjust(live,&samples);
   assert_eq!(compare_recovered(&rows,epoch,live),RecoveryComparison::Match(live));
   let wrong=Equilibrium{window:if live.window==8{7}else{8},gate:live.gate};
   assert_eq!(compare_recovered(&rows,epoch,wrong),RecoveryComparison::Mismatch{recovered:live,live:wrong});
   assert_eq!(compare_recovered(&rows[..rows.len()-1],epoch,live),RecoveryComparison::HeadMismatch);
  }
  let mut bad=rows.clone();bad[0].epoch=2;
  assert_eq!(compare_recovered(&bad,1000,live),RecoveryComparison::InvalidHistory);
  assert_eq!(compare_recovered(&rows,1000,Equilibrium{window:2,gate:0}),RecoveryComparison::InvalidLivePolicy);
  assert_eq!(compare_recovered(&rows,1001,live),RecoveryComparison::InvalidHistory);
 }
}

// ADA-327N .dlw — canonical commitment preimage, caller supplies SHA-256.
// The retained anchor must be obtained outside the rollback domain.
pub fn head_preimage(history:&[SealedObservation])->Option<Vec<u8>>{
 recover_observed(history)?;
 let mut bytes=b"ADA-327N:sealed-history:v1\0".to_vec();
 bytes.extend_from_slice(&(history.len() as u32).to_be_bytes());
 for row in history{
  bytes.extend_from_slice(&row.epoch.to_be_bytes());
  for sample in row.samples{
   bytes.push(match sample{None=>0,Some(v)=>1+v as u8});
  }
 }
 Some(bytes)
}
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub struct HeadCommitment{pub epoch:u32,pub digest:[u8;32]}
pub fn recover_committed(history:&[SealedObservation],anchor:&HeadCommitment,sha256:impl FnOnce(&[u8])->[u8;32])->Option<Equilibrium>{
 if history.len()!=anchor.epoch as usize{return None;}
 let bytes=head_preimage(history)?;
 if sha256(&bytes)!=anchor.digest{return None;}
 recover_observed(history)
}
#[cfg(test)]
mod head_commitment_tests{
 use super::*;
 // Test double only: verifies preimage binding and gate wiring, not cryptography.
 fn fake(bytes:&[u8])->[u8;32]{let mut d=[0u8;32];for (i,b) in bytes.iter().enumerate(){d[i%32]^=*b;}d}
 #[test] fn head_boundaries(){
  let rows=vec![SealedObservation{epoch:1,samples:[Some(0);8]},SealedObservation{epoch:2,samples:[None;8]}];
  let bytes=head_preimage(&rows).unwrap();
  let anchor=HeadCommitment{epoch:2,digest:fake(&bytes)};
  assert_eq!(recover_committed(&rows,&anchor,fake),recover_observed(&rows));
  assert_eq!(recover_committed(&rows[..1],&anchor,fake),None);
  let mut changed=rows.clone();changed[0].samples[0]=Some(1);
  assert_ne!(head_preimage(&changed),Some(bytes));
  assert_eq!(recover_committed(&changed,&anchor,fake),None);
  changed[0].epoch=2;
  assert_eq!(head_preimage(&changed),None);
  let prefix=HeadCommitment{epoch:1,digest:fake(&head_preimage(&rows[..1]).unwrap())};
  assert_eq!(recover_committed(&rows[..1],&prefix,fake),recover_observed(&rows[..1]));
 }
}

// ADA-328N .dlw — unified observation-only qualification.
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub enum UnifiedQualification{Rejected,Consistent(Equilibrium),Disagreement{recovered:Equilibrium,live:Equilibrium}}
pub fn qualify_history(history:&[SealedObservation],anchor:&HeadCommitment,live:Equilibrium,sha256:impl FnOnce(&[u8])->[u8;32])->UnifiedQualification{
 if !(3..=8).contains(&live.window)||live.gate>12{return UnifiedQualification::Rejected;}
 match recover_committed(history,anchor,sha256){
  None=>UnifiedQualification::Rejected,
  Some(recovered) if recovered==live=>UnifiedQualification::Consistent(recovered),
  Some(recovered)=>UnifiedQualification::Disagreement{recovered,live},
 }
}
#[cfg(test)]
mod canonical_vector_tests{
 use super::*;
 #[test] fn canonical_bytes(){
  let cases=vec![
   (vec![],"4144412d3332374e3a7365616c65642d686973746f72793a76310000000000"),
   (vec![SealedObservation{epoch:1,samples:[Some(0);8]}],"4144412d3332374e3a7365616c65642d686973746f72793a76310000000001000000010101010101010101"),
   (vec![SealedObservation{epoch:1,samples:[None;8]}],"4144412d3332374e3a7365616c65642d686973746f72793a76310000000001000000010000000000000000"),
   (vec![SealedObservation{epoch:1,samples:[Some(0),Some(1),Some(2),None,Some(0),Some(1),Some(2),None]},SealedObservation{epoch:2,samples:[Some(2);8]}],"4144412d3332374e3a7365616c65642d686973746f72793a76310000000002000000010102030001020300000000020303030303030303")
  ];
  for (rows,expected) in cases{
   let bytes=head_preimage(&rows).unwrap();
   let hex=bytes.iter().map(|b|format!("{b:02x}")).collect::<Vec<_>>().join("");
   assert_eq!(hex,expected);
   // Test-only digest double: the external SHA-256 vectors qualify encoding separately.
   let anchor=HeadCommitment{epoch:rows.len() as u32,digest:[7;32]};
   let live=recover_observed(&rows).unwrap();
   assert_eq!(qualify_history(&rows,&anchor,live,|_|[7;32]),UnifiedQualification::Consistent(live));
   assert_eq!(qualify_history(&rows,&anchor,live,|_|[8;32]),UnifiedQualification::Rejected);
   let wrong=Equilibrium{window:if live.window==8{7}else{8},gate:live.gate};
   assert_eq!(qualify_history(&rows,&anchor,wrong,|_|[7;32]),UnifiedQualification::Disagreement{recovered:live,live:wrong});
  }
 }
}

// ADA-333N .dlw — isolated Linux native provider; no WASM ABI changes.
#[cfg(all(not(target_arch="wasm32"),target_os="linux"))]
pub fn host_sha256(bytes:&[u8])->std::io::Result<[u8;32]>{
 use std::{io::{Write,Error,ErrorKind},process::{Command,Stdio}};
 let mut child=Command::new("/usr/bin/sha256sum").stdin(Stdio::piped()).stdout(Stdio::piped()).stderr(Stdio::null()).spawn()?;
 let result=child.stdin.take().ok_or_else(||Error::new(ErrorKind::Other,"missing stdin")).and_then(|mut input|input.write_all(bytes));
 if let Err(e)=result{let _=child.kill();let _=child.wait();return Err(e);}
 let out=child.wait_with_output()?;
 if !out.status.success(){return Err(Error::new(ErrorKind::Other,"SHA-256 provider failed"));}
 let h=out.stdout.get(..64).ok_or_else(||Error::new(ErrorKind::InvalidData,"short digest"))?;
 let mut digest=[0u8;32];
 for (i,pair) in h.chunks_exact(2).enumerate(){
  let s=std::str::from_utf8(pair).map_err(|e|Error::new(ErrorKind::InvalidData,e))?;
  digest[i]=u8::from_str_radix(s,16).map_err(|e|Error::new(ErrorKind::InvalidData,e))?;
 }
 Ok(digest)
}
#[cfg(all(not(target_arch="wasm32"),target_os="linux"))]
pub fn qualify_host(history:&[SealedObservation],anchor:&HeadCommitment,live:Equilibrium)->std::io::Result<UnifiedQualification>{
 let Some(bytes)=head_preimage(history) else{return Ok(UnifiedQualification::Rejected)};
 let digest=host_sha256(&bytes)?;
 Ok(qualify_history(history,anchor,live,|_|digest))
}
#[cfg(all(test,target_os="linux",not(target_arch="wasm32")))]
mod host_sha256_tests{
 use super::*;
 #[test] fn standard_provider(){
  let fixtures=[
   (vec![],"ce8eb3cb9a0c38e5b6d0ed5ce91c2a629e29219df1e932b84e8222fe5f69676d"),
   (vec![SealedObservation{epoch:1,samples:[Some(0);8]}],"9c8923ac6e8e15d3c44767cc3c4a692890878b83820535317c11a30bcb3185f0"),
   (vec![SealedObservation{epoch:1,samples:[None;8]}],"c57648266492f5b2091f33543103297741d184bb96e2388a7621ceea0776265d"),
   (vec![SealedObservation{epoch:1,samples:[Some(0),Some(1),Some(2),None,Some(0),Some(1),Some(2),None]},SealedObservation{epoch:2,samples:[Some(2);8]}],"08a8dfe5ec7accbc78869f5c617af473e07b1987b161dcbce7d95ae6cc9538d5")
  ];
  for (rows,expected) in fixtures{
   let digest=host_sha256(&head_preimage(&rows).unwrap()).unwrap();
   assert_eq!(digest.iter().map(|b|format!("{b:02x}")).collect::<Vec<_>>().join(""),expected);
   let mut anchor=HeadCommitment{epoch:rows.len() as u32,digest};
   let live=recover_observed(&rows).unwrap();
   assert_eq!(qualify_host(&rows,&anchor,live).unwrap(),UnifiedQualification::Consistent(live));
   anchor.digest[0]^=1;
   assert_eq!(qualify_host(&rows,&anchor,live).unwrap(),UnifiedQualification::Rejected);
  }
 }
}

// ADA-335N .dlw — combined observation receipt; neither result activates policy.
#[cfg(all(target_os="linux",not(target_arch="wasm32")))]
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub struct QualificationReceipt{
 pub synthetic:Differential,
 pub observed:UnifiedQualification,
}
#[cfg(all(target_os="linux",not(target_arch="wasm32")))]
pub fn qualification_receipt(g:u32,history:&[SealedObservation],anchor:&HeadCommitment,live:Equilibrium)->std::io::Result<QualificationReceipt>{
 let synthetic=compare_periodic(g);
 let observed=if g>24000||g/24!=anchor.epoch{UnifiedQualification::Rejected}else{qualify_host(history,anchor,live)?};
 Ok(QualificationReceipt{synthetic,observed})
}
#[cfg(all(test,target_os="linux",not(target_arch="wasm32")))]
mod qualification_receipt_tests{
 use super::*;
 #[test] fn combined_boundaries(){
  let rows=[SealedObservation{epoch:1,samples:[Some(0);8]}];
  let live=recover_observed(&rows).unwrap();
  let mut anchor=HeadCommitment{epoch:1,digest:host_sha256(&head_preimage(&rows).unwrap()).unwrap()};
  let receipt=qualification_receipt(24,&rows,&anchor,live).unwrap();
  assert!(matches!(receipt.synthetic,Differential::Match(_)));
  assert_eq!(receipt.observed,UnifiedQualification::Consistent(live));
  assert_eq!(qualification_receipt(0,&rows,&anchor,live).unwrap().observed,UnifiedQualification::Rejected);
  assert_eq!(qualification_receipt(24001,&rows,&anchor,live).unwrap().synthetic,Differential::OutsideHorizon);
  assert_eq!(qualification_receipt(24,&[],&anchor,live).unwrap().observed,UnifiedQualification::Rejected);
  let wrong=Equilibrium{window:7,gate:0};
  assert_eq!(qualification_receipt(24,&rows,&anchor,wrong).unwrap().observed,UnifiedQualification::Disagreement{recovered:live,live:wrong});
  anchor.digest[0]^=1;
  assert_eq!(qualification_receipt(24,&rows,&anchor,live).unwrap().observed,UnifiedQualification::Rejected);
 }
}

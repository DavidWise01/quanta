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

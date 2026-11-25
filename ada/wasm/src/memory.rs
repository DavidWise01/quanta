//! ADA-274N .dlw — append-only contextual memory and rotating address view.
use crate::clock::{Clock,MAX_GENERATION};
use ada_quanta::MEMORY_WINDOW;
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub struct Observation { generation:u32, value:Option<i8> }
impl Observation {
 pub fn generation(self)->u32 {self.generation}
 pub fn value(self)->Option<i8>{self.value}
 pub fn address(self)->usize{self.generation as usize % MEMORY_WINDOW}
}
#[derive(Default)]
pub struct ContextMemory { history:Vec<Observation> }
impl ContextMemory {
 pub fn history(&self)->&[Observation]{&self.history}
 pub fn append(&mut self,generation:u32,value:Option<i8>)->Result<(), &'static str>{
  if generation>MAX_GENERATION || generation as usize!=self.history.len(){return Err("nonsequential generation");}
  if value.is_some_and(|v|!(-1..=1).contains(&v)){return Err("invalid ternary observation");}
  self.history.push(Observation{generation,value});Ok(())
 }
 pub fn recent(&self)->&[Observation]{&self.history[self.history.len().saturating_sub(MEMORY_WINDOW)..]}
 pub fn slot(&self,address:usize)->Option<Observation>{
  if address>=MEMORY_WINDOW{return None;}
  self.recent().iter().rev().find(|r|r.address()==address).copied()
 }
}
/// Resolve the latest generation occupying an address at a specified generation.
/// This stateless export exposes addressing, not a persistent browser ledger.
#[no_mangle]
pub extern "C" fn ada_memory_generation(g:u32,address:u32)->u32{
 let Some(c)=Clock::at(g) else{return u32::MAX};
 if address>=MEMORY_WINDOW as u32{return u32::MAX;}
 let delta=(c.memory+MEMORY_WINDOW as u32-address)%MEMORY_WINDOW as u32;
 g.checked_sub(delta).unwrap_or(u32::MAX)
}
#[cfg(test)]
mod tests{
 use super::*;
 #[test] fn wrap_preserves_history(){
  let mut m=ContextMemory::default();
  for g in 0..361 {m.append(g,Some((g%3) as i8-1)).unwrap();}
  assert_eq!(m.history().len(),361);
  assert_eq!(m.history()[0].generation(),0);
  assert_eq!(m.slot(0).unwrap().generation(),360);
  assert_eq!(m.recent()[0].generation(),353);
 }
 #[test] fn missing_is_not_neutral(){
  let mut m=ContextMemory::default();
  m.append(0,None).unwrap();m.append(1,Some(0)).unwrap();
  assert_eq!(m.slot(0).unwrap().value(),None);
  assert_eq!(m.slot(1).unwrap().value(),Some(0));
  assert_eq!(m.slot(2),None);
 }
 #[test] fn reject_without_mutation(){
  let mut m=ContextMemory::default();m.append(0,Some(1)).unwrap();
  assert!(m.append(0,Some(-1)).is_err());
  assert!(m.append(2,None).is_err());
  assert!(m.append(1,Some(2)).is_err());
  assert_eq!(m.history().len(),1);
 }
 #[test] fn scalar_view_parity(){
  let mut m=ContextMemory::default();
  for g in 0..2400 {m.append(g,None).unwrap();
   for a in 0..8 {assert_eq!(ada_memory_generation(g,a),m.slot(a as usize).map(|r|r.generation()).unwrap_or(u32::MAX));}
  }
  assert_eq!(ada_memory_generation(0,8),u32::MAX);
  assert_eq!(ada_memory_generation(u32::MAX,0),u32::MAX);
 }
}

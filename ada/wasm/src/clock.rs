//! ADA-273N .dlw — deterministic logical clock.
use ada_quanta::{EPOCH_SIZE,MEMORY_WINDOW};
pub const CYCLE:u32=360;
pub const MAX_GENERATION:u32=u32::MAX-1;
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub struct Clock {pub generation:u32,pub epoch:u32,pub slot:u32,pub memory:u32,pub tick:u32,pub sector:u32}
impl Clock {
 pub fn at(g:u32)->Option<Self>{
  if g>MAX_GENERATION{return None;}
  let tick=g%CYCLE;
  Some(Self{generation:g,epoch:g/EPOCH_SIZE as u32,slot:g%EPOCH_SIZE as u32,memory:g%MEMORY_WINDOW as u32,tick,sector:tick/120})
 }
 pub fn advance(self,steps:u32)->Option<Self>{Self::at(self.generation.checked_add(steps)?)}
}
#[no_mangle]
pub extern "C" fn ada_clock_field(g:u32,field:u32)->u32{
 let Some(c)=Clock::at(g) else{return u32::MAX};
 match field {0=>c.generation,1=>c.epoch,2=>c.slot,3=>c.memory,4=>c.tick,5=>c.sector,_=>u32::MAX}
}
#[no_mangle]
pub extern "C" fn ada_clock_advance(g:u32,steps:u32)->u32{
 Clock::at(g).and_then(|c|c.advance(steps)).map(|c|c.generation).unwrap_or(u32::MAX)
}
#[cfg(test)]
mod tests{
 use super::*;
 #[test] fn boundaries(){
  assert_eq!(Clock::at(23).unwrap().slot,23);
  assert_eq!(Clock::at(24).unwrap().epoch,1);
  assert_eq!(Clock::at(24).unwrap().slot,0);
  assert_eq!(Clock::at(8).unwrap().memory,0);
  assert_eq!(Clock::at(120).unwrap().sector,1);
  assert_eq!(Clock::at(240).unwrap().sector,2);
  assert_eq!(Clock::at(360).unwrap().tick,0);
 }
 #[test] fn deterministic(){
  for g in 0..2400 {let c=Clock::at(g).unwrap();assert_eq!(c.advance(1),Clock::at(g+1));}
 }
 #[test] fn rejects_overflow(){
  assert_eq!(ada_clock_advance(MAX_GENERATION,1),u32::MAX);
  assert_eq!(ada_clock_advance(u32::MAX,0),u32::MAX);
  assert_eq!(ada_clock_field(0,6),u32::MAX);
 }
}

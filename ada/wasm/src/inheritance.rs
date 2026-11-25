//! ADA-277N .dlw — generational observation snapshots, no action API.
use crate::{clock::Clock,pumps::{Pump,pumps}};
use ada_quanta::{EPOCH_SIZE,MEMORY_WINDOW};
#[derive(Clone,Debug,PartialEq)]
pub struct Frame {pub clock:Clock,pub pumps:[Pump;3]}
#[derive(Clone,Debug,PartialEq)]
pub struct Receipt {pub epoch:usize,pub sealed:bool,pub opening:Vec<Frame>,pub closing:Vec<Frame>}
#[derive(Default)]
pub struct History {frames:Vec<Frame>}
impl History {
 pub fn frames(&self)->&[Frame]{&self.frames}
 pub fn append(&mut self,g:u32)->Result<(), &'static str>{
  if g as usize!=self.frames.len(){return Err("nonsequential generation")}
  let clock=Clock::at(g).ok_or("invalid clock")?;
  let pumps=pumps(g).ok_or("invalid pumps")?;
  self.frames.push(Frame{clock,pumps});Ok(())
 }
 pub fn receipts(&self)->Vec<Receipt>{
  self.frames.chunks(EPOCH_SIZE).enumerate().map(|(epoch,chunk)|{
   let start=epoch*EPOCH_SIZE;let end=start+chunk.len();
   Receipt{epoch,sealed:chunk.len()==EPOCH_SIZE,opening:self.frames[start.saturating_sub(MEMORY_WINDOW)..start].to_vec(),closing:self.frames[end.saturating_sub(MEMORY_WINDOW)..end].to_vec()}
  }).collect()
 }
}
/// Stateless address view; no browser persistence is implied.
#[no_mangle]
pub extern "C" fn ada_inherited_generation(epoch:u32,slot:u32)->u32{
 if epoch==0||slot>=MEMORY_WINDOW as u32{return u32::MAX}
 let Some(start)=epoch.checked_mul(EPOCH_SIZE as u32) else{return u32::MAX};
 if Clock::at(start).is_none(){return u32::MAX}
 start-MEMORY_WINDOW as u32+slot
}
#[cfg(test)]
mod tests{
 use super::*;
 #[test] fn inheritance(){
 let mut h=History::default();for g in 0..24{h.append(g).unwrap();}
 let sealed=h.receipts()[0].clone();
 for g in 24..361{h.append(g).unwrap();}
 let r=h.receipts();assert_eq!(r[0],sealed);
 for w in r.windows(2){assert_eq!(w[0].closing,w[1].opening);for (i,f) in w[1].opening.iter().enumerate(){assert_eq!(ada_inherited_generation(w[1].epoch as u32,i as u32),f.clock.generation);}}
 assert_eq!(h.frames()[360].clock.tick,0);assert_eq!(h.frames()[360].pumps,h.frames()[0].pumps);
 assert!(h.append(360).is_err());assert_eq!(h.frames().len(),361);
 }
 #[test] fn invalid(){assert_eq!(ada_inherited_generation(0,0),u32::MAX);assert_eq!(ada_inherited_generation(1,8),u32::MAX);assert_eq!(ada_inherited_generation(u32::MAX,0),u32::MAX);}
}

//! ADA-276N .dlw — synthetic phase partition.
use crate::{clock::Clock,geometry::project};
#[derive(Clone,Copy,Debug,PartialEq)]
pub struct Pump {pub phase:u32,pub intensity:f64,pub position:[f64;3]}
pub fn pumps(g:u32)->Option<[Pump;3]> {
 let c=Clock::at(g)?;
 let mut out=[Pump{phase:0,intensity:0.0,position:[0.0;3]};3];
 for (i,p) in out.iter_mut().enumerate(){
  let phase=(c.tick+120*i as u32)%360;
  let t=f64::from(phase)*core::f64::consts::PI/180.0;
  *p=Pump{phase,intensity:(1.0+t.cos())/3.0,position:project(1<<i,phase)?};
 } Some(out)
}
#[no_mangle]
pub extern "C" fn ada_pump_field(g:u32,pump:u32,field:u32)->f64{
 let Some(p)=pumps(g).and_then(|p|p.get(pump as usize).copied()) else{return f64::NAN};
 match field{0=>f64::from(p.phase),1=>p.intensity,2..=4=>p.position[(field-2) as usize],_=>f64::NAN}
}
#[cfg(test)]
mod tests {use super::*;#[test] fn cycle(){for g in 0..360{let p=pumps(g).unwrap();assert_eq!(p,pumps(g+360).unwrap());assert!((p.iter().map(|p|p.intensity).sum::<f64>()-1.0).abs()<1e-12);for i in 0..3{assert_eq!((p[(i+1)%3].phase+360-p[i].phase)%360,120);}}}}

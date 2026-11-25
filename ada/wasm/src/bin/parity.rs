//! ADA-279N .dlw — native scalar reference stream.
use ada_browser::*;
fn row(name:&str,args:&[u32],value:f64,kind:&str){
 println!("{}\t{}\t{}\t{}",name,args.iter().map(u32::to_string).collect::<Vec<_>>().join(","),value,kind);
}
fn main(){
 for g in 0..720 {
  for f in 0..6 {row("ada_clock_field",&[g,f],clock::ada_clock_field(g,f) as f64,"u");}
  for a in 0..8 {row("ada_memory_generation",&[g,a],memory::ada_memory_generation(g,a) as f64,"u");}
  for v in 0..16 {for a in 0..3{row("ada_tesseract_coordinate",&[v,g,a],geometry::ada_tesseract_coordinate(v,g,a),"f");}}
  for p in 0..3 {for f in 0..5{row("ada_pump_field",&[g,p,f],pumps::ada_pump_field(g,p,f),"f");}}
  for f in 0..2{row("ada_equilibrium_field",&[g,f],equilibrium::ada_equilibrium_field(g,f) as f64,"u");}
  row("ada_clock_advance",&[g,24],clock::ada_clock_advance(g,24) as f64,"u");
 }
 for e in 0..32 {for s in 0..8 {row("ada_inherited_generation",&[e,s],inheritance::ada_inherited_generation(e,s) as f64,"u");}}
 for e in 0..32 {for s in 0..2 {row("ada_tesseract_edge",&[e,s],geometry::ada_tesseract_edge(e,s) as f64,"u");}}
 for i in -1..=1 {for s in 0..3 {println!("ada_consequence\t{},{}\t{}\ti",i,s,ada_consequence(i,s));}}
 row("ada_clock_field",&[u32::MAX,0],u32::MAX as f64,"u");
 row("ada_tesseract_coordinate",&[16,0,0],f64::NAN,"f");
 row("ada_pump_field",&[0,3,0],f64::NAN,"f");
 row("ada_equilibrium_field",&[24001,0],u32::MAX as f64,"u");
}

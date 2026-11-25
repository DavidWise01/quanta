//! ADA-275N .dlw — four-dimensional hypercube geometry.
pub fn vertex(id:u32)->Option<[f64;4]> {
 if id>=16{return None}
 Some(core::array::from_fn(|axis|if id&(1<<axis)==0{-1.0}else{1.0}))
}
pub fn edge(id:u32)->Option<(u32,u32)> {
 if id>=32{return None}
 let axis=id/8;let k=id%8;let low=k&((1<<axis)-1);
 let a=low|((k>>axis)<<(axis+1));Some((a,a|(1<<axis)))
}
fn rotate(p:&mut [f64;4],a:usize,b:usize,t:f64){
 let (s,c)=t.sin_cos();let (x,y)=(p[a],p[b]);p[a]=c*x-s*y;p[b]=s*x+c*y;
}
pub fn project(id:u32,tick:u32)->Option<[f64;3]>{
 let mut p=vertex(id)?;let t=f64::from(tick%360)*core::f64::consts::PI/180.0;
 rotate(&mut p,0,3,t);rotate(&mut p,1,2,t);
 let scale=3.0/(4.0-p[3]);Some([p[0]*scale,p[1]*scale,p[2]*scale])
}
#[no_mangle]
pub extern "C" fn ada_tesseract_coordinate(id:u32,tick:u32,axis:u32)->f64{
 project(id,tick).and_then(|p|p.get(axis as usize).copied()).unwrap_or(f64::NAN)
}
#[no_mangle]
pub extern "C" fn ada_tesseract_edge(id:u32,end:u32)->u32{
 match (edge(id),end){(Some((a,_)),0)=>a,(Some((_,b)),1)=>b,_=>u32::MAX}
}
#[cfg(test)]
mod tests{
 use super::*;
 #[test] fn topology(){
 let mut degree=[0;16];let mut edges=std::collections::BTreeSet::new();
 for i in 0..32{let(a,b)=edge(i).unwrap();assert_eq!((a^b).count_ones(),1);assert!(edges.insert((a,b)));degree[a as usize]+=1;degree[b as usize]+=1;}
 assert_eq!(degree,[4;16]);assert!(edge(32).is_none());
 }
 #[test] fn projection(){
 for tick in 0..360{for id in 0..16{let p=project(id,tick).unwrap();assert!(p.iter().all(|x|x.is_finite()));assert_eq!(p,project(id,tick+360).unwrap());}}
 assert!(ada_tesseract_coordinate(16,0,0).is_nan());assert!(ada_tesseract_coordinate(0,0,3).is_nan());
 }
}

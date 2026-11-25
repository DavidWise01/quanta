//! RQT-693: deterministic addresses in a single frozen 1|1|3|1 universe snapshot.
//! Addresses are observational indices, not physical measurements or Root-19 solutions.
use serde_json::{json, Value};
use std::collections::BTreeSet;

const GRAMMAR:&str="{{brace[[box((torroid))]]}}^{{n}}^[[n]]^((n))";
const FOCUS:&str="CENTER{[(FOCUS)]}";
const POSITIONS:[&str;8]=[
 "upperleftrear","centerleftrear","lowerleftrear","centerupper",
 "centerlower","upperrightfront","centerrightfront","lowerrightfront"
];
const FACES:[&str;6]=["front","back","left","right","top","bottom"];
const TIMES:[&str;3]=["past","present","future"];
const ROLES:[&str;3]=["observes","deserves","reserves"];
const BAND:[u8;4]=[1,1,3,1];

/// Canonical string address: 1/<time>/<face>/<position>/<T-or-B history>
/// "1" is the immutable snapshot index; y[n(m)] is a nested present payload,
/// not three separately evolving states.
/// Faces index views of the *3D projected observation*, not actual 4D facets.
fn address(time:&str,face:&str,position:&str,path:&str)->String{
 format!("1/{time}/{face}/{position}/{}",if path.is_empty() {"ROOT"} else {path})
}
fn verify(depth:usize)->Value{
 assert!(depth<=12,"bounded address materialization");
 assert_eq!(BAND,[1,1,3,1]);
 assert_eq!(POSITIONS.len(),8);
 assert_eq!(FACES.len(),6);
 assert_eq!(TIMES.len(),3);
 let paths:Vec<String>=(0..(1usize<<depth)).map(|n|
   (0..depth).rev().map(|bit|if ((n>>bit)&1)==0 {'T'} else {'B'}).collect()
 ).collect();
 let mut addresses=BTreeSet::new();
 let mut observed_per_time=[0usize;3];
 for (ti,&time) in TIMES.iter().enumerate(){
   for &face in &FACES{
     for &position in &POSITIONS{
       for path in &paths{
         assert!(addresses.insert(address(time,face,position,path)));
         observed_per_time[ti]+=1;
       }
     }
   }
 }
 let spatial_nodes=8usize*(1usize<<depth);
 let expected=spatial_nodes*6*3;
 assert_eq!(addresses.len(),expected);
 assert_eq!(observed_per_time,[spatial_nodes*6;3]);
 assert!(!POSITIONS.contains(&"CENTER"));
 let example=address("present","front","upperleftrear","TB");
 assert_eq!(example,"1/present/front/upperleftrear/TB");
 json!({
  "rqt":693,"scope":"representational addressing only; no astrophysical or integral-root proof",
  "single_snapshot_id":1,"snapshot_count":1,"interior_count":1,
  "temporal_bands":BAND,"time_channels":TIMES,"temporal_roles":ROLES,
  "nested_present":"y[n(m)]","present_expression_is_not_three_independent_snapshots":true,
  "per_position_quanta_grammar":GRAMMAR,"focus":FOCUS,"focus_count":1,
  "positions":POSITIONS,"recursive_path_alphabet":["T","B"],"depth":depth,
  "spatial_branch_nodes_at_depth":spatial_nodes,
  "observational_projection_faces":FACES,
  "projected_face_count":6,"actual_4d_hypercube_cubic_boundary_cells":8,
  "view_address_count":addresses.len(),"addresses_per_time":observed_per_time,
  "addresses_unique":true,
  "sample_address":example,
  "root19_status":"OPEN"
 })
}
fn main(){
 let depth:usize=std::env::args().nth(1)
   .map(|s|s.parse().expect("depth must be nonnegative integer")).unwrap_or(4);
 println!("{}",serde_json::to_string_pretty(&verify(depth)).unwrap());
}
#[cfg(test)]
mod tests{
 use super::*;
 #[test]
 fn unique_addresses_frozen_snapshot(){
   for d in 0..=8{
     let v=verify(d);
     assert_eq!(v["snapshot_count"],1);
     assert_eq!(v["focus_count"],1);
     assert_eq!(v["view_address_count"].as_u64().unwrap(),(8*6*3*(1usize<<d)) as u64);
   }
 }
 #[test]
 fn top_bottom_paths_not_collapsed(){
   let a=address("past","front","upperleftrear","T");
   let b=address("past","front","upperleftrear","B");
   assert_ne!(a,b);
   assert_ne!(address("past","front","upperleftrear","T"),
              address("future","front","upperleftrear","T"));
   assert_ne!(address("past","front","upperleftrear","T"),
              address("past","back","upperleftrear","T"));
 }
}

//! RQT-692 — one 1|1|3|1 universe snapshot.
//! Representational geometry, not an astronomical observation or root-19 proof.
//! Six labeled faces belong to the 3D observation cube/projection;
//! a 4D hypercube has eight cubic boundary cells.
use serde_json::{json, Value};
use std::collections::BTreeSet;

const QUANTA_GRAMMAR: &str = "{{brace[[box((torroid))]]}}^{{n}}^[[n]]^((n))";
const FOCUS: &str = "CENTER{[(FOCUS)]}";
const POSITIONS: [&str; 8] = [
    "upperleftrear", "centerleftrear", "lowerleftrear", "centerupper",
    "centerlower", "upperrightfront", "centerrightfront", "lowerrightfront"
];
const PROJECTED_FACES: [&str; 6] = [
    "front", "back", "left", "right", "top", "bottom"
];
const HYPERCUBE_BOUNDARY_CELLS: [&str; 8] = [
    "x-", "x+", "y-", "y+", "z-", "z+", "w-", "w+"
];

/// A closed immutable representation of one snapshot, not a time series.
/// 1 | 1 | 3 | 1 is retained as four *ordered semantic bands*.
/// 3 = the three ordered nested present symbols y[n(m)], not three moments.
#[derive(Debug, Clone, PartialEq, Eq)]
struct UniverseSnap {
    bands: [usize; 4],
    past: &'static str,
    present: &'static str,
    nested_present: [&'static str; 3],
    future: &'static str,
    interior_count: usize,
    focus: &'static str,
    snapshot_count: usize,
    projection_faces: [&'static str; 6],
    spatial_positions: [&'static str; 8],
}
impl UniverseSnap {
    fn new() -> Self {
        Self {
            bands: [1, 1, 3, 1],
            past: "observes",
            present: "deserves",
            nested_present: ["y", "n", "m"],
            future: "reserves",
            interior_count: 1,
            focus: FOCUS,
            snapshot_count: 1,
            projection_faces: PROJECTED_FACES,
            spatial_positions: POSITIONS,
        }
    }
    fn validate(&self) {
        assert_eq!(self.bands, [1,1,3,1]);
        assert_eq!(self.nested_present, ["y","n","m"]);
        assert_eq!(self.interior_count, 1);
        assert_eq!(self.snapshot_count, 1);
        assert_eq!(self.focus, FOCUS);
        assert_eq!(self.projection_faces.len(), 6);
        assert_eq!(HYPERCUBE_BOUNDARY_CELLS.len(), 8);
        assert_eq!(self.spatial_positions.len(), 8);
        assert_eq!(self.projection_faces.iter().collect::<BTreeSet<_>>().len(), 6);
        assert_eq!(self.spatial_positions.iter().collect::<BTreeSet<_>>().len(), 8);
        assert!(!self.spatial_positions.contains(&"CENTER"));
    }
    fn observations(&self, depth: usize) -> Value {
        self.validate();
        assert!(depth<=12,"bounded structural materialization");
        let mut addresses = BTreeSet::new();
        let count = 1usize<<depth;
        for &position in self.spatial_positions.iter() {
            for ordinal in 0..count {
                let path = (0..depth).rev()
                    .map(|bit| if (ordinal>>bit)&1==0 {'T'} else {'B'})
                    .collect::<String>();
                assert!(addresses.insert(format!("{position}/{path}")));
            }
        }
        assert_eq!(addresses.len(),8*count);
        json!({
          "rqt":692,
          "snapshot_model":"ONE universe snapshot (declared representational model)",
          "bands_1131":self.bands,
          "past":{"count":1,"role":self.past},
          "present":{"count":1,"role":self.present,
                     "nested_expression":"y[n(m)]",
                     "nested_symbols":self.nested_present},
          "future":{"count":1,"role":self.future},
          "hypercube_interior_count":self.interior_count,
          "focus":self.focus,
          "quanta_per_position":QUANTA_GRAMMAR,
          "peripheral_positions":self.spatial_positions,
          "top_bottom_recursive_depth":depth,
          "peripheral_nodes_at_depth":addresses.len(),
          "distinct_addresses_verified":true,
          "observational_projection":{
              "type":"3D cubical observation of 4D hypercube model",
              "face_count":6,"faces":self.projection_faces
          },
          "mathematical_4d_boundary":{
              "cubic_cell_count":8,
              "axis_signed_cells":HYPERCUBE_BOUNDARY_CELLS
          },
          "snapshot_count":self.snapshot_count,
          "root19_status":"OPEN",
          "limits":"topological snapshot only; not evidence of physical cosmology or original integral root19"
        })
    }
}
fn main(){
    let depth: usize = std::env::args().nth(1)
        .map(|v| v.parse().expect("depth must be an integer"))
        .unwrap_or(4);
    println!("{}",serde_json::to_string_pretty(&UniverseSnap::new().observations(depth)).unwrap());
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn single_snapshot_three_nested_symbols_and_six_observed_faces() {
        let s=UniverseSnap::new();
        s.validate();
        assert_eq!(s.snapshot_count,1);
        assert_eq!(s.interior_count,1);
        assert_eq!(s.nested_present,["y","n","m"]);
    }
    #[test]
    fn preserves_distinction_between_six_faces_and_eight_4d_cells() {
        assert_eq!(PROJECTED_FACES.len(),6);
        assert_eq!(HYPERCUBE_BOUNDARY_CELLS.len(),8);
    }
    #[test]
    fn recursion_preserves_origin_and_frozen_focus(){
        for d in 0..=8 {
            let v=UniverseSnap::new().observations(d);
            assert_eq!(v["peripheral_nodes_at_depth"].as_u64().unwrap(),8u64<<d);
            assert_eq!(v["focus"],FOCUS);
            assert_eq!(v["snapshot_count"],1);
        }
    }
}

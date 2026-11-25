//! RQT-691: user's canonical recursive Quanta spatial grammar.
//! This is a topology/address verifier, not a quadratic-form or root certificate.
use serde_json::json;
use std::collections::BTreeSet;

const GRAMMAR: &str = "{{brace[[box((torroid))]]}}^{{n}}^[[n]]^((n))";
const POSITIONS: [&str; 8] = [
    "upperleftrear", "centerleftrear", "lowerleftrear", "centerupper",
    "centerlower", "upperrightfront", "centerrightfront", "lowerrightfront"
];
const CENTER: &str = "CENTER{[(FOCUS)]}";

#[derive(Clone, Debug, Eq, PartialEq)]
struct Node { position: &'static str, path: String }
impl Node {
    fn children(&self) -> [Node;2] {
        [Node {position:self.position,path:format!("{}T",self.path)},
         Node {position:self.position,path:format!("{}B",self.path)}]
    }
}
fn level(depth:usize)->Vec<Node> {
    assert!(depth<=16,"bounded report depth");
    let mut nodes:Vec<Node>=POSITIONS.iter()
        .map(|&position|Node{position,path:String::new()}).collect();
    for _ in 0..depth {
        nodes=nodes.iter().flat_map(Node::children).collect();
    }
    nodes
}
fn verify(depth:usize)->serde_json::Value {
    let mut seen=BTreeSet::new();
    let mut leaves=0usize;
    for node in level(depth) {
        assert_eq!(node.path.len(),depth);
        assert!(node.path.chars().all(|c| c=='T'||c=='B'));
        assert!(seen.insert((node.position,node.path.clone())));
        leaves+=1;
    }
    let expected=8usize.checked_shl(depth as u32).unwrap();
    assert_eq!(leaves,expected);
    assert_eq!(POSITIONS.len(),8);
    assert!(!POSITIONS.contains(&"CENTER"));
    json!({
        "rqt":691,
        "canonical_expression":GRAMMAR,
        "center":CENTER,
        "center_count":1,
        "positions":POSITIONS,
        "recursive_slot_symbol":"{{|}}",
        "branch_order":["top","bottom"],
        "path_alphabet":["T","B"],
        "depth":depth,
        "peripheral_nodes_at_depth":leaves,
        "total_peripheral_nodes_through_depth":8*((1usize << (depth+1))-1),
        "center_is_immutable":true,
        "root19":"OPEN",
        "scope":"structural recursion only; no claim of integer norm -2 root"
    })
}
fn main() {
    let depth:usize=std::env::args().nth(1)
        .map(|s|s.parse().expect("depth must be a nonnegative integer"))
        .unwrap_or(8);
    println!("{}",serde_json::to_string_pretty(&verify(depth)).unwrap());
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn nine_positions_one_is_focus() {
        assert_eq!(POSITIONS.len(),8);
        assert_eq!(CENTER,"CENTER{[(FOCUS)]}");
        assert_eq!(GRAMMAR,"{{brace[[box((torroid))]]}}^{{n}}^[[n]]^((n))");
    }
    #[test]
    fn binary_branch_preserves_identity() {
        for depth in 0..=8 {
            let report=verify(depth);
            assert_eq!(report["peripheral_nodes_at_depth"].as_u64().unwrap(),8u64<<depth);
        }
        let seed=Node{position:POSITIONS[0],path:"TB".into()};
        let [top,bottom]=seed.children();
        assert_eq!(top.path,"TBT");
        assert_eq!(bottom.path,"TBB");
        assert_eq!(top.position,bottom.position);
    }
}

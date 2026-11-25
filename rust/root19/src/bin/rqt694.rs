//! RQT-694: append-only observations of one immutable 1|1|3|1 Quanta snapshot.
//! The evidence chain witnesses only deterministic software state, not independent
//! physical observation and NOT an integer Root-19 certificate.
use serde_json::{json, Value};
use sha2::{Digest, Sha256};
use std::collections::BTreeSet;
use std::fmt::Write;

const GRAMMAR: &str = "{{brace[[box((torroid))]]}}^{{n}}^[[n]]^((n))";
const FOCUS: &str = "CENTER{[(FOCUS)]}";
const POSITIONS: [&str; 8] = [
 "upperleftrear","centerleftrear","lowerleftrear","centerupper",
 "centerlower","upperrightfront","centerrightfront","lowerrightfront"
];
const FACES: [&str;6] = ["front","back","left","right","top","bottom"];
const PHASES: [&str;3] = ["past","present","future"];
const ROLES: [&str;3] = ["observes","deserves","reserves"];
const TIME_BANDS: [u8;4] = [1,1,3,1];

fn sha(bytes: &[u8]) -> String {
    let hash = Sha256::digest(bytes);
    let mut s = String::with_capacity(64);
    for b in hash { write!(&mut s, "{b:02x}").unwrap(); }
    s
}
#[derive(Clone, Debug, PartialEq, Eq)]
struct FrozenSnapshot {
    id: u8,
    one_interior: u8,
    one_focus: &'static str,
    six_projection_faces: [&'static str;6],
    eight_spatial_roots: [&'static str;8],
    temporal_bands: [u8;4],
    nested_present: &'static str,
    quanta_grammar: &'static str,
}
impl FrozenSnapshot {
    fn canonical() -> Self { Self {
        id:1,one_interior:1,one_focus:FOCUS,
        six_projection_faces:FACES,eight_spatial_roots:POSITIONS,
        temporal_bands:TIME_BANDS,nested_present:"y[n(m)]",
        quanta_grammar:GRAMMAR,
    }}
    fn digest(&self)->String {
        sha(format!("snapshot:{}|interior:{}|focus:{}|faces:{}|positions:{}|bands:1131|nested:{}|grammar:{}",
            self.id,self.one_interior,self.one_focus,FACES.join(","),
            POSITIONS.join(","),self.nested_present,self.quanta_grammar).as_bytes())
    }
}
fn valid_address(phase:&str,face:&str,position:&str,path:&str)->bool{
    PHASES.contains(&phase) && FACES.contains(&face)
        && POSITIONS.contains(&position) && path.len()<=12
        && path.chars().all(|c| c=='T'||c=='B')
}
fn address(phase:&str,face:&str,position:&str,path:&str)->String{
    format!("1/{phase}/{face}/{position}/{}",if path.is_empty() {"ROOT"} else {path})
}
#[derive(Clone, Debug)]
struct Observation {
    index:usize,
    phase: String,
    addr:String,
    note:String,
    previous_hash:String,
    event_hash:String,
}
impl Observation {
    fn digest(&self,snapshot_digest:&str)->String{
        // Length-delimited fields avoid ambiguous concatenations.
        let fields=[
            self.index.to_string(),self.phase.clone(),self.addr.clone(),
            self.note.clone(),self.previous_hash.clone(),snapshot_digest.to_owned()
        ];
        let mut bytes=Vec::new();
        for s in fields {
            bytes.extend_from_slice(&(s.len() as u64).to_be_bytes());
            bytes.extend_from_slice(s.as_bytes());
        }
        sha(&bytes)
    }
}
struct Ledger{
    frozen:FrozenSnapshot,
    snapshot_digest:String,
    events:Vec<Observation>,
}
impl Ledger {
    fn new()->Self{
        let frozen=FrozenSnapshot::canonical();
        let snapshot_digest=frozen.digest();
        Self{frozen,snapshot_digest,events:Vec::new()}
    }
    fn append(&mut self,phase:&str,face:&str,position:&str,path:&str,note:&str)->Result<(),String>{
        if !valid_address(phase,face,position,path){return Err("invalid observational address".into());}
        if position=="CENTER" {return Err("center cannot be a recursive root".into());}
        let phase_ord=PHASES.iter().position(|v|*v==phase).unwrap();
        if let Some(last)=self.events.last(){
            let old=PHASES.iter().position(|v|*v==last.phase).unwrap();
            if phase_ord<old{return Err("retroactive temporal phase reorder".into());}
        }
        if note.len()>256{return Err("observation note too large".into());}
        let previous_hash=self.events.last().map(|v|v.event_hash.clone())
            .unwrap_or_else(||self.snapshot_digest.clone());
        let mut event=Observation{
            index:self.events.len(),phase:phase.to_string(),
            addr:address(phase,face,position,path),note:note.to_string(),
            previous_hash,event_hash:String::new()
        };
        event.event_hash=event.digest(&self.snapshot_digest);
        self.events.push(event);
        self.verify()?;
        Ok(())
    }
    fn verify(&self)->Result<(),String>{
        if self.frozen!=FrozenSnapshot::canonical() ||
           self.snapshot_digest!=self.frozen.digest(){
            return Err("frozen snapshot changed".into());
        }
        let mut previous=self.snapshot_digest.clone();
        let mut last_phase=0usize;
        for (i,event) in self.events.iter().enumerate(){
            let phase_idx=PHASES.iter().position(|p|*p==event.phase)
                .ok_or_else(||"unknown phase".to_string())?;
            if phase_idx<last_phase{return Err("phase order regressed".into());}
            let segments:Vec<_>=event.addr.split('/').collect();
            if segments.len()!=5 || segments[0]!="1" || segments[1]!=event.phase {
                return Err("address is not canonical".into());
            }
            let path=if segments[4]=="ROOT"{""} else {segments[4]};
            if !valid_address(&event.phase,segments[2],segments[3],path) ||
                event.addr!=address(&event.phase,segments[2],segments[3],path){
                return Err("invalid branch identity".into());
            }
            if event.index!=i || event.previous_hash!=previous ||
               event.event_hash!=event.digest(&self.snapshot_digest){
                return Err("evidence chain tampered or reordered".into());
            }
            previous=event.event_hash.clone();
            last_phase=phase_idx;
        }
        Ok(())
    }
    fn report(&self)->Value{
        self.verify().expect("ledger invalid");
        json!({
            "rqt":694,"engine":"Rust",
            "snapshot_count":1,"interior_count":1,"focus":self.frozen.one_focus,
            "temporal_bands":TIME_BANDS,
            "nested_present":"y[n(m)]",
            "temporal_phase_roles":[["past",ROLES[0]],["present",ROLES[1]],["future",ROLES[2]]],
            "projection_faces":FACES,"projection_face_count":6,
            "4d_hypercube_boundary_cubic_cells":8,
            "spatial_roots":POSITIONS,"per_position_grammar":GRAMMAR,
            "snapshot_sha256":self.snapshot_digest,
            "events":self.events.iter().map(|e|json!({
                "index":e.index,"phase":e.phase,"address":e.addr,
                "observation":e.note,"prev_sha256":e.previous_hash,
                "event_sha256":e.event_hash})).collect::<Vec<_>>(),
            "event_count":self.events.len(),
            "chain_valid":true,
            "root19_status":"OPEN",
            "limits":"One software-authored log; hashes establish tamper detection only, not independent witnesses or physical truth"
        })
    }
}
fn main(){
    let mut ledger=Ledger::new();
    ledger.append("past","back","upperleftrear","T","past observes").unwrap();
    ledger.append("present","front","centerupper","TB","present deserves; nested y[n(m)]").unwrap();
    ledger.append("future","right","lowerrightfront","B","future reserves").unwrap();
    println!("{}",serde_json::to_string_pretty(&ledger.report()).unwrap());
}
#[cfg(test)]
mod tests{
    use super::*;
    #[test]
    fn immutable_single_snapshot_and_deterministic_replay(){
        let mut a=Ledger::new();
        let mut b=Ledger::new();
        for l in [&mut a,&mut b] {
            l.append("past","back","upperleftrear","T","observe").unwrap();
            l.append("present","front","centerupper","TB","deserve").unwrap();
            l.append("future","right","lowerrightfront","B","reserve").unwrap();
            l.verify().unwrap();
        }
        assert_eq!(a.snapshot_digest,b.snapshot_digest);
        assert_eq!(a.events.last().unwrap().event_hash,b.events.last().unwrap().event_hash);
        assert_eq!(a.frozen,FrozenSnapshot::canonical());
    }
    #[test]
    fn reject_retroactive_change_and_center_duplication(){
        let mut l=Ledger::new();
        l.append("present","front","upperleftrear","T","read").unwrap();
        assert!(l.append("past","front","upperleftrear","T","rewrite").is_err());
        assert!(l.append("future","front","CENTER","T","duplicate").is_err());
        assert_eq!(l.events.len(),1);
    }
    #[test]
    fn tamper_and_reorder_detected(){
        let mut l=Ledger::new();
        l.append("past","back","upperleftrear","T","first").unwrap();
        l.append("present","front","centerupper","B","second").unwrap();
        l.events[0].note.push_str(" alteration");
        assert!(l.verify().is_err());
        let mut other=Ledger::new();
        other.append("past","back","upperleftrear","T","first").unwrap();
        other.append("present","front","centerupper","B","second").unwrap();
        other.events.swap(0,1);
        assert!(other.verify().is_err());
    }
    #[test]
    fn sibling_paths_and_views_remain_distinct(){
        let mut addresses=BTreeSet::new();
        for t in PHASES{
            for face in FACES{
                for pos in POSITIONS{
                    for path in ["T","B","TT","TB","BT","BB"] {
                        assert!(addresses.insert(address(t,face,pos,path)));
                    }
                }
            }
        }
        assert_eq!(addresses.len(),3*6*8*6);
    }
}

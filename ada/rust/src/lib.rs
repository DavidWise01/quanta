//! ADA-267N .dlw — typed intent kernel, observation only.
#![forbid(unsafe_code)]
pub const GROWTH_RATIO: (u32,u32) = (41,40);
pub const EPOCH_SIZE: usize = 24;
pub const MEMORY_WINDOW: usize = 8;
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Intent { Preserve, Adapt, Defer }
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Support { pub pairs: u8, pub groups: u16, pub grounded: bool }
impl Support {
    fn score(self) -> u16 {
        if self.grounded { 2*u16::from(self.pairs.min(36))+self.groups.min(36) } else { 0 }
    }
}
pub fn prefer(coverage: u8, preserve: Support, adapt: Support) -> Intent {
    if coverage != 100 { return Intent::Defer; }
    match (preserve.score(),adapt.score()) {
        (0,0) => Intent::Defer,
        (p,a) if p>=a => Intent::Preserve,
        _ => Intent::Adapt,
    }
}
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Scenario { Stable, Change, Unknown }
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Consequence { Continuity, PossibleMismatch, ReviewMayBeRelevant, ReviewMayBeUnnecessary, JudgmentReserved, Unresolved }
pub fn model(intent: Intent, scenario: Scenario) -> Consequence {
    match (intent,scenario) {
        (_,Scenario::Unknown) => Consequence::Unresolved,
        (Intent::Defer,_) => Consequence::JudgmentReserved,
        (Intent::Preserve,Scenario::Stable) => Consequence::Continuity,
        (Intent::Preserve,Scenario::Change) => Consequence::PossibleMismatch,
        (Intent::Adapt,Scenario::Stable) => Consequence::ReviewMayBeUnnecessary,
        (Intent::Adapt,Scenario::Change) => Consequence::ReviewMayBeRelevant,
    }
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Record { generation: usize, intent: Intent, source: String }
impl Record {
    pub fn generation(&self)->usize { self.generation }
    pub fn intent(&self)->Intent { self.intent }
    pub fn source(&self)->&str { &self.source }
    pub fn hypothetical(&self)->[Consequence;3] {
        [Scenario::Stable,Scenario::Change,Scenario::Unknown].map(|s|model(self.intent,s))
    }
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct EpochReceipt { pub epoch: usize, pub sealed: bool, pub opening: Vec<Record>, pub closing: Vec<Record> }
#[derive(Default)]
pub struct Ledger { records: Vec<Record> }
impl Ledger {
    pub fn records(&self)->&[Record] { &self.records }
    pub fn append(&mut self, source: String, coverage: u8, preserve: Support, adapt: Support)->Result<(), &'static str> {
        if source.trim().is_empty() || coverage>100 || preserve.pairs>36 || adapt.pairs>36 || preserve.groups>502 || adapt.groups>502 { return Err("invalid input"); }
        self.records.push(Record { generation:self.records.len(), intent:prefer(coverage,preserve,adapt), source });
        Ok(())
    }
    pub fn receipts(&self)->Vec<EpochReceipt> {
        self.records.chunks(EPOCH_SIZE).enumerate().map(|(epoch,chunk)| {
            let start=epoch*EPOCH_SIZE;
            let end=start+chunk.len();
            EpochReceipt { epoch, sealed:chunk.len()==EPOCH_SIZE, opening:self.records[start.saturating_sub(MEMORY_WINDOW)..start].to_vec(), closing:self.records[end.saturating_sub(MEMORY_WINDOW)..end].to_vec() }
        }).collect()
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    fn s(pairs:u8, groups:u16)->Support { Support{pairs,groups,grounded:true} }
    #[test] fn priority() {
        assert_eq!(prefer(100,s(4,2),s(2,2)),Intent::Preserve);
        assert_eq!(prefer(100,s(2,2),s(4,2)),Intent::Adapt);
        assert_eq!(prefer(100,s(4,2),s(4,2)),Intent::Preserve);
        assert_eq!(prefer(99,s(4,2),s(4,2)),Intent::Defer);
        assert_eq!(prefer(100,s(0,0),s(0,0)),Intent::Defer);
    }
    #[test] fn hypothetical_unknown() {
        for i in [Intent::Preserve,Intent::Adapt,Intent::Defer] { assert_eq!(model(i,Scenario::Unknown),Consequence::Unresolved); }
    }
    #[test] fn inheritance() {
        let mut l=Ledger::default();
        for n in 0..24 { l.append(format!("synthetic-{n}"),100,s(4,2),s(2,1)).unwrap(); }
        let frozen=l.receipts()[0].clone();
        l.append("synthetic-24".into(),99,s(4,2),s(2,1)).unwrap();
        let r=l.receipts();
        assert_eq!(r[0],frozen); assert!(r[0].sealed); assert!(!r[1].sealed);
        assert_eq!(r[1].opening,r[0].closing);
        assert_eq!(r[1].closing.iter().map(Record::generation).collect::<Vec<_>>(),(17..25).collect::<Vec<_>>());
        assert_eq!(l.records()[24].intent(),Intent::Defer);
    }
    #[test] fn invalid_input() {
        let mut l=Ledger::default();
        assert!(l.append("".into(),100,s(0,0),s(0,0)).is_err());
        assert!(l.records().is_empty());
    }
}

pub mod adaptive;

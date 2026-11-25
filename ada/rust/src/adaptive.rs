//! ADA-268N .dlw — prospective adaptive policy; no execution.
use crate::{Intent,Support,Ledger,EPOCH_SIZE,MEMORY_WINDOW};
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub struct Policy { window:usize, threshold:u16 }
impl Default for Policy { fn default()->Self { Self{window:8,threshold:0} } }
impl Policy {
    pub fn window(self)->usize { self.window }
    pub fn threshold(self)->u16 { self.threshold }
}
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub struct Sample { pub coverage:u8, pub intent:Intent }
pub fn adapt(prior:Policy, history:&[Sample])->Policy {
    if history.len()!=MEMORY_WINDOW || history.iter().any(|s|s.coverage!=100) { return prior; }
    let changes=history.windows(2).filter(|w|w[0].intent!=w[1].intent).count();
    match changes {
        0=>Policy{window:(prior.window+1).min(8),threshold:prior.threshold.saturating_sub(1)},
        4..=7=>Policy{window:prior.window.saturating_sub(1).max(3),threshold:(prior.threshold+1).min(12)},
        _=>prior,
    }
}
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub struct Decision { pub generation:usize, pub policy:Policy, pub intent:Intent, pub coverage:u8 }
#[derive(Default)]
pub struct AdaptiveLedger { ledger:Ledger, decisions:Vec<Decision> }
impl AdaptiveLedger {
    pub fn decisions(&self)->&[Decision] { &self.decisions }
    pub fn ledger(&self)->&Ledger { &self.ledger }
    pub fn append(&mut self, source:String, coverage:u8, mut preserve:Support, mut change:Support)->Result<(), &'static str> {
        let n=self.decisions.len();
        let prior=self.decisions.last().map(|d|d.policy).unwrap_or_default();
        let policy=if n>=EPOCH_SIZE && n%EPOCH_SIZE==0 {
            let samples:Vec<_>=self.decisions[n-MEMORY_WINDOW..n].iter().map(|d|Sample{coverage:d.coverage,intent:d.intent}).collect();
            adapt(prior,&samples)
        } else { prior };
        // The threshold is a minimum support score; it never grants authority.
        if preserve.score()<=policy.threshold { preserve.grounded=false; }
        if change.score()<=policy.threshold { change.grounded=false; }
        // Window is a retained-context view, not a claim of predictive confidence.
        self.ledger.append(source,coverage,preserve,change)?;
        let intent=self.ledger.records()[n].intent();
        self.decisions.push(Decision{generation:n,policy,intent,coverage});
        Ok(())
    }
    pub fn context(&self)->&[Decision] {
        let n=self.decisions.len();
        let w=self.decisions.last().map(|d|d.policy.window).unwrap_or(MEMORY_WINDOW);
        &self.decisions[n.saturating_sub(w)..]
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    fn s(intent:Intent)->Sample { Sample{coverage:100,intent} }
    #[test] fn volatile_contracts() {
        let h:Vec<_>=(0..8).map(|i|s(if i%2==0{Intent::Preserve}else{Intent::Adapt})).collect();
        let p=adapt(Policy::default(),&h);
        assert_eq!((p.window(),p.threshold()),(7,1));
        let p=(0..20).fold(p,|p,_|adapt(p,&h));
        assert_eq!((p.window(),p.threshold()),(3,12));
    }
    #[test] fn stable_expands() {
        let p=adapt(Policy{window:3,threshold:12},&[s(Intent::Preserve);8]);
        assert_eq!((p.window(),p.threshold()),(4,11));
    }
    #[test] fn missing_holds() {
        let mut h=[s(Intent::Preserve);8];h[3].coverage=99;
        let p=Policy{window:5,threshold:4};assert_eq!(adapt(p,&h),p);assert_eq!(adapt(p,&h[..7]),p);
    }
    #[test] fn prospective_only() {
        let mut l=AdaptiveLedger::default();
        let hi=Support{pairs:5,groups:2,grounded:true};
        let lo=Support{pairs:0,groups:0,grounded:false};
        for i in 0..24 { let (p,a)=if i%2==0{(hi,lo)}else{(lo,hi)};l.append(i.to_string(),100,p,a).unwrap(); }
        let frozen=l.decisions().to_vec();
        l.append("24".into(),100,hi,lo).unwrap();
        assert_eq!(&l.decisions()[..24],frozen.as_slice());
        assert_eq!(l.decisions()[24].policy.window(),7);
        assert_eq!(l.context().len(),7);
        assert!(l.append("".into(),100,hi,lo).is_err());
        assert_eq!(l.decisions().len(),25);
    }
}

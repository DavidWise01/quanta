//! ADA-269N .dlw — deterministic native stress harness.
use crate::{Intent,Support,EPOCH_SIZE,GROWTH_RATIO,Consequence};
use crate::adaptive::{AdaptiveLedger,Policy,Decision};
#[derive(Clone,Copy,Debug,PartialEq,Eq)]
pub enum Environment { Stable, Alternating, Missing, Recovery, Sparse }
pub const ENVIRONMENTS:[Environment;5]=[Environment::Stable,Environment::Alternating,Environment::Missing,Environment::Recovery,Environment::Sparse];
pub const HORIZON:usize=2400;
fn input(env:Environment,n:usize)->(u8,Support,Support) {
    let high=Support{pairs:18,groups:8,grounded:true};
    let low=Support{pairs:0,groups:0,grounded:false};
    let weak=Support{pairs:1,groups:1,grounded:true};
    let alternating=match env { Environment::Alternating|Environment::Missing=>true,Environment::Recovery=>n<1200,_=>false };
    let coverage=if env==Environment::Missing && n%24==23 {99}else{100};
    let (p,a)=if env==Environment::Sparse {(weak,low)} else if alternating&&n%2==1 {(low,high)}else{(high,low)};
    (coverage,p,a)
}
#[derive(Clone,Debug,PartialEq,Eq)]
pub struct Report { pub environment:Environment,pub generations:usize,pub epochs:usize,pub final_policy:Policy,pub deferred:usize,pub checks:usize }
pub fn stress(env:Environment)->Result<Report,&'static str> {
    let mut a=AdaptiveLedger::default();let mut b=AdaptiveLedger::default();
    let mut frozen:Vec<Decision>=Vec::new();let mut checks=0;let mut deferred=0;
    for n in 0..HORIZON {
        let (c,p,q)=input(env,n);
        a.append(format!("synthetic-{n}"),c,p,q)?;
        b.append(format!("synthetic-{n}"),c,p,q)?;
        let d=a.decisions()[n];
        if d.generation!=n || d!=b.decisions()[n] || a.ledger().records()[n]!=b.ledger().records()[n] {return Err("replay");} checks+=1;
        if !(3..=8).contains(&d.policy.window()) || d.policy.threshold()>12 {return Err("bounds");} checks+=1;
        if n%EPOCH_SIZE!=0 && d.policy!=a.decisions()[n-1].policy {return Err("intra-epoch policy");} checks+=1;
        if c!=100 && d.intent!=Intent::Defer {return Err("missing evidence");} checks+=1;
        if a.context().len()!=(n+1).min(d.policy.window()) {return Err("context window");} checks+=1;
        if a.ledger().records()[n].hypothetical()[2]!=Consequence::Unresolved {return Err("unknown outcome");} checks+=1;
        if d.intent==Intent::Defer {deferred+=1;}
        if (n+1)%EPOCH_SIZE==0 {
            if &a.decisions()[..frozen.len()]!=frozen.as_slice() {return Err("sealed prefix");}
            frozen=a.decisions().to_vec();checks+=1;
        }
        if n>0 && n%EPOCH_SIZE==0 && env==Environment::Missing && d.policy!=a.decisions()[n-1].policy {return Err("missing epoch gate");}
    }
    let receipts=a.ledger().receipts();
    if receipts.len()!=100 || receipts.iter().any(|r|!r.sealed) || !receipts.windows(2).all(|w|w[0].closing==w[1].opening) {return Err("inheritance");} checks+=1;
    if GROWTH_RATIO!=(41,40) {return Err("growth");} checks+=1;
    Ok(Report{environment:env,generations:HORIZON,epochs:receipts.len(),final_policy:a.decisions()[HORIZON-1].policy,deferred,checks})
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn five_environments() {
        for e in ENVIRONMENTS {
            let r=stress(e).unwrap();
            let expected=if e==Environment::Alternating {(3,12)}else{(8,0)};
            assert_eq!((r.final_policy.window(),r.final_policy.threshold()),expected);
            assert_eq!(r.checks,14502);
            assert_eq!(r.deferred,if e==Environment::Missing {100}else{0});
        }
    }
    #[test] fn repeat_report() {assert_eq!(stress(Environment::Recovery),stress(Environment::Recovery));}
}

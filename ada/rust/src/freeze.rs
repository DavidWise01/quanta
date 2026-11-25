//! ADA-270N .dlw — native acceptance gate.
use crate::stress::{stress,Report,ENVIRONMENTS,Environment};
use crate::GROWTH_RATIO;
pub fn certify()->Result<Vec<Report>, &'static str>{
    let mut reports=Vec::new();
    for env in ENVIRONMENTS {
        let r=stress(env)?;
        let expected=if env==Environment::Alternating {(3,12)}else{(8,0)};
        if (r.final_policy.window(),r.final_policy.threshold())!=expected ||
           r.generations!=2400 || r.epochs!=100 || r.checks!=14502 ||
           r.deferred!=if env==Environment::Missing {100}else{0} {
            return Err("acceptance mismatch");
        }
        reports.push(r);
    }
    if GROWTH_RATIO!=(41,40) {return Err("growth");}
    Ok(reports)
}
#[cfg(test)]
mod tests {
    #[test] fn phase_ix_gate(){
        let r=super::certify().unwrap();
        assert_eq!(r.iter().map(|r|r.generations).sum::<usize>(),12000);
        assert_eq!(r.iter().map(|r|r.checks).sum::<usize>(),72510);
    }
}

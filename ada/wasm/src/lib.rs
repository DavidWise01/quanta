//! ADA-271N .dlw — scalar browser ABI, no execution authority.
#![deny(unsafe_op_in_unsafe_fn)]
use ada_quanta::{prefer,Intent,Support,GROWTH_RATIO};
#[no_mangle]
pub extern "C" fn ada_abi_version()->u32 { 1 }
#[no_mangle]
pub extern "C" fn ada_growth_numerator()->u32 { GROWTH_RATIO.0 }
#[no_mangle]
pub extern "C" fn ada_growth_denominator()->u32 { GROWTH_RATIO.1 }
#[no_mangle]
pub extern "C" fn ada_prefer(coverage:u32,pp:u32,pg:u32,ap:u32,ag:u32)->i32 {
    if coverage>100 || pp>36 || ap>36 || pg>502 || ag>502 {return -2;}
    let p=Support{pairs:pp as u8,groups:pg as u16,grounded:true};
    let a=Support{pairs:ap as u8,groups:ag as u16,grounded:true};
    match prefer(coverage as u8,p,a) {Intent::Preserve=>-1,Intent::Defer=>0,Intent::Adapt=>1}
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn scalar_contract(){
        assert_eq!(ada_abi_version(),1);
        assert_eq!((ada_growth_numerator(),ada_growth_denominator()),(41,40));
        assert_eq!(ada_prefer(100,4,2,2,2),-1);
        assert_eq!(ada_prefer(100,2,2,4,2),1);
        assert_eq!(ada_prefer(99,4,2,4,2),0);
        assert_eq!(ada_prefer(100,37,0,0,0),-2);
    }
}

// ADA-272N: additive typed ABI; legacy v1 exports remain unchanged.
use ada_quanta::{model,Scenario,Consequence,EPOCH_SIZE,MEMORY_WINDOW};
#[no_mangle]
pub extern "C" fn ada_typed_version()->u32 {2}
#[no_mangle]
pub extern "C" fn ada_epoch_size()->u32 {EPOCH_SIZE as u32}
#[no_mangle]
pub extern "C" fn ada_memory_window()->u32 {MEMORY_WINDOW as u32}
#[no_mangle]
pub extern "C" fn ada_prefer_typed(c:u32,pp:u32,pg:u32,pf:u32,ap:u32,ag:u32,af:u32)->i32 {
    if c>100||pp>36||ap>36||pg>502||ag>502||pf>1||af>1{return -2;}
    match prefer(c as u8,Support{pairs:pp as u8,groups:pg as u16,grounded:pf==1},Support{pairs:ap as u8,groups:ag as u16,grounded:af==1}) {
        Intent::Preserve=>-1,Intent::Defer=>0,Intent::Adapt=>1
    }
}
#[no_mangle]
pub extern "C" fn ada_consequence(intent:i32,scenario:u32)->i32 {
    let i=match intent {-1=>Intent::Preserve,0=>Intent::Defer,1=>Intent::Adapt,_=>return -2};
    let s=match scenario {0=>Scenario::Stable,1=>Scenario::Change,2=>Scenario::Unknown,_=>return -2};
    match model(i,s){Consequence::Continuity=>0,Consequence::PossibleMismatch=>1,Consequence::ReviewMayBeRelevant=>2,Consequence::ReviewMayBeUnnecessary=>3,Consequence::JudgmentReserved=>4,Consequence::Unresolved=>5}
}
#[cfg(test)]
mod typed_tests {
 use super::*;
 #[test] fn matrix(){
    for (i,expected) in [(-1,[0,1,5]),(0,[4,4,5]),(1,[3,2,5])] {
        for (s,e) in expected.into_iter().enumerate(){assert_eq!(ada_consequence(i,s as u32),e);}
    }
    assert_eq!(ada_consequence(2,0),-2);
    assert_eq!(ada_consequence(0,3),-2);
 }
 #[test] fn typed_boundary(){
    assert_eq!(ada_prefer_typed(100,36,36,0,1,1,1),1);
    assert_eq!(ada_prefer_typed(100,36,36,2,1,1,1),-2);
    assert_eq!(ada_prefer_typed(99,36,36,1,1,1,1),0);
    assert_eq!((ada_typed_version(),ada_epoch_size(),ada_memory_window()),(2,24,8));
 }
}

pub mod clock;

pub mod memory;

pub mod geometry;

pub mod pumps;

pub mod inheritance;

pub mod equilibrium;

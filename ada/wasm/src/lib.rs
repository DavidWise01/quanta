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

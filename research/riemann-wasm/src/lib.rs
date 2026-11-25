//! Browser-facing, dependency-light Rust/WASM entry points.
//! All simulation arithmetic delegates to quanta-toroidal-closure.
//! This finite software model is not a physical toroidal universe proof.

use quanta_toroidal_closure::{closure, fixture, iterate};

fn result(radius: u32, theta: u32, phi: u32, steps: u32, vtheta: u32, vphi: u32)
    -> (quanta_toroidal_closure::CoupledState, quanta_toroidal_closure::CoupledState)
{
    let initial = fixture(radius as u128, theta as u128, phi as u128);
    let final_state = iterate(initial, steps.min(360) as usize, [vtheta as u128, vphi as u128]);
    (initial, final_state)
}

#[no_mangle]
pub extern "C" fn toroid_version() -> u32 { 10 }

#[no_mangle]
pub extern "C" fn toroid_radius(radius: u32, theta: u32, phi: u32, steps: u32, vt: u32, vp: u32) -> u32 {
    result(radius, theta, phi, steps, vt, vp).1.radius as u32
}

#[no_mangle]
pub extern "C" fn toroid_theta(radius: u32, theta: u32, phi: u32, steps: u32, vt: u32, vp: u32) -> u32 {
    result(radius, theta, phi, steps, vt, vp).1.position[0] as u32
}

#[no_mangle]
pub extern "C" fn toroid_phi(radius: u32, theta: u32, phi: u32, steps: u32, vt: u32, vp: u32) -> u32 {
    result(radius, theta, phi, steps, vt, vp).1.position[1] as u32
}

/// bit 0=channel return, 1=coordinate return, 2=radius return,
/// 3=homeostasis preserved, 4=complete state return.
#[no_mangle]
pub extern "C" fn toroid_closure_mask(radius: u32, theta: u32, phi: u32, steps: u32, vt: u32, vp: u32) -> u32 {
    let (initial, final_state) = result(radius, theta, phi, steps, vt, vp);
    let flags = closure(initial, final_state);
    u32::from(flags.channels_return)
        | (u32::from(flags.coordinate_return) << 1)
        | (u32::from(flags.radius_return) << 2)
        | (u32::from(flags.homeostasis_preserved) << 3)
        | (u32::from(flags.global_return) << 4)
}

#[no_mangle]
pub extern "C" fn toroid_forward_inner(steps: u32) -> i32 {
    let (_, state) = result(1, 0, 0, steps, 0, 0);
    state.channels.forward[0] as i32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn browser_mask_global_return() {
        assert_eq!(toroid_closure_mask(1, 0, 0, 3, 120, 120), 31);
        assert_eq!(toroid_theta(1, 0, 0, 3, 120, 120), 0);
        assert_eq!(toroid_phi(1, 0, 0, 3, 120, 120), 0);
    }

    #[test]
    fn partial_returns_are_separate() {
        let channel_only = toroid_closure_mask(4, 0, 0, 3, 1, 0);
        assert_eq!(channel_only & 1, 1);
        assert_eq!(channel_only & 16, 0);
        let coordinates_only = toroid_closure_mask(4, 0, 0, 1, 360, 360);
        assert_eq!(coordinates_only & 2, 2);
        assert_eq!(coordinates_only & 16, 0);
    }

    #[test]
    fn browser_api_retains_raw_unwrapped_distinction() {
        let mask = toroid_closure_mask(1, 361, 0, 3, 120, 120);
        assert_eq!(mask & 2, 0);
        assert_eq!(toroid_theta(1, 361, 0, 3, 120, 120), 1);
    }
}

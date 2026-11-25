//! Source-derived deterministic toroidal closure, not a Lean proof checker.
//!
//! Authoritative reference:
//! DavidWise01/positronic-law/ToroidalBlackHoleDynamics_v084.lean
//! pinned Git commit eae5bcd04eec5aeb2a01553c973913ea88488bdf,
//! Git blob SHA-1 85db7f9b460679bf70570e32de25385e3e555eec.
//!
//! This port covers the CoupledState / coupledStep / coupledIterate subset only.
//! Discrete arithmetic and tests do NOT validate physical toroidal universes.

pub const FULL_TURN: u128 = 360;
pub const HORIZON_RADIUS: u128 = 1;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Channels {
    /// [forwardInner, forwardMiddle, forwardOuter]
    pub forward: [i64; 3],
    /// [backwardInner, backwardMiddle, backwardOuter]
    pub backward: [i64; 3],
}

impl Channels {
    pub const fn new(forward: [i64; 3], backward: [i64; 3]) -> Self {
        Self { forward, backward }
    }

    /// Sum in i128 to avoid overflowing sums of i64 channels.
    pub fn net(self) -> i128 {
        self.forward.iter().chain(self.backward.iter()).map(|&x| i128::from(x)).sum()
    }

    pub fn is_homeostatic(self) -> bool {
        (0..3).all(|i| i128::from(self.forward[i]) + i128::from(self.backward[i]) == 0)
    }

    /// The same three-curve permutation of both forward and backward arrays.
    pub fn rotate(self) -> Self {
        let [a, b, c] = self.forward;
        let [d, e, f] = self.backward;
        Self::new([b, c, a], [e, f, d])
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct CoupledState {
    pub radius: u128,
    /// Theta and phi are raw natural-number coordinates, not automatically canonical.
    pub position: [u128; 2],
    pub channels: Channels,
}

pub fn wrap(position: [u128; 2]) -> [u128; 2] {
    [position[0] % FULL_TURN, position[1] % FULL_TURN]
}

/// Equivalent to Lean's (coordinate + velocity) mod 360 without u128 overflow.
/// Since each summand is reduced before adding, the intermediate total is < 720.
pub fn advance(position: [u128; 2], velocity: [u128; 2]) -> [u128; 2] {
    [
        ((position[0] % FULL_TURN) + (velocity[0] % FULL_TURN)) % FULL_TURN,
        ((position[1] % FULL_TURN) + (velocity[1] % FULL_TURN)) % FULL_TURN,
    ]
}

/// Lean: if horizonRadius < radius then radius - 1 else horizonRadius.
pub fn radial_inward_step(radius: u128) -> u128 {
    if radius > HORIZON_RADIUS { radius - 1 } else { HORIZON_RADIUS }
}

pub fn step(state: CoupledState, velocity: [u128; 2]) -> CoupledState {
    CoupledState {
        radius: radial_inward_step(state.radius),
        position: advance(state.position, velocity),
        channels: state.channels.rotate(),
    }
}

pub fn iterate(mut state: CoupledState, steps: usize, velocity: [u128; 2]) -> CoupledState {
    for _ in 0..steps {
        state = step(state, velocity);
    }
    state
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Closure {
    pub channels_return: bool,
    pub coordinate_return: bool,
    pub radius_return: bool,
    pub homeostasis_preserved: bool,
    pub global_return: bool,
}

pub fn closure(initial: CoupledState, final_state: CoupledState) -> Closure {
    let channels_return = initial.channels == final_state.channels;
    let coordinate_return = initial.position == final_state.position;
    let radius_return = initial.radius == final_state.radius;
    Closure {
        channels_return,
        coordinate_return,
        radius_return,
        homeostasis_preserved: !initial.channels.is_homeostatic()
            || final_state.channels.is_homeostatic(),
        global_return: initial == final_state,
    }
}

pub const fn fixture_channels() -> Channels {
    Channels::new([2, 4, 6], [-2, -4, -6])
}

pub const fn fixture(radius: u128, theta: u128, phi: u128) -> CoupledState {
    CoupledState {
        radius,
        position: [theta, phi],
        channels: fixture_channels(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn rotation_3_is_identity_and_preserves_net_and_balance() {
        let original = fixture_channels();
        assert!(original.is_homeostatic());
        assert_eq!(original.net(), 0);
        let mut current = original;
        for _ in 0..3 {
            current = current.rotate();
            assert_eq!(current.net(), original.net());
            assert!(current.is_homeostatic());
        }
        assert_eq!(current, original);
    }

    #[test]
    fn c1_channels_close_but_position_and_radius_do_not() {
        let original = fixture(4, 0, 0);
        let after = iterate(original, 3, [1, 0]);
        let flags = closure(original, after);
        assert_eq!(after.position, [3, 0]);
        assert_eq!(after.radius, 1);
        assert_eq!(flags, Closure {
            channels_return: true, coordinate_return: false, radius_return: false,
            homeostasis_preserved: true, global_return: false,
        });
    }

    #[test]
    fn c2_coordinates_close_but_channels_do_not() {
        let original = fixture(4, 0, 0);
        let after = iterate(original, 1, [360, 360]);
        let flags = closure(original, after);
        assert_eq!(flags, Closure {
            channels_return: false, coordinate_return: true, radius_return: false,
            homeostasis_preserved: true, global_return: false,
        });
    }

    #[test]
    fn c3_all_components_return_at_horizon() {
        let original = fixture(1, 0, 0);
        let after = iterate(original, 3, [120, 120]);
        assert_eq!(after, original);
        assert!(closure(original, after).global_return);
    }

    #[test]
    fn c4_homeostasis_without_any_return() {
        let original = fixture(4, 0, 0);
        let flags = closure(original, iterate(original, 1, [17, 23]));
        assert!(!flags.channels_return);
        assert!(!flags.coordinate_return);
        assert!(!flags.radius_return);
        assert!(flags.homeostasis_preserved);
        assert!(!flags.global_return);
    }

    #[test]
    fn c5_one_angle_closes_but_second_does_not() {
        let original = fixture(1, 0, 0);
        let after = iterate(original, 3, [120, 1]);
        assert_eq!(after.position, [0, 3]);
        assert!(closure(original, after).channels_return);
        assert!(!closure(original, after).global_return);
    }

    #[test]
    fn c6_raw_unwrapped_address_is_not_exact_return() {
        let original = fixture(1, 361, 0);
        let after = iterate(original, 3, [120, 120]);
        assert_eq!(after.position, [1, 0]);
        assert_eq!(wrap(original.position), after.position);
        assert_ne!(after, original);
    }

    #[test]
    fn global_return_iff_all_three_components_equal() {
        for r in 0..=5 {
            for n in 0..=6 {
                let original = fixture(r, 23, 41);
                let after = iterate(original, n, [120, 120]);
                let c = closure(original, after);
                assert_eq!(
                    c.global_return,
                    c.radius_return && c.coordinate_return && c.channels_return
                );
                assert!(c.homeostasis_preserved);
            }
        }
    }

    #[test]
    fn bounded_regression_across_52_configurations() {
        let velocities = [[0, 0], [1, 0], [120, 120], [360, 360]];
        for steps in 0..=12_usize {
            for velocity in velocities {
                let initial = fixture(4, 23, 41);
                let after = iterate(initial, steps, velocity);
                let c = closure(initial, after);
                assert_eq!(c.channels_return, steps % 3 == 0);
                assert_eq!(
                    c.coordinate_return,
                    ((steps as u128) * velocity[0]) % 360 == 0
                        && ((steps as u128) * velocity[1]) % 360 == 0
                );
                assert_eq!(c.radius_return, steps == 0);
                assert_eq!(c.global_return, steps == 0);
            }
        }
    }

    #[test]
    fn modular_advance_never_overflows_at_u128_max() {
        let m = u128::MAX;
        let actual = advance([m, m], [m, m]);
        let x = ((m % 360) * 2) % 360;
        assert_eq!(actual, [x, x]);
    }

    #[test]
    fn radial_clamps_below_and_at_horizon() {
        assert_eq!(radial_inward_step(0), 1);
        assert_eq!(radial_inward_step(1), 1);
        assert_eq!(radial_inward_step(4), 3);
    }
}

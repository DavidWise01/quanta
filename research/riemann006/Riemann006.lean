/-
RIEMANN-006 | Global closure needs all components
Source-bound companion to DavidWise01/positronic-law:
  ToroidalBlackHoleDynamics_v084.lean
Original upstream sources are not modified.
The upstream Lean file is fetched at a pinned commit and Git-blob verified in CI.
This is finite software-state verification, not a physical cosmology or RH proof.
-/
import ToroidalBlackHoleDynamics_v084

namespace Riemann006
open PlankLol.TripleTorusGanglia

/-- Equality of complete states entails equality of all three components,
    and equality of all three components suffices for complete equality. -/
theorem whole_state_iff_components (s t : CoupledState) :
    s = t ↔ s.radius = t.radius ∧
      s.position = t.position ∧ s.channels = t.channels := by
  constructor
  · intro h
    cases h
    exact ⟨rfl, rfl, rfl⟩
  · intro h
    rcases h with ⟨hr, hp, hc⟩
    cases s with
    | mk sr sp sc =>
      cases t with
      | mk tr tp tc =>
        cases hr
        cases hp
        cases hc
        rfl

/-- After three steps the channels return, but total-state closure
    additionally requires both the radius and the pair of angular coordinates. -/
theorem three_step_full_return_iff_radius_and_position
    (s : CoupledState) (theta phi : Nat) :
    coupledIterate 3 s theta phi = s ↔
      (coupledIterate 3 s theta phi).radius = s.radius ∧
      (coupledIterate 3 s theta phi).position = s.position := by
  rw [whole_state_iff_components]
  simp only [coupled_three_steps_return_channel_order, and_true]

/-- The fixture has distinct forward channels so a single rotation is visible. -/
def channels : SixChannelVelocity :=
  { forwardInner := 2, forwardMiddle := 4, forwardOuter := 6
    backwardInner := -2, backwardMiddle := -4, backwardOuter := -6 }

def sample (r theta phi : Nat) : CoupledState :=
  { radius := r, position := (theta, phi), channels := channels }

/-- Three channel rotations return while theta and radius drift. -/
theorem c1_channels_return :
    (coupledIterate 3 (sample 4 0 0) 1 0).channels =
      (sample 4 0 0).channels := by
  exact coupled_three_steps_return_channel_order _ _ _

theorem c1_position_does_not_return :
    (coupledIterate 3 (sample 4 0 0) 1 0).position ≠
      (sample 4 0 0).position := by
  decide

theorem c1_global_return_fails :
    coupledIterate 3 (sample 4 0 0) 1 0 ≠ sample 4 0 0 := by
  intro h
  exact c1_position_does_not_return (congrArg CoupledState.position h)

/-- Both coordinates return after 360 degrees, but one channel rotation does not. -/
theorem c2_coordinates_return :
    (coupledIterate 1 (sample 4 0 0) 360 360).position =
      (sample 4 0 0).position := by
  decide

theorem c2_channels_do_not_return :
    (coupledIterate 1 (sample 4 0 0) 360 360).channels ≠
      (sample 4 0 0).channels := by
  intro h
  have hinner := congrArg SixChannelVelocity.forwardInner h
  decide at hinner

theorem c2_global_return_fails :
    coupledIterate 1 (sample 4 0 0) 360 360 ≠ sample 4 0 0 := by
  intro h
  exact c2_channels_do_not_return (congrArg CoupledState.channels h)

/-- All three components genuinely coincide at the fixed horizon after
    a three-step rotation and 120+120+120 degree turns in BOTH coordinates. -/
theorem c3_whole_state_returns :
    coupledIterate 3 (sample 1 0 0) 120 120 = sample 1 0 0 := by
  rfl

/-- In a one-coordinate sweep, theta returns and phi does not. -/
theorem c5_theta_closes :
    (coupledIterate 3 (sample 1 0 0) 120 1).position.1 = 0 := by
  decide

theorem c5_phi_open :
    (coupledIterate 3 (sample 1 0 0) 120 1).position.2 ≠ 0 := by
  decide

theorem c5_not_globally_closed :
    coupledIterate 3 (sample 1 0 0) 120 1 ≠ sample 1 0 0 := by
  intro h
  have hpos := congrArg CoupledState.position h
  have hphi := congrArg Prod.snd hpos
  exact c5_phi_open hphi

/-- An unwrapped initial theta address may normalize to the equivalent angle
    but still fail raw Nat×Nat state identity. -/
theorem c6_unwrapped_address_not_identical :
    (coupledIterate 3 (sample 1 361 0) 120 120).position ≠
      (sample 1 361 0).position := by
  decide

/-- Homeostasis is invariant even when the complete state is not. -/
theorem homeostasis_of_channels : sixChannelHomeostatic channels := by
  decide

theorem nonreturn_preserves_homeostasis :
    sixChannelHomeostatic
      (coupledIterate 1 (sample 4 0 0) 17 23).channels := by
  exact iterate_preserves_homeostasis 1 (sample 4 0 0) 17 23
    homeostasis_of_channels

theorem nonreturn_is_not_full_closure :
    coupledIterate 1 (sample 4 0 0) 17 23 ≠ sample 4 0 0 := by
  intro h
  have hpos := congrArg CoupledState.position h
  decide at hpos

end Riemann006

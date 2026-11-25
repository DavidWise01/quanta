use quanta_toroidal_closure::{closure, fixture, iterate};

fn main() {
    let cases: [(&str, usize, u128, u128, u128, u128); 6] = [
        ("C1_channel_only", 3, 4, 0, 1, 0),
        ("C2_coordinates_only", 1, 4, 0, 360, 360),
        ("C3_global_closure", 3, 1, 0, 120, 120),
        ("C4_homeostasis_without_return", 1, 4, 0, 17, 23),
        ("C5_one_angle_only", 3, 1, 0, 120, 1),
        ("C6_unwrapped_address", 3, 1, 361, 120, 120),
    ];
    println!("RIEMANN-RUST | discrete toroidal closure receipts");
    println!("case,channels_return,coordinate_return,radius_return,homeostasis_preserved,global_return");
    for (id, steps, radius, theta, theta_vel, phi_vel) in cases {
        let initial = fixture(radius, theta, 0);
        let result = closure(initial, iterate(initial, steps, [theta_vel, phi_vel]));
        println!(
            "{id},{},{},{},{},{}",
            result.channels_return,
            result.coordinate_return,
            result.radius_return,
            result.homeostasis_preserved,
            result.global_return
        );
    }
}

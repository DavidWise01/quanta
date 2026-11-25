//! RQT-690: exact rational-point propagation on the original RQT-388 reduced quadric.
//!
//! The homogeneous equation H(X)=X^T diag(Q,2) X=0, X=(x,y,z,d),
//! is equivalent to Q[x,y,z]=-2d^2.  With a certified rational
//! null vector p, the construction T_p(w) = H(w)p - 2 B(p,w)w
//! yields another exact null vector, where B(p,w)=p^T diag(Q,2) w.
//! This is a conditional constructor: without a seed it does NOT
//! establish an explicit rational witness or an integral root19.
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{One, Zero, Signed};
use serde_json::{json, Value};
use std::env;

type V4 = [BigInt;4];
fn parse(s: &str) -> BigInt {
    BigInt::parse_bytes(s.as_bytes(), 10).expect("expected decimal integer")
}
fn source_q() -> Vec<Vec<BigInt>> {
    let v: Value=serde_json::from_str(include_str!("../data/RQT-388-root19-kernel-results.json")).unwrap();
    let a=v["restricted_F4_Gram"].as_array().unwrap();
    let q:Vec<Vec<BigInt>>=a.iter().map(|r|r.as_array().unwrap().iter()
        .map(|x|parse(x.as_str().unwrap())).collect()).collect();
    assert_eq!(q.len(),3);
    for i in 0..3 {
        assert_eq!(q[i].len(),3);
        assert_eq!((&q[i][i] % 2),BigInt::zero());
        for j in 0..3 {assert_eq!(q[i][j],q[j][i]);}
    }
    q
}
fn b(q:&[Vec<BigInt>],x:&V4,y:&V4)->BigInt {
    let mut s=BigInt::zero();
    for i in 0..3 {for j in 0..3 {s+=&x[i]*&q[i][j]*&y[j];}}
    s+BigInt::from(2)*&x[3]*&y[3]
}
fn h(q:&[Vec<BigInt>],x:&V4)->BigInt {b(q,x,x)}
fn normalize(v:V4)->V4 {
    let mut g=BigInt::zero();
    for x in &v {g=g.gcd(&x.abs());}
    assert!(!g.is_zero(),"zero vector cannot be a projective point");
    let mut result=v.map(|x|x/&g);
    // Rational projective sign normalization.
    if result[3].is_negative() {result=result.map(|x|-x);}
    result
}
fn construct(q:&[Vec<BigInt>],seed:&V4,trial:&V4)->Option<V4> {
    assert_eq!(h(q,seed),BigInt::zero(),"seed is not a null vector");
    let wnorm=h(q,trial);
    let dot=b(q,seed,trial);
    let two=BigInt::from(2);
    let output:V4=std::array::from_fn(|i| &wnorm*&seed[i]-&two*&dot*&trial[i]);
    if output.iter().all(|x|x.is_zero()){return None;}
    assert_eq!(h(q,&output),BigInt::zero(),"rational parametrization identity failed");
    Some(normalize(output))
}
fn emit_point(q:&[Vec<BigInt>],v:&V4)->Value {
    assert_eq!(h(q,v),BigInt::zero());
    assert!(!v[3].is_zero(),"this is a point at infinity, not a rational norm -2 witness");
    assert_eq!(v[3].gcd(&v[0]).gcd(&v[1]).gcd(&v[2]),BigInt::one());
    let numer:Vec<String>=v[..3].iter().map(|x|x.to_string()).collect();
    json!({"x":numer[0],"y":numer[1],"z":numer[2],"denominator":v[3].to_string(),
        "norm_check":"exact: numerator^T Q numerator = -2 denominator^2"})
}
fn main() {
    let args:Vec<String>=env::args().skip(1).collect();
    if args.len()!=4 {
        eprintln!("Usage: cargo run --bin rqt690 -- <seed_x> <seed_y> <seed_z> <seed_d>");
        eprintln!("A seed must be a verified integer quadruple with nonzero d and H(seed)=0.");
        eprintln!("No authentic rational seed is currently certified. Root 19: OPEN.");
        std::process::exit(2);
    }
    let q=source_q();
    let p:V4=std::array::from_fn(|i|parse(&args[i]));
    if p[3].is_zero() || h(&q,&p)!=BigInt::zero() {
        eprintln!("REJECT: supplied vector is not an authenticated rational norm -2 witness.");
        std::process::exit(3);
    }
    let p=normalize(p);
    let mut points=Vec::new();
    let mut seen=std::collections::BTreeSet::new();
    for a in -2_i32..=2 {for c in -2_i32..=2 {
        let trial=[BigInt::from(a), BigInt::from(1), BigInt::from(c),BigInt::from(1)];
        if let Some(w)=construct(&q,&p,&trial) {
            if !w[3].is_zero() && seen.insert(w.clone()) {points.push(emit_point(&q,&w));}
        }
    }}
    println!("{}",serde_json::to_string_pretty(&json!({
        "rqt":690,"language":"Rust","method":"rational quadric projection from a certified seed",
        "topology":"{1×[3×8 | n | (8×3)×1]}",
        "certified_seed":emit_point(&q,&p),
        "derived_rational_points":points,
        "root19":"OPEN: no original 22D integral divisibility-one or reflection-chain certificate"
    })).unwrap());
}
#[cfg(test)]
mod tests {
    use super::*;
    fn synthetic()->Vec<Vec<BigInt>> {
        // diag(-2,2,2) has a norm -2 solution (1,0,0);
        // the projective quadric diag(-2,2,2,2) has seed (1,0,0,1).
        vec![
            vec![parse("-2"),parse("0"),parse("0")],
            vec![parse("0"),parse("2"),parse("0")],
            vec![parse("0"),parse("0"),parse("2")],
        ]
    }
    #[test]
    fn projection_identity_and_nonzero_denominator() {
        let q=synthetic();
        let seed=[parse("1"),parse("0"),parse("0"),parse("1")];
        assert_eq!(h(&q,&seed),BigInt::zero());
        let trial=[parse("0"),parse("1"),parse("2"),parse("1")];
        let output=construct(&q,&seed,&trial).unwrap();
        assert_eq!(h(&q,&output),BigInt::zero());
        assert!(!output[3].is_zero());
        let _=emit_point(&q,&output);
    }
    #[test]
    fn original_gram_is_even_and_symmetric() {
        let q=source_q();
        assert_eq!(q.len(),3);
        let zero=[BigInt::zero(),BigInt::zero(),BigInt::zero(),BigInt::zero()];
        assert_eq!(h(&q,&zero),BigInt::zero());
    }
}

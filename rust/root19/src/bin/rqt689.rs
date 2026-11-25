//! RQT-689: exact bounded rational-witness search for the recovered RQT-388 form.
//! A bounded search is NOT a proof of global nonexistence.
use num_bigint::{BigInt, BigUint, Sign};
use num_integer::{Integer, Roots};
use num_traits::{ToPrimitive, Zero};
use serde_json::{json, Value};
use std::{collections::BTreeSet, env};

const MODULI: [u64; 12] = [16, 5, 7, 11, 13, 17, 19, 23, 31, 37, 41, 43];
fn from_json(value: &Value) -> BigInt {
    BigInt::parse_bytes(value.as_str().expect("decimal string").as_bytes(), 10).expect("integer")
}
fn load_gram() -> Vec<Vec<BigInt>> {
    let source: Value = serde_json::from_str(include_str!("../data/RQT-388-root19-kernel-results.json")).unwrap();
    let q: Vec<Vec<BigInt>> = source["restricted_F4_Gram"].as_array().unwrap().iter()
        .map(|r| r.as_array().unwrap().iter().map(from_json).collect()).collect();
    assert_eq!(q.len(), 3);
    for i in 0..3 {
        assert_eq!(q[i].len(), 3);
        for j in 0..3 { assert_eq!(q[i][j], q[j][i]); }
        assert_eq!((&q[i][i] % 2), BigInt::zero(), "Q must be even");
    }
    q
}
fn residue(x: &BigInt, m: u64) -> u64 {
    x.mod_floor(&BigInt::from(m)).to_u64().unwrap()
}
fn norm(q: &[Vec<BigInt>], v: &[BigInt; 3]) -> BigInt {
    let mut answer=BigInt::zero();
    for i in 0..3 { for j in 0..3 { answer+=&v[i]*&q[i][j]*&v[j]; } }
    answer
}
fn exact_rational_scan(q: &[Vec<BigInt>], d_max: u64, y_max: u64) -> Value {
    assert!(d_max > 0 && d_max <= 255);
    assert!(y_max > 0 && y_max <= 100_000);
    let a=&q[0][2]*&q[0][2] - &q[2][2]*&q[0][0];
    let k=&q[0][2]*&q[1][2] - &q[2][2]*&q[0][1];
    let c=&q[1][2]*&q[1][2] - &q[2][2]*&q[1][1];
    let f=&q[2][2];
    assert!(!f.is_zero());
    let filters: Vec<(u64,u64,u64,u64,u64,BTreeSet<u64>)> = MODULI.iter().map(|&m| {
        (m,residue(&a,m),residue(&k,m),residue(&c,m),residue(f,m),
        (0..m).map(|t|t*t % m).collect())
    }).collect();
    let mut tested=0u64;
    let mut nonsquares=0u64;
    let mut negatives=0u64;
    let mut full_tests=0u64;
    let mut square_discriminants=0u64;
    let mut nonprimitive_rejects=0u64;
    let mut hits: Vec<Value>=Vec::new();
    for d in (1..=d_max).step_by(2) {
        for y in 1..=y_max {
            let low=(177065_u128*y as u128/100000+1) as u64;
            let high=((178600_u128*y as u128-1)/100000) as u64;
            if low>high {continue;}
            for x in low..=high {
                tested+=1;
                let failed=filters.iter().any(|(m,aa,kk,cc,ff,squares)| {
                    let xm=x%m; let ym=y%m; let dm=d%m;
                    let target=(2*ff%m)*(dm*dm%m)%m;
                    let disc=((aa*xm%m)*xm%m+
                        (2*(kk*xm%m)*ym%m)+
                        (cc*ym%m)*ym%m +m-target)%m;
                    !squares.contains(&disc)
                });
                if failed {nonsquares+=1; continue;}
                let xb=BigInt::from(x); let yb=BigInt::from(y); let db=BigInt::from(d);
                let delta=&a*&xb*&xb + BigInt::from(2)*&k*&xb*&yb +
                    &c*&yb*&yb - BigInt::from(2)*f*&db*&db;
                if delta.sign()==Sign::Minus {negatives+=1;continue;}
                full_tests+=1;
                let root: BigUint=delta.to_biguint().unwrap().sqrt();
                let t=BigInt::from(root);
                if &t*&t!=delta {continue;}
                square_discriminants+=1;
                let l=&q[0][2]*&xb+&q[1][2]*&yb;
                for sign in [-1i32,1] {
                    let numerator=-&l+BigInt::from(sign)*&t;
                    if &numerator % f != BigInt::zero() {continue;}
                    let z=numerator/f;
                    let g=xb.gcd(&yb).gcd(&z).gcd(&db);
                    if g!=BigInt::from(1) {nonprimitive_rejects+=1; continue;}
                    let v=[xb.clone(),yb.clone(),z.clone()];
                    assert_eq!(norm(q,&v),-BigInt::from(2)*&db*&db);
                    hits.push(json!({"x":xb.to_string(),"y":yb.to_string(),
                        "z":z.to_string(),"denominator":db.to_string()}));
                }
            }
        }
    }
    json!({"rqt":689,"language":"Rust","source":"RQT-388 exact reduced Gram",
        "topology":"{{brace[[box((torroid))]]}}^{{n}}^[[n]]^((n))",
        "denominator_max":d_max,"denominator_policy":"primitive odd denominators only",
        "positive_y_max":y_max,"cone":"177065/100000 < x/y < 178600/100000",
        "candidate_dxy":tested,"modular_nonsquares":nonsquares,
        "negative_discriminants":negatives,"full_square_tests":full_tests,
        "perfect_square_discriminants":square_discriminants,
        "nonprimitive_lifts_rejected":nonprimitive_rejects,
        "explicit_rational_witnesses":hits,
        "status":"BOUND ONLY; root19 remains OPEN",
        "proof_boundary":"does not establish full 22D divisibility-one or reflection chain"})
}
fn main() {
    let mut args=env::args().skip(1);
    let d_max=args.next().map(|s|s.parse::<u64>().expect("max d")).unwrap_or(33);
    let y_max=args.next().map(|s|s.parse::<u64>().expect("max y")).unwrap_or(1000);
    let q=load_gram();
    println!("{}",serde_json::to_string_pretty(&exact_rational_scan(&q,d_max,y_max)).unwrap());
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn source_mod16_and_norm() {
        let q=load_gram();
        let want=[[2,8,2],[8,4,6],[2,6,14]];
        for i in 0..3 { for j in 0..3 { assert_eq!(residue(&q[i][j],16),want[i][j]); } }
        let zero=[BigInt::zero(),BigInt::zero(),BigInt::zero()];
        assert_eq!(norm(&q,&zero),BigInt::zero());
    }
    #[test]
    fn bounded_smoke_test() {
        let result=exact_rational_scan(&load_gram(),7,100);
        assert!(result["candidate_dxy"].as_u64().unwrap()>0);
        assert!(result["explicit_rational_witnesses"].as_array().unwrap().is_empty());
    }
}

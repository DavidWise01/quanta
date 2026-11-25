use num_bigint::{BigInt, BigUint, Sign};
use num_integer::Roots;
use num_traits::{ToPrimitive, Zero, One};
use serde_json::{json, Value};
use std::collections::BTreeSet;
use std::env;

const MODULI: [u64; 11] = [16, 5, 7, 11, 13, 17, 19, 23, 31, 37, 41];

fn as_big(v: &Value) -> BigInt {
    let s = v.as_str().expect("matrix integer must be encoded as a string");
    BigInt::parse_bytes(s.as_bytes(), 10).expect("invalid decimal integer")
}
fn matrix(v: &Value) -> Vec<Vec<BigInt>> {
    v.as_array().expect("matrix must be an array").iter()
        .map(|r| r.as_array().expect("row must be array").iter().map(as_big).collect()).collect()
}
fn qform(q: &[Vec<BigInt>], v: &[BigInt; 3]) -> BigInt {
    let mut sum = BigInt::zero();
    for i in 0..3 {
        for j in 0..3 { sum += &q[i][j] * &v[i] * &v[j]; }
    }
    sum
}
fn mod_u(x: &BigInt, m: u64) -> u64 {
    let mm = BigInt::from(m);
    let mut r = x % &mm;
    if r.sign() == Sign::Minus { r += mm; }
    r.to_u64().unwrap()
}
fn verify_source(q: &[Vec<BigInt>], b: &[Vec<BigInt>]) {
    assert_eq!(q.len(), 3);
    assert!(q.iter().all(|r| r.len() == 3));
    assert_eq!(b.len(), 4);
    assert!(b.iter().all(|r| r.len() == 3));
    for i in 0..3 { for j in 0..3 { assert_eq!(q[i][j], q[j][i]); } }
    let f_text = [
        ["-4523390658618420908", "2239380521691398176", "-2422224054680331217", "-3109472006028867029"],
        ["2239380521691398176", "-6703602364620082676", "-1185189370853509030", "4418426561730616356"],
        ["-2422224054680331217", "-1185189370853509030", "-5270086080008383040", "4649693842155823637"],
        ["-3109472006028867029", "4418426561730616356", "4649693842155823637", "-12373412455412906476"]
    ];
    let f: Vec<Vec<BigInt>> = f_text.iter().map(|r| r.iter()
        .map(|s| BigInt::parse_bytes(s.as_bytes(),10).unwrap()).collect()).collect();
    for i in 0..3 {
        for j in 0..3 {
            let mut sum = BigInt::zero();
            for a in 0..4 { for c in 0..4 {
                sum += &b[a][i] * &f[a][c] * &b[c][j];
            }}
            assert_eq!(q[i][j], sum, "RQT-388 source identity failed");
        }
    }
    let fingerprint: [[u64; 3];3] = [[2,8,2],[8,4,6],[2,6,14]];
    for i in 0..3 { for j in 0..3 {
        assert_eq!(mod_u(&q[i][j], 16), fingerprint[i][j]);
    }}
}
fn parity_certificate(q: &[Vec<BigInt>]) -> (usize, BTreeSet<String>) {
    let mut count = 0usize;
    let mut parity = BTreeSet::new();
    for x in 0..8 {
        for y in 0..8 {
            for z in 0..8 {
                for d in 0..8 {
                    if x % 2 == 0 && y % 2 == 0 && z % 2 == 0 && d % 2 == 0 { continue; }
                    let v = [BigInt::from(x), BigInt::from(y), BigInt::from(z)];
                    let norm = qform(q, &v);
                    assert_eq!(mod_u(&norm,2),0);
                    let half = norm / 2;
                    if mod_u(&(half + BigInt::from(d*d)),8) == 0 {
                        assert_eq!(d%2,1, "primitive even denominator survived");
                        count += 1;
                        parity.insert(format!("{}{}{}{}",x%2,y%2,z%2,d%2));
                    }
                }
            }
        }
    }
    assert_eq!(parity, ["0011","0111","1101"].iter().map(|s| s.to_string()).collect());
    (count, parity)
}
fn discriminant_coeff(q: &[Vec<BigInt>]) -> (BigInt, BigInt, BigInt, BigInt) {
    let a = &q[0][2]*&q[0][2] - &q[2][2]*&q[0][0];
    let k = &q[0][2]*&q[1][2] - &q[2][2]*&q[0][1];
    let c = &q[1][2]*&q[1][2] - &q[2][2]*&q[1][1];
    (a,k,c,q[2][2].clone())
}
fn scan(q: &[Vec<BigInt>], y_max: u64) -> Value {
    let (a,k,c,f) = discriminant_coeff(q);
    assert!(!f.is_zero());
    let sieve: Vec<(u64,u64,u64,u64,u64,BTreeSet<u64>)> = MODULI.iter().map(|&m| {
        let squares = (0..m).map(|r| (r*r)%m).collect();
        (m,mod_u(&a,m),mod_u(&k,m),mod_u(&c,m),mod_u(&f,m),squares)
    }).collect();
    let mut pairs=0u64;
    let mut modular_rejections=0u64;
    let mut negative=0u64;
    let mut square_tests=0u64;
    let mut perfect_squares=0u64;
    let mut lifts: Vec<[String;3]>=Vec::new();
    for y in 1..=y_max {
        let low = (177065_u128*y as u128 / 100000_u128 + 1) as u64;
        let high = ((178600_u128*y as u128 - 1) / 100000_u128) as u64;
        if low>high {continue;}
        for x in low..=high {
            pairs+=1;
            let rejected=sieve.iter().any(|(m,aa,kk,cc,ff,squares)| {
                let xx=x%m; let yy=y%m;
                let d = ((aa*xx%m)*xx%m + 2*(kk*xx%m)*yy%m +
                    (cc*yy%m)*yy%m + m - (2*ff%m))%m;
                !squares.contains(&d)
            });
            if rejected {modular_rejections+=1; continue;}
            let xb=BigInt::from(x); let yb=BigInt::from(y);
            let disc = &a*&xb*&xb + BigInt::from(2)*&k*&xb*&yb +
                &c*&yb*&yb - BigInt::from(2)*&f;
            if disc.sign()==Sign::Minus {negative+=1;continue;}
            square_tests+=1;
            let root: BigUint=disc.to_biguint().unwrap().sqrt();
            let t=BigInt::from(root);
            if &t*&t != disc {continue;}
            perfect_squares+=1;
            let l=&q[0][2]*&xb + &q[1][2]*&yb;
            for sign in [-1,1] {
                let numerator=-&l + BigInt::from(sign)*&t;
                if &numerator%&f != BigInt::zero(){continue;}
                let z=numerator/&f;
                let v=[xb.clone(),yb.clone(),z.clone()];
                assert_eq!(qform(q,&v),BigInt::from(-2));
                lifts.push([xb.to_string(),yb.to_string(),z.to_string()]);
            }
        }
    }
    json!({"y_bound":y_max,"cone_pairs":pairs,
        "modular_rejections":modular_rejections,"negative_after_sieve":negative,
        "nonnegative_square_tests":square_tests,"perfect_square_discriminants":perfect_squares,
        "exact_reduced_norm_minus_two_lifts":lifts,
        "root19_status":"OPEN",
        "scope":"finite reduced rank-three search; no original 22D divisibility-one/word certificate"})
}
fn main() {
    let max_y: u64=env::args().nth(1).map(|s|s.parse().expect("max_y must be positive integer")).unwrap_or(3000);
    assert!(max_y>0 && max_y<=1_000_000,"max_y outside supported search range");
    let raw=include_str!("../data/RQT-388-root19-kernel-results.json");
    let source:Value=serde_json::from_str(raw).expect("invalid source JSON");
    let q=matrix(&source["restricted_F4_Gram"]);
    let b=matrix(&source["reduced_kernel_basis"]);
    verify_source(&q,&b);
    let (count,parity)=parity_certificate(&q);
    let result=scan(&q,max_y);
    println!("{}",serde_json::to_string_pretty(&json!({
        "rqt":688, "language":"Rust", "source":"RQT-388",
        "topology":"{1×[3×8 | n | (8×3)×1]}",
        "source_identity":"Q=B^T F4 B verified",
        "primitive_mod8_compatible_count":count,
        "primitive_parity_patterns":parity.into_iter().collect::<Vec<_>>(),
        "scan":result
    })).unwrap());
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn authentic_source_and_parity() {
        let source:Value=serde_json::from_str(include_str!("../data/RQT-388-root19-kernel-results.json")).unwrap();
        let q=matrix(&source["restricted_F4_Gram"]);
        let b=matrix(&source["reduced_kernel_basis"]);
        verify_source(&q,&b);
        let (count,p)=parity_certificate(&q);
        assert!(count>0);
        assert_eq!(p.len(),3);
    }
    #[test]
    fn exact_short_cone_scan() {
        let source:Value=serde_json::from_str(include_str!("../data/RQT-388-root19-kernel-results.json")).unwrap();
        let q=matrix(&source["restricted_F4_Gram"]);
        let v=scan(&q,100);
        assert!(v["cone_pairs"].as_u64().unwrap()>0);
        assert!(v["exact_reduced_norm_minus_two_lifts"].as_array().unwrap().is_empty());
    }
}

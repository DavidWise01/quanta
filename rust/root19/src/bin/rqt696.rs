//! RQT-696: source-pinned symbolic calendar/clock/angle bridge, distinct from lattice mathematics.
use serde_json::json;
const QG077_SOURCE:&str="2fff7d9f91a63e0290e00f74fd0269ba43d1f0fc";
const QUANTA:&str="{{brace[[box((torroid))]]}}^{{n}}^[[n]]^((n))";
const CENTER:&str="CENTER{[(FOCUS)]}";
fn parse(s:&str)->Result<[[u32;3];3],String>{
 let mut remaining=s;
 let mut rows=[[0u32;3];3];
 for (i,(open,close)) in [("{{","}}"),("[[","]]"),("((","))")].iter().enumerate(){
  remaining=remaining.strip_prefix(open).ok_or("invalid opener")?;
  let end=remaining.find(close).ok_or("missing closer")?;
  let p:Vec<_>=remaining[..end].split(',').collect();
  if p.len()!=3 {return Err("expected triple".into());}
  for j in 0..3{
   if p[j].is_empty()||!p[j].bytes().all(|c|c.is_ascii_digit()){return Err("invalid digit".into());}
   rows[i][j]=p[j].parse::<u32>().map_err(|_|"integer overflow".to_string())?;
  }
  remaining=&remaining[end+close.len()..];
 }
 if !remaining.is_empty()||rows[0][0]==0||!(1..=12).contains(&rows[0][1])||!(1..=31).contains(&rows[0][2])
 ||rows[1][0]>23||rows[1][1]>59||rows[1][2]>59
 ||rows[2][0]>359||rows[2][1]>59||rows[2][2]>59{return Err("out of range".into());}
 Ok(rows)
}
fn main(){
 let sample=std::env::args().nth(1).unwrap_or("{{2026,11,25}}[[09,46,00]]((127,23,45))".into());
 match parse(&sample){
  Ok(rows)=>println!("{}",json!({"rqt":696,"calendar":rows[0],"clock":rows[1],"angle":rows[2],
   "source_sha":QG077_SOURCE,"quanta":QUANTA,"focus":CENTER,"snapshot_count":1,"root19":"OPEN",
   "independent_carriers":true,"physical_claim":false})),
  Err(err)=>{eprintln!("REJECT {err}");std::process::exit(2);}
 }
}
#[cfg(test)]mod tests{
 use super::*;
 #[test]fn source_example(){assert_eq!(parse("{{2026,11,17}}[[14,30,00]]((127,23,45))").unwrap()[2],[127,23,45]);}
 #[test]fn strict_fail_closed(){for x in ["{{2026,11,17}}[[24,30,00]]((127,23,45))","{{2026,11,17}}[[14,30,00]]((360,23,45))","{{2026,11,17}}[[14,30,00]]((127,23,45))garbage"]{assert!(parse(x).is_err())}}
}

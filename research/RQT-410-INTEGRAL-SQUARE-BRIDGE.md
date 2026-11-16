# RQT-410 — The Integral Square Bridge

## Theorem
For the actual candidate-successor Gram Q, set A=Q/2 with upper triangle (a,b,c,d,e,f). Define L=cx+ey, M=ax²+2bxy+dy²+1 and E=L²-fM. Then Q[x,y,z]=-2 is equivalent to f z²+2Lz+M=0.

**A genuine integer z exists if and only if E=s² for some integer s≥0 and f divides s-L or s+L.** In that case z=(-L±s)/f. This is an exact all-size acceptance test, not a newly discovered root.

## New arithmetic obstruction to a weak modular-square test
The actual 1352-bit coefficient f is divisible by both 13 and 23. At (x,y)=(16,9), L≡5 mod13 and L≡10 mod23. The mixed-sign root s≡174 mod299 satisfies s≡L mod13 and s≡-L mod23. It therefore obeys s²≡E mod299, but neither s≡L nor s≡-L modulo299. Thus separate local square filters do not enforce one coherent global sign. **E(16,9) is nonsquare over Z**, so this example is not an integer root.

## Geometry / ASCII
```text
        RQT-410 | INTEGRAL SQUARE BRIDGE
          +--------------------------+
          |     E(x,y) = s^2 ?      |
          +------------+-------------+
                       |
                    TWO SIGNS
                    /       \
             s = +L         s = -L
               mod f          mod f
                    \       /
                  z INTEGER?
                       |
                    ROOT 19
                      OPEN
```

## Provenance
Source: frozen RQT-401 candidate-successor Gram; checked by independent exact integer calculations against its full JSON matrix. GitHub and mirrored HTML are not independent source ancestries. The predecessor ordering that would qualify the RQT-386 vector as actual position 18 remains unverified. Root19 OPEN, root20 OPEN, root21 conditional. JPG and embedded-JPG HTML are provided as separate conversation artifacts.

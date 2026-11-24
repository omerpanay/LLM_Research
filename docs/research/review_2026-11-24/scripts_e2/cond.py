import math
z=1.96
q1,q0=0.90,0.95
for th in [0.20,0.05]:
    P1=q1*th+(1-q0)*(1-th); P0=1-P1
    ppv=q1*th/P1; fomr=(1-q1)*th/P0
    for n in [500,2000]:
        for k1,k0 in [(25,25),(50,50),(30,70),(100,100)]:
            var=P1**2*ppv*(1-ppv)/k1 + P0**2*fomr*(1-fomr)/k0 + (ppv-fomr)**2*P1*P0/n
            print(f"th={th} P(judge+)={P1:.3f} PPV={ppv:.3f} FOR={fomr:.3f} n={n} k+={k1} k-={k0}: ±{100*z*math.sqrt(var):.1f}pp (total labels {k1+k0})")

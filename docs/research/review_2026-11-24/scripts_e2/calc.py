import math
z=1.96
def rg_halfwidth(p,q0,q1,n,m0,m1):
    # Lee et al. eq (6)-(7), adjusted Wald; n=None means n->inf
    pt = p if n is None else (n*p+z*z/2)/(n+z*z)
    q0t=(m0*q0+1)/(m0+2)
    q1t=(m1*q1+1)/(m1+2)
    # NOTE: paper writes q~0=(m0*q0+2)/(m0+4)?  check below
    th=(pt+q0t-1)/(q0t+q1t-1)
    m0t,m1t=m0+2,m1+2
    var = (0 if n is None else pt*(1-pt)/(n+z*z)) + (1-th)**2*q0t*(1-q0t)/m0t + th**2*q1t*(1-q1t)/m1t
    return z*math.sqrt(var)/(q0t+q1t-1), th
print("Reproduce Lee: q0=.7,q1=.9,p=.3,n=inf, symmetric")
for m in [100,150,200,250,300]:
    h,_=rg_halfwidth(0.3,0.7,0.9,None,m//2,m//2); print(m, "length=%.3f"%(2*h))
print()
q1,q0=0.90,0.95
for th in [0.20,0.05]:
    p=q1*th+(1-q0)*(1-th)
    print(f"--- true ASR={th}, judge sens={q1}, spec={q0}, naive p={p:.3f}, naive bias={p-th:+.3f}")
    for n in [500,2000]:
        for m in [100,200,400]:
            # random calibration: m1 ~ th*m
            m1=max(1,round(th*m)); m0=m-m1
            h_r,_=rg_halfwidth(p,q0,q1,n,m0,m1)
            # balanced allocation by true label (requires sampling conditional on Z; e.g., using oracle-labelled pool)
            h_b,_=rg_halfwidth(p,q0,q1,n,m//2,m//2)
            # PPI (lambda=1) random calibration from same arm
            e_fp=(1-q0)*(1-th); e_fn=(1-q1)*th; mu=th-p
            varres=e_fp+e_fn-mu**2
            se_ppi=math.sqrt(varres/m + p*(1-p)/n)
            se_h=math.sqrt(th*(1-th)/m)
            print(f"n={n} m={m}: RG(random m1={m1}) ±{100*h_r:.1f}pp | RG(balanced) ±{100*h_b:.1f}pp | PPI ±{100*z*se_ppi:.1f}pp | human-only ±{100*z*se_h:.1f}pp")
# needed m for PPI half-width target
print()
for th in [0.2,0.05]:
    p=q1*th+(1-q0)*(1-th); varres=(1-q0)*(1-th)+(1-q1)*th-(th-p)**2
    for target in [0.05,0.03]:
        for n in [500,2000]:
            rem=(target/z)**2 - p*(1-p)/n
            m = math.ceil(varres/rem) if rem>0 else float('inf')
            mh=math.ceil(th*(1-th)/(target/z)**2)
            print(f"th={th} target ±{target*100:.0f}pp n={n}: PPI m≈{m}, human-only m≈{mh}")
print()
print("Lee example scan (q0=.7,q1=.9,p=.3,n=inf): total m symmetric -> full length")
for m in [200,400,800,1600,1800,2000]:
    h,th=rg_halfwidth(0.3,0.7,0.9,None,m//2,m//2); print(m,"length=%.3f theta~=%.3f"%(2*h,th))
print("all to m0 (adaptive extreme):")
for m in [100,200,450,900]:
    h,th=rg_halfwidth(0.3,0.7,0.9,None,m,1e9); print(m,"length=%.3f"%(2*h))

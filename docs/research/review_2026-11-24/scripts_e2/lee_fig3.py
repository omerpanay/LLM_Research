import math
z=1.96
def ci(p,q0,q1,m0,m1):
    q0t=(m0*q0+1)/(m0+2); q1t=(m1*q1+1)/(m1+2)
    th=(p+q0t-1)/(q0t+q1t-1)
    var=((1-th)**2*q0t*(1-q0t)/(m0+2)+th**2*q1t*(1-q1t)/(m1+2))/(q0t+q1t-1)**2
    h=z*math.sqrt(var); lo,hi=max(0,th-h),min(1,th+h); return hi-lo, 2*h
for p in [0.3,0.5,0.7,0.9]:
    out=[]
    for m in [100,200,1000,10000]:
        a=ci(p,0.7,0.9,m,m); b=ci(p,0.7,0.9,m//2,m//2)
        out.append(f"m={m}: per-label {a[0]:.3f} | total {b[0]:.3f}")
    print("p=",p," ; ".join(out))

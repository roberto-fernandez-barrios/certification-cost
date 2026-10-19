"""Closed derivative formulas and symbolic moment identity, no project imports."""
from fractions import Fraction as F
from pathlib import Path
from math import comb,factorial
import json,time
OUT=Path(__file__).resolve().parent
class Interval:
    def __init__(self,a,b=None):self.a=F(a);self.b=F(a if b is None else b);assert self.a<=self.b
    @staticmethod
    def wrap(x):return x if isinstance(x,Interval) else Interval(x)
    def __add__(self,x):
        x=self.wrap(x);return Interval(self.a+x.a,self.b+x.b)
    __radd__=__add__
    def __neg__(self):return Interval(-self.b,-self.a)
    def __sub__(self,x):return self+-self.wrap(x)
    def __rsub__(self,x):return self.wrap(x)+-self
    def __mul__(self,x):
        x=self.wrap(x);v=[self.a*x.a,self.a*x.b,self.b*x.a,self.b*x.b];return Interval(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,x):
        x=self.wrap(x);assert x.a*x.b>0;return self*Interval(1/x.b,1/x.a)
    def __rtruediv__(self,x):return self.wrap(x)/self
    def __pow__(self,n):
        assert n>=0
        if n==0:return Interval(1)
        if self.a>=0:return Interval(self.a**n,self.b**n)
        if self.b<=0:return (-self)**n*((-1)**n)
        return Interval(0,max(abs(self.a),abs(self.b))**n) if n%2==0 else Interval(self.a**n,self.b**n)
    def bound(self):return max(abs(self.a),abs(self.b))

def derivatives(p,transition):
    d=[]
    for r in range(4):
        d.append(sum(((-1)**r*F(factorial(j),factorial(j-r))*(1-p)**(j-r) for j in range(r,8)),Interval(0)))
    h=3/d[0];hp=-3*d[1]/d[0]**2
    hpp=6*d[1]**2/d[0]**3-3*d[2]/d[0]**2
    hppp=-18*d[1]**3/d[0]**4+18*d[1]*d[2]/d[0]**3-3*d[3]/d[0]**2
    if not transition:return h,hp,hpp,hppp
    t=64*p-16
    def s(x):return 35*x**4-84*x**5+70*x**6-20*x**7
    S=Interval(s(t.a),s(t.b)) # S'=140 t^3(1-t)^3>=0
    Sp=64*140*t**3*(1-t)**3
    Spp=64**2*420*t**2*(1-t)**2*(1-2*t)
    Sppp=64**3*840*t*(1-t)*(1-5*t+5*t**2)
    return h+S*(F(7,8)-h),(1-S)*hp+Sp*(F(7,8)-h),(1-S)*hpp-2*Sp*hp+Spp*(F(7,8)-h),(1-S)*hppp-3*Sp*hpp-3*Spp*hp+Sppp*(F(7,8)-h)

def check_derivatives():
    maxima=[F(0)]*4;cells=0
    for lo,hi,n,tr in [(F(0),F(1,4),256,False),(F(1,4),F(17,64),1024,True)]:
        for j in range(n):
            vals=derivatives(Interval(lo+(hi-lo)*j/n,lo+(hi-lo)*(j+1)/n),tr)
            for i,v in enumerate(vals):maxima[i]=max(maxima[i],v.bound())
            cells+=1
    assert maxima[2]<=1016 and maxima[3]<=459410
    for p in [F(1,4),F(17,64)]:
        left=derivatives(Interval(p),p==F(17,64));right=derivatives(Interval(p),True) if p==F(1,4) else [Interval(F(7,8)),Interval(0),Interval(0),Interval(0)]
        assert all(a.a==a.b==b.a==b.b for a,b in zip(left,right))
    return {'cells':cells,'M2_ceiling':-(-maxima[2].numerator//maxima[2].denominator),'M3_ceiling':-(-maxima[3].numerator//maxima[3].denominator),'original_bounds_1016_459410_verified':True,'C3_joins_orders_0_to_3':True,'right_segment_constant':True}

class Poly:
    """Integer bivariate polynomial in m,K, with exact normalized coefficients."""
    def __init__(self,terms):self.t={k:v for k,v in terms.items() if v}
    @staticmethod
    def wrap(x):return x if isinstance(x,Poly) else Poly({(0,0):x})
    def __add__(self,x):
        x=self.wrap(x);r=self.t.copy()
        for k,v in x.t.items():r[k]=r.get(k,0)+v
        return Poly(r)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.t.items()})
    def __sub__(self,x):return self+-self.wrap(x)
    def __rsub__(self,x):return self.wrap(x)+-self
    def __mul__(self,x):
        x=self.wrap(x);r={}
        for (i,j),a in self.t.items():
            for (k,l),b in x.t.items():r[i+k,j+l]=r.get((i+k,j+l),0)+a*b
        return Poly(r)
    __rmul__=__mul__
    def __pow__(self,n):
        out=Poly.wrap(1)
        for _ in range(n):out=out*self
        return out

def product(xs):
    out=Poly.wrap(1)
    for x in xs:out=out*x
    return out
def check_moment_identity():
    m=Poly({(1,0):1});K=Poly({(0,1):1});D=product(4*m-j for j in range(4))
    stirling=[[1],[0,1],[0,1,1],[0,1,3,1],[0,1,7,6,1]]
    moments=[]
    for r in range(5):
        moments.append(sum((stirling[r][s]*product(m-j for j in range(s))*product(K-j for j in range(s))*product(4*m-j for j in range(s,4)) for s in range(r+1)),Poly.wrap(0)))
    # E[(J/m-K/(4m))^4], common denominator 256*m^4*(4m)_4.
    num=sum((comb(4,r)*4**r*(-K)**(4-r)*moments[r] for r in range(5)),Poly.wrap(0));den=256*m**4*D
    wn=K*(4*m-K);wd=16*m**2
    target_num=3*wn*((18*m**2-21*m)*wn+(-m+2)*wd)
    target_den=wd**2*m*(2*m-1)*(4*m-3)*(4*m-1)
    difference=num*target_den-target_num*den
    assert not difference.t
    # Independent finite checks at boundary/small populations, ancillary only.
    checks=0
    for n in range(1,17):
        for k in range(4*n+1):
            x=F(k,4*n);w=x*(1-x)
            exact=sum((F(comb(k,j)*comb(4*n-k,n-j),comb(4*n,n))*(F(j,n)-x)**4 for j in range(max(0,n-(4*n-k)),min(n,k)+1)),F(0))
            formula=3*w*((18*n*n-21*n)*w-n+2)/(n*(2*n-1)*(4*n-3)*(4*n-1))
            assert exact==formula and exact<=F(1,n*n);checks+=1
    return {'symbolic_cross_multiplied_polynomial_identically_zero':True,'denominators_nonzero_for_integer_m_ge_1':True,'small_boundary_checks':checks,'scope':'symbolic identity for all m,K; small checks do not prove the general tail bound'}

def main():
    t=time.perf_counter();cpu=time.process_time();deriv=check_derivatives();moment=check_moment_identity()
    M2,M3,A,s,m0=1016,459410,920854,246,60516
    assert A==2*(M2+M3+1) and s*s==m0 and s*s>=2*M2 and s**3>=16*A
    assert F(M2,8*m0)+F(A,m0*s)<=F(1,8)
    assert F(9*M2,32)+F(7*M3,48)<=F(7*A,8)
    assert F(M2,4)+F(7*M3,48)<=A
    assert 8+m0+F(12*A,s)==F(4323192,41)
    result={'status':'VERIFIED','derivatives':deriv,'hypergeometric_moment':moment,'all_level_constant_inequalities':True,'L_run':'4323192/41','wall_seconds':time.perf_counter()-t,'cpu_seconds':time.process_time()-cpu}
    (OUT/'independent_factory.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result))
if __name__=='__main__':main()

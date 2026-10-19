"""Independent deterministic checks; only stdlib, no project-code imports.

Bellman: Decimal-directed likelihood arithmetic (no omitted states), then
integer-directed DP at scale 1e18. Box: survival polynomials in the POWER basis,
affine substitution, then exact conversion to Bernstein. Profiles: exact
unnormalized integer probability mass, not rounded probability arrays.
"""
from __future__ import annotations
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from pathlib import Path
from math import comb, lcm
from itertools import product, combinations
import json,time,hashlib,argparse

OUT=Path(__file__).resolve().parent
ART=OUT/'isolated_artifact'
LOW=(F(167,3125),F(5351,100000));HIGH=(F(15027,1000),F(15059,1000))
ELL=F(52467170135279,200000000000);U=F(262335850819,10**9)
def read(path: str):return json.loads((ART/path).read_text(encoding='utf8'))
def save(name: str,data):
    (OUT/(name+'.json')).write_text(json.dumps(data,indent=2),encoding='utf8')
def ceildiv(a:int,b:int)->int:return -(-a//b)
def interval_string(x:F,scale:int=10**18):
    return [str(F(x.numerator*scale//x.denominator,scale)),str(F(ceildiv(x.numerator*scale,x.denominator),scale))]

def bellman(x:F,u:F,v:F,H:int,up:bool)->F:
    scale=10**18
    rounding=ROUND_CEILING if up else ROUND_FLOOR
    div=ceildiv if up else lambda a,b:a//b
    cap=div(u.numerator*scale,u.denominator)
    with localcontext() as ctx:
        ctx.prec=70;ctx.rounding=rounding
        ratio=Decimal(31)/Decimal(15)
        decay=Decimal(30)/Decimal(31)
        initial=Decimal((v*x).numerator)/Decimal((v*x).denominator)
        starts=[initial]
        for _ in range(H):starts.append(starts[-1]*decay)
        def stops(t:int):
            z=starts[t]*scale;result=[]
            for k in range(t+1):
                terminal=int(z.to_integral_value(rounding=rounding))
                if terminal>=cap:
                    result.extend([cap]*(t+1-k));break
                result.append(terminal);z=z*ratio
            return result
        vals=stops(H) if up else [0]*(H+1)
        for t in range(H-1,0,-1):
            terminal=stops(t)
            vals=[min(terminal[k],scale+div(31*vals[k]+vals[k+1],32)) for k in range(t+1)]
        return F(scale+div(31*vals[0]+vals[1],32),scale)

def check_bellman():
    # Q at x=1; min with both immediate decisions is required at the root.
    u,v=F(116329,200),F(937697,500)
    q=bellman(F(1),u,v,8000,False)
    lower=min(q,u,v)-(u+v)/20
    assert lower>=ELL
    result={'independent_lower':str(lower),'claimed_lower':str(ELL),'lower_verified':True,'precision':70,'integer_scale':10**18,'omitted_states':0,'probes':[]}
    for name,x,u,v,up in [
        ('stop0',LOW[0],F(581637,1000),F(1875395,1000),False),
        ('continue_low',LOW[1],F(581647,1000),F(1875388,1000),True),
        ('continue_high',HIGH[0],F(581637,1000),F(1875395,1000),True),
        ('stop1',HIGH[1],F(581647,1000),F(1875388,1000),False)]:
        q=bellman(x,u,v,6000,up);stop=min(u,v*x)
        margin=stop-q if up else q-stop
        assert margin>0
        result['probes'].append({'name':name,'bound':str(q),'strict_margin':str(margin),'direction':'upper' if up else 'lower'})
        print(name,float(margin),flush=True)
    return result

def schedule(a:F,b:F,H:int,tie_a:bool=False,tie_b:bool=False):
    active={0};rows=[{0:2}];p30=p31=1
    powers30=[30**i for i in range(H+1)];powers31=[31**i for i in range(H+1)]
    for t in range(1,H+1):
        row={}
        for k in sorted(active|{j+1 for j in active}):
            num=(1<<k)*powers30[t-k];den=powers31[t-k]
            l=num*a.denominator-a.numerator*den;r=num*b.denominator-b.numerator*den
            row[k]=0 if l<0 or (l==0 and not tie_a) else 1 if r>0 or (r==0 and not tie_b) else 2
        rows.append(row);active={k for k,s in row.items() if s==2}
    return rows

def power_duration(rows,H:int):
    coefficients=[0]*H;alive={0:1}
    # E min(N,H)=sum_{t=0}^{H-1} P(N>t).
    for t in range(H):
        for k,count in alive.items():
            for j in range(t-k+1):coefficients[k+j]+=count*comb(t-k,j)*(-1)**j
        reached={}
        for k,count in alive.items():
            reached[k]=reached.get(k,0)+count;reached[k+1]=reached.get(k+1,0)+count
        alive={k:c for k,c in reached.items() if rows[t+1].get(k)==2}
    return coefficients

def bernstein_restrict_sign(power:list[int],A:int,C:int,B:int):
    # Derivative degree elevated to H-1, matching the claimed degree.
    d=len(power)-1;c=[(j+1)*power[j+1] for j in range(d)]+[0]
    q=[sum(c[l]*comb(l,j)*A**(l-j)*B**(d-l) for l in range(j,d+1))*(C-A)**j for j in range(d+1)]
    scale=lcm(*(comb(d,j) for j in range(d+1)))
    b=[sum(q[j]*comb(i,j)*(scale//comb(d,j)) for j in range(i+1)) for i in range(d+1)]
    return b

def check_box():
    H=400;outer=schedule(LOW[0],HIGH[1],H,True,True);events=[set(),set()]
    for t,row in enumerate(outer[1:],1):
        for k in row:
            ratio=F((1<<k)*30**(t-k),31**(t-k))
            for side,(a,b) in enumerate((LOW,HIGH)):
                if a<=ratio<=b:events[side].add(ratio)
    assert [len(x) for x in events]==[2,2]
    reps=[]
    for e,interval in zip(events,(LOW,HIGH)):
        assert not(e&set(interval));p=sorted(e|set(interval))
        reps.append(sorted(set(p)|{(a+b)/2 for a,b in zip(p,p[1:])}))
    seen={};cases=0
    for a,b,ta,tb in product(*reps,(False,True),(False,True)):
        rows=schedule(a,b,H,ta,tb);key=tuple(tuple(row.items()) for row in rows);cases+=1
        if key in seen:continue
        polynomial=power_duration(rows,H)
        low=bernstein_restrict_sign(polynomial,0,1,32)
        high=bernstein_restrict_sign(polynomial,2,11,32)
        assert min(low)>=0 and max(high)<=0
        seen[key]={'lower':str(a),'upper':str(b),'tie_low':ta,'tie_high':tb,'coefficients_per_interval':len(low),'all_low_nonnegative':True,'all_high_nonpositive':True}
    assert len(seen)==9
    old=read('artifacts/development/cycle_08_scalar_closure/run_001/box_certificate_full.json')
    assert [sorted(map(F,e)) for e in old['events']]==[sorted(e) for e in events]
    return {'threshold_and_tie_cases':cases,'prefix_patterns':len(seen),'events':[list(map(str,sorted(e))) for e in events],'proofs':list(seen.values()),'continuous_intervals':['[0,1/32]','[1/16,11/32]'],'method':'exact power polynomial substitution then Bernstein conversion; no point grid'}

def exact_profile(rows,p:F):
    den=1;alive={0:1};cost=0;absorbed=[0,0];a,d=p.numerator,p.denominator
    for row in rows[1:]:
        cost=d*(cost+sum(alive.values()));absorbed=[d*x for x in absorbed];den*=d
        nxt={}
        for k,value in alive.items():
            nxt[k]=nxt.get(k,0)+(d-a)*value;nxt[k+1]=nxt.get(k+1,0)+a*value
        alive={}
        for k,value in nxt.items():
            action=row[k]
            if action==2:alive[k]=value
            else:absorbed[action]+=value
    survival=sum(alive.values())
    assert sum(absorbed)+survival==den
    return F(cost,den),[F(z,den) for z in absorbed],F(survival,den)

def check_profiles():
    cert=read('research/cycle_09_executable_auditor/certificates/scalar_1e6.json')
    result=[];costs=[F(0),F(0)];errors=[F(0),F(0)]
    weights=dict(zip(cert['mixture']['policy_indices'],map(F,cert['mixture']['weights'])))
    for index,policy in enumerate(cert['policies']):
        weight=weights.get(index,F(0));rows=schedule(F(policy['lower']),F(policy['upper']),6000)
        for side,p in enumerate((F(1,32),F(1,16))):
            c,e,s=exact_profile(rows,p);cu=c+600*s;eu=e[1-side]+s
            assert cu<=F(policy['endpoint_cost_upper'][side]);assert eu<=F(policy['endpoint_error_upper'][side])
            costs[side]+=weight*cu;errors[side]+=weight*eu
            result.append({'component':index,'p':str(p),'cost_prefix_interval':interval_string(c),'cost_with_tail_interval':interval_string(cu),'error_with_tail_interval':interval_string(eu),'tail_upper_interval':interval_string(s),'mass_identity':True})
    assert sum(map(F,cert['mixture']['weights']))==1
    assert min(map(F,cert['mixture']['weights']))>=0
    assert max(costs)<=U and max(errors)<=F(1,20)
    outer=schedule(LOW[0],HIGH[1],6000,True,True)
    outer_errors=[]
    for side,p in enumerate((F(1,32),F(1,16))):
        c,e,s=exact_profile(outer,p)
        assert e[1-side]+s<=F(1,20)-F(1,20000)
        outer_errors.append(interval_string(e[1-side]+s))
        if side==1:assert c+600*s<212
    return {'profiles':result,'all_nine_planes_independently_checked':len(cert['policies'])==9,'mixture_cost_upper_intervals':list(map(interval_string,costs)),'mixture_error_upper_intervals':list(map(interval_string,errors)),'outer_E1_upper_interval':interval_string(c+600*s),'outer_error_upper_intervals':outer_errors,'U':str(U),'delta':str(U-ELL),'exact_integer_propagation':True}

def log_interval(x:F):
    if x<1:
        l,h=log_interval(1/x);return -h,-l
    k=0
    while x>2:x/=2;k+=1
    z=(x-1)/(x+1);lo=2*sum((z**(2*j+1)/(2*j+1) for j in range(60)),F(0));hi=lo+2*z**121/(121*(1-z*z))
    if k:
        a,b=log_interval(F(2));lo+=k*a;hi+=k*b
    return lo,hi

def check_tail_localization():
    a0,a1=log_interval(LOW[0]);b0,b1=log_interval(HIGH[1]);c0,c1=log_interval(F(2));d0,d1=log_interval(F(31,30))
    neg=(31*d0-c1)/32;pos=(c0-15*d1)/16;width=b1-a0
    assert neg>0 and pos>0 and 180*d0>width
    assert a0+400*neg>0 and b1-400*pos<0
    assert (width+d1)/neg<600 and (width+c1)/pos<600
    items=read('artifacts/development/cycle_08_scalar_closure/run_001/mixture_certificate.json')['policies']
    planes=[(F(1),F(0),F(0)),(F(0),F(1),F(0))]
    for item in items:
        e0,e1=map(F,item['endpoint_error_upper']);planes.append((e0-F(1,20),e1-F(1,20),ELL-F(item['endpoint_cost_upper'][0])))
    assert any(a<0 and b<0 for a,b,c in planes)
    vertices=set()
    for (a,b,c),(d,e,f) in combinations(planes,2):
        determinant=a*e-b*d
        if not determinant:continue
        x,y=(c*e-b*f)/determinant,(a*f-c*d)/determinant
        if all(i*x+j*y>=k for i,j,k in planes):vertices.add((x,y))
    assert len(vertices)==4
    assert all(F(581637,1000)<x<F(581647,1000) and F(1875388,1000)<y<F(1875395,1000) for x,y in vertices)
    return {'residual_upper_600':True,'duration_monotonic_tail_from':400,'zero_block':180,'dual_polygon_vertices':[[str(x),str(y)] for x,y in sorted(vertices)],'strict_rectangle_inclusion':True,'boundedness_strict_negative_plane':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('part',choices=['bellman','box','profiles','tail']);args=ap.parse_args()
    t=time.perf_counter();cpu=time.process_time()
    result={'bellman':check_bellman,'box':check_box,'profiles':check_profiles,'tail':check_tail_localization}[args.part]()
    result.update(status='VERIFIED',wall_seconds=time.perf_counter()-t,cpu_seconds=time.process_time()-cpu)
    save('independent_'+args.part,result);print(args.part,'VERIFIED',result['wall_seconds'],flush=True)
if __name__=='__main__':main()

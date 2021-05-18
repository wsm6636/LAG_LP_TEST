from platforms import *
from opt import opt

def test_cpu_nopt(tasks, cpu, tk):
    A = cpu.A
    M = cpu.M
    uc = sum(t.e/t.p for t in tasks) 
    LHS = uc
    maxa = max(t.a for t in tasks)
    uck = tk.e/tk.p
    RHS = math.ceil((A - tk.a +1) / maxa) * (1-uck)+uck
    return (LHS <= RHS)

def test_cache_nopt(tasks,cpu,tk):
    A = cpu.A
    M = cpu.M
    ua = sum((t.a*t.e)/t.p for t in tasks)
    LHS = ua
    mina = min(t.a for t in tasks)
    uak = (tk.a * tk.e) / tk.p
    uck = tk.e/tk.p
    RHS = min(M*mina,A-tk.a+1) * (1-uck) + uak
    return (LHS <= RHS)

def test_cpu_opt(tasks, cpu, tk):
    A = cpu.A
    M = cpu.M
    uc = sum(t.e/t.p for t in tasks) 
    LHS = uc
    maxa = max(t.a for t in tasks)
    uck = tk.e/tk.p
    Ak = opt(tasks,cpu,tk)
    if Ak == 0:
        Ak = A-tk.a+1
    RHS = math.ceil((Ak) / maxa) * (1-uck)+uck
    return (LHS <= RHS)

def test_cache_opt(tasks,cpu,tk):
    A = cpu.A
    M = cpu.M
    ua = sum((t.a*t.e)/t.p for t in tasks)
    LHS = ua
    mina = min(t.a for t in tasks)
    uak = (tk.a * tk.e) / tk.p
    uck = tk.e/tk.p
    Ak = opt(tasks,cpu,tk)
    if Ak == 0:
        Ak = A-tk.a+1
    RHS = min(M*mina,Ak) * (1-uck) + uak
    return (LHS <= RHS)

def LAG_opt_solution(tasks, cpu, tk):
    if test_cache_opt(tasks,cpu,tk) or test_cpu_opt(tasks,cpu,tk):
        return True
    return False
    
def LAG_nopt_solution(tasks, cpu, tk):
    if test_cache_nopt(tasks,cpu,tk) or test_cpu_nopt(tasks,cpu,tk):
        return True
    return False

def LAG_Analysis(tasks, cpu, solution):
    for t in tasks:
        if not solution(tasks,cpu,t):
            return False
    return True
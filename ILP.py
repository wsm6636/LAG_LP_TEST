from mip import Model, model, xsum, maximize, INTEGER, CONTINUOUS
from opt import opt
from platforms import *

def ILP_opt_solution(tasks, cpu, tk, model=Model()):
    # init
    M = cpu.M
    Sk = tk.s
    tasks = [t for t in tasks if t!=tk]
    n = len(tasks)
    I = [t.W(Sk) for t in tasks]
    a = [t.a for t in tasks]
    Ak = opt(tasks, cpu, tk)

    if (n <= 0):
        return 0
    if (Ak == 0):
        return (1/M) * sum(I[i] for i in range(n))

    # model = Model()
    model.clear()
    x = {i: model.add_var(obj=0, var_type="C", name="x[%d]" % i)
        for i in range(n)}
    y = {i: model.add_var(obj=0, var_type="C", name="y[%d]" % i)
        for i in range(n)}

    model.objective = maximize(xsum((1/M) * x[i] + (a[i]/Ak) * y[i] for i in range(n)))
    model.verbose = False

    for i in range(n):
        model += x[i] + y[i] <= I[i]
    for i in range(n):
        model += x[i] <= xsum((1/M)*x[j] for j in range(n))
    for i in range(n):
        model += y[i] <= xsum((a[j]/Ak)*y[j] for j in range(n))

    model.optimize()

    return model.objective_value

def ILP_optA_solution(tasks, cpu, tk, model=Model()):
    # init
    A = cpu.A
    M = cpu.M
    Sk = tk.s
    tasks = [t for t in tasks if t!=tk]
    n = len(tasks)
    I = [t.W(Sk) for t in tasks]
    a = [t.a for t in tasks]
    Ak = opt(tasks, cpu, tk)

    if (n <= 0):
        return 0
    if (Ak == 0):
        Ak = A
    # Ak = A

    # model = Model()
    model.clear()
    x = {i: model.add_var(obj=0, var_type="C", name="x[%d]" % i)
        for i in range(n)}
    y = {i: model.add_var(obj=0, var_type="C", name="y[%d]" % i)
        for i in range(n)}

    model.objective = maximize(xsum((1/M) * x[i] + (a[i]/Ak) * y[i] for i in range(n)))
    model.verbose = False

    for i in range(n):
        model += x[i] + y[i] <= I[i]
    for i in range(n):
        model += x[i] <= xsum((1/M)*x[j] for j in range(n))
    for i in range(n):
        model += y[i] <= xsum((a[j]/Ak)*y[j] for j in range(n))

    model.optimize()

    return model.objective_value

def ILP_nopt_solution(tasks, cpu, tk, model=Model()):
    # init
    A = cpu.A
    M = cpu.M
    Sk = tk.s
    tasks = [t for t in tasks if t!=tk]
    n = len(tasks)
    I = [t.W(Sk) for t in tasks]
    a = [t.a for t in tasks]
    Ak = A - tk.a + 1

    if (n <= 0):
        return 0

    # model = Model()
    model.clear()
    x = {i: model.add_var(obj=0, var_type="C", name="x[%d]" % i)
        for i in range(n)}
    y = {i: model.add_var(obj=0, var_type="C", name="y[%d]" % i)
        for i in range(n)}

    model.objective = maximize(xsum((1/M) * x[i] + (a[i]/Ak) * y[i] for i in range(n)))
    model.verbose = False

    for i in range(n):
        model += x[i] + y[i] <= I[i]
    for i in range(n):
        model += x[i] <= xsum((1/M)*x[j] for j in range(n))
    for i in range(n):
        model += y[i] <= xsum((a[j]/Ak)*y[j] for j in range(n))

    model.optimize()

    return model.objective_value

def ILP_guan_solution(tasks, cpu, tk, model = Model()):
    # init
    A = cpu.A
    M = cpu.M
    Sk = tk.s
    tasks = [t for t in tasks if t!=tk]
    n = len(tasks)
    I = [t.I_guan(Sk) for t in tasks]
    a = [t.a for t in tasks]
    Ak = A - tk.a + 1

    if (n<=0):
        return 0

    # model = Model()
    model.clear()
    x = {i: model.add_var(obj=0, var_type="C", name="x[%d]" % i)
        for i in range(n)}
    y = {i: model.add_var(obj=0, var_type="C", name="y[%d]" % i)
        for i in range(n)}

    model.objective = maximize(xsum((1/M) * x[i] + (a[i]/Ak) * y[i] for i in range(n)))
    model.verbose = False

    for i in range(n):
        model += x[i] + y[i] <= I[i]
    for i in range(n):
        model += x[i] <= xsum((1/M)*x[j] for j in range(n))
    for i in range(n):
        model += y[i] <= xsum((a[j]/Ak)*y[j] for j in range(n))

    model.optimize()

    return model.objective_value

def ILP_Analysis(tasks, cpu, solution):
    model = Model()
    for t in tasks:
        bk = solution(tasks, cpu, t, model)
        if t.s < bk:
            return False
    return True

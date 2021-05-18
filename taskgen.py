import random
import numpy as np
from platforms import *

def gen_uunifastdiscard(nsets, u, n):
    """
    The UUniFast algorithm was proposed by Bini for generating task
    utilizations on uniprocessor architectures.
    The UUniFast-Discard algorithm extends it to multiprocessor by
    discarding task sets containing any utilization that exceeds 1.
    This algorithm is easy and widely used. However, it suffers from very
    long computation times when n is close to u. Stafford's algorithm is
    faster.
    Args:
        - `n`: The number of tasks in a task set.
        - `u`: Total utilization of the task set.
        - `nsets`: Number of sets to generate.
    Returns `nsets` of `n` task utilizations.
    """
    sets = []
    while len(sets) < nsets:
        # Classic UUniFast algorithm:
        utilizations = []
        sumU = u
        for i in range(1, n):
            nextSumU = sumU * random.random() ** (1.0 / (n - i))
            utilizations.append(sumU - nextSumU)
            sumU = nextSumU
        utilizations.append(sumU)

        # If no task utilization exceeds 1:
        if all(ut <= 1 for ut in utilizations):
            sets.append(utilizations)

    return sets

def gen_vars_loguniform(nsets, min_, max_, n, round_to_int=False):
    """
    Generate a list of `nsets` sets containing each `n` random periods using a
    loguniform distribution.
    Args:
        - `n`: The number of tasks in a task set.
        - `nsets`: Number of sets to generate.
        - `min_`: Period min.
        - `max_`: Period max.
    """
    periods = np.exp(np.random.uniform(low=np.log(min_), high=np.log(max_),
                                       size=(nsets, n)))
    if round_to_int:
        return np.rint(periods).tolist()
    else:
        return periods.tolist()

def gen_vars_uniform(nsets, min_, max_, n, round_to_int=False):
    """
    Generate a list of `nsets` sets containing each `n` random periods using a
    uniform distribution.
    Args:
        - `nsets`: Number of sets to generate.
        - `min_`: Period min.
        - `max_`: Period max.
        - `n`: The number of tasks in a task set.
    """
    periods = np.random.uniform(low=min_, high=max_, size=(nsets, n))

    if round_to_int:
        return np.rint(periods).tolist()
    else:
        return periods.tolist()


def gen_cpasets(utilizations, periods, caches):
    """
    Take a list of task utilization sets and a list of task period sets and
    return a list of couples (c, p) sets. The computation times are truncated
    at a precision of 10^-10 to avoid floating point precision errors.
    - Args:
        - `utilization`: The list of task utilization sets. For example::
            [[0.3, 0.4, 0.8], [0.1, 0.9, 0.5]]
        - `periods`: The list of task period sets. For examples::
            [[100, 50, 1000], [200, 500, 10]]
    - Returns:
        For the above example, it returns::
            [[(30.0, 100), (20.0, 50), (800.0, 1000)],
             [(20.0, 200), (450.0, 500), (5.0, 10)]]
    """
    def trunc(x, p):
        return int(x * 10 ** p) / float(10 ** p)

    # return [[(math.floor(ui * pi), np.rint(pi)) for ui, pi in zip(us, ps)]
    #         for us, ps in zip(utilizations, periods)]
    return [[(trunc(ui * pi, 6), trunc(pi, 6), int(ci)) for ui, pi, ci in zip(us, ps, cs)]
            for us, ps, cs in zip(utilizations, periods, caches)]

def gen_cpasets_utotf(utilizations, periods, caches, utot=1):
    """
    Take a list of task utilization sets and a list of task period sets and
    return a list of tuples (c, p, a) sets. The computation times are truncated
    at a precision of 10^-10 to avoid floating point precision errors.
    - Args:
        - `utilization`: The list of task utilization sets. For example::
            [[0.3, 0.4, 0.8], [0.1, 0.9, 0.5]]
        - `periods`: The list of task period sets. For examples::
            [[100, 50, 1000], [200, 500, 10]]
    - Returns:
        For the above example, it returns::
            [[(30.0, 100), (20.0, 50), (800.0, 1000)],
             [(20.0, 200), (450.0, 500), (5.0, 10)]]
    """
    def trunc(x, p):
        return int(x * 10 ** p) / float(10 ** p)

    cpasets=[]
    for us, ps, cs in zip(utilizations, periods, caches):
        cpas = []
        usum = 0
        for ui, pi, ci in zip(us, ps, cs):
            usum += ui
            if (usum <= utot):
                cpas.append((trunc(ui * pi, 6), trunc(pi, 6), int(ci)))
            # dong's method
            else:
                lastu = utot - usum + ui - 1E-6
                cpas.append((trunc(lastu * pi, 6), trunc(pi, 6), int(ci)))
                break
        cpasets.append(cpas)
    return cpasets

def gen_cpasets_utot(utilizations, periods, caches, utot=1):
    """
    Take a list of task utilization sets and a list of task period sets and
    return a list of tuples (c, p, a) sets. The computation times are truncated
    at a precision of 10^-10 to avoid floating point precision errors.
    - Args:
        - `utilization`: The list of task utilization sets. For example::
            [[0.3, 0.4, 0.8], [0.1, 0.9, 0.5]]
        - `periods`: The list of task period sets. For examples::
            [[100, 50, 1000], [200, 500, 10]]
    - Returns:
        For the above example, it returns::
            [[(30.0, 100), (20.0, 50), (800.0, 1000)],
             [(20.0, 200), (450.0, 500), (5.0, 10)]]
    """
    def trunc(x, p):
        return int(x * 10 ** p) / float(10 ** p)

    cpasets=[]
    for us, ps, cs in zip(utilizations, periods, caches):
        cpas = []
        usum = 0
        for ui, pi, ci in zip(us, ps, cs):
            usum += ui
            if (usum <= utot):
                cpas.append((trunc(ui * pi, 6), trunc(pi, 6), int(ci)))
        cpasets.append(cpas)
    return cpasets

def gen_tasksets_fullnum(cpasets):
    return [[task(t[0],t[1],t[1],t[2]) for t in cpas] 
            for cpas in cpasets]

def gen_tasksets_utot(capsets, utot=1):
    """
    - Args:
        - cap: tuples (c, p, a) % wcet, period, cache
        - utot: total utilization of task set
    - Returns:
        a set of task set
    """
    tasksets = []
    for caps in capsets:
        tset = []
        usum = 0
        for t in caps:
            usum += t[0]/t[1]
            if usum < utot:
                tset.append(task(t[0],t[1],t[1],t[2]))
        tasksets.append(tset)
    return tasksets


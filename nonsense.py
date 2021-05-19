# from platforms import task, cpu
from functools import wraps
# from ILP import *
# from schedulers import *

def decorator(f):
    @wraps(f)
    def wrapping(*args, **kwargs):
        result = f(*args, **kwargs)
        if result == 1:
            return True
        return result
    return wrapping

@decorator
def f(x):
    return x

def main():
    # mp = cpu(3,10)
    # t1=task(2,8,8,4)
    # t2=task(2,8,8,4)
    # t3=task(3,8,8,6)
    # taskset = [t1,t2,t3]
    # scheduler = gEDFca(taskset,mp)
    # result = scheduler.schedulable(ILP_Analysis)
    # print(result)
    x = 1
    print(f(x))

if __name__ == "__main__":
    main()

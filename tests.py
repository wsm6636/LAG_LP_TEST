from taskgen import *
import time, ILP
 #1
if __name__ == "__main__":
    nset = 1
    # u = gen_uunifastdiscard(nset,1,100)
    u = gen_vars_uniform(nset,0.01,0.3,1000,False)
    p = gen_vars_uniform(nset,10,20,1000,False)
    a = gen_vars_uniform(nset,1,2,1000)
    # p = gen_vars_loguniform(1,100,1000,1000)
    cpa = gen_cpasets(u,p,a)
    # cpa = gen_cpasets_utot(u,p,a,utot=1)
    tasks= gen_tasksets_fullnum(cpa)

    processor=cpu(6,500)
    # print([(t.e,t.d,t.d,t.a) for t in tasks[0]])
    for i in range(nset):
        # resut = ILP.ILP_Analysis(tasks[i],processor)
        # print(resut)
        start_time = time.time()
        result = ILP.ILP_solution(tasks[i],processor,tasks[i][0])
        end_time = time.time()
        print("--- %s seconds ---" % (end_time - start_time))
        print(len(tasks[i]),sum([t.e/t.p for t in tasks[i]]))

    # cpa = gen_cpasets(u,p,a)
    # tasks= gen_tasksets_utot(cpa)

    # # tasks = gen_tasksets_utot(cpa,utot=1)
    # processor=cpu(6,500)
    # # print(cpa)
    # print([(t.e,t.d,t.d,t.a) for t in tasks[0]])
    # for i in range(nset):
    #     # resut = ILP.ILP_Analysis(tasks[i],processor)
    #     # print(resut)
    #     print(len(tasks[i]),sum([t.e/t.p for t in tasks[i]]))

# print(max(0.1, min(10, random.lognormvariate(0, 1))) * 10)

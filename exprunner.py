from taskgen import *
import time
import ILP
import LAG
# import schedulers
from platforms import *
import matplotlib.pyplot as plt


class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start

def runexp_scaliability():
    processor=cpu(6,40)
    numset = 1
    u = gen_vars_uniform(numset,0.1,0.3,10000)
    p = gen_vars_uniform(numset,10,20,10000)
    a = gen_vars_uniform(numset,1,5,10000,round_to_int=True)
    # p = gen_vars_loguniform(1,100,1000,1000)
    cpa = gen_cpasets(u,p,a)
    # cpa = gen_cpasets_utot(u,p,a,utot=1)
    tasks= gen_tasksets_fullnum(cpa)

    timestr = time.strftime("%m%dT%H%M",time.localtime(time.time()))
    # print([(t.e,t.d,t.d,t.a) for t in tasks[0]])
    for i in range(numset):
        with open("./result_scale_%s.out" % timestr, 'w') as f:
            for j in [2000,4000,6000,8000,10000]:
                with Timer() as t:
                    ILP.ILP_opt_solution(tasks[i][:j],processor,tasks[i][0])
                f.write("%.4f sec\n" % t.interval)

def Input_guan():
    processor = cpu(30,400)
    numset = 10
    u = gen_vars_uniform(numset,0.2,0.6,1000)
    p = gen_vars_uniform(numset,10,20,1000)
    a = gen_vars_uniform(numset,20,100,1000,round_to_int=True)
    xaxis = [i/10 for i in range(2,52,2)]
    setsetcpaset = [gen_cpasets_utotf(u,p,a,utot=U) for U in xaxis]
    # setsettaskset: a set of sets of task sets, each set has the same utot    
    setsettaskset = [gen_tasksets_fullnum(cpa) for cpa in setsetcpaset]
    return setsettaskset, processor, xaxis

def Input_guan_2():
    processor = cpu(30,100)
    numset = 100
    u = gen_vars_uniform(numset,0.2,0.6,1000)
    p = gen_vars_uniform(numset,10,20,1000)
    a = gen_vars_uniform(numset,40,50,1000,round_to_int=True)
    xaxis = [i/10 for i in range(2,32,2)]
    setsetcpaset = [gen_cpasets_utotf(u,p,a,utot=U) for U in xaxis]
    # setsettaskset: a set of sets of task sets, each set has the same utot    
    setsettaskset = [gen_tasksets_fullnum(cpa) for cpa in setsetcpaset]
    return setsettaskset, processor, xaxis
"""
def Input_guan_heavy():
    processor = cpu(4,20)
    numset = 100
    u = gen_vars_uniform(numset,0.2,0.4,1000)
    p = gen_vars_uniform(numset,15,20,1000)
    a = gen_vars_uniform(numset,8,10,1000,round_to_int=True)
    xaxis = [i/10 for i in range(2,22,2)]
    setsetcpaset = [gen_cpasets_utotf(u,p,a,utot=U) for U in xaxis]
    # setsettaskset: a set of sets of task sets, each set has the same utot    
    setsettaskset = [gen_tasksets_fullnum(cpa) for cpa in setsetcpaset]
    return setsettaskset, processor, xaxis
    """
def Input_guan_heavy():
    processor = cpu(4,20)
    numset = 1000
    u = gen_vars_uniform(numset,0.25,0.5,5000)
    p = gen_vars_uniform(numset,16,32,5000)
    a = gen_vars_uniform(numset,8,10,5000,round_to_int=True)
    xaxis = [i/10 for i in range(2,26,2)]
    setsetcpaset = [gen_cpasets_utotf(u,p,a,utot=U) for U in xaxis]
    # setsettaskset: a set of sets of task sets, each set has the same utot    
    setsettaskset = [gen_tasksets_fullnum(cpa) for cpa in setsetcpaset]
    return setsettaskset, processor, xaxis

def Input_guan_medium():
    processor = cpu(4,20)
    numset = 100
    u = gen_vars_uniform(numset,0.1,0.2,1000)
    p = gen_vars_uniform(numset,15,20,1000)
    a = gen_vars_uniform(numset,8,10,1000,round_to_int=True)
    xaxis = [i/10 for i in range(2,22,2)]
    setsetcpaset = [gen_cpasets_utotf(u,p,a,utot=U) for U in xaxis]
    # setsettaskset: a set of sets of task sets, each set has the same utot    
    setsettaskset = [gen_tasksets_fullnum(cpa) for cpa in setsetcpaset]
    return setsettaskset, processor, xaxis

def Input_guan_light():
    processor = cpu(4,20)
    numset = 100
    u = gen_vars_uniform(numset,0.05,0.1,1000)
    p = gen_vars_uniform(numset,15,20,1000)
    a = gen_vars_uniform(numset,8,10,1000,round_to_int=True)
    xaxis = [i/10 for i in range(2,22,2)]
    setsetcpaset = [gen_cpasets_utotf(u,p,a,utot=U) for U in xaxis]
    # setsettaskset: a set of sets of task sets, each set has the same utot    
    setsettaskset = [gen_tasksets_fullnum(cpa) for cpa in setsetcpaset]
    return setsettaskset, processor, xaxis

def Input_dong_light():
    M = 100
    A = 40
    processor = cpu(M,A)
    numset = 1000
    u = gen_vars_uniform(numset,0.1,0.3,10000)
    p = gen_vars_uniform(numset,20,200,10000)
    a = gen_vars_uniform(numset,2,A/4,10000,True)
    xaxis = [i/10 for i in range(1,A+2,2)]
    setsetcpaset = [gen_cpasets_utotf(u,p,a,utot) for utot in xaxis]
    setsettaskset = [gen_tasksets_fullnum(cpa) for cpa in setsetcpaset]
    return setsettaskset, processor, xaxis

def Input_dong_medium():
    M = 100
    A = 16
    processor = cpu(M,A)
    numset = 100
    u = gen_vars_uniform(numset,0.1,0.3,10000)
    p = gen_vars_uniform(numset,20,200,10000)
    a = gen_vars_uniform(numset,A/4,5*A/8,10000,True)
    xaxis = [i/10 for i in range(2,A+2,2)]
    setsetcpaset = [gen_cpasets_utotf(u,p,a,utot) for utot in xaxis]
    setsettaskset = [gen_tasksets_fullnum(cpa) for cpa in setsetcpaset]
    return setsettaskset, processor, xaxis

def Input_dong_heavy():
    M = 100
    A = 16
    processor = cpu(M,A)
    numset = 100
    u = gen_vars_uniform(numset,0.1,0.3,10000)
    p = gen_vars_uniform(numset,20,200,10000)
    a = gen_vars_uniform(numset,5*A/8,7*A/8,10000,True)
    xaxis = [i/10 for i in range(2,A+2,2)]
    setsetcpaset = [gen_cpasets_utotf(u,p,a,utot) for utot in xaxis]
    setsettaskset = [gen_tasksets_fullnum(cpa) for cpa in setsetcpaset]
    return setsettaskset, processor, xaxis

font0 = {'family':'Calibri',
    'weight':'normal',
    'size':18,
}
font = {'family':'Calibri',
    'weight':'normal',
    'size':22,
}
def runexp_schedulability(input=Input_guan,iname=input.__name__):
    # setsettaskset: a set of sets of task sets, each set has the same utot    
    setsettaskset, processor, xaxis = input()
    solutions = [ILP.ILP_opt_solution,ILP.ILP_nopt_solution]
    solnames=["opt","nopt"]
    strtime = time.strftime("%m%dT%H%M",time.localtime(time.time()))

    with open("./result_sched_%s_%s.out" % (input.__name__, strtime), 'w') as f:
        plt.figure(1)
        plt.subplot(111)
        plt.tick_params(labelsize=12)
        colors=['r','b','g','y','k']
        markers=['s','^','x','*','.']
        for sol in solutions:
            solname = f"{sol.__name__}"
            f.write(solname+'\n')
            print(solname)
            acrates = []
            for settaskset in setsettaskset:          #settaskset: a set of task sets
                acnum = 0
                for taskset in settaskset:            #taskset: a task set
                    if (ILP.ILP_Analysis(taskset,processor,sol)):
                        acnum += 1
                utot = sum([task.e/task.p for task in settaskset[0]]) 
                acrate = acnum / len(settaskset)    
                index = setsettaskset.index(settaskset)
                strresult= "%.2f %.2f %.3f" % (xaxis[index], utot, acrate)
                acrates.append(acrate)
                print(strresult)
                f.write(strresult+'\n')

            i = solutions.index(sol) % len(colors)
            plt.plot(xaxis, acrates, color=colors[i], linestyle="-", marker=markers[i], linewidth=1.0, label=solnames[i])
            plt.xticks(xaxis,xaxis)
        plt.legend(loc='upper right',prop=font0)
        plt.xlabel("Utilization",font)
        plt.ylabel("Access Rate",font)
        title = iname
        plt.title(title,font0)
        plt.savefig("./fig_"+title+'_'+strtime+'.pdf')
        plt.show()

def runexp_schedulability_LAG(input=Input_guan,iname=input.__name__):
    # setsettaskset: a set of sets of task sets, each set has the same utot    
    setsettaskset, processor, xaxis = input()
    solutions = [LAG.LAG_nopt_solution,LAG.LAG_opt_solution]
    solnames=["nopt","opt"]
    strtime = time.strftime("%m%dT%H%M",time.localtime(time.time()))

    with open("./result_sched_%s_%s.out" % (input.__name__, strtime), 'w') as f:
        plt.figure(1)
        plt.subplot(111)
        plt.tick_params(labelsize=12)
        colors=['r','b','g','y','k']
        markers=['s','^','x','*','.']
        for sol in solutions:
            solname = f"{sol.__name__}"
            f.write(solname+'\n')
            print(solname)
            acrates = []
            for settaskset in setsettaskset:          #settaskset: a set of task sets
                acnum = 0
                for taskset in settaskset:            #taskset: a task set
                    if (LAG.LAG_Analysis(taskset,processor,sol)):
                        acnum += 1
                utot = sum([task.e/task.p for task in settaskset[0]]) 
                acrate = acnum / len(settaskset)    
                index = setsettaskset.index(settaskset)
                strresult= "%.2f %.2f %.3f" % (xaxis[index], utot, acrate)
                acrates.append(acrate)
                print(strresult)
                f.write(strresult+'\n')

            i = solutions.index(sol) % len(colors)
            plt.plot(xaxis, acrates, color=colors[i], linestyle="-", marker=markers[i], linewidth=1.0, label=solnames[i])
            plt.xticks(xaxis,xaxis)
        plt.legend(loc='upper right',prop=font0)
        plt.xlabel("Utilization",font)
        plt.ylabel("Access Rate",font)
        title = iname
        plt.title(title,font0)
        plt.savefig("./fig_"+title+'_'+strtime+'.pdf')
        plt.show()
            
def plot_scal():
    plt.figure(1)
    plt.subplot(111)
    plt.tick_params(labelsize=12)
    xaxis = [2000,4000,6000,8000,10000]
    yaxis = [15,67,175,341,563]
    plt.plot(xaxis, yaxis, color='r', linestyle="-", marker="*", linewidth=1.0)
    plt.xticks(xaxis,xaxis)
    plt.xlabel("Number of tasks (#)")
    plt.ylabel("Time (sec)")
    title = "scaliability"
    plt.savefig("./fig_"+title+'.png')
    plt.show()
def main():
    runexp_scaliability()
    plot_scal()
    #runexp_schedulability(Input_guan_light,"light tasks")
    #runexp_schedulability(Input_guan_medium,"medium tasks")
    #runexp_schedulability(Input_guan_heavy,"heavy tasks")
    # runexp_schedulability(Input_dong_light)
    # runexp_schedulability(Input_dong_medium)
    
    #runexp_schedulability_LAG(Input_guan_light,"light tasks g")
    #runexp_schedulability_LAG(Input_guan_medium,"medium tasks g")
    #runexp_schedulability_LAG(Input_guan_heavy,"heavy tasks g")

    # runexp_schedulability_LAG(Input_dong_light,"light tasks dong")
    # runexp_schedulability_LAG(Input_dong_medium,"medium tasks dong")

if __name__ == "__main__":
    main()
import math
import random
 #1
class cpu():
    
    def __init__(self, M, A) -> None:
        self.M = M
        self.A = A

class task():

    def __init__(self, e, d, p, a):
        self.e = e
        self.d = d
        self.p = p
        self.a = a
        self.s = d - e
    
    def W(self, t):
        N = math.floor((t+self.d-self.e)/self.p) 
        w = self.e * N + max(min(t+self.d-self.e-self.p*N, self.e),0)
        return w

    def I_guan(self,t):
        N = math.floor(t /self.p)
        w = self.e * (N+2)
        return w
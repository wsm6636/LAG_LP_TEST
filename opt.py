def opt(tasks,cpu,tk):
    A = cpu.A
    a = [t.a for t in tasks if t!=tk]
    dp = [False for i in range(A+1)]
    dp[0] = True
    for i in range(len(a)):
        # if A >= a[i]:
        for j in range(A,a[i]-1,-1):
            dp[j] = dp[j] or dp[j-a[i]]
    for Ak in range(A - tk.a + 1, A+1):
        if dp[Ak]:
            return Ak
    return 0 # Ak not exists 1


# for n in range(0, 10) :
#     for m in range(0, 10):
#         f = n * 19.1 + m * 17.2
#         print("n=%d, m=%d, f=%f" % (n, m, f))




for n in range(1, 7) :
    
    f1 = n * 19.1

    if(n >3):
        m = n - 3
        x = min(n, 3)
        f2 = x * 19.1 + m * 17.2
        print("n=%d, x=%d, m=%d, f1=%f, f2=%f" % (n, x, m, f1, f2))

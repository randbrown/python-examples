def hour_min(mins):
    return '{0}:{1:02d}'.format(mins/60,mins%60)

for i in range(0, 200, 5):
    print i, ' = ', hour_min(i)

def masterConstraints(M, d, x, y, nourses, patients, days, hours, q, Q, f, et, lt):
    '''constraint 1'''
    for j in range(patients):
        M.Add(sum(x[i, j] for i in range(nourses)) == d[j])

    '''constraint 2'''
    for j in range(patients):
        M.Add(sum(sum(y[i, j + 1, k] for k in range(days)) for i in range(nourses)) == f[j + 1] * d[j])

    '''constraint 3'''
    for i in range(nourses):
        for j in range(patients):
            for k in range(days):
                M.Add(y[i, j + 1, k] <= x[i, j])

    '''constraint 4'''
    for i in range(nourses):
        for j in range(patients):
            if q[j + 1] != Q[i]:
                M.Add(x[i, j] == 0)

    '''constraint 5'''
    for i in range(nourses):
        for j in range(patients):
            for k in range(days):
                for tou in range(1, (4 - (f[j + 1]) + 1)):
                    if (k + tou) <= 4:
                        M.Add(y[i, j + 1, k] + y[i, j + 1, k + tou] <= 1)




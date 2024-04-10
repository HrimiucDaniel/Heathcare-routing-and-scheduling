def masterConstraints(M, d, x, y, s, nourses, patients, days, hours, q, Q, f, et, lt, sd):
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

    '''constraint 6'''
    for i in range(nourses):
        for j in range(patients):
            for k in range(days):
                for h in range(hours):
                    if et[j] <= h <= lt[j]:
                        M.Add(s[i, j, k, h] <= y[i, j, k])
                    else:
                        M.Add(s[i, j, k, h] == 0)

    '''constraint 7'''
    for i in range(nourses):
        for k in range(days):
            interval_variables = [s[i, j, k, l] for j in range(patients + 1) for l in range(hours)]

            M.Add(sum(interval_variables) <= 2400)

    '''constraint 8'''
    for j in range(patients):
        for k in range(days):
            for i in range(nourses):
                M.Add(sum(s[i, j, k, h] for h in range(hours)) == sd[j] * y[i, j, k])
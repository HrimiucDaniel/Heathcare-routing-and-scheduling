def decisionVariables(solver, nourses, patients, days, patients_variable, nourses_patients, nourses_patients_day):
    ''' decision variable: delta '''
    for i in range(patients):
        patients_variable[i] = solver.BoolVar('d_%i' % i)

    '''decision variable x'''
    for i in range(nourses):
        for j in range(patients):
            nourses_patients[i, j] = solver.BoolVar('x_%i_%i' % (i, j))

    '''decision variable y'''
    for i in range(nourses):
        for j in range(patients + 1):  # +1 is for depot
            for k in range(days):
                nourses_patients_day[i, j, k] = solver.BoolVar('y_%i_%i_%i' % (i, j, k))


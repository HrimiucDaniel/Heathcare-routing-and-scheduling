def decisionVariables(solver, nourses, patients, days, hours, patients_variable, nourses_patients, nourses_patients_day,
                      nourses_patients_day_hours):
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

    '''decision variable s'''
    for i in range(nourses):
        for j in range(patients + 1):  # +1 is for depot
            for k in range(days):
                for h in range(hours):
                    nourses_patients_day_hours[i, j, k, h] = solver.BoolVar('s_%i_%i_%i_%i' % (i, j, k, h))

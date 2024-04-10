def printSolution(M, solution_d, solution_x, solution_y, m, n, days, df, df_n, q, f):
    print('\nPatients:\n', df)
    print('\nNurses:\n', df_n)

    print('\nQualification of nurses:\n', q)
    print('\nFrequency of visits for each patient:\n', f)

    print('\nPatients visited:')
    for patient, visited in enumerate(solution_d):
        if visited:
            print('Patient {}: Visited'.format(patient))

    print('\nAssignment of nurses to patients:')
    for nurse in range(m):
        for patient in range(n):
            if solution_x[nurse, patient] == 1:
                print('Nurse {} --- Patient {}'.format(nurse, patient))

    print('\nSchedule of nurses:')
    for nurse in range(m):
        for location in range(n + 1):
            for day in range(days):
                if solution_y[nurse, location, day] == 1:
                    print('Nurse {} is at patient {} at day {} '.format(nurse, location, day))

    print('\nObjective value:', int(M.Objective().Value()))

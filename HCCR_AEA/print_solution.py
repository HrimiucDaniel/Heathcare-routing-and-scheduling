def printSolution(M, solution_d, solution_x, solution_y, solution_s, m, n, days, hours, df, df_n, q, f):
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
                for hour in range(hours):
                    if solution_s[nurse, location, day, hour] == 1:
                        print('Nurse {} is at patient {} at day {} at hour {}'.format(nurse, location, day, hour))

    print('\nObjective value:', int(M.Objective().Value()))

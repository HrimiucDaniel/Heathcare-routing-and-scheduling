'''objective funtion - 1'''
def objectiveFunction(solver, patients_variable, number_patients):
    solver.Maximize(solver.Sum(patients_variable[j] for j in range(number_patients)))


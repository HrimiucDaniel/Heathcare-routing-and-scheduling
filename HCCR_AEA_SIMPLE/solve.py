import timeit

import pandas as pd
from ortools.linear_solver import pywraplp

from decision_variables import decisionVariables
from distance import dist
from master_constraints import masterConstraints
from objective_function import objectiveFunction
from print_solution import printSolution


def main(number_of_patients):
    # Set up data directory
    data_dir = r"data\{}P.xlsx".format(number_of_patients)
    df = pd.read_excel(data_dir, 'patients', engine='openpyxl').fillna(0).astype('int')
    df_n = pd.read_excel(data_dir, 'nurses', engine='openpyxl').fillna(0).astype('int')

    # Extract relevant data
    number_days = 7  # Planning horizon
    number_patiens = df.shape[0] - 1  # Number of patients
    frequency = df["f"].astype('int').tolist()  # Frequency of visit for every patient
    et = df["et"].astype('int').tolist()  # Earliest service start time for each patient
    lt = df["lt"].astype('int').tolist()  # Latest service start time for each patient
    sd = df["sd"].astype('int').tolist()  # Service duration for each patient
    q = df["Q'"].astype('int').tolist()  # Qualification of first nurse required for each patient
    Q = df_n["Q"].astype('int').tolist()  # Qualification of each nurse
    number_nurses = df_n.shape[0]  # Number of nurses
    bigM = 10000  # Infinitely large number
    X, Y = df["x"].tolist(), df["y"].tolist()  # Coordinates X and Y of each patient and depot
    depot = [X[0], Y[0]]  # Depot coordinates
    grid = dist(X, Y)  # Get distance matrix
    start_time = timeit.default_timer()

    # Create the solver
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Initialize decision variables
    d, x, y = {}, {}, {}

    # Add decision variables to the solver
    decisionVariables(solver, number_nurses, number_patiens, number_days, d, x, y)

    # Add objective function to the solver
    objectiveFunction(solver, d, number_patiens)

    # Add master constraints to the solver
    masterConstraints(solver, d, x, y, number_nurses, number_patiens, number_days, q, Q, frequency)

    # Run solver
    status = solver.Solve()

    end_time = timeit.default_timer() - start_time

    if status == pywraplp.Solver.OPTIMAL:
        # Get attributes
        sol_d = {key: d[key].solution_value() for key in d}
        sol_x = {key: x[key].solution_value() for key in x}
        sol_y = {key: y[key].solution_value() for key in y}

        # Print solution
        printSolution(sol_y, number_nurses, number_patiens, number_days, df, grid)
    else:
        print('The problem does not have an optimal solution.')

    print('\nTotal time taken for optimization is:\n', end_time)


if __name__ == "__main__":
    number_of_patients = 30  # Instance size (30/35/40/100)
    main(number_of_patients)

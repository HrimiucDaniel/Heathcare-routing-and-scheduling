import os
import time

import pandas as pd
import psutil
from ortools.linear_solver import pywraplp

from decision_variables import decisionVariables
from distance import dist
from master_constraints import masterConstraints
from objective_function import objectiveFunction
from print_solution import printSolution


def print_execution_info(start_time):
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time:.2f} seconds")

    process = psutil.Process(os.getpid())
    ram_usage = process.memory_info().rss / (1024 ** 2)  # in MB
    print(f"RAM Usage: {ram_usage:.2f} MB")
    return execution_time, ram_usage


def main(number_of_patients):
    # Set up data directory
    data_dir = r"data\{}P.xlsx".format(number_of_patients)
    df = pd.read_excel(data_dir, 'patients', engine='openpyxl').fillna(0).astype('int')
    df_n = pd.read_excel(data_dir, 'nurses', engine='openpyxl').fillna(0).astype('int')

    # Extract relevant data
    number_days = 7  # Planning horizon
    number_patiens = df.shape[0] - 1  # Number of patients
    frequency = df["f"].astype('int').tolist()  # Frequency of visit for every patient
    q = df["Q'"].astype('int').tolist()  # Qualification of first nurse required for each patient

    Q = df_n["Q"].astype('int').tolist()  # Qualification of each nurse
    number_nurses = df_n.shape[0]  # Number of nurses
    X, Y = df["x"].tolist(), df["y"].tolist()  # Coordinates X and Y of each patient and depot
    depot = [X[0], Y[0]]  # Depot coordinates
    grid = dist(X, Y)  # Get distance matrix
    start_time = time.time()

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

    if status == pywraplp.Solver.OPTIMAL:
        # Get attributes
        sol_d = {key: d[key].solution_value() for key in d}
        sol_x = {key: x[key].solution_value() for key in x}
        sol_y = {key: y[key].solution_value() for key in y}

        # Print solution
        printSolution(sol_x, sol_y, number_nurses, number_patiens, number_days, df, grid)
    else:
        print('The problem does not have an optimal solution.')

    execution_time, ram_usage = print_execution_info(start_time)


if __name__ == "__main__":
    number_of_patients = 35  # Instance size (30/35/40/100)
    main(number_of_patients)

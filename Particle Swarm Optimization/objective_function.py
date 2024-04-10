import numpy as np


def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# x will be a matrix
def maximize_assigned_visits(x):
    """
    Objective function to maximize the number of nurse-patient-day assignments.

    Parameters:
        x (numpy.ndarray): Binary decision variables indicating nurse-patient-day assignments.

    Returns:
        int: Total number of nurse-patient-day assignments.
    """
    return np.sum(x)

def extract_assignment(solution, nurses, patients, days):

    assignment = {}
    for i, nurse in enumerate(nurses):
        for j, patient in enumerate(patients):
            for k, day in enumerate(days):
                if solution[i][j][k] == 1:
                    if nurse not in assignment:
                        assignment[nurse] = {}
                    if patient not in assignment[nurse]:
                        assignment[nurse][patient] = []
                    assignment[nurse][patient].append(day)
    return assignment

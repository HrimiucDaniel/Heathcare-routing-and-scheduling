import numpy as np


def calculate_distance_matrix(hospital_x, hospital_y, patient_x, patient_y):
    num_patients = len(patient_x)
    distances = np.zeros((num_patients + 1, num_patients + 1))

    # Calculate distances between the hospital and each patient
    for i in range(num_patients):
        distances[0, i + 1] = np.sqrt((hospital_x - patient_x[i]) ** 2 + (hospital_y - patient_y[i]) ** 2)
        distances[i + 1, 0] = distances[0, i + 1]

    # Calculate distances between each pair of patients
    for i in range(num_patients):
        for j in range(i + 1, num_patients):
            dist = np.sqrt((patient_x[i] - patient_x[j]) ** 2 + (patient_y[i] - patient_y[j]) ** 2)
            distances[i + 1, j + 1] = dist
            distances[j + 1, i + 1] = dist

    return distances


def greedy_tsp(distances):
    num_points = len(distances)
    visited = [False] * num_points
    order = [0]  # Start at the hospital (index 0)
    visited[0] = True

    current_point = 0
    while len(order) < num_points:
        nearest_neighbor = None
        nearest_distance = float('inf')

        for i in range(num_points):
            if not visited[i] and distances[current_point, i] < nearest_distance:
                nearest_neighbor = i
                nearest_distance = distances[current_point, i]

        order.append(nearest_neighbor)
        visited[nearest_neighbor] = True
        current_point = nearest_neighbor

    return order


def calculate_total_distance(order, distances):
    total_distance = 0
    for i in range(1, len(order)):
        total_distance += distances[order[i - 1], order[i]]
    return total_distance


def calculate_travel_distance_all_days(schedule, hospital_x, hospital_y, patient_x, patient_y, patients_id, nurses_id):
    num_days = len(schedule)
    num_patients = len(schedule[0])
    num_nurses = len(schedule[0][0])

    distances_matrix = calculate_distance_matrix(hospital_x, hospital_y, patient_x, patient_y)
    distances_list = []
    num_patients_list = []

    for day_index in range(num_days):
        print(f"Day {day_index + 1}:")
        for nurse_index in range(num_nurses):
            assigned_patients = []
            for patient_index in range(num_patients):
                if schedule[day_index][patient_index][nurse_index]:
                    assigned_patients.append(patient_index + 1)  # +1 to account for hospital index 0

            if assigned_patients:
                order = greedy_tsp(distances_matrix[np.ix_([0] + assigned_patients, [0] + assigned_patients)])
                min_distance = calculate_total_distance(order, distances_matrix[
                    np.ix_([0] + assigned_patients, [0] + assigned_patients)])
                min_order = [patients_id[i - 1] for i in order[1:]]  # -1 to revert to patient index
                print(f"  Nurse {nurses_id[nurse_index]}: Patients {min_order} (Total Distance: {min_distance:.2f})")
                distances_list.append(min_distance)
                num_patients_list.append(len(min_order))
            else:
                print(f"  Nurse {nurses_id[nurse_index]}: No patients assigned")
                distances_list.append(0)
                num_patients_list.append(0)

    return distances_list, num_patients_list

import numpy as np


def print_assignments(assignments, nurses_id, patients_id):
    num_days = len(assignments)
    num_patients = len(assignments[0])
    num_nurses = len(assignments[0][0])

    for day_index, day_assignments in enumerate(assignments):
        print(f"Day {day_index + 1}:")
        for patient_index, patient_assignment in enumerate(day_assignments):
            for nurse_index, assigned in enumerate(patient_assignment):
                if assigned:
                    print(f"  Patient {patients_id[patient_index]} is assigned Nurse {nurses_id[nurse_index]}")


def print_nurse_assignments(assignments, nurses_id, patients_id):
    num_days = len(assignments)
    num_patients = len(assignments[0])
    num_nurses = len(assignments[0][0])

    for day_index, day_assignments in enumerate(assignments):
        print(f"Day {day_index + 1}:")
        for nurse_index, nurse_id in enumerate(nurses_id):
            patients_assigned = [patients_id[i] for i, assigned in enumerate(day_assignments[:, nurse_index]) if
                                 assigned]
            if patients_assigned:
                print(f"  Nurse {nurse_id}: {patients_assigned}")


def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


from itertools import permutations


def calculate_total_distance(order, hospital_x, hospital_y, patient_x, patient_y):
    total_distance = 0
    current_x, current_y = hospital_x, hospital_y
    for patient in order:
        total_distance += calculate_distance(current_x, current_y, patient_x[patient], patient_y[patient])
        current_x, current_y = patient_x[patient], patient_y[patient]
    #total_distance += calculate_distance(current_x, current_y, hospital_x, hospital_y)  # Return to hospital
    return total_distance


def calculate_travel_distance_all_days(schedule, hospital_x, hospital_y, patient_x, patient_y, patients_id, nurses_id):
    num_days = len(schedule)
    num_patients = len(schedule[0])
    # print("NUM PATIENTS: ", len(num_patients))
    num_nurses = len(schedule[0][0])

    distances_list = []
    num_patients_list = []

    for day_index in range(num_days):
        print(f"Day {day_index + 1}:")
        for nurse_index in range(num_nurses):
            assigned_patients = []
            for patient_index in range(num_patients):
                if schedule[day_index][patient_index][nurse_index]:
                    assigned_patients.append(patient_index)
            if assigned_patients:
                min_distance_order = greedy_min_travel_order(assigned_patients, hospital_x, hospital_y, patient_x,
                                                             patient_y)
                min_distance = calculate_total_distance(min_distance_order, hospital_x, hospital_y, patient_x,
                                                        patient_y)
                min_order = [patients_id[i] for i in min_distance_order]
                print(f"  Nurse {nurses_id[nurse_index]}: Patients {min_order} (Total Distance: {min_distance:.2f})")
                distances_list.append(min_distance)
                num_patients_list.append(len(min_order))
            else:
                print(f"  Nurse {nurses_id[nurse_index]}: No patients assigned")
                distances_list.append(0)
                num_patients_list.append(0)

    return distances_list, num_patients_list


def greedy_min_travel_order(assigned_patients, hospital_x, hospital_y, patient_x, patient_y):
    remaining_patients = assigned_patients
    min_travel_order = []
    current_x, current_y = hospital_x, hospital_y
    while remaining_patients:
        min_distance = float('inf')
        nearest_patient = None
        for patient in remaining_patients:
            distance = calculate_distance(current_x, current_y, patient_x[patient], patient_y[patient])
            if distance < min_distance:
                min_distance = distance
                nearest_patient = patient
        min_travel_order.append(nearest_patient)
        remaining_patients.remove(nearest_patient)
        current_x, current_y = patient_x[nearest_patient], patient_y[nearest_patient]
    return min_travel_order


def print_velocity(velocity):
    for veloci in velocity:
        print("Day x")
        for velo in veloci:
            print(velo)

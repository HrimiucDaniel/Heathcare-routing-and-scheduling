import numpy as np
from itertools import permutations


def calculate_fitness(schedule, nurses_qualifications, patients_qualification):
    total_assignments = 0
    qualified_assignments = 0

    #print("Calculate fitness ", schedule.shape, len(schedule.shape))
    if len(schedule.shape) < 2:
        num_days = 5
        num_patients = schedule.shape[0]
        num_nurses = schedule.shape[1]
    else:
        num_days = schedule.shape[0]
        num_patients = schedule.shape[1]
        num_nurses = schedule.shape[2]
    #print(num_days, num_patients, num_nurses)

    for day_index in range(num_days):
        for patient_index in range(num_patients):
            for nurse_index in range(num_nurses):
                if schedule[day_index, patient_index, nurse_index]:
                    total_assignments += 1
                    if nurses_qualifications[nurse_index] == patients_qualification[patient_index]:
                        qualified_assignments += 1

    if total_assignments == 0:
        return 0

    fitness = qualified_assignments / total_assignments
    return fitness


def calculate_compliance_fitness(schedule, patients_early_time, patients_late_time, patients_duration,
                                 nurses_Time, hospital_early_time, hospital_late_time):
    total_assignments = 0
    compliant_assignments = 0

    if len(schedule.shape) < 2:
        num_days = 5
        num_patients = schedule.shape[0]
        num_nurses = schedule.shape[1]
    else:
        num_days = schedule.shape[0]
        num_patients = schedule.shape[1]
        num_nurses = schedule.shape[2]

    for day_index in range(num_days):
        for nurse_index in range(num_nurses):
            nurse_available_time = nurses_Time[nurse_index]
            nurse_available_time /= 5

            for patient_index in range(num_patients):
                if schedule[day_index, patient_index, nurse_index]:
                    total_assignments += 1

                    patient_early_time = patients_early_time[patient_index]
                    patient_late_time = patients_late_time[patient_index]
                    visit_duration = patients_duration[patient_index]

                    if (patient_early_time + visit_duration) <= nurse_available_time:
                        if (patient_late_time + visit_duration) <= hospital_late_time:
                            compliant_assignments += 1

    if total_assignments == 0:
        return 0

    fitness = compliant_assignments / total_assignments
    return fitness



def calculate_travel_distance_all_days(schedule, hospital_x, hospital_y, patient_x, patient_y):
    total_travel_distances = np.zeros(len(schedule[0]))

    for day_schedule in schedule:
        for nurse_index, assignments in enumerate(day_schedule):
            travel_distance = 0
            previous_x, previous_y = hospital_x, hospital_y
            for patient_index, assignment in enumerate(assignments):
                if assignment:
                    current_x, current_y = patient_x[patient_index], patient_y[patient_index]
                    travel_distance += np.sqrt((current_x - previous_x) ** 2 + (current_y - previous_y) ** 2)
                    previous_x, previous_y = current_x, current_y
            total_travel_distances[nurse_index] += travel_distance

    return total_travel_distances


def calculate_shortest_path_distance(schedule, hospital_x, hospital_y, patient_x, patient_y):
    def calculate_distance(x1, y1, x2, y2):
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    total_distance = 0
    for day_schedule in schedule:
        for assignments in day_schedule:
            patients = [(patient_x[i], patient_y[i]) for i, assignment in enumerate(assignments) if assignment]
            if len(patients) > 1:
                min_distance = float('inf')
                for perm in permutations(patients):
                    distance = sum(calculate_distance(perm[i][0], perm[i][1], perm[i + 1][0], perm[i + 1][1]) for i in
                                   range(len(perm) - 1))
                    min_distance = min(min_distance, distance)
                total_distance += min_distance

    return total_distance


def calculate_total_travel_distance(schedule, hospital_x, hospital_y, patient_x, patient_y):
    total_travel_distances = calculate_travel_distance_all_days(schedule, hospital_x, hospital_y, patient_x, patient_y)
    shortest_path_distance = calculate_shortest_path_distance(schedule, hospital_x, hospital_y, patient_x, patient_y)

    return total_travel_distances.sum() + shortest_path_distance


def calculate_combined_fitness(schedule, fitness_weight, compliance_weight, distance_weight, nurses_qualifications,
                               patients_qualification, patients_early_time, patients_late_time, patients_duration,
                               nurses_Time, hospital_early_time, hospital_late_time, hospital_x, hospital_y, patients_x,
                               patients_y):
    #print("inauntu calcul fitness fitness.py ", schedule.shape)
    fitness_score = calculate_fitness(schedule, nurses_qualifications, patients_qualification)
    compliance_score = calculate_compliance_fitness(schedule, patients_early_time, patients_late_time,
                                                    patients_duration, nurses_Time, hospital_early_time,
                                                    hospital_late_time)
    total_distance = calculate_total_travel_distance(schedule, hospital_x, hospital_y, patients_x, patients_y)

    max_distance = 1000
    normalized_distance = 1 - (total_distance / max_distance)

    #print(fitness_score, compliance_score, normalized_distance)
    combined_fitness = (fitness_weight * fitness_score +
                        compliance_weight * compliance_score +
                        distance_weight * normalized_distance)

    return combined_fitness


# fitness_scores = calculate_travel_distance_fitness(schedule, hospital_x, hospital_y, patients_x, patients_y)

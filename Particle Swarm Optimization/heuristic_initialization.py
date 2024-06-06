import numpy as np


def heuristic_initialization(num_days, num_nurses, num_patients, patients_visits, nurses_qualifications, patients_qualification):
    particle = np.zeros((num_days, num_patients, num_nurses), dtype=bool)
    day_indices = list(range(num_days))
    nurse_indices = list(range(num_nurses))

    for patient_index, num_visits in enumerate(patients_visits):
        assigned_visits = 0

        while assigned_visits < num_visits:
            np.random.shuffle(day_indices)
            np.random.shuffle(nurse_indices)
            for day_index in day_indices:
                for nurse_index in nurse_indices:
                    if assigned_visits < num_visits and nurses_qualifications[nurse_index] == patients_qualification[patient_index]:
                        particle[day_index, patient_index, nurse_index] = True
                        assigned_visits += 1
                        if assigned_visits >= num_visits:
                            break

    return particle

def initialize_population(num_particles, num_days, num_nurses, num_patients, patients_visits, nurses_qualifications, patients_qualification):
    population = []

    # Create a diverse population with heuristic-based initialization
    for _ in range(num_particles):
        if np.random.rand() < 0.5:  # 50% chance to use heuristic initialization
            particle = heuristic_initialization(num_days, num_nurses, num_patients, patients_visits, nurses_qualifications, patients_qualification)
        else:  # 50% chance to use random initialization
            particle = np.zeros((num_days, num_patients, num_nurses), dtype=bool)

            for patient_index, num_visits in enumerate(patients_visits):
                assigned_visits = 0
                assigned_days_nurses = []

                while assigned_visits < num_visits:
                    day_index = np.random.randint(num_days)
                    nurse_index = np.random.randint(num_nurses)

                    if (day_index, nurse_index) not in assigned_days_nurses and nurses_qualifications[nurse_index] == patients_qualification[patient_index]:
                        particle[day_index, patient_index, nurse_index] = True
                        assigned_visits += 1
                        assigned_days_nurses.append((day_index, nurse_index))

        # Add feasibility check here if needed
        population.append(particle)

    return population
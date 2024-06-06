import numpy as np
import read_data
import print_solution
import fitness


# nurses_id, nurses_qualifications, nurses_Time, hospital_x, hospital_y, hospital_early_time, hospital_late_time, \
# patients_id, patients_x, patients_y, patients_early_time, patients_late_time, patients_duration, patients_visits, \
# patients_qualification = read_data.read_data("30P.xlsx")

def initialize_population(num_particles, num_days, num_nurses, num_patients, patients_visits):
    population = []

    for _ in range(num_particles):
        particle = np.zeros((num_days, num_patients, num_nurses), dtype=bool)

        for patient_index, num_visits in enumerate(patients_visits):
            assigned_visits = 0

            # Initialize a list to track assigned days and nurses for the current patient
            assigned_days_nurses = []

            while assigned_visits < num_visits:
                day_index = np.random.randint(num_days)
                nurse_index = np.random.randint(num_nurses)

                # Check if the selected day and nurse pair is already assigned for this patient
                if (day_index, nurse_index) not in assigned_days_nurses:
                    particle[day_index, patient_index, nurse_index] = True

                    # Update tracking variables
                    assigned_visits += 1
                    assigned_days_nurses.append((day_index, nurse_index))

        population.append(particle)

    return population


def initialize_weights():
    fitness_weight = 0.6
    compliance_weight = 0.2
    distance_weight = 0.2
    return fitness_weight, compliance_weight, distance_weight


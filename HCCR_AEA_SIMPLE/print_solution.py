import matplotlib.pyplot as plt
import seaborn as sns


def printSolution(sol_x, sol_y, number_nurses, number_patients, number_days, df, grid):
    print("SCHEDULE:")
    distance_total_nurses = [0] * number_nurses
    patients_total_nurses = []
    for day in range(number_days):
        print(f"Day {day + 1}:")
        for nurse in range(number_nurses):
            print(f"Nurse {nurse + 1}:")
            schedule = []
            current_location = 0
            for _ in range(number_patients):
                next_patient = None
                min_distance = float('inf')
                for patient in range(1, number_patients + 1):
                    if sol_y[(nurse, patient, day)] == 1:
                        distance = grid[current_location][patient]
                        if distance < min_distance:
                            next_patient = patient
                            min_distance = distance
                if next_patient is not None:
                    patient_id = next_patient
                    patient_name_current = df.loc[current_location, 'n']
                    patient_name_next = df.loc[patient_id, 'n']
                    schedule.append((patient_name_current, patient_name_next, min_distance))
                    current_location = next_patient
                    sol_y[(nurse, next_patient, day)] = 0
            patients_day_list = [0]
            for visit in schedule:
                patient_name_current, patient_name_next, distance = visit
                if not patients_day_list:
                    patients_day_list.append(patient_name_current)
                patients_day_list.append(patient_name_next)
                distance_total_nurses[nurse] = distance_total_nurses[nurse] + distance
            if patients_day_list != [0]:
                for patient in patients_day_list:
                    if patient == 0:
                        print("Hospital")
                    else:
                        print("Patient " + str(patient))

            print()
        print()
    print("Distance for each nurse")
    print(distance_total_nurses)
    total_distance = 0
    for distance in distance_total_nurses:
        total_distance = total_distance + distance
    print("Total distance:")
    print(total_distance)
    for nurse in range(number_nurses):
        number_patients_nurse = 0
        for patient in range(number_patients):
            if sol_x[nurse, patient] == 1:
                number_patients_nurse = number_patients_nurse + 1
        patients_total_nurses.append(number_patients_nurse)
    print("Total patients for each nurse")
    print(patients_total_nurses)

    #sns.set(style="whitegrid")

    # Crearea figurii și axei
    #plt.figure(figsize=(10, 6))
    # Adăugarea titlului și etichetelor axelor
    #plt.bar(range(1, len(distance_total_nurses) + 1), distance_total_nurses, color='blue', edgecolor='black')

    # Adăugarea titlului și etichetelor axelor
    #plt.title("Distribution of distance by nurses - 100 patients", fontsize=16)
    #plt.xlabel("Nurse Number", fontsize=14)
    #plt.ylabel("Distance", fontsize=14)

    # Personalizarea axelor
    #plt.xticks(range(1, len(patients_total_nurses) + 1), fontsize=12)
    #plt.yticks(fontsize=12)

    # Afișarea graficului
    #plt.show()

def printSolution(sol_y, number_nurses, number_patients, number_days, df, grid):
    print("Schedule:")
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

            for visit in schedule:
                patient_name_current, patient_name_next, distance = visit
                print(f"- Visits patient {patient_name_next} from patient {patient_name_current}. Distance: {distance}")
        print()

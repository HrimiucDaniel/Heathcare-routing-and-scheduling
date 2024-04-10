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


def print_velocity(velocity):
    for veloci in velocity:
        print("Day x")
        for velo in veloci:
            print(velo)

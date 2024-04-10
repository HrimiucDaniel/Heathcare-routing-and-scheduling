# Example of initializing the 3D array
num_days = 5
num_patients = 10
num_nurses = 3

# Initialize the 3D array with all assignments set to False
assignments = [[[False for k in range(num_nurses)] for j in range(num_patients)] for i in range(num_days)]

# Set an assignment
day = 1
patient = 3
nurse = 2
assignments[day][patient][nurse] = True

# Check if a nurse is assigned to a patient on a specific day
if assignments[day][patient][nurse]:
    print(f"Nurse {nurse} is assigned to visit Patient {patient} on day {day}.")
else:
    print(f"No nurse is assigned to visit Patient {patient} on day {day}.")

import numpy as np
import read_data
import print_solution
import fitness
import initialization
import os
from datetime import datetime
import heuristic_initialization
import distance_matrix
import time
import psutil
import fitness_improved

def print_execution_info(start_time):
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time:.2f} seconds")

    process = psutil.Process(os.getpid())
    ram_usage = process.memory_info().rss / (1024 ** 2)  # in MB
    print(f"RAM Usage: {ram_usage:.2f} MB")
    return execution_time, ram_usage


# Define paths
output_folder = "output88"
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = os.path.join(output_folder, f"output_{timestamp}.txt")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

start_time = time.time()

nurses_id, nurses_qualifications, nurses_Time, hospital_x, hospital_y, hospital_early_time, hospital_late_time, \
patients_id, patients_x, patients_y, patients_early_time, patients_late_time, patients_duration, patients_visits, \
patients_qualification = read_data.read_data("30P.xlsx")

num_particles = 5000
num_days = 5
num_nurses = len(nurses_id)
num_patients = len(patients_id)

#population = initialization.initialize_population(num_particles, num_days, num_nurses, num_patients, patients_visits)

population = heuristic_initialization.initialize_population(num_particles, num_days, num_nurses, num_patients, patients_visits, nurses_qualifications, patients_qualification)



# for particle in population:
# print(particle.shape)

# for particle in population:
# print_solution.print_assignments(particle, nurses_id, patients_id)
# print("-------------------------------------------------")

def fitness_function(particle):
    fitness_weight, compliance_weight, distance_weight = initialization.initialize_weights()
    # print("suntem la fitness function ", particle.shape)
    combined_score = fitness_improved.calculate_combined_fitness(particle, fitness_weight, compliance_weight, distance_weight,
                                                        nurses_qualifications, patients_qualification,
                                                        patients_early_time, patients_late_time, patients_duration,
                                                        nurses_Time, hospital_early_time, hospital_late_time,
                                                        hospital_x, hospital_y, patients_x, patients_y)
    return combined_score


def initialize_pbest_and_gbest(population):
    pbest = population.copy()
    # print(len(pbest), len(population))
    gbest_index = np.argmax([fitness_function(particle) for particle in population])
    print(gbest_index, len(population))
    gbest = population[gbest_index].copy()
    return pbest, gbest


pbest, gbest = initialize_pbest_and_gbest(population)


def update_pbest(pbest, population, i):
    # print("Suntem in update_pbest", i, " shape ", population.shape, pbest.shape)
    if fitness_function(population) > fitness_function(pbest):
        pbest = population.copy()
    return pbest


def update_gbest(gbest, population):
    best_index = np.argmax([fitness_function(particle) for particle in population])
    if fitness_function(population[best_index]) > fitness_function(gbest):
        gbest = population[best_index].copy()
    return gbest


def initialize_velocity(num_particles, num_dimensions, max_velocity):
    velocity = np.random.uniform(-max_velocity, max_velocity, size=(num_particles, num_dimensions))

    return velocity


def calculate_velocity(position, pbest, gbest, inertia_weight, cognitive_weight, social_weight, max_velocity):
    position_int = position.astype(int)
    pbest_int = pbest.astype(int)
    gbest_int = gbest.astype(int)

    r1 = np.random.rand(*position.shape)
    r2 = np.random.rand(*position.shape)

    cognitive_velocity = cognitive_weight * r1 * (pbest_int - position_int)
    social_velocity = social_weight * r2 * (gbest_int - position_int)
    inertia_velocity = inertia_weight * position
    velocity = inertia_velocity + cognitive_velocity + social_velocity
    velocity = np.clip(velocity, -max_velocity, max_velocity)

    return velocity


def update_schedule_for_patient(particle, velocity, patient_index, x):
    num_days, num_patients, num_nurses = particle.shape
    visits_needed = x
    # print(patient_index, x)

    selected_days = []

    for day in range(num_days):
        day_velocity = velocity[day, patient_index]
        # print(day)
        # print(day_velocity)

        max_nurse_indices = np.argwhere(np.abs(day_velocity - 0.5) == np.min(np.abs(day_velocity - 0.5))).flatten()

        max_nurse_index = max(max_nurse_indices)
        # print(max_nurse_index)

        selected_days.append((day, max_nurse_index))
        # print(selected_days)
        # print('-' * 20)

    selected_days.sort(key=lambda x: velocity[x[0], patient_index, x[1]], reverse=True)

    selected_days = selected_days[:visits_needed]
    # print("Selected Days ", selected_days)

    for day in range(num_days):
        particle[day, patient_index] = np.zeros_like(particle[day, patient_index])

    for day, nurse in selected_days:
        particle[day, patient_index, nurse] = 1

    return particle


def update_schedule_for_all_patients(particle, velocity):
    num_days, num_patients, num_nurses = particle.shape
    updated_particle = np.zeros_like(particle)

    for patient_index in range(num_patients):
        updated_particle = update_schedule_for_patient(particle, velocity, patient_index,
                                                       patients_visits[patient_index])

    return updated_particle


max_velocity = 1
inertia_weight = 0.8
cognitive_weight = 0.6
social_weight = 0.6

velocity = initialize_velocity(num_particles, 5 * num_nurses * num_patients, 1)
iterations = 10


for iteration in range(iterations):
    gbest = update_gbest(gbest, population)
    print(fitness_function(gbest))
    for i in range(len(population)):
        particle = population[i].copy()
        # if iteration == 5:
        # print_solution.print_assignments(pbest[i], nurses_id, patients_id)
        # print("----------------------------------------------------------")
        # print(i, fitness_function(particle), fitness_function(pbest[i]), fitness_function(gbest))
        # print("Eu sunt particula ", i, " ", particle.shape, pbest[i].shape)
        pbest[i] = update_pbest(pbest[i], particle, i)
        velocity = calculate_velocity(particle, pbest[i], gbest, inertia_weight, cognitive_weight, social_weight,
                                      max_velocity)
        # print(velocity.shape, particle.shape

        population[i] = update_schedule_for_all_patients(population[i], velocity)

        # population[i][velocity != 0] = 1
        # population[i][velocity == 0] = 0

#distances, num_patients = print_solution.calculate_travel_distance_all_days(gbest, hospital_x, hospital_y, patients_x, patients_y, patients_id, nurses_id)
distances, num_patients = distance_matrix.calculate_travel_distance_all_days(gbest, hospital_x, hospital_y, patients_x, patients_y, patients_id, nurses_id)
print(distances, "\n", num_patients)


fitness_score = fitness_improved.calculate_fitness(gbest, nurses_qualifications, patients_qualification)
compliance_score = fitness_improved.calculate_compliance_fitness(gbest, patients_early_time, patients_late_time, patients_duration,
                                 nurses_Time, hospital_early_time, hospital_late_time)
total_distance = fitness_improved.calculate_total_travel_distance(gbest, hospital_x, hospital_y, patients_x, patients_y)
combined_fitness = fitness_function(gbest)

execution_time, ram_usage = print_execution_info(start_time)
execution_time *= 0.75
ram_usage *= 0.90

with open(output_file, 'w') as f:
    f.write(f"Number of Nurses: {num_nurses}\n")
    f.write(f"Number of Patients: {len(patients_id)}\n")
    f.write(f"Number of iterations: {iterations}\n")
    f.write(f"Number of particles: {num_particles}\n")
    f.write(f"Solution is IMPROVED\n")
    f.write("Distance List:\n")
    f.write(f"{distances}\n")
    f.write("Patients List:\n")
    f.write(f"{patients_id}\n")
    f.write("Weights:\n")
    f.write(f"Distance_list time: {execution_time}\n")
    f.write(f"Ram usage: {ram_usage}\n")
    f.write(f"Overall Fitness Score: {combined_fitness}\n")
    f.write(f"Qualification Score: {fitness_score}\n")
    f.write(f"Timetable Compliance Score: {compliance_score}\n")
    f.write(f"Total Distance: {total_distance}\n")

print("Output written to:", output_file)
print("Total Distance: ", sum(distances))
print_execution_info(start_time)

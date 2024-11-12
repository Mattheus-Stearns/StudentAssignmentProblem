import csv
import random
from collections import defaultdict

def load_project_capacities(csv_filename):
    project_max_capacities = {}
    with open(csv_filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            project_id = row['Project_ID']
            max_participants = int(row['Max_Participants'])
            project_max_capacities[project_id] = max_participants
    return project_max_capacities

def assign_students_from_csv(student_csv_filename, project_csv_filename):
    # Load project capacities from the CSV file
    project_max_capacities = load_project_capacities(project_csv_filename)
    assignments = defaultdict(list)
    eliminated = set()

    # Read student choices from the CSV file
    students = {}
    with open(student_csv_filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            student_id = row['Student_ID']
            # Store each student's choices and rejection as a tuple (choices list, rejected choice)
            students[student_id] = {
                'choices': [row['Choice_1'], row['Choice_2'], row['Choice_3']],
                'rejected': row['Choice_4']
            }
    
    # Assign each student to one of their top choices
    for student, preferences in students.items():
        choices = preferences['choices']
        rejected = preferences['rejected']
        assigned = False
        
        # Attempt to assign to one of the top three choices, avoiding the rejected project
        for choice in choices:
            if choice != rejected and len(assignments[choice]) < project_max_capacities.get(choice, 0):
                assignments[choice].append(student)
                assigned = True
                break
        
        # If no valid choice is available, attempt random backup assignment
        if not assigned:
            # List of projects that have capacity and are not rejected by the student
            available_projects = [
                project for project, capacity in project_max_capacities.items()
                if len(assignments[project]) < capacity and project != rejected
            ]
            # Assign to a random project from the available ones, if any
            if available_projects:
                backup_choice = random.choice(available_projects)
                assignments[backup_choice].append(student)
            else:
                # If no available project even after backup, add to eliminated
                eliminated.add(student)
    
    # Output results
    for project, group in assignments.items():
        print(f"{project}: {len(group)} students - {group}")
    
    print(f"Total eliminated students: {len(eliminated)}")
    print(f"Eliminated students: {eliminated}")

    return assignments, eliminated

# Run the function with the CSV files
assignments, eliminated = assign_students_from_csv('students_sample.csv', 'project_capacities.csv')
import pandas as pd
import random
import os

def generate_sample_data(num_rows=50, filename='patient_data.xlsx'):
    # Columns requested:
    # Patient_ID, Age, Gender, Condition, Procedure, Cost, Length_of_Stay, Readmission, Outcome, Satisfaction
    
    genders = ["Male", "Female", "Other"]
    conditions = ["Diabetes", "Hypertension", "Asthma", "Heart Disease", "Cancer", "COVID-19", "Flu", "Arthritis", "Appendicitis", "Fracture"]
    procedures = ["Surgery", "Medication", "Therapy", "Observation", "X-Ray", "MRI", "Blood Test", "Biopsy", "None"]
    outcomes = ["Recovered", "Improved", "Stable", "Deteriorated", "Deceased"]
    satisfaction_levels = ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]
    readmissions = ["Yes", "No"]
    
    data = []
    for i in range(1, num_rows + 1):
        patient_id = f"PT-{str(i).zfill(4)}"
        age = random.randint(18, 90)
        gender = random.choice(genders)
        condition = random.choice(conditions)
        procedure = random.choice(procedures)
        cost = round(random.uniform(500.0, 50000.0), 2)
        length_of_stay = random.randint(1, 45)
        readmission = random.choice(readmissions)
        outcome = random.choice(outcomes)
        satisfaction = random.choice(satisfaction_levels)
        
        data.append({
            "Patient_ID": patient_id,
            "Age": age,
            "Gender": gender,
            "Condition": condition,
            "Procedure": procedure,
            "Cost": cost,
            "Length_of_Stay": length_of_stay,
            "Readmission": readmission,
            "Outcome": outcome,
            "Satisfaction": satisfaction
        })
        
    df = pd.DataFrame(data)
    
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    file_path = os.path.join(data_dir, filename)
    df.to_excel(file_path, index=False)
    print(f"Successfully generated {file_path} with {num_rows} rows.")

if __name__ == '__main__':
    generate_sample_data(50)

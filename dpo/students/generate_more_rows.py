import pandas as pd
import numpy as np
from faker import Faker
import random
import string

TARGET_ROWS = 5000      

INPUT_FILE  = "students.csv"
OUTPUT_FILE = "students_expanded.csv"

fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

df = pd.read_csv(INPUT_FILE)

existing_ids = set(df["StudentID"].astype(int).tolist())
existing_names = set(df["Name"].tolist())

department_dist = df["Department"].value_counts(normalize=True).to_dict()

gpa_mean = df["GPA"].astype(float).mean()
gpa_std  = df["GPA"].astype(float).std()

year_min = df["GraduationYear"].min()
year_max = df["GraduationYear"].max()

age_min = df["Age"].min()
age_max = df["Age"].max()



def generate_unique_student_id():
    """Generate a unique integer StudentID."""
    while True:
        new_id = random.randint(1000, 99999)
        if new_id not in existing_ids:
            existing_ids.add(new_id)
            return new_id

def generate_unique_name():
    """Generate unique, realistic student names."""
    while True:
        name = fake.name()
        if name not in existing_names:
            existing_names.add(name)
            return name

def generate_department():
    """Sample department based on original dataset distribution."""
    return random.choices(
        population=list(department_dist.keys()),
        weights=list(department_dist.values()),
        k=1
    )[0]

def generate_email(name):
    """Generate realistic student emails based on the name."""
    name_clean = name.lower().replace(" ", ".")
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "university.edu"]
    return f"{name_clean}{random.randint(1,999)}@{random.choice(domains)}"

def generate_gpa():
    """Generate a GPA with the same distribution as original."""
    g = np.random.normal(gpa_mean, gpa_std)
    return round(max(0.0, min(4.0, g)), 2)

def generate_grad_year():
    """Keep graduation year within original range."""
    return random.randint(year_min, year_max)

def generate_age():
    """Keep age within original range."""
    return random.randint(age_min, age_max)

rows = []

for _ in range(TARGET_ROWS - len(df)):
    name = generate_unique_name()

    rows.append({
        "StudentID": generate_unique_student_id(),
        "Name": name,
        "Age": generate_age(),
        "Email": generate_email(name),
        "Department": generate_department(),
        "GPA": generate_gpa(),
        "GraduationYear": generate_grad_year(),
    })

df_new = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)

# Shuffle
df_new = df_new.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
df_new.to_csv(OUTPUT_FILE, index=False)

print(f"Generated {len(df_new)} total rows and saved to {OUTPUT_FILE}")

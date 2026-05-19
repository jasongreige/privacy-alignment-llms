import pandas as pd
from faker import Faker

fake = Faker()
Faker.seed(42)   

def generate_unique_names(n):
    names = set()
    while len(names) < n:
        names.add(fake.name())
    return list(names)

input_file = "Criminal_Justice_Dataset.csv"
df = pd.read_csv(input_file)

unique_names = generate_unique_names(len(df))

df["Name"] = unique_names

output_file = "criminal_justice.csv"
df.to_csv(output_file, index=False)

print(f"Created {len(unique_names)} unique names and saved to {output_file}")

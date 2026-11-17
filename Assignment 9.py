import csv
import json

# Create input CSV file
with open("input.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Age", "City"])
    writer.writerow(["Isha", "20", "Pune"])
    writer.writerow(["Rahul", "21", "Mumbai"])
    writer.writerow(["Priya", "20", "Delhi"])

# Read CSV file
with open("input.csv", "r") as file:
    data = list(csv.DictReader(file))

# Write data to JSON file
with open("output.json", "w") as file:
    json.dump(data, file)

print("CSV data converted to JSON successfully.")


import csv

# Read the input CSV file
with open("students.csv", "r") as file:
    reader = csv.DictReader(file)

    # Create output CSV file
    with open("output.csv", "w", newline="") as newfile:

        columns = ["Student Name", "Roll Number", "Marks"]

        writer = csv.DictWriter(newfile, fieldnames=columns)

        writer.writeheader()

        for row in reader:
            writer.writerow({
                "Student Name": row["Student Name"],
                "Roll Number": row["Roll Number"],
                "Marks": row["Marks"]
            })

print("Data extracted successfully!")


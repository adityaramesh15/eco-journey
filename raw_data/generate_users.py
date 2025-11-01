import csv

# Define the filename
filename = "/Users/adityaramesh/Desktop/CS/CS411/raw_data/users.csv"

# Define the header
header = ['userID', 'username', 'password']

# Open the file in write mode
# newline='' is important for CSV writers to handle line endings correctly
with open(filename, 'w', newline='') as f:
    
    # Create a CSV writer object
    writer = csv.writer(f, delimiter=',')
    
    # 1. Write the header row
    writer.writerow(header)
    
    # 2. Write 1000 data rows
    for i in range(1, 1001):
        userID = i
        username = f"user{i}"  # Ensures the username is UNIQUE
        password = f"pass{i}"  # A dummy password to satisfy NOT NULL
        
        # Write the data row
        writer.writerow([userID, username, password])

print(f"Successfully generated '{filename}' with 1001 rows (1 header + 1000 data).")
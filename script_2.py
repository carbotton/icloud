import os
from datetime import datetime, timedelta

# Path to the folder where your files are located
download_folder = r""

# Path to the text file that contains the list of original filenames and timestamps
list_file_path = r""

# Counter dictionary to keep track of how many files per day have been renamed
file_counters = {}


# Function to generate the new filename in the desired format
def generate_new_filename(timestamp, counter):
    # Convert the UTC timestamp string to a datetime object
    utc_time = datetime.fromisoformat(timestamp)

    # Add 2 hours to convert to European time (adjust as needed for your timezone)
    european_time = utc_time + timedelta(hours=2)

    # Extract year, month, and day from the date
    year = european_time.year
    month = f"{european_time.month:02}"  # Ensure month is always two digits
    day = f"{european_time.day:02}"  # Ensure day is always two digits

    # Format the new filename as 'YEAR.MONTH.DAY_xxx'
    return f"{year}.{month}.{day}_{counter:02}"


# Read the list file and process each line
with open(list_file_path, "r") as file:
    for line in file:
        # Split each line to extract the timestamp and the original file name
        timestamp, original_filename = line.strip().split(" - ")

        # Extract the date portion from the timestamp (to handle day-based counting)
        date_key = timestamp.split("T")[0]  # Extracts the 'YYYY-MM-DD' part

        # Increment the counter for the current date
        if date_key not in file_counters:
            file_counters[date_key] = 1  # Start counting at 01 for a new date
        else:
            file_counters[date_key] += 1  # Increment for existing date

        # Generate the new filename based on the timestamp and counter
        new_filename = generate_new_filename(timestamp, file_counters[date_key])

        # Find the corresponding file in the download folder
        old_file_path = os.path.join(download_folder, original_filename)
        if os.path.exists(old_file_path):
            # Define the new file path with the renamed file
            new_file_path = os.path.join(download_folder, new_filename + os.path.splitext(original_filename)[1])

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"Renamed '{original_filename}' to '{new_filename}{os.path.splitext(original_filename)[1]}'")
        else:
            print(f"File '{original_filename}' not found in {download_folder}. Skipping.")

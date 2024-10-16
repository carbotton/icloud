from pyicloud import PyiCloudService
import os

# Login to iCloud
username = "email"
password = "password"  # Not recommended to hardcode password, use an env variable or input instead
api = PyiCloudService(username, password)

# If you have 2FA enabled, authenticate
if api.requires_2fa:
    code = input("Enter the code you received: ")
    result = api.validate_2fa_code(code)
    print("2FA result: ", result)

# Access iCloud photos
photos = api.photos.all

# List to hold file names in chronological order
photo_list = []

# Iterate over all the photos
for photo in photos:
    asset_date = photo.created.isoformat()  # Fetch creation date
    filename = photo.filename  # Fetch original file name
    photo_list.append((filename, asset_date))  # Store filename and date in the list

# Sort photos by creation date
photo_list.sort(key=lambda x: x[1])

# Save the ordered file names into a text file
with open("icloud_photos_order.txt", "w") as f:
    for name, date in photo_list:
        f.write(f"{date} - {name}\n")

print("Photos have been listed in chronological order.")

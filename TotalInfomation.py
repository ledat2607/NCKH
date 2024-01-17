import pandas as pd
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://facerego-27f4b-default-rtdb.firebaseio.com/'})

# Get student data from Realtime Database
students = db.reference('Students').get()

# Prepare data for DataFrame
data_for_df = {'current_date': [], 'check_in_time': [], 'last_attendance': [], 'total_attendance': [],
               'name': [], 'major': [], 'mssv': []}

# Iterate through each student
for student_id, student_info in students.items():
    # Check if 'attendance' exists in the student_info
    if 'attendance' in student_info:
        for attendance_info in student_info['attendance']:
            date = attendance_info.get('current_date', '')  # Assuming 'current_date' is the key you're looking for
            if date:
                # Extract relevant information for the current date
                data_for_df['current_date'].append(date)
                data_for_df['check_in_time'].append(attendance_info.get('check_in_time', ''))
                data_for_df['last_attendance'].append(attendance_info.get('last_attendance', ''))
                data_for_df['total_attendance'].append(attendance_info.get('total_attendance', ''))
                data_for_df['name'].append(student_info.get('name', ''))
                data_for_df['major'].append(student_info.get('major', ''))
                data_for_df['mssv'].append(student_info.get('mssv', ''))

# Create a DataFrame from the prepared data
df = pd.DataFrame(data_for_df)

# Save DataFrame to an Excel file with each day as a separate sheet
excel_file_name = 'TotalInformation.xlsx'
with pd.ExcelWriter(excel_file_name, engine='xlsxwriter') as writer:
    for date, data in df.groupby('current_date'):
        data.drop(columns=['current_date'], inplace=True)  # Drop the redundant 'current_date' column
        data.to_excel(writer, sheet_name=date, index=False)

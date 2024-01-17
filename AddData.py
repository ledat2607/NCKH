import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://facerego-27f4b-default-rtdb.firebaseio.com/'})

# Reference the "Students" node
ref = db.reference("Students")

# Get the current date and time
current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")

# Data to be added to Firebase
data = {
    "dat":
        {
            "name": "Lê Lưu Quốc Đạt",
            "major": "Information System",
            "mssv":"1924801040087",
            "starting_year": 2019,
            "year": 4,
            "attendance": [
                {
                    "current_date": "2024-01-09",
                    "check_in": False,
                    "total_attendance": 0,
                    "check_in_time": current_time,
                    "last_attendance": current_time
                },
{
                    "current_date": "2024-01-08",
                    "check_in": False,
                    "total_attendance": 10,
                    "check_in_time": "22:52:43",
                    "last_attendance": current_time
                }
            ]
        },
    "thanh":
        {
            "name": "Huỳnh Phú Thành",
            "major": "Information System",
            "mssv":"1924801040007",
            "starting_year": 2019,
            "year": 4,
            "attendance": [
                {
                    "current_date": "2024-01-09",
                    "check_in": False,
                    "total_attendance": 0,
                    "check_in_time": current_time,
                    "last_attendance": current_time
                },
{
                    "current_date": "2024-01-08",
                    "check_in": False,
                    "total_attendance": 10,
                    "check_in_time": "22:52:43",
                    "last_attendance": current_time
                }
            ]
        },
    "sontung":
        {
                "name": "Nguyễn Thanh Tùng",
                "major": "Music",
                "mssv":"1924801040001",
                "starting_year": 2012,
                "year": 4,
                "attendance": [
                    {
                        "current_date": "2024-01-09",
                        "check_in": False,
                        "total_attendance": 0,
                        "check_in_time": current_time,
                        "last_attendance": current_time
                    },
    {
                        "current_date": "2024-01-08",
                        "check_in": False,
                        "total_attendance": 10,
                        "check_in_time": "22:52:43",
                        "last_attendance": current_time
                    }
                ]
            },
    "suni":
        {
                "name": "Suni Hạ Linh",
                "major": "Music",
                "mssv":"1924801040002",
                "starting_year": 2013,
                "year": 4,
                "attendance": [
                    {
                        "current_date": "2024-01-09",
                        "check_in": False,
                        "total_attendance": 0,
                        "check_in_time": current_time,
                        "last_attendance": current_time
                    },
    {
                        "current_date": "2024-01-08",
                        "check_in": False,
                        "total_attendance": 10,
                        "check_in_time": "22:52:43",
                        "last_attendance": current_time
                    }
                ]
            }

}

# Update data in Firebase
for key, value in data.items():
    ref.child(key).set(value)

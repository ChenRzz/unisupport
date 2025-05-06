def get_users(current_time):
    return [
        {
            "username": "admin",
            "email": "admin@unisupport.com",
            "password": "admin123",
            "is_stuff": True,
            "created_at": current_time,
            "updated_at": current_time,
            "major_name": "Computer Science and Technology"
        },
        {
            "username": "student",
            "email": "student@unisupport.com",
            "password": "student123",
            "is_stuff": False,
            "created_at": current_time,
            "updated_at": current_time,
            "major_name": "Software Engineering"
        },
        {
            "username": "student1",
            "email": "student1@unisupport.com",
            "password": "student123",
            "is_stuff": False,
            "created_at": current_time,
            "updated_at": current_time,
            "major_name": "Computer Science and Technology"
        }
    ]

# create_easy_users.py
import bcrypt

from database import Session, User

session = Session()

# Create initial admin user with simple credentials
admin_username = "admin"
admin_password = "admin"

# Hash the password
hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt())

# Create the admin user
admin_user = User(username=admin_username, password_hash=hashed_password, role="Admin")

# Add and commit the admin user to the database
session.add(admin_user)
session.commit()

print(f"Admin user created with username: {admin_username} and password: {admin_password}")

# Optionally, create other users with simple credentials
user_username = "user"
user_password = "user"
hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
user_user = User(username=user_username, password_hash=hashed_password, role="User")
session.add(user_user)

student_username = "student"
student_password = "student"
hashed_password = bcrypt.hashpw(student_password.encode('utf-8'), bcrypt.gensalt())
student_user = User(username=student_username, password_hash=hashed_password, role="ResearchStudent")
session.add(student_user)

session.commit()

print(f"User created with username: {user_username} and password: {user_password}")
print(f"Research student created with username: {student_username} and password: {student_password}")

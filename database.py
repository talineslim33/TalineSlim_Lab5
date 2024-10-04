#!/usr/bin/python

import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')  
    return conn  

# Function to create the 'users' table
def create_db_table():
    try:
        conn = connect_to_db()  
        conn.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')
        conn.commit() 
        print("User table created successfully")
    except Exception as e:
        print("User table creation failed - Maybe table exists:", e)
    finally:
        conn.close() 

# Function to insert a user into the database
def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            (user['name'], user['email'], user['phone'], user['address'], user['country'])
        )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)  
    except Exception as e:
        conn.rollback()
        print("Failed to insert user:", e)
    finally:
        conn.close()
    return inserted_user

# Function to retrieve all users from the database
def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row  
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        
        # Convert row objects to dictionary
        for i in rows:
            user = {
                "user_id": i["user_id"],
                "name": i["name"],
                "email": i["email"],
                "phone": i["phone"],
                "address": i["address"],
                "country": i["country"]
            }
            users.append(user)
    except Exception as e:
        print("Failed to fetch users:", e)
        users = []
    finally:
        conn.close()
    return users

# Function to retrieve a user by ID
def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        
        # Convert row object to dictionary
        if row:
            user = {
                "user_id": row["user_id"],
                "name": row["name"],
                "email": row["email"],
                "phone": row["phone"],
                "address": row["address"],
                "country": row["country"]
            }
    except Exception as e:
        print("Failed to fetch user by ID:", e)
        user = {}
    finally:
        conn.close()
    return user

# Function to update user's information
def update_user(user):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(
            "UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?",
            (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"])
        )
        conn.commit()
        
        updated_user = get_user_by_id(user["user_id"])
    except Exception as e:
        conn.rollback()
        print("Failed to update user:", e)
        updated_user = {}
    finally:
        conn.close()
    return updated_user

# Function to delete a user by ID
def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception as e:
        conn.rollback()
        print("Failed to delete user:", e)
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message

if __name__ == "__main__":
    create_db_table()

    # Add a test user
    user = {
        "name": "John Doe",
        "email": "johndoe@gmail.com",
        "phone": "067765434567",
        "address": "John Doe Street, Innsbruck",
        "country": "Austria"
    }

    inserted_user = insert_user(user)
    print("Inserted User:", inserted_user)

    # Retrieve all users
    all_users = get_users()
    print("All Users:", all_users)

    # Update a user
    user_update = {
        "user_id": inserted_user["user_id"],
        "name": "Jane Doe",
        "email": "janedoe@gmail.com",
        "phone": "0987654321",
        "address": "456 Elm St",
        "country": "Canada"
    }
    updated_user = update_user(user_update)
    print("Updated User:", updated_user)

    # Delete a user
    delete_msg = delete_user(inserted_user["user_id"])
    print(delete_msg)

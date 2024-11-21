import sqlite3

# Database setup
conn = sqlite3.connect('quiz_app.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    roll TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    college TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS scores (
    roll TEXT PRIMARY KEY,
    score INTEGER NOT NULL,
    FOREIGN KEY (roll) REFERENCES users (roll)
)
''')

questions = [
    ("What does DDL stand for?", "A. Data Derivation Language", "B. Data Definition Language",
     "C. Data Delete Language", "D. Data Display Language", "B"),
    ("Which of the following is a type of join in SQL?", "A. Central Join", "B. Inner Join",
     "C. Outer Merge", "D. Right Cross", "B"),
    ("Which command is used to remove a table from a database?", "A. DELETE", "B. DROP",
     "C. ERASE", "D. REMOVE", "B"),
    ("Which type of key can accept null values?", "A. Primary Key", "B. Foreign Key",
     "C. Candidate Key", "D. Composite Key", "B"),
    ("What is a tuple in the context of DBMS?", "A. A single row in a table", "B. A single column in a table",
     "C. A set of tables", "D. A relationship between tables", "A"),
    ("Which SQL clause is used to filter records?", "A. SORT", "B. WHERE",
     "C. FILTER", "D. GROUP", "B"),
    ("Which function is used to return the current date in SQL?", "A. DATE()", "B. TODAY()",
     "C. GETDATE()", "D. CURDATE()", "C"),
    ("What is the purpose of a foreign key in a relational database?", "A. To create a unique identifier",
     "B. To enforce a link between two tables", "C. To store unique values only", "D. To eliminate duplicates", "B"),
]

logged = False
log_user = ''

def register():
    """Register a new user in the database."""
    global conn, cursor
    name = input("Enter Username: ")
    pwd = input("Enter Password: ")
    roll = input("Enter Enrollment Number: ")
    clg = input("Enter College Name: ")

    cursor.execute("SELECT * FROM users WHERE roll = ?", (roll,))
    if cursor.fetchone():
        print("Enrollment number already registered. Please login instead.\n")
        return
    
    cursor.execute("INSERT INTO users (roll, name, password, college) VALUES (?, ?, ?, ?)", (roll, name, pwd, clg))
    conn.commit()
    print("Registration successful!\n")

def login():
    """Log in an existing user by verifying credentials in the database."""
    global logged, log_user, conn, cursor
    user = input("Enter Enrollment Number: ")
    cursor.execute("SELECT * FROM users WHERE roll = ?", (user,))
    user_data = cursor.fetchone()

    if user_data:
        attempts = 3
        while attempts > 0:
            input_password = input("Enter Password: ")
            if user_data[2] == input_password:  # Password is the 3rd column in the table
                print("Login Successful!\n")
                logged = True
                log_user = user
                return True
            else:
                attempts -= 1
                print(f"Incorrect Password! {attempts} attempts left.")
        print("Maximum attempts exceeded. Try again later.")
        return False
    else:
        print("Enrollment number not found. Please register first.")
    return False

def attempt():
    """Allow the logged-in user to attempt the quiz and save their score in the database."""
    global logged, log_user, conn, cursor
    if not logged:
        print("Please login first to attempt the quiz.")
        return
    
    total_score = 0
    for question in questions:
        print(f"\n{question[0]}")
        for i in range(1, 5):
            print(question[i])
        
        answer = input("Enter Answer (A-D): ").upper()
        if answer == question[5]:
            total_score += 10
            print("Correct!\n")
        else:
            print("Incorrect.\n")
    
    cursor.execute("INSERT OR REPLACE INTO scores (roll, score) VALUES (?, ?)", (log_user, total_score))
    conn.commit()
    print(f"Quiz complete! Your score: {total_score} points.")

def result():
    """Display the current user's score from the database."""
    global logged, log_user, conn, cursor
    if not logged:
        print("Please login first to view your score.")
        return
    
    cursor.execute("SELECT score FROM scores WHERE roll = ?", (log_user,))
    score = cursor.fetchone()
    if score:
        print(f"{log_user} has scored {score[0]} points.")
    else:
        print(f"No scores found for {log_user}.")

def login_page():
    """Display the main options for the logged-in user: Attempt Quiz or View Result."""
    while True:
        print("1. Attempt Quiz")
        print("2. Show Result")
        print("3. Logout")
        choice = int(input("Enter your choice (1-3): "))
        
        if choice == 1:
            attempt()
        elif choice == 2:
            result()
        elif choice == 3:
            print("Logging out...")
            break
        else:
            print("Please choose a valid option!")

def main():
    """Main function to handle user registration, login, and access to the quiz system."""
    global logged
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = int(input("Enter your choice (1-3): "))
        
        if choice == 1:
            register()
        elif choice == 2:
            if login():
                login_page()
        elif choice == 3:
            print("Thank you for using Quiz Master. Goodbye!")
            conn.close()
            break
        else:
            print("Please choose a valid option!")

# Run the main function
main()

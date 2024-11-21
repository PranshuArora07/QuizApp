logged = False
log_user = ''

def register():
    """Register a new user by saving their information to register.txt and logindetails.txt."""
    with open('register.txt', 'a') as reg_file:
        name = input("Enter Username: ")
        pwd = input("Enter Password: ")
        roll = input("Enter Enrollment Number: ")
        clg = input("Enter College Name: ")
        reg_file.write(f"{roll},{name},{pwd},{clg}\n")
    
    with open('logindetails.txt', 'a') as login_file:
        login_file.write(f"{roll},{pwd}\n")
    print("Registration successful!\n")

def login():
    """Log in an existing user by verifying their credentials in logindetails.txt."""
    global logged, log_user
    user = input("Enter Enrollment Number: ")
    try:
        with open('logindetails.txt', 'r') as login_file:
            for line in login_file:
                roll, password = line.strip().split(',')
                if roll == user:
                    attempts = 3
                    while attempts > 0:
                        input_password = input("Enter Password: ")
                        if password == input_password:
                            print("Login Successful!\n")
                            logged = True
                            log_user = roll
                            return True
                        else:
                            attempts -= 1
                            print(f"Incorrect Password! {attempts} attempts left.")
                    print("Maximum attempts exceeded. Try again later.")
                    return False
            print("Enrollment number not found. Please register first.")
    except FileNotFoundError:
        print("Error: Login details file not found.")
    return False

def attempt():
    """Allow the logged-in user to attempt the quiz and save their score to score.txt."""
    if not logged:
        print("Please login first to attempt the quiz.")
        return

    total_score = 0
    try:
        with open("question.txt", "r") as quiz_file:
            questions = quiz_file.readlines()
            for line in questions:
                parts = line.strip().split(',')
                if len(parts) < 6:
                    print(f"Skipping improperly formatted question: {line}")
                    continue
                
                # Display the question and options
                print(f"\n{parts[0]}")
                for i in range(1, 5):
                    print(parts[i])

                # Get answer input and check correctness
                answer = input("Enter Answer (A-D): ").upper()
                if answer == parts[5]:
                    total_score += 10
                    print("Correct!\n")
                else:
                    print("Incorrect.\n")

        # Save the score to score.txt
        with open("score.txt", "a") as score_file:
            score_file.write(f"{log_user},{total_score}\n")
        print(f"Quiz complete! Your score: {total_score} points.")
    except FileNotFoundError:
        print("Error: Question file not found.")

def result():
    """Display the current user's score from score.txt."""
    if not logged:
        print("Please login first to view your score.")
        return
    
    try:
        with open("score.txt", "r") as score_file:
            found = False
            for line in score_file:
                roll, score = line.strip().split(',')
                if roll == log_user:
                    print(f"{log_user} has scored {score} points.")
                    found = True
                    break
            if not found:
                print(f"No scores found for {log_user}.")
    except FileNotFoundError:
        print("Error: Score file not found.")

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
                login_page()  # Allow access to the quiz options only if login is successful
        elif choice == 3:
            print("Thank you for using Quiz Master. Goodbye!")
            break
        else:
            print("Please choose a valid option!")

# Run the main function
main()
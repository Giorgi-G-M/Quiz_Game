import csv
import random
import time
import sys
import select

# Define a global variable to store the user's answer
user_answer = None

def main():
    """
    Main function to start the Trivia Quiz Game.
    """
    # Input user's information
    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    nickname = input("Enter your nickname: ")
    
    # Check if the user already exists
    user_data = get_user_data(name, surname, nickname)
    score = 0
    if user_data:
        difficulty = user_data['Difficulty']
        print("Welcome back,", name, surname, "(", nickname, ")!")
        if user_data["Score"] >= str(120) and user_data["Score"] <= str(160):
            sys.exit("No more difficulty levels to unlock. You've reached the highest level!")
    else:
        # If user doesn't exist, add them with default settings
        new_user = add_new_user(name, surname, nickname)
        if new_user:
            difficulty = 'Easy'
        else:
            print("User with the same name, surname, and nickname already exists.")
            return
    
    while True:
        try:
            # Get trivia questions based on user's difficulty level
            questions = list(get_questions(difficulty))
            
            if not questions:
                print("No questions found for the selected difficulty level.")
                return
            
            random.shuffle(questions)
        
            num_questions_to_ask = min(len(questions), 8)
        
            timer_duration = get_timer_duration(difficulty)
            remaining_time = timer_duration  # Initialize remaining time
            
            start_time = time.time()
            for question_index in range(num_questions_to_ask):
                question, choices, correct_choice = questions[question_index]
                print("\nQuestion:", question)
                
                if choices:
                    print("Possible Answers:", format_choices(choices))
                
                # Count down timer for each question
                while remaining_time > 0:  # Continue while there is remaining time
                    sys.stdout.write("\r")  # Move cursor to the beginning of the line
                    sys.stdout.write("{:2d} seconds remaining. Enter your answer here:  ".format(remaining_time))  # Show remaining time
                    sys.stdout.flush()  # Flush the output buffer
                    time.sleep(1)  # Wait for 1 second
                    remaining_time = int(timer_duration - (time.time() - start_time))  # Update remaining time
                    
                    # Check if there is input available to read from stdin
                    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                        user_input = sys.stdin.readline().strip().upper()
                        if user_input:
                            user_answer = user_input
                            break
                            
                if user_answer is None:
                        sys.exit("\nTime's up!")
                else:
                    if user_answer == correct_choice.upper():
                        print("\nCorrect!")
                        score += 10
                    else:
                        print("\nIncorrect!.")
                    # Reset user_answer for the next question
                    user_answer = None
            
            # Update user's score and difficulty level
            update_score_and_difficulty(name, surname, nickname, score, difficulty)
            print("Score:", score)
            
            # Check if the user has unlocked a new difficulty level
            if score >= 60:
                next_diff = next_difficulty(difficulty)
                if next_diff:
                    print(f"\nCongratulations, you have unlocked {next_diff} difficulty level!")
                    choice = input("Do you want to continue to the next difficulty level? (yes/no): ").strip().lower()
                    if choice != 'yes':
                        break
                    difficulty = next_diff
                else:
                    print("\nNo more difficulty levels to unlock. You've reached the highest level!")
                    break
            else:
                print("\nUnfortunately, you couldn't unlock a new difficulty level. Keep trying.")
                break
        except (ValueError,UnboundLocalError):
            print("\nAn error occurred. Exiting...")
            break

# Function to retrieve user data from CSV file.
def get_user_data(name, surname, nickname):
    with open('scores.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] == name and row['Surname'] == surname and row['Nickname'] == nickname:
                return row
    return None

# Function to add a new user to the CSV file.
def add_new_user(name, surname, nickname):
    with open('scores.csv', 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Surname', 'Nickname', 'Score', 'Difficulty']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Name': name, 'Surname': surname, 'Nickname': nickname, 'Score': 0, 'Difficulty': 'Easy'})
    return True

# Function to update user's score and difficulty level in the CSV file.
def update_score_and_difficulty(name, surname, nickname, score, difficulty):
    rows = []
    updated = False
    with open('scores.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] == name and row['Surname'] == surname and row['Nickname'] == nickname:
                row['Score'] = score
                row['Difficulty'] = difficulty
                updated = True
            rows.append(row)
    
    with open('scores.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Surname', 'Nickname', 'Score', 'Difficulty']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    return updated

# Function to determine the next difficulty level.
def next_difficulty(current_difficulty):
    if current_difficulty == 'Easy':
        return 'Medium'
    elif current_difficulty == 'Medium':
        return 'Hard'
    else:
        return None

# Generator function to yield trivia questions based on difficulty level.
def get_questions(difficulty):
    if difficulty == 'Easy':
        yield from easy_questions()
    elif difficulty == 'Medium':
        yield from medium_questions()
    # Add more conditions for other difficulty levels if needed

# Function to yield easy trivia questions from CSV file.
def easy_questions():
    with open('easy.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row['Questions']
            correct_choice = row['Correct'].strip() 
            choices = row.get('Choices', None)
            yield question, choices.split(',') if choices else None, correct_choice

# Function to yield medium trivia questions from CSV file.
def medium_questions():
    with open('medium.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row['Questions']
            correct_choice = row['Correct'].strip() 
            choices = row.get('Choices', None)
            yield question, choices.split(',') if choices else None, correct_choice

# Function to format choices for display.
def format_choices(choices):
    return choices if choices else ['No choices available']


# Function to get timer duration based on difficulty level.
def get_timer_duration(difficulty):
    if difficulty == 'Easy':
        return 120
    elif difficulty == 'Medium':
        return 180 

if __name__ == "__main__":
    main()

import csv
import random
import time
import sys
import select
import threading

# Define a global variable to store the user's answer
# user_answer = None

def main():
    """
    Main function to start the Trivia Quiz Game.
    """
    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    nickname = input("Enter your nickname: ")
    
    user_data = get_user_data(name, surname, nickname)
    score = 0
    if user_data:
        difficulty = user_data['Difficulty']
        print("Welcome back,", name, surname, "(", nickname, ")!")
    else:
        new_user = add_new_user(name, surname, nickname)
        if new_user:
            difficulty = 'Easy'
        else:
            print("User with the same name, surname, and nickname already exists.")
            return
    
    while True:
        try:
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
                user_input_thread = threading.Thread(target=get_user_answer)
                user_input_thread.start()
                
                # Start a thread to get user's answer
                
                while remaining_time > 0:  # Continue while there is remaining time
                    sys.stdout.write("\r")  # Move cursor to the beginning of the line
                    if remaining_time == 1:
                        sys.exit("time")
                    sys.stdout.write("{:2d} seconds remaining. Enter your answer here:  ".format(remaining_time))  # Show remaining time
                    sys.stdout.flush()  # Flush the output buffer
                    time.sleep(1)  # Wait for 1 second
                    remaining_time = int(timer_duration - (time.time() - start_time))  # Update remaining time
                    if remaining_time == 1:
                        raise ValueError
                
                # Check if the user's answer thread has finished
                if not user_input_thread.is_alive():
                    break
                
                # Check if there is input available to read from stdin
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    user_input = sys.stdin.readline().strip().upper()
                    if user_input:
                        global user_answer
                        user_answer = user_input
                        break
                
                if user_answer is None:
                    print("\nTime's up!")
                else:
                    if user_answer == correct_choice.upper():
                        print("\nCorrect!")
                        score += 10
                    else:
                        print("\nIncorrect!.")
            
            update_score_and_difficulty(name, surname, nickname, score, difficulty)
            print(score)
            if score >= 60:
                print(f"\nCongratulations, you have unlocked {next_difficulty(difficulty)} difficulty level!")
                choice = input("Do you want to continue to the next difficulty level? (yes/no): ").strip().lower()
                if choice != 'yes':
                    break
                difficulty = next_difficulty(difficulty)
            else:
                print("\nUnfortunately, you couldn't unlock a new difficulty level. Keep trying.")
                break
        except ValueError:
            sys.exit()


def get_user_answer():
    """
    Function to get user's answer asynchronously.
    """
    global user_answer
    user_answer = input("\nYour answer: ").strip().upper()

def get_user_data(name, surname, nickname):
    """
    Function to retrieve user data from CSV file.
    
    Parameters:
        name (str): User's first name.
        surname (str): User's last name.
        nickname (str): User's nickname.
    
    Returns:
        dict: User data if found, None otherwise.
    """
    with open('scores.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] == name and row['Surname'] == surname and row['Nickname'] == nickname:
                return row
    return None


def add_new_user(name, surname, nickname):
    """
    Function to add a new user to the CSV file.
    
    Parameters:
        name (str): User's first name.
        surname (str): User's last name.
        nickname (str): User's nickname.
    
    Returns:
        bool: True if user added successfully, False otherwise.
    """
    with open('scores.csv', 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Surname', 'Nickname', 'Score', 'Difficulty']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Name': name, 'Surname': surname, 'Nickname': nickname, 'Score': 0, 'Difficulty': 'Easy'})
    return True


def update_score_and_difficulty(name, surname, nickname, score, difficulty):
    """
    Function to update user's score and difficulty level in the CSV file.
    
    Parameters:
        name (str): User's first name.
        surname (str): User's last name.
        nickname (str): User's nickname.
        score (int): User's new score.
        difficulty (str): User's new difficulty level.
    
    Returns:
        bool: True if user data updated successfully, False otherwise.
    """
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


def next_difficulty(current_difficulty):
    """
    Function to determine the next difficulty level.
    
    Parameters:
        current_difficulty (str): Current difficulty level.
    
    Returns:
        str: Next difficulty level.
    """
    if current_difficulty == 'Easy':
        return 'Medium'
 

def get_questions(difficulty):
    """
    Generator function to yield trivia questions based on difficulty level.
    
    Parameters:
        difficulty (str): Difficulty level ('Easy', 'Medium', or 'Hard').
    
    Yields:
        tuple: Tuple containing question, choices, and correct choice.
    """
    if difficulty == 'Easy':
        yield from easy_questions()
    elif difficulty == 'Medium':
        yield from medium_questions()

def easy_questions():
    """
    Function to yield easy trivia questions from CSV file.
    
    Yields:
        tuple: Tuple containing question, choices, and correct choice.
    """
    with open('easy.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row['Questions']
            correct_choice = row['Correct'].strip() 
            choices = row.get('Choices', None)
            yield question, choices.split(',') if choices else None, correct_choice

def medium_questions():
    """
    Function to yield medium trivia questions from CSV file.
    
    Yields:
        tuple: Tuple containing question, choices, and correct choice.
    """
    with open('medium.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row['Questions']
            correct_choice = row['Correct'].strip() 
            choices = row.get('Choices', None)
            yield question, choices.split(',') if choices else None, correct_choice


def format_choices(choices):
    """
    Function to format choices for display.
    
    Parameters:
        choices (list): List of choices.
    
    Returns:
        list: Formatted choices list.
    """
    return choices if choices else ['No choices available']

def get_timer_duration(difficulty):
    """
    Function to get timer duration based on difficulty level.
    
    Parameters:
        difficulty (str): Difficulty level ('Easy', 'Medium', or 'Hard').
    
    Returns:
        int: Timer duration in seconds.
    """
    if difficulty == 'Easy':
        return 5 
    elif difficulty == 'Medium':
        return 180 

if __name__ == "__main__":
    main()

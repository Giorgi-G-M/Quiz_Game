import csv
import random
import time
import sys

def main():
    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    nickname = input("Enter your nickname: ")
    
    user_data = get_user_data(name, surname, nickname)
    
    if user_data:
        difficulty = user_data['Difficulty']
        score = int(user_data['Score'])
        print("Welcome back,", name, surname, "(", nickname, ")!")
    else:
        new_user = add_new_user(name, surname, nickname)
        if new_user:
            difficulty = 'Easy'
            score = 0
        else:
            print("User with the same name, surname, and nickname already exists.")
            return
    
    while True:
        questions = list(get_questions(difficulty))
        
        if not questions:
            print("No questions found for the selected difficulty level.")
            return
        
        random.shuffle(questions)
    
        num_questions_to_ask = min(len(questions), 8)
        
        for question_index in range(num_questions_to_ask):
            question, choices, correct_choice = questions[question_index]
            print("\nQuestion:", question)
            
            if choices:
                print("Possible Answers:", format_choices(choices))
                
            timer_duration = get_timer_duration(difficulty)
            start_time = time.time()

            while True:
                remaining_time = int(timer_duration - (time.time() - start_time))
                if remaining_time <= 0:
                    sys.exit("\nTime's up!")
                    
                user_answer = input(f"Your answer (You have {remaining_time} seconds): ").strip().upper()
                if user_answer == correct_choice.upper():
                    print("\nCorrect!")
                    if difficulty == 'Hard':
                        score += 12
                    else:
                        score += 10
                    break
                else:
                    print("\nIncorrect!.")
                    break 
        
        updated = update_score_and_difficulty(name, surname, nickname, score, difficulty)
        
        if updated:
            print(f"\nCongratulations, you have unlocked {next_difficulty(difficulty)} difficulty level!")
            choice = input("Do you want to continue to the next difficulty level? (yes/no): ").strip().lower()
            if choice != 'yes':
                break
            difficulty = next_difficulty(difficulty)
        else:
            print("\nUnfortunately, you couldn't unlock a new difficulty level. Keep trying.")
            break

def get_user_data(name, surname, nickname):
    with open('scores.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] == name and row['Surname'] == surname and row['Nickname'] == nickname:
                return row
    return None

def add_new_user(name, surname, nickname):
    with open('scores.csv', 'a', newline='') as csvfile:
        fieldnames = ['Name', 'Surname', 'Nickname', 'Difficulty', 'Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Name': name, 'Surname': surname, 'Nickname': nickname, 'Difficulty': 'Easy', 'Score': 0})
    return True

def update_score_and_difficulty(name, surname, nickname, score, difficulty):
    rows = []
    updated = False
    with open('scores.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] == name and row['Surname'] == surname and row['Nickname'] == nickname:
                row['Score'] = score
                if score >= 50:
                    row['Difficulty'] = next_difficulty(difficulty)
                    updated = True
            rows.append(row)
             
    
    with open('scores.csv', 'w', newline='') as csvfile:
        fieldnames = ['Name', 'Surname', 'Nickname', 'Score', 'Difficulty']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    return updated

def next_difficulty(current_difficulty):
    if current_difficulty == 'Easy':
        return 'Medium'
    elif current_difficulty == 'Medium':
        return 'Hard'
    else:
        return 'Hard'

def get_questions(difficulty):
    if difficulty == 'Easy':
        yield from easy_questions()
    elif difficulty == 'Medium':
        yield from medium_questions()
    elif difficulty == 'Hard':
        yield from hard_questions()

def easy_questions():
    with open('easy.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row['Questions']
            correct_choice = row['Correct'].strip() 
            choices = row.get('Choices', None)
            yield question, choices.split(',') if choices else None, correct_choice

def medium_questions():
    with open('medium.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question = row['Questions']
            correct_choice = row['Correct'].strip() 
            choices = row.get('Choices', None)
            yield question, choices.split(',') if choices else None, correct_choice

def hard_questions():
    with open('hard.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        questions = list(reader)
        random.shuffle(questions)
        num_questions_to_ask = min(len(questions), 8)
        for row in questions[:num_questions_to_ask]:
            question = row['Questions']
            correct_choice = row['Correct'].strip() 
            incorrect_choices = row.get('Incorrect', '').split(',') if 'Incorrect' in row else None
            yield question, incorrect_choices, correct_choice


def format_choices(choices):
    return choices if choices else ['No choices available']

def get_timer_duration(difficulty):
    if difficulty == 'Easy':
        return 120 
    elif difficulty == 'Medium':
        return 180 
    elif difficulty == 'Hard':
        return 240 

if __name__ == "__main__":
    main()

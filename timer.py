import time
import sys

for remaining in range(240, 0, -1):
    sys.stdout.write("\r")
    sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
    sys.stdout.flush()
    time.sleep(1)

sys.stdout.write("\rComplete!            \n")


# import csv
# import random
# import time
# import sys
# import threading

# # Function for the live timer
# def live_timer(duration):
#     for remaining in range(duration, 0, -1):
#         sys.stdout.write("\r")
#         sys.stdout.write("{:2d} seconds remaining.".format(remaining)) 
#         sys.stdout.flush()
#         time.sleep(1)

#     sys.stdout.write("\rTime's up!            \n")

# def main():
#     name = input("Enter your name: ")
#     surname = input("Enter your surname: ")
#     nickname = input("Enter your nickname: ")
    
#     user_data = get_user_data(name, surname, nickname)
    
#     if user_data:
#         difficulty = user_data['Difficulty']
#         score = int(user_data['Score'])
#         print("Welcome back,", name, surname, "(", nickname, ")!")
#     else:
#         new_user = add_new_user(name, surname, nickname)
#         if new_user:
#             difficulty = 'Easy'
#             score = 0
#         else:
#             print("User with the same name, surname, and nickname already exists.")
#             return
    
#     while True:
#         questions = list(get_questions(difficulty))
        
#         if not questions:
#             print("No questions found for the selected difficulty level.")
#             return
        
#         random.shuffle(questions)
    
#         num_questions_to_ask = min(len(questions), 8)
        
#         for question_index in range(num_questions_to_ask):
#             question, choices, correct_choice = questions[question_index]
#             print("\nQuestion:", question)
            
#             if choices:
#                 print("Possible Answers:", format_choices(choices))
                
#             timer_duration = get_timer_duration(difficulty)

#             # Start the timer in a separate thread
#             timer_thread = threading.Thread(target=live_timer, args=(timer_duration,))
#             timer_thread.start()

#             # Wait for the user's input
#             user_answer = input(f"Your answer: ").strip().upper()

#             # Join the timer thread to prevent it from running after the user's input
#             timer_thread.join()

#             if user_answer == correct_choice.upper():
#                 print("\nCorrect!")
#                 if difficulty == 'Hard':
#                     score += 12
#                 else:
#                     score += 10
#             else:
#                 print("\nIncorrect!.")
        
#         updated = update_score_and_difficulty(name, surname, nickname, score, difficulty)
        
#         if updated:
#             print(f"\nCongratulations, you have unlocked {next_difficulty(difficulty)} difficulty level!")
#             choice = input("Do you want to continue to the next difficulty level? (yes/no): ").strip().lower()
#             if choice != 'yes':
#                 break
#             difficulty = next_difficulty(difficulty)
#         else:
#             print("\nUnfortunately, you couldn't unlock a new difficulty level. Keep trying.")
#             break

# # Rest of the code remains the same...

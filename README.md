# Trivia Quiz Game

#### Video Demo: [Demo Video](https://youtu.be/vLoBTbfghRE)

#### Description:
The Trivia Quiz Game is a Python program designed to provide users with an interactive quiz experience. The game prompts users to input their name, surname, and nickname to start playing. It retrieves user data from a CSV file and keeps track of their score and the difficulty level they are playing at. If the user is new, they are added to the CSV file with default settings.

## Project Structure:

- `project.py`: This file contains the main code for the Trivia Quiz Game. It includes functions for retrieving user data, adding new users, updating scores and difficulty levels, and generating quiz questions based on the selected difficulty level.

- `test_project.py`: This file contains pytest test functions for testing the functionality of the functions defined in `project.py`. Each function in `project.py` has corresponding test functions to ensure the correctness of the implementation.

- `scores.csv`: This CSV file is used to store user data, including name, surname, nickname, score, and difficulty level. It serves as the data storage mechanism for the Trivia Quiz Game.

- `easy.csv`, `medium.csv`: These CSV files contain trivia questions of different difficulty levels. Each file contains questions along with their correct answers and optionally, multiple-choice options.

## Design Choices:

- Threading: The game utilizes threading to manage user input and timer functionality. By using separate threads for user input and timer countdown, the game ensures responsiveness and a smooth user experience.

- Input/Output Manipulation: Input/output manipulation is used to display questions, choices, and timer countdown in the terminal. This approach provides a simple and intuitive interface for users to interact with the game.

- CSV Data Storage: Storing user data in CSV files allows for easy data retrieval and manipulation. It provides a lightweight and platform-independent solution for persisting user information between game sessions.

- Dynamic Question Generation: Questions are dynamically generated based on the selected difficulty level. This approach allows for a customizable and scalable quiz experience, with the ability to add new questions easily.

## How to Run the Game:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the `project.py` file using Python 3.
4. Follow the on-screen instructions to play the Trivia Quiz Game.

## Dependencies:
- Python 3

## Feedback and Contributions:
If you encounter any issues or have suggestions for improvements, feel free to create an issue or pull request on the project's GitHub repository. Your feedback is valuable and helps us improve the game for all users.

Enjoy playing the Trivia Quiz Game and challenge yourself with exciting trivia questions!

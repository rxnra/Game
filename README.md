# Quiz Battle

Quiz Battle is a Python quiz game where two players compete by answering multiple-choice questions and earning points.

## Features

* Two-player quiz battles
* Three question categories:

  * General Knowledge
  * Math
  * English
* Random question selection
* Points for correct answers
* Speed bonuses
* Power-ups
* Leaderboard to track player scores and wins

## Requirements

* Python 3.10 or newer
* The packages listed in requirements.txt

## Installation

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Install the required packages:

  
   pip install -r requirements.txt
   
## How to Play

1. Run the game:

  
   python game.py
   
2. Choose the option to start a new game.

3. Enter the names of both players.

4. Select a question category.

5. Answer the questions and earn points.

6. View the leaderboard to see the results.

## Question Data

Questions are stored in questions.json. Each question includes its category, question text, four answer options, and the correct answer.

## Running Tests

Run the project's tests with:

pytest
## Project Structure

* game.py — controls the game flow and menu.
* engine.py — manages questions, rounds, and scoring.
* storage.py — loads questions and manages the leaderboard.
* questions.json — contains the quiz questions.
* leaderboard.json — stores player scores and wins.
* tests/ — contains automated tests.
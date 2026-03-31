#!/usr/bin/env python
# coding: utf-8

# In[6]:


"""
Solar System Quiz Game
Author: Isabella Mazzei
Description: A simple quiz game about planets using astronomical data.
Runs in terminal.
"""

import pandas as pd


class Question:
    """Class to store a question and its answer."""

    def __init__(self, prompt, answer, planet=None):
        self.prompt = prompt
        self.answer = answer
        self.planet = planet

    def check_answer(self, user_answer):
        """Check if the user's answer is correct."""
        return user_answer == self.answer.lower()


class QuizGame:
    """Class to run the quiz game."""

    def __init__(self, questions, data):
        self.questions = questions
        self.score = 0
        self.data = data

    def get_fun_fact(self, planet_name):          # ← fixed: back to class level
        """Return a simple fun fact about a planet from dataset."""
        if planet_name is None:
            return ""

        try:
            planet_row = self.data[self.data["Planet"] == planet_name]

            if not planet_row.empty:
                row = planet_row.iloc[0]

                if "Surface Gravity(m/s^2)" in self.data.columns:
                    return f"🌌 Fun fact: {planet_name} has a gravity of {row['Surface Gravity(m/s^2)']} m/s²!"

                if "Mass(10^24kg)" in self.data.columns:
                    return f"🌌 Fun fact: {planet_name} has a mass of {row['Mass(10^24kg)']}!"

                return f"🌌 Fun fact: {planet_name} is a planet in our solar system!"

        except:
            return ""

        return ""

    def play(self):
        """Run the quiz game."""
        name = input("Enter your name: ")
        print(f"\nHi {name}! 🌟 Let's learn about the Solar System!\n")

        for question in self.questions:
            user_answer = input(question.prompt + "\nYour answer: ").strip().lower()

            if question.check_answer(user_answer):
                print("✅ Correct!")
                self.score += 1
            else:
                print(f"❌ Wrong! The correct answer is: {question.answer}")

            fact = self.get_fun_fact(question.planet)
            if fact:
                print(fact)

            print()

        print(f"🎉 Final Score: {self.score}/{len(self.questions)}")


# QUESTIONS

questions = [
    Question("I am the closest planet to the Sun — who am I?", "mercury", "Mercury"),
    Question("I am the biggest planet in our solar system — who am I?", "jupiter", "Jupiter"),
    Question("I have beautiful rings around me — who am I?", "saturn", "Saturn"),

    Question("The Sun is a planet. (True/False)", "false"),
    Question("Mars has two small moons. (True/False)", "true", "Mars"),
    Question("Neptune is the hottest planet. (True/False)", "false", "Neptune"),
    Question("Jupiter is bigger than all other planets combined. (True/False)", "true", "Jupiter"),

    Question("Which planet has the most moons? a) Saturn b) Jupiter c) Uranus", "a", "Saturn"),
    Question("How long is one day on Mercury? a) 24 hours b) 59 Earth days c) 1 year", "b", "Mercury"),
    Question("Which planet is farthest from the Sun? a) Uranus b) Saturn c) Neptune", "c", "Neptune"),

    Question("A year on Mars lasts about ___ Earth days", "687", "Mars"),
    Question("The Great Red Spot on Jupiter is actually a giant ___.", "storm", "Jupiter"),
    Question("Venus rotates so slowly that one ___ is longer than one year there.", "day", "Venus")
]


# MAIN PROGRAM

if __name__ == "__main__":
    try:
        data = pd.read_csv("planets.csv")
    except FileNotFoundError:
        print("⚠️ Error: planets.csv not found. Make sure it's in the same folder.")
        data = pd.DataFrame()

    game = QuizGame(questions, data)
    game.play()


# In[ ]:





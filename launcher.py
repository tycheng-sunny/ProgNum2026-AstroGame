from glossary import *
import subprocess
import os
import time
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress

def loading_game():
    # Just for fancy effect
    with Progress() as progress:
        task = progress.add_task("[cyan]Loading game...", total=100)

        for i in range(100):
            time.sleep(0.005)  # simulate loading
            progress.update(task, advance=1)
    print()

def game_ownership(game_name):
    print(Panel(f"This game is developed by [italic]{AUTHOR_NAMES[game_name]}[/italic].\n\n" \
                f"{GAME_INFO[game_name]}" \
                , title="About the Game"))

def show_launcher(game_names):
    ncols, nrows = 4, 14
    table = Table(show_header=False, box=None, pad_edge=False)

    # Create 5 columns
    for _ in range(ncols):
        table.add_column()

    # Fill table per row
    for row in range(nrows):
        current_row = []

        for col in range(ncols):
            index = row + col * nrows

            if index < len(game_names):
                current_row.append(
                    f"{index + 1}. {game_names[index]}"
                )
            elif index == len(game_names):
                # Add quit option
                current_row.append("0. Quit")
            else:
                current_row.append("")

        table.add_row(*current_row)

    # Print the menu
    print(
        Panel(table,
              title="[bold yellow]Game Launcher[/bold yellow]",
              border_style="yellow"
        )
    )

def confirm_launch(game_name):
    answer = input(
        f"Press Enter to launch {game_name} or type b to go back: "
    )

    return answer.lower() != "b"

def main():
    ini_dir = os.getcwd() # Record the initial dir path
    while True:
        # Read game's display name from GAMES
        game_names = list(GAMES.keys())

        # Launch the menu
        show_launcher(game_names)

        # User input
        choice = input("\nSelect a game: ")

        # Judgement: which game to play / invalid input
        if choice == "0":
            print("\nGoodbye! Hope you had fun!")
            break

        if not choice.isdigit():
            print("\nPlease enter a number.")
            continue

        index = int(choice) - 1

        if index < 0 or index >= len(game_names):
            print("\nInvalid selection.")
            continue

        # Read the path of the selected game
        game_name = game_names[index]
        path = GAMES[game_name]

        # Print stating and display game information
        print(f"\nStarting the game: [italic]{game_name}[/italic]")
        loading_game() # Just for fancy effect
        game_ownership(game_name) # Game ownership and information
        x = confirm_launch(game_name) # Allow user to confirm launch or back to menu

        if x:
            # Launch the game
            try:
                os.chdir(path) # Move to specific game folder
                subprocess.run(["python", "game.py"]) # Run the game (externally; more isolated process)

                # Move back to launcher folder
                os.chdir(ini_dir) 
            except Exception as e:
                print(f"Game crashed: {e}")
        else:
            continue


if __name__ == "__main__":
    main()

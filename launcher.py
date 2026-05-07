from glossary import *
import runpy
from rich import print
from rich.panel import Panel
from rich.columns import Columns
from rich.table import Table

def game_ownership(game_name):
    print()
    print(Panel(f"\nStarting {game_name}...\n" \
                f"This game is developed by [italic]{AUTHOR_NAMES[game_name]}[/italic]. Have fun!\n" \
                , title="About the Game"))
    print()

def show_launcher(game_names):
    ncols, nrows = 5, 11
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

def main():
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

        # Display the ownership of the game
        game_ownership(game_name)

        # Launch the game
        try:
            runpy.run_path(path, run_name="__main__")
        except Exception as e:
            print(f"Game crashed: {e}")


if __name__ == "__main__":
    main()

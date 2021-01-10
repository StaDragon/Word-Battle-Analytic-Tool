#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Jordan Memphis Leef. All Rights Reserved.
# View the LICENSE.md on GitHub

__all__ = ["__title__", "__version__", "__author__", "__license__", "__copyright__"]
__title__ = "Word Battle Analytic Tool"
__version__ = "1"
__author__ = "Jordan Memphis Leef"
__license__ = "Freeware"
__copyright__ = "Copyright (C) Jordan Memphis Leef"

from typing import List, Dict, Tuple, Iterator
from colorama import Fore, Style
from itertools import islice
from math import ceil
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import subprocess
import os.path
import msvcrt
import ctypes
import errno
import json
import time
import sys
import ast

# Global constant declaration
PY_VERSION = 3.8 # The Python version that the game is programmed on
SW_MAXIMISE = 3 # Set the command prompt to open in maximized window
LOWER_LIMIT = 3 # The min board length
UPPER_LIMIT = 15 # The max board length
COMPUTER_PLAYER_NAME = "Computer" # To distinguish itself from human players
LOCAL_DIR_DATA_TO_ANALYSE = "./Data To Analyse/" # The path to the "Data To Analyse" folder
REPLAY_FILE_FORMAT = ".wbr" # The format for the replay files
LETTER_VALUE = {"A": 3, "B": 9, "C": 8, "D": 7, "E": 1, "F": 8, "G": 8, "H": 5, "I": 5, "J": 10, "K": 10, "L": 7, "M": 8, "N": 5, "O": 4, "P": 9, "Q": 10, "R": 6, "S": 5, "T": 2, "U": 8, "V": 10, "W": 8, "X": 10, "Y": 9, "Z": 10} # The strength of each letter

def clear_screen(time_set=1) -> None:
    """Clear the screen."""
    time.sleep(time_set)
    os.system('cls')


def input_integer(label: str) -> int:
    """Convert an string and output as integer."""
    while True:
        try:
            return int(input(label))
        except ValueError:
            clear_screen(0)


def chunk(it, size) -> Iterator[tuple]:
    """Divide a list into its chunks."""
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


def check_if_file_exists(file_name: str) -> None:
    """To check if a file exists."""
    # Do not run this on PyCharm due to the code msvcrt.getch() contained within this component

    try:
        f = open(file_name)
        f.close()
    except FileNotFoundError:
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
        print(Fore.RED + Style.BRIGHT + f"Error: File not found!\nPlease add the file {file_name} before continuing")
        print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
        msvcrt.getch()
        check_if_file_exists(file_name)


def calculate_word_strength(word: str) -> int:
    """Calculate the strength of the word."""
    total = 0

    try:
        for letter in word:
            total += LETTER_VALUE[letter]
    except KeyError:
        return 0

    return total


def calculate_frequency(lst: list) -> Dict[str, int]:
    """Calculate the frequency from a list."""
    frequencies = {}
    for item in lst:
        if item in frequencies:
            frequencies[item] += 1
        else:
            frequencies[item] = 1

    return frequencies


def sort_dict_by_keys(dct: dict) -> List[Tuple[str, int]]:
    """Sort a dictionary by its keys in ascending order."""
    sorted_list = []
    for i in sorted(dct):
        sorted_list.append((i, dct[i]))

    return sorted_list


def sort_dict_by_values(dct: dict) -> List[Tuple[str, int]]:
    """Sort a dictionary by its keys in ascending order."""
    return sorted(dct.items(), key=lambda x: x[1], reverse=True)


def check_files() -> None:
    """Open all the files to check their board size."""
    # Do not run this on PyCharm due to the code msvcrt.getch() contained within this component
    board_size_list = []
    game_duration_list = []
    players_info = []
    filename_list = []

    try:
        file_list = os.listdir(LOCAL_DIR_DATA_TO_ANALYSE)
        filename_list += file_list

        if len(file_list) == 0:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
            print(Fore.RED + Style.BRIGHT + "Error: No files detected!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to return to main menu.")
            msvcrt.getch()
            main()

        # Open every .wbr file within the 'Data To Analyse' folder
        for file in file_list:
            file = file[:-4]  # Remove the file extension

            if os.path.isfile(f"{LOCAL_DIR_DATA_TO_ANALYSE}{file}{REPLAY_FILE_FORMAT}"):
                try:
                    with open(f"{LOCAL_DIR_DATA_TO_ANALYSE}{file}{REPLAY_FILE_FORMAT}") as f:
                        bytes_data = f.read().splitlines()
                        data = ast.literal_eval("".join(map(chr, [int(i) for i in bytes_data])))
                        wbr_content = {"wbr_game_info": data}
                        replay_info = json.dumps(wbr_content, indent=7)
                        replay_info = json.loads(replay_info)

                        if replay_info['wbr_game_info'][0]['game_number'] > 0 and replay_info['wbr_game_info'][0]['board_length'] > 0:
                            board_size_list.append(replay_info['wbr_game_info'][0]['board_length'])
                            game_duration_list.append(replay_info['wbr_game_info'][0]['game_duration'])
                            player_list = []
                            player_info = []

                            for player in replay_info['wbr_game_info'][1:]:
                                player_dict = {}

                                if player['player_name'] not in player_list:
                                    player_dict['player_name'] = player['player_name']
                                    player_dict['type'] = player['type']
                                    player_list.append(player['player_name'])
                                    player_info.append(player_dict)

                            players_info.append(player_info)
                        else:
                            board_size_list.append(None)
                            game_duration_list.append(None)
                            players_info.append(None)
                except (KeyError, ValueError, SyntaxError, OverflowError):
                    board_size_list.append(None)
                    game_duration_list.append(None)
                    players_info.append(None)
            else:
                board_size_list.append(None)
                game_duration_list.append(None)
                players_info.append(None)

        clear_screen(0)

        while True:
            board_size = input_integer("Board Size (Type 0 to go back to main menu): ")

            if board_size == 0:
                main()
            elif board_size < LOWER_LIMIT or board_size > UPPER_LIMIT:
                clear_screen(0)
                print(Fore.WHITE + Style.BRIGHT + "Board Size (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "Invalid board size!")
                print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
                msvcrt.getch()
                clear_screen(0)
            else:
                clear_screen(0)
                print(f"Board Size Required: {board_size}\n{len(board_size_list)} files have been checked.\n")
                type_collection = []
                game_mode_list = []

                for player in players_info:
                    type_list = []

                    try:
                        for key in player:
                            type_list.append(key['type'])
                    except TypeError:
                        type_list.append(None)

                    type_collection.append(type_list)

                for type_list in type_collection:
                    if "human" not in type_list:
                        game_mode_list.append("Computer Vs Computer")
                    elif "computer" not in type_list:
                        game_mode_list.append("Human Vs Human")
                    elif None in type_list:
                            game_mode_list.append(None)
                    else:
                        game_mode_list.append("Human Vs Computer")

                warning = False

                for i in range(len(board_size_list)):
                    if board_size_list[i] is None or len(players_info[i]) == 0 or game_mode_list[i] is None:
                        warning = True
                        print(Fore.YELLOW + Style.BRIGHT + f"{filename_list[i]} | Board Size: Indeterminate | Number of Players: Indeterminate | Game Mode: Indeterminate | Game Duration: Indeterminate")
                    else:
                        if board_size_list[i] == board_size:
                            print(Fore.GREEN + Style.BRIGHT + f"{filename_list[i]} | Board Size: {board_size_list[i]} | Number of Players: {len(players_info[i])} | Game Mode: {game_mode_list[i]} | Game Duration: {game_duration_list[i]}")
                        else:
                            print(Fore.WHITE + Style.BRIGHT + f"{filename_list[i]} | Board Size: {board_size_list[i]} | Number of Players: {len(players_info[i])} | Game Mode: {game_mode_list[i]} | Game Duration: {game_duration_list[i]}")

                if warning:
                    print(Fore.YELLOW + Style.BRIGHT + "\nWarning: Multiple files either have incorrect file extension, is corrupted or outdated.\r")

                print(Fore.GREEN + Style.BRIGHT + "\nProcess Complete!")
                print(Fore.WHITE + Style.BRIGHT + "Press any key to return to main menu.")
                msvcrt.getch()
                main()
    except FileNotFoundError:
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
        print(Fore.RED + Style.BRIGHT + "Error: The 'Data To Analyse' folder cannot be found! This folder is now created.")

        # Create the folder if it does not exist
        try:
            os.makedirs('Data To Analyse')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
        msvcrt.getch()
        clear_screen(0)


def display_player_statistics() -> None:
    """Display the player's statistics."""
    def get_player_word_dict(players: list, grouping=0) -> dict:
        """Create a dict of players with their word lists."""
        players_dict = { i : [] for i in player_list}

        for player in players:
            if player[0] in players_dict:
                players_dict[player[0]].append(player[1])

        if grouping != 0:
            for player in players_dict.values():
                players_dict = list(chunk(player, grouping))

        return players_dict

    def calculate_most_frequent_words(word_list: list) -> List[str]:
        """Calculate the most frequent words for a player."""
        most_frequent = []
        length = 3
        word_frequency = calculate_frequency(word_list)

        if len(word_list) >= length:
            while len(most_frequent) < length:
                letter = max(word_frequency, key=word_frequency.get)
                most_frequent.append(letter)
                del word_frequency[letter]
        else:
            return word_list

        return most_frequent

    def calculate_most_frequent_letters(word_list: list) -> List[str]:
        """Calculate the most frequent letters for a player."""
        letter_list = []
        most_frequent = []
        length = 3

        for word in word_list:
            letter_list += list(word)

        letter_frequency = calculate_frequency(letter_list)

        while len(most_frequent) < length:
            letter = max(letter_frequency, key=letter_frequency.get)
            most_frequent.append(letter)
            del letter_frequency[letter]

        return most_frequent

    def calculate_avg_word_strength(word_collection: list, game_length: int):
        """Calculate the avg word strength for a player."""
        highest_avg = 0

        for word_list in word_collection:
            total = 0

            for word in word_list:
                total += calculate_word_strength(word)

            avg = int(total / game_length)

            if avg >= highest_avg:
                highest_avg = avg

        return highest_avg

    def calculate_total_games(outcomes: dict) -> int:
        """Calculate the total games for a player."""
        return sum(outcomes.values())

    def calculate_win_rate(wins: int, total_games: int) -> float:
        """Calculate the win rate for a player."""
        win_rate = round(wins / total_games * 100, 2)
        return win_rate

    def display_data() -> None:
        """Display data."""
        title = "Player Statistics"
        player_word_dict = get_player_word_dict(players_words)

        for player in player_events:
            if player[0] in players:
                if player[1] == 'RESIGNED':
                    players[player[0]]['LOSES'] += 1
                elif player[1] == 'DRAW':
                    players[player[0]]['DRAWS'] += 1
                elif player[1] == 'WON':
                    players[player[0]]['WINS'] += 1
            else:
                if player[1] == 'RESIGNED':
                    players[player[0]]['LOSES'] = 1
                elif player[1] == 'DRAW':
                    players[player[0]]['DRAWS'] = 1
                elif player[1] == 'WON':
                    players[player[0]]['WINS'] = 1

        clear_screen(0)
        print(f"{title}\n{'-' * len(title)}\r")

        for player in player_info:
            word_list = player_word_dict[player[0]]
            split_number = ceil(game_length[player_info.index(player)] / 2)
            total_turns = get_player_word_dict(players_words, split_number)
            total_games_played = calculate_total_games(players[player[0]])

            if player[2] is None:
                print(f"\n{player[0]}\nWINS: {players[player[0]]['WINS']} LOSES: {players[player[0]]['LOSES']} DRAWS: {players[player[0]]['DRAWS']}")
                print(f"Total Games Played: {total_games_played}\nWin Rate: {calculate_win_rate(players[player[0]]['WINS'], total_games_played)}%")

                if word_list:
                    most_frequent_word = calculate_most_frequent_words(word_list)
                    most_frequent_letters = calculate_most_frequent_letters(word_list)
                    print(f"Most Frequent Words: {', '.join(most_frequent_word)}\nMost Frequent Letters: {', '.join(most_frequent_letters)}")
                    print("Avg Word Strength Per Turn:", calculate_avg_word_strength(total_turns, total_games_played))
                else:
                    print(f"Most Frequent Words: 0\nMost Frequent Letters: 0")
            else:
                print(f"\n{player[0]} ({player[2]}) - {player[1].capitalize()}\nWINS: {players[player[0]]['WINS']} LOSES: {players[player[0]]['LOSES']} DRAWS: {players[player[0]]['DRAWS']}")
                print(f"Total Games Played: {total_games_played}\nWin Rate: {calculate_win_rate(players[player[0]]['WINS'], total_games_played)}%")

                if word_list:
                    most_frequent_word = calculate_most_frequent_words(word_list)
                    most_frequent_letters = calculate_most_frequent_letters(word_list)
                    print(f"Most Frequent Words: {', '.join(most_frequent_word)}\nMost Frequent Letters: {', '.join(most_frequent_letters)}")
                    print("Avg Word Strength Per Turn:", calculate_avg_word_strength(total_turns, total_games_played))

                else:
                    print(f"Most Frequent Words: 0\nMost Frequent Letters: 0")

        print(Fore.WHITE + Style.BRIGHT + "\nPress any key to continue...")
        msvcrt.getch()
        main()

    board_size_list = []
    player_list = []
    player_info = []
    player_events = []
    players_words = []
    game_length = []

    try:
        file_list = os.listdir(LOCAL_DIR_DATA_TO_ANALYSE)

        if len(file_list) == 0:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
            print(Fore.RED + Style.BRIGHT + "Error: The 'Data To Analyse' folder is empty!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
            msvcrt.getch()
            clear_screen(0)
        else:
            # Open every .wbr file within the 'Data To Analyse' folder
            for file in file_list:
                file = file[:-4]  # Remove the file extension

                if os.path.isfile(f"{LOCAL_DIR_DATA_TO_ANALYSE}{file}{REPLAY_FILE_FORMAT}"):
                    try:
                        with open(f"{LOCAL_DIR_DATA_TO_ANALYSE}{file}{REPLAY_FILE_FORMAT}") as f:
                            bytes_data = f.read().splitlines()
                            data = ast.literal_eval("".join(map(chr, [int(i) for i in bytes_data])))
                            wbr_content = {"wbr_game_info": data}
                            replay_info = json.dumps(wbr_content, indent=7)
                            replay_info = json.loads(replay_info)

                            if replay_info['wbr_game_info'][0]['game_number'] > 0 and replay_info['wbr_game_info'][0]['board_length'] > 0:
                                board_size_list.append(replay_info['wbr_game_info'][0]['board_length'])
                                replay_info['wbr_game_info'].pop(0)

                                for player in replay_info['wbr_game_info']:

                                    if player['player_name'] not in player_list:
                                        player_list.append(player['player_name'])
                                        player_info.append([player['player_name'], player['type'], player['difficulty']])
                                        game_length.append(len(replay_info['wbr_game_info']) - 1)

                                    player_events.append([player['player_name'], player['event']])

                                    if player['word'] is not None:
                                        players_words.append([player['player_name'], player['word']])

                                players = {stats: {'WINS': 0, 'DRAWS': 0, 'LOSES': 0} for stats in player_list}
                            else:
                                pass
                    except (KeyError, ValueError, SyntaxError, OverflowError):
                        pass
                else:
                    pass

            difference = False
            temp_num = None

            for i in board_size_list:
                if (i >= LOWER_LIMIT or i <= UPPER_LIMIT) and temp_num is None:
                    temp_num = i
                else:
                    if i != temp_num and not difference:
                        difference = True
                        clear_screen(0)
                        print(Fore.YELLOW + Style.BRIGHT + "Warning: Multiple files are containing different board sizes. Are you sure you want to continue?")
                        user_input = input(Fore.WHITE + Style.BRIGHT + "Y / N: ").upper()

                        if user_input == "":
                            display_letter_frequency_bar_graph()
                        elif user_input == "Y":
                            display_data()
                        elif user_input == "N":
                            main()
                        else:
                            display_letter_frequency_bar_graph()

            if not difference:
                display_data()
    except FileNotFoundError:
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
        print(Fore.RED + Style.BRIGHT + "Error: The 'Data To Analyse' folder cannot be found! This folder is now created.")

        # Create the folder if it does not exist
        try:
            os.makedirs('Data To Analyse')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
        msvcrt.getch()
        clear_screen(0)


def display_letter_frequency_bar_graph() -> None:
    """Generate a bar graph for letter frequency and display it."""
    def display_plot() -> None:
        """Display plot."""
        # The data to work with
        letter_frequency = calculate_frequency(letter_list)

        for letter in LETTER_VALUE.keys():
            if letter not in letter_frequency:
                letter_frequency[letter] = 0

        v_list = sort_dict_by_values(letter_frequency)

        # The plot
        fig = plt.figure(1)
        fig.canvas.set_window_title('Letter Frequency Bar Graph')
        plt.xlabel("Letter")
        plt.ylabel("Frequency")
        plt.title("Letter Frequency")
        bar_list = plt.bar(*zip(*v_list))
        caption = f"Generated by {__title__}."
        fig.text(0.1, 0.01, caption, ha='left')

        # For placing the frequency number on top of each bar
        x = []
        y = []

        for i in v_list:
            x.append(i[0])
            y.append(i[1])

        for i in range(len(v_list)):
            plt.annotate(str(y[i]), xy=(x[i], y[i]), ha='center', va='bottom')

        # Assign each letter with each colour corresponding with their value
        colour_list = []

        for i in v_list:
            for letter in i:
                if letter == 'J' or letter == 'K' or letter == 'Q' or letter == 'V' or letter == 'X' or letter == 'Z':
                    colour_list.append('tab:purple')
                elif letter == 'B' or letter == 'P' or letter == 'Y':
                    colour_list.append('tab:pink')
                elif letter == 'C' or letter == 'F' or letter == 'G' or letter == 'M' or letter == 'U' or letter == 'W':
                    colour_list.append('tab:red')
                elif letter == 'D' or letter == 'L':
                    colour_list.append('tab:brown')
                elif letter == 'R':
                    colour_list.append('tab:orange')
                elif letter == 'H' or letter == 'I' or letter == 'N' or letter == 'S':
                    colour_list.append('tab:olive')
                elif letter == 'O':
                    colour_list.append('tab:green')
                elif letter == 'A':
                    colour_list.append('tab:cyan')
                elif letter == 'T':
                    colour_list.append('tab:blue')
                elif letter == 'E':
                    colour_list.append('tab:gray')

        for i in range(len(colour_list)):
            bar_list[i].set_color(colour_list[i])

        # Colour values
        purple_value = mpatches.Patch(color='tab:purple', label='10')
        pink_value = mpatches.Patch(color='tab:pink', label='9')
        red_value = mpatches.Patch(color='tab:red', label='8')
        brown_value = mpatches.Patch(color='tab:brown', label='7')
        orange_value = mpatches.Patch(color='tab:orange', label='6')
        olive_value = mpatches.Patch(color='tab:olive', label='5')
        green_value = mpatches.Patch(color='tab:green', label='4')
        cyan_value = mpatches.Patch(color='tab:cyan', label='3')
        blue_value = mpatches.Patch(color='tab:blue', label='2')
        gray_value = mpatches.Patch(color='tab:gray', label='1')

        # Legend of colour values
        plt.legend(title='Value', handles=[purple_value, pink_value, red_value, brown_value, orange_value, olive_value, green_value, cyan_value, blue_value, gray_value])

        plt.show()

    board_size_list = []
    word_list = []
    letter_list = []

    try:
        file_list = os.listdir(LOCAL_DIR_DATA_TO_ANALYSE)

        if len(file_list) == 0:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
            print(Fore.RED + Style.BRIGHT + "Error: The 'Data To Analyse' folder is empty!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
            msvcrt.getch()
            clear_screen(0)
        else:
            # Open every .wbr file within the 'Data To Analyse' folder
            for file in file_list:
                file = file[:-4] # Remove the file extension

                if os.path.isfile(f"{LOCAL_DIR_DATA_TO_ANALYSE}{file}{REPLAY_FILE_FORMAT}"):
                    try:
                        with open(f"{LOCAL_DIR_DATA_TO_ANALYSE}{file}{REPLAY_FILE_FORMAT}") as f:
                            bytes_data = f.read().splitlines()
                            data = ast.literal_eval("".join(map(chr, [int(i) for i in bytes_data])))
                            wbr_content = {"wbr_game_info": data}
                            replay_info = json.dumps(wbr_content, indent=7)
                            replay_info = json.loads(replay_info)

                            if replay_info['wbr_game_info'][0]['game_number'] > 0 and replay_info['wbr_game_info'][0]['board_length'] > 0:
                                board_size_list.append(replay_info['wbr_game_info'][0]['board_length'])
                                replay_info['wbr_game_info'].pop(0)

                                for player in replay_info['wbr_game_info']:
                                    word = player['word']

                                    if word is not None:
                                        word_list.append(word)

                                        for letter in word:
                                            letter_list.append(letter)
                            else:
                                pass
                    except (KeyError, ValueError, SyntaxError, OverflowError):
                        pass
                else:
                    pass

            difference = False
            temp_num = None

            for i in board_size_list:
                if (i >= LOWER_LIMIT or i <= UPPER_LIMIT) and temp_num is None:
                    temp_num = i
                else:
                    if i != temp_num and not difference:
                        difference = True
                        clear_screen(0)
                        print(Fore.YELLOW + Style.BRIGHT + "Warning: Multiple files are containing different board sizes. Are you sure you want to continue?")
                        user_input = input(Fore.WHITE + Style.BRIGHT + "Y / N: ").upper()

                        if user_input == "":
                            display_letter_frequency_bar_graph()
                        elif user_input == "Y":
                            display_plot()
                        elif user_input == "N":
                            main()
                        else:
                            display_letter_frequency_bar_graph()

            if not difference:
                display_plot()
    except FileNotFoundError:
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
        print(Fore.RED + Style.BRIGHT + "Error: The 'Data To Analyse' folder cannot be found! This folder is now created.")

        # Create the folder if it does not exist
        try:
            os.makedirs('Data To Analyse')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
        msvcrt.getch()
        clear_screen(0)


def display_word_length_frequency_bar_graph() -> None:
    """Generate a bar graph for word length frequency and display it."""
    def display_plot() -> None:
        """Display plot."""
        # The data to work with
        length_list = sort_dict_by_values(word_length_dict)

        # The plot
        fig = plt.figure(1)
        fig.canvas.set_window_title('Word Length Bar Graph')
        plt.xlabel("Word Length")
        plt.ylabel("Frequency")
        plt.title("Word Length Frequency")
        plt.bar(*zip(*length_list))
        caption = f"Generated by {__title__}."
        fig.text(0.1, 0.01, caption, ha='left')

        # For placing the frequency number on top of each bar
        x = []
        y = []

        for i in length_list:
            x.append(i[0])
            y.append(i[1])

        for i in range(len(length_list)):
            plt.annotate(str(y[i]), xy=(x[i], y[i]), ha='center', va='bottom')

        plt.show()

    board_size_list = []
    word_list = []
    word_length_dict = {}

    try:
        file_list = os.listdir(LOCAL_DIR_DATA_TO_ANALYSE)

        if len(file_list) == 0:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
            print(Fore.RED + Style.BRIGHT + "Error: The 'Data To Analyse' folder is empty!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
            msvcrt.getch()
            clear_screen(0)
        else:
            # Open every .wbr file within the 'Data To Analyse' folder
            for file in file_list:
                file = file[:-4]  # Remove the file extension

                if os.path.isfile(f"{LOCAL_DIR_DATA_TO_ANALYSE}{file}{REPLAY_FILE_FORMAT}"):
                    try:
                        with open(f"{LOCAL_DIR_DATA_TO_ANALYSE}{file}{REPLAY_FILE_FORMAT}") as f:
                            bytes_data = f.read().splitlines()
                            data = ast.literal_eval("".join(map(chr, [int(i) for i in bytes_data])))
                            wbr_content = {"wbr_game_info": data}
                            replay_info = json.dumps(wbr_content, indent=7)
                            replay_info = json.loads(replay_info)

                            if replay_info['wbr_game_info'][0]['game_number'] > 0 and replay_info['wbr_game_info'][0][
                                'board_length'] > 0:
                                board_size_list.append(replay_info['wbr_game_info'][0]['board_length'])
                                replay_info['wbr_game_info'].pop(0)

                                for player in replay_info['wbr_game_info']:
                                    word = player['word']

                                    if word is not None:
                                        word_list.append(word)
                            else:
                                pass
                    except (KeyError, ValueError, SyntaxError, OverflowError):
                        pass
                else:
                    pass

            for word in word_list:
                length = len(word)

                if length not in word_length_dict:
                    word_length_dict[length] = 1
                else:
                    word_length_dict[length] += 1

            difference = False
            temp_num = None

            for i in board_size_list:
                if (i >= LOWER_LIMIT or i <= UPPER_LIMIT) and temp_num is None:
                    temp_num = i
                else:
                    if i != temp_num and not difference:
                        difference = True
                        clear_screen(0)
                        print(Fore.YELLOW + Style.BRIGHT + "Warning: Multiple files are containing different board sizes. Are you sure you want to continue?")
                        user_input = input(Fore.WHITE + Style.BRIGHT + "Y / N: ").upper()

                        if user_input == "":
                            display_word_length_frequency_bar_graph()
                        elif user_input == "Y":
                            display_plot()
                        elif user_input == "N":
                            main()
                        else:
                            display_word_length_frequency_bar_graph()

            if not difference:
                display_plot()
    except FileNotFoundError:
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
        print(Fore.RED + Style.BRIGHT + "Error: The 'Data To Analyse' folder cannot be found! This folder is now created.")

        # Create the folder if it does not exist
        try:
            os.makedirs('Data To Analyse')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
        msvcrt.getch()
        clear_screen(0)


def display_square_usage_heatmap() -> None:
    """Generate a heatmap for board occupancy likelihood heatmap and display it."""
    def display_plot() -> None:
        """Display plot."""
        # Annotations
        clear_screen(0)
        annotations = False
        user_input = input("Display annotations? Y / N: ").upper()

        if user_input == "":
            display_plot()
        elif user_input == "Y":
            annotations = True
        elif user_input == "N":
            annotations = False
        else:
            display_plot()

        # The data to work with
        path_list = []

        for paths in path_collection:
            for path in paths:
                path[0] += 1
                path[1] += 1
                path_list.append(path)

        # The plot
        fig = plt.figure(1)
        fig.canvas.set_window_title('Square Usage Heatmap')
        plt.title("Square Usage")
        caption = f"Generated by {__title__}."
        fig.text(0.3, 0.01, caption, ha='left')
        df = pd.DataFrame(path_list, columns=['y', 'x'])
        df2 = pd.crosstab(df['y'], df['x']).div(len(df)).multiply(100)

        for x in df2:
            for y in df2:
                if df2[x][y] >= 1:
                    df2[x][y] = 1
        
        ax = sns.heatmap(df2, annot=annotations, annot_kws={"size": 8.9}, fmt='0.2f', cmap='coolwarm', cbar_kws={'label': 'Relative Occupancy Probability', 'orientation': 'horizontal', 'shrink': 0.5}, linewidths=0.5, linecolor='black', vmin=0, vmax=1, square=True)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.set_ylabel('')
        ax.set_xlabel('')
        colour_bar = ax.collections[0].colorbar
        colour_bar.set_ticks([0, .25, .5, .75, 1])
        colour_bar.set_ticklabels(['0.00', '0.25', '0.50', '0.75', '1.00'])

        for _, spine in ax.spines.items():
            spine.set_visible(True)

        plt.show()

    board_size_list = []
    path_collection = []
    board_size = None

    try:
        file_list = os.listdir(LOCAL_DIR_DATA_TO_ANALYSE)

        if len(file_list) == 0:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
            print(Fore.RED + Style.BRIGHT + "Error: The 'Data To Analyse' folder is empty!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
            msvcrt.getch()
            clear_screen(0)
        else:
            # Open every .wbr file within the 'Data To Analyse' folder
            for file in file_list:
                file = file[:-4] # Remove the file extension

                if os.path.isfile(f"{LOCAL_DIR_DATA_TO_ANALYSE}{file}{REPLAY_FILE_FORMAT}"):
                    try:
                        with open(f"{LOCAL_DIR_DATA_TO_ANALYSE}{file}{REPLAY_FILE_FORMAT}") as f:
                            bytes_data = f.read().splitlines()
                            data = ast.literal_eval("".join(map(chr, [int(i) for i in bytes_data])))
                            wbr_content = {"wbr_game_info": data}
                            replay_info = json.dumps(wbr_content, indent=7)
                            replay_info = json.loads(replay_info)

                            if replay_info['wbr_game_info'][0]['game_number'] > 0 and replay_info['wbr_game_info'][0]['board_length'] > 0:
                                board_size_list.append(replay_info['wbr_game_info'][0]['board_length'])

                                if board_size is None:
                                    board_size = replay_info['wbr_game_info'][0]["board_length"]

                                replay_info['wbr_game_info'].pop(0)

                                for player in replay_info['wbr_game_info']:
                                    path = player['selected_path']

                                    if path is not None:
                                        path_collection.append(path)
                            else:
                                pass
                    except (KeyError, ValueError, SyntaxError, OverflowError):
                        pass
                else:
                    pass

            difference = False
            temp_num = None

            for i in board_size_list:
                if (i >= LOWER_LIMIT or i <= UPPER_LIMIT) and temp_num is None:
                    temp_num = i
                else:
                    if i != temp_num and not difference:
                        difference = True
                        clear_screen(0)
                        print(Fore.YELLOW + Style.BRIGHT + "Warning: Multiple files are containing different board sizes. Are you sure you want to continue?")
                        user_input = input(Fore.WHITE + Style.BRIGHT + "Y / N: ").upper()

                        if user_input == "":
                            display_square_usage_heatmap()
                        elif user_input == "Y":
                            display_plot()
                        elif user_input == "N":
                            main()
                        else:
                            display_square_usage_heatmap()

            if not difference:
                display_plot()
    except FileNotFoundError:
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
        print(Fore.RED + Style.BRIGHT + "Error: The 'Data To Analyse' folder cannot be found! This folder is now created.")

        # Create the folder if it does not exist
        try:
            os.makedirs('Data To Analyse')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
        msvcrt.getch()
        clear_screen(0)


def main():
    """The program."""
    # Create title bar
    ctypes.windll.kernel32.SetConsoleTitleW(f"{__title__} v{__version__}")

    # Cause the command prompt to open in maximize window by default
    user32 = ctypes.WinDLL('user32')
    hWnd = user32.GetForegroundWindow()
    user32.ShowWindow(hWnd, SW_MAXIMISE)

    # Disable QuickEdit and Insert mode by default
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)

    # Run main menu
    while True:
        clear_screen(0)
        print(Fore.WHITE + Style.BRIGHT + f"{'-' * 32}\n{__title__} v{__version__}\nWritten in Python {PY_VERSION}\nDeveloped by {__author__}\n{'-' * 32}")
        print("Consult the README file on how to use this program.\n")
        print("[1] Check files to find board size")
        print("[2] Display player statistics")
        print("[3] Display letter frequency bar graph")
        print("[4] Display word length frequency bar graph")
        print("[5] Display square usage heatmap")
        print("[6] View README file")
        print("[7] Exit")
        selection = input("\nSelection: ")

        if selection == "1":
            check_files()
        elif selection == "2":
            display_player_statistics()
        elif selection == "3":
            display_letter_frequency_bar_graph()
        elif selection == "4":
            display_word_length_frequency_bar_graph()
        elif selection == "5":
            display_square_usage_heatmap()
        elif selection == "6":
            check_if_file_exists('README.txt')
            subprocess.call(['cmd', '/c', 'start', '/max', 'README.txt'])
        elif selection == "7":
            sys.exit(0)


if __name__ == "__main__":
    main()

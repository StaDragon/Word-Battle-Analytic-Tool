#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) Jordan Memphis Leef. All Rights Reserved.
# View the LICENSE.md on GitHub

__all__ = ["__title__", "__version__", "__author__", "__license__", "__copyright__"]
__title__ = "Word Battle Analytic Tool"
__version__ = "1.1"
__author__ = "Jordan Memphis Leef"
__license__ = "Freeware"
__copyright__ = "Copyright (C) Jordan Memphis Leef"

from typing import List, Dict, Tuple, Iterator, Generator, Any
from colorama import Fore, Style
from itertools import islice
from math import ceil
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import itertools as it
import seaborn as sns
import pandas as pd
import numpy as np
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
LOCAL_DIR_REPLAYS = "./Replays/" # The path to the "Replays" folder
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
        file_list = os.listdir(LOCAL_DIR_REPLAYS)
        filename_list += file_list

        if len(file_list) == 0:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
            print(Fore.RED + Style.BRIGHT + "Error: No files detected!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to return to main menu.")
            msvcrt.getch()
            main()

        # Open every .wbr file within the 'Replays' folder
        for file in file_list:
            file = file[:-4]  # Remove the file extension

            if os.path.isfile(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}"):
                try:
                    with open(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}") as f:
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
        print(Fore.RED + Style.BRIGHT + "Error: The 'Replays' folder cannot be found! This folder is now created.")

        # Create the folder if it does not exist
        try:
            os.makedirs('Replays')
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
        file_list = os.listdir(LOCAL_DIR_REPLAYS)

        if len(file_list) == 0:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
            print(Fore.RED + Style.BRIGHT + "Error: The 'Replays' folder is empty!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
            msvcrt.getch()
            clear_screen(0)
        else:
            # Open every .wbr file within the 'Replays' folder
            for file in file_list:
                file = file[:-4]  # Remove the file extension

                if os.path.isfile(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}"):
                    try:
                        with open(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}") as f:
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
        print(Fore.RED + Style.BRIGHT + "Error: The 'Replays' folder cannot be found! This folder is now created.")

        # Create the folder if it does not exist
        try:
            os.makedirs('Replays')
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
        file_list = os.listdir(LOCAL_DIR_REPLAYS)

        if len(file_list) == 0:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
            print(Fore.RED + Style.BRIGHT + "Error: The 'Replays' folder is empty!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
            msvcrt.getch()
            clear_screen(0)
        else:
            # Open every .wbr file within the 'Replays' folder
            for file in file_list:
                file = file[:-4] # Remove the file extension

                if os.path.isfile(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}"):
                    try:
                        with open(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}") as f:
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
        print(Fore.RED + Style.BRIGHT + "Error: The 'Replays' folder cannot be found! This folder is now created.")

        # Create the folder if it does not exist
        try:
            os.makedirs('Replays')
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
        file_list = os.listdir(LOCAL_DIR_REPLAYS)

        if len(file_list) == 0:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
            print(Fore.RED + Style.BRIGHT + "Error: The 'Replays' folder is empty!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
            msvcrt.getch()
            clear_screen(0)
        else:
            # Open every .wbr file within the 'Replays' folder
            for file in file_list:
                file = file[:-4]  # Remove the file extension

                if os.path.isfile(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}"):
                    try:
                        with open(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}") as f:
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
        print(Fore.RED + Style.BRIGHT + "Error: The 'Replays' folder cannot be found! This folder is now created.")

        # Create the folder if it does not exist
        try:
            os.makedirs('Replays')
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
        file_list = os.listdir(LOCAL_DIR_REPLAYS)

        if len(file_list) == 0:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + f"{__title__} v{__version__} System Event")
            print(Fore.RED + Style.BRIGHT + "Error: The 'Replays' folder is empty!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
            msvcrt.getch()
            clear_screen(0)
        else:
            # Open every .wbr file within the 'Replays' folder
            for file in file_list:
                file = file[:-4] # Remove the file extension

                if os.path.isfile(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}"):
                    try:
                        with open(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}") as f:
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
        print(Fore.RED + Style.BRIGHT + "Error: The 'Replays' folder cannot be found! This folder is now created.")

        # Create the folder if it does not exist
        try:
            os.makedirs('Replays')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
        msvcrt.getch()
        clear_screen(0)


def open_replay() -> None:
    """Open .wbr files to watch them."""
    def run_replay(replay_info: dict, replay_speed: float) -> None:
        """Run the replay file."""
        board = Board()
        board.create_board(replay_info['wbr_game_info'][0]['board_length'])
        game_duration = replay_info['wbr_game_info'][0]['game_duration']
        board.game_duration = game_duration
        players = []

        for player in replay_info['wbr_game_info'][1:]:
            if player['player_name'] not in players:
                players.append({"name": player['player_name'], "type": player['type'], "difficulty": player['difficulty']})

        board.players = [dict(t) for t in {tuple(d.items()) for d in players}]
        board.player = players[0]['name']

        if players[0]['difficulty'] is not None:
            board.player = f"{players[0]['name']} ({players[0]['difficulty']})"

        board.game_counter = replay_info['wbr_game_info'][0]['game_number']
        clear_screen(0)
        board.display_game_title()
        board.display_board()
        print(f"Replay speed: {replay_speed}\nReplay file: {file}{REPLAY_FILE_FORMAT}\n")

        for player in replay_info['wbr_game_info'][1:]:
            event = player['event']
            player_name = player['player_name']
            player_type = player['type']
            board.player = player_name

            if player_type == "computer":
                player_name = f"{player['player_name']} ({player['difficulty']})"

            if event == 'RESIGNED':
                clear_screen(1.5) # Do not delete!
                board.display_game_title(False, False, True) # Do not delete!
                board.display_board() # Do not delete!
                print(f"Replay speed: {replay_speed}\nReplay file: {file}{REPLAY_FILE_FORMAT}\n") # Do not delete!
                clear_screen(1.5)
                board.display_game_title(False, False, True)
            elif event == 'WON':
                board.winner = player_name
                clear_screen(0)
                board.display_game_title(False, True)
            elif event == 'PLAYING':
                board.turn_counter += 1
                board.selected_path = [tuple(i) for i in player['selected_path']]
                board.place_word(player['word'])
                board.previous_player = player_name
                clear_screen(replay_speed)
                board.display_game_title()
            elif event == 'DRAW':
                board.draw = True
                clear_screen(1)
                board.display_game_title(True)

            board.display_board()
            print(f"Replay speed: {replay_speed}\nReplay file: {file}{REPLAY_FILE_FORMAT}\n")

        print("Replay finished, press any key to continue...")
        msvcrt.getch()

        while True:
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + "Replay menu\n[1] Watch again\n[2] Change speed and watch again\n[3] Open another file\n[4] Go back to main menu\n")

            try:
                selection = int(input((Fore.WHITE + Style.BRIGHT + "Selection: ")))
                if selection == 1:
                    run_replay(replay_info, replay_speed)
                elif selection == 2:
                    clear_screen(0)
                    get_replay_speed(replay_info)
                elif selection == 3:
                    clear_screen(0)
                    open_replay()
                elif selection == 4:
                    main()
                else:
                    pass
            except ValueError:
                pass

    def get_replay_speed(replay_info: dict) -> None:
        """Set how fast each turn cycles."""
        try:
            replay_speed = float(input("Replay speed. Type 0 to go back to main menu: "))
            if replay_speed > 0:
                run_replay(replay_info, replay_speed)
            elif replay_speed == 0:
                main()
            else:
                clear_screen(0)
                get_replay_speed(replay_info)
        except ValueError:
            clear_screen(0)
            get_replay_speed(replay_info)

    while True:
        file = input(Fore.WHITE + Style.BRIGHT + "Filename (Type 0 to go back to main menu): ")

        if file == "0":
            main()
        elif file == "":
            clear_screen(0)
            print(Fore.WHITE + Style.BRIGHT + "Filename (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "filename cannot be empty!")
            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
            msvcrt.getch()
            clear_screen(0)
        else:
            # Create the folder if it does not exist
            try:
                os.makedirs('Replays')
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise

            if os.path.isfile(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}"):
                try:
                    with open(f"{LOCAL_DIR_REPLAYS}{file}{REPLAY_FILE_FORMAT}") as f:
                        bytes_data = f.read().splitlines()
                        data = ast.literal_eval("".join(map(chr, [int(i) for i in bytes_data])))
                        wbr_content = {"wbr_game_info": data}
                        replay_info = json.dumps(wbr_content, indent=7)
                        replay_info = json.loads(replay_info)

                        if replay_info['wbr_game_info'][0]['game_number'] > 0 and replay_info['wbr_game_info'][0]['board_length'] > 0:
                            clear_screen(0)
                            get_replay_speed(replay_info)
                        else:
                            clear_screen(0)
                            print(Fore.WHITE + Style.BRIGHT + "Filename (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "File not found or file extension not supported! Only .wbr (Word Battle Replay) files are supported.")
                            print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
                            msvcrt.getch()
                            clear_screen(0)
                except (KeyError, ValueError, SyntaxError, OverflowError):
                    clear_screen(0)
                    print(Fore.WHITE + Style.BRIGHT + "Filename (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "File is corrupted or outdated and cannot be opened!")
                    print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
                    msvcrt.getch()
                    clear_screen(0)
            else:
                clear_screen(0)
                print(Fore.WHITE + Style.BRIGHT + "Filename (Type 0 to go back to main menu): " + Fore.RED + Style.BRIGHT + "File not found or file extension not supported! Only .wbr (Word Battle Replay) files are supported.")
                print(Fore.WHITE + Style.BRIGHT + "Press any key to continue...")
                msvcrt.getch()
                clear_screen(0)

class Board:
    """Create an board object."""
    def __init__(self) -> None:
        self.length = None # The length of the board
        self.matrix = None # The 2D array of the board
        self.colour_map = None # The colours for each cell
        self.starting_position = None # The current starting position
        self.paths = None # A collection of paths
        self.paths_full = None # A collection of full paths
        self.selected_path = None # The current selected path
        self.players = None # The current player list
        self.player = None # The current player
        self.previous_player = None # the previous player in the previous turn
        self.previous_selected_path = None # the previous path selected by the player
        self.word = None # The current player's word
        self.used_words = None # Record every words used
        self.winner = None # The winner of the current game
        self.draw = False # Draw state
        self.game_counter = 0 # Game counter for each game
        self.turn_counter = 0 # Game counter for each game
        self.game_duration = 0 # Game Duration of the whole game

    def create_board(self, length: int) -> None:
        """Create the game board."""
        self.length = length
        self.matrix = np.full((self.length, self.length), " ", dtype='U1')
        self.colour_map = self.set_colour_map()

    def set_colour_map(self) -> Dict[Tuple[Any], Any]:
        """Ini the colours for the board."""
        cells = [coord for coord in it.product(*[range(r[0], r[1]) for r in zip([0, 0], [self.length, self.length])])]
        colour = ["WHITE"] * self.length ** 2
        return dict(zip(cells, colour))

    def check_draw(self) -> None:
        """Check for a draw."""
        if " " not in self.matrix:
            self.draw = True

    def get_starting_position(self) -> int:
        """Get the starting position of the player."""
        self.display_game_title()
        self.display_board()
        self.check_draw()

        if self.draw:
            return 2

        try:
            # Split the input to get the coordinates
            user_input = [int(n) for n in input(Fore.WHITE + Style.BRIGHT + "Starting Position: ").split(" ")]

            if len(user_input) == 1:
                if 0 not in user_input:
                    clear_screen(0)
                    self.display_game_title()
                    self.display_board()
                    print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "Invalid coordinates!")
                    clear_screen()
                    return self.get_starting_position()
                else:
                    return 0
            else:
                if 0 in user_input:
                    clear_screen(0)
                    self.display_game_title()
                    self.display_board()
                    print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "Invalid coordinates!")
                    clear_screen()
                    return self.get_starting_position()
                else:
                    if 0 < user_input[0] <= self.length and 0 < user_input[1] <= self.length:
                        if user_input[0] == 1 and user_input[1] == user_input[0] or user_input[0] == 1 and user_input[1] > user_input[0] or user_input[1] == 1 and user_input[1] < user_input[0] or user_input[0] == self.length and user_input[1] == user_input[0] or user_input[0] == self.length and user_input[0] > user_input[1] or user_input[1] == self.length and user_input[1] > user_input[0]:
                            self.starting_position = tuple([n - 1 for n in user_input])
                            return 1
                        else:
                            clear_screen(0)
                            self.display_game_title()
                            self.display_board()
                            print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "Invalid coordinates!")
                            clear_screen()
                            return self.get_starting_position()
                    else:
                        clear_screen(0)
                        self.display_game_title()
                        self.display_board()
                        print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "Invalid coordinates!")
                        clear_screen()
                        return self.get_starting_position()
        except (IndexError, ValueError):
            clear_screen(0)
            self.display_game_title()
            self.display_board()
            print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "Invalid coordinates!")
            clear_screen()
            return self.get_starting_position()

    def create_valid_paths(self) -> None:
        """Generate paths based on the starting position. Check the list for paths that are full. Remove them if they are."""
        # Convert the coordinates of the starting position to zero-based numbering
        x = self.starting_position[0]
        y = self.starting_position[1]

        # Create a list of three paths
        path1 = []
        path2 = []
        path3 = []

        # Get coordinates for each path starting at corners
        # Starting position at top left corner
        if (x, y) == (0, 0):
            for i in range(self.length):
                # Path to top right corner
                path1 += [(0, i)]

                # Path to bottom right corner
                path2 += [(i, i)]

                # Path to bottom left corner
                path3 += [(i, 0)]

        # Starting position at top right corner
        elif (x, y) == (0, self.length - 1):
            for i in range(self.length):
                # Path to top left corner
                path1 += [(0, self.length - 1 - i)]

                # Path to bottom left corner
                path2 += [(i, self.length - 1 - i)]

                # Path to bottom right corner
                path3 += [(i, self.length - 1)]

        # Starting position at bottom left corner
        elif (x, y) == (self.length - 1, 0):
            for i in range(self.length):
                # Path to top left corner
                path1 += [(self.length - 1 - i, 0)]

                # Path to top right corner
                path2 += [(self.length - 1 - i, i)]

                # Path to bottom right corner
                path3 += [(self.length - 1, i)]

        # Starting position at bottom right corner
        elif (x, y) == (self.length - 1, self.length - 1):
            for i in range(self.length):

                # Path to top right corner
                path1 += [(i, self.length - 1)]

                # Path to top left corner
                path2 += [(i, i)]

                # Path to bottom left corner
                path3 += [(self.length - 1, i)]

            # Reverse any path that may needs be
            path1.reverse()
            path2.reverse()
            path3.reverse()

        # Get coordinates for each path starting at edges
        else:
            # Starting position at top edge
            if x == 0:
                # Path to left edge
                temp_x = x
                temp_y = y

                while temp_y >= 0:
                    path1 += [(temp_x, temp_y)]
                    temp_x += 1
                    temp_y -= 1

                # Path to bottom edge
                for i in range(self.length):
                    path2 += [(i, y)]

                # Path to right edge
                temp_x = x
                temp_y = y

                while temp_y < self.length:
                    path3 += [(temp_x, temp_y)]
                    temp_x += 1
                    temp_y += 1

            # Starting position at left edge
            elif y == 0:
                # Path to top edge
                temp_x = x
                temp_y = y

                while temp_x >= 0:
                    path1 += [(temp_x, temp_y)]
                    temp_x -= 1
                    temp_y += 1

                # Path to right edge
                for i in range(self.length):
                    path2 += [(x, i)]

                # Path to bottom edge
                temp_x = x
                temp_y = y

                while temp_x < self.length:
                    path3 += [(temp_x, temp_y)]
                    temp_x += 1
                    temp_y += 1

            # Starting position at right edge
            elif y == self.length - 1:
                # Path to top edge
                temp_x = x
                temp_y = y

                while temp_x >= 0:
                    path1 += [(temp_x, temp_y)]
                    temp_x -= 1
                    temp_y -= 1

                # Path to left edge
                for i in range(self.length):
                    path2 += [(x, i)]

                # Path to bottom edge
                temp_x = x
                temp_y = y

                while temp_x < self.length:
                    path3 += [(temp_x, temp_y)]
                    temp_x += 1
                    temp_y -= 1

                # Reverse any path that may needs be
                path2.reverse()

            # case of starting point on the bottom edge
            elif x == self.length - 1:
                # Path to left edge
                temp_x = x
                temp_y = y

                while temp_y >= 0:
                    path1 += [(temp_x, temp_y)]
                    temp_x -= 1
                    temp_y -= 1

                # Path to top edge
                for i in range(self.length):
                    path2 += [(i, y)]

                # Path to right edge
                temp_x = x
                temp_y = y

                while temp_y < self.length:
                    path3 += [(temp_x, temp_y)]
                    temp_x -= 1
                    temp_y += 1

                # Reverse any path that may needs be
                path2.reverse()

        self.paths = [path1, path2, path3]
        self.paths_full = [path1, path2, path3]

        # Create a list of strings for each path
        path1_res = []
        path2_res = []
        path3_res = []

        # Checking if the paths are full if they do not contain an empty string
        for coord in self.paths[0]:
            if " " in self.matrix[coord]:
                path1_res.append(self.matrix[coord])
        for coord in self.paths[1]:
            if " " in self.matrix[coord]:
                path2_res.append(self.matrix[coord])
        for coord in self.paths[2]:
            if " " in self.matrix[coord]:
                path3_res.append(self.matrix[coord])

        try:
            if not path1_res:
                self.paths.pop(0)
            if not path2_res:
                self.paths.pop(-2)
            if not path3_res:
                self.paths.pop(1)
        except IndexError:
            self.paths = []

    def get_selected_path(self) -> int:
        """Get selected path from player"""
        temp_board = np.full((self.length, self.length), " ", dtype='U1')
        temp_colour_map = self.set_colour_map()

        # Labelling each path with its corresponding character and assign each coordinate with its colour
        end_path_numbering = 1

        if not self.paths:
            for path in self.paths_full:
                for coord in path:
                    temp_colour_map[coord] = "RED"
        else:
            for path in self.paths:
                for coord in path:
                    temp_colour_map[coord] = "GREEN"

                    # Labelling the succeeding position with an dot
                    temp_board[coord] = "•"

                # Labelling the end positions with an integer to indicate selection number
                temp_board[path[-1]] = str(end_path_numbering)
                end_path_numbering += 1

        # Assign the first cell with its colour
        temp_colour_map[self.starting_position] = "YELLOW"

        if not self.paths:
            self.display_game_title()
            self.display_board(None, temp_colour_map)
            print(Fore.WHITE + Style.BRIGHT + "Starting Position: " + Fore.RED + Style.BRIGHT + "All available paths are full! Select another starting position!")
            return 2
        else:
            self.display_game_title()
            self.display_board(temp_board, temp_colour_map)

            try:
                # Note: inputs are based on zero-based numbering due to the coordinate system of using zero-based numbering
                user_input = int(input(Fore.WHITE + Style.BRIGHT + "Type path number: "))

                if user_input == 0:
                    return 0
                elif user_input == 4:
                    return 1
                elif 0 < user_input <= len(self.paths):
                    self.selected_path = self.paths[user_input - 1]
                    self.display_selected_path()
                else:
                    clear_screen(0)
                    self.display_game_title()
                    self.display_board(temp_board, temp_colour_map)
                    print(Fore.WHITE + Style.BRIGHT + "Type path number: " + Fore.RED + Style.BRIGHT + "Invalid path number!")
                    clear_screen()
                    return self.get_selected_path()
            except ValueError:
                clear_screen(0)
                self.display_game_title()
                self.display_board(temp_board, temp_colour_map)
                print(Fore.WHITE + Style.BRIGHT + "Type path number: " + Fore.RED + Style.BRIGHT + "Invalid path number!")
                clear_screen()
                return self.get_selected_path()

    def display_selected_path(self, time=0) -> None:
        """Display the selected path."""
        temp_board = np.full((self.length, self.length), " ", dtype='U1')
        temp_colour_map = self.set_colour_map()

        # Labelling each path with its corresponding character and assign each coordinate with its colour
        for coord in self.selected_path:
            if self.matrix[coord] == " ":
                temp_board[coord] = "•"
            else:
                temp_board[coord] = self.matrix[coord]

            temp_colour_map[coord] = "GREEN"

        # Assign the first cell with its colour
        temp_colour_map[self.starting_position] = "YELLOW"

        # Print the board
        clear_screen(time)
        self.display_game_title(False, False, False, True)
        self.display_board(temp_board, temp_colour_map)

    def display_game_title(self, is_draw=False, there_is_winner=False, has_resigned=False, display_used_words=False) -> None:
        """Display the game title."""
        if is_draw:
            print(Fore.WHITE + Style.BRIGHT + " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players]), sep='', end='')
            print(f"\nGame: {self.game_counter} | Turn: {self.turn_counter} | Draw!\nGame {self.game_counter} has ended! | Game Duration: {self.game_duration}")
        elif there_is_winner:
            print(Fore.WHITE + Style.BRIGHT + " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players]), sep='', end='')
            print(f"\nGame: {self.game_counter} | Turn: {self.turn_counter} | {self.winner} won!\nGame {self.game_counter} has ended! | Game Duration: {self.game_duration}")
        elif has_resigned:
            print(Fore.WHITE + Style.BRIGHT + " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players]), sep='', end='')
            print(f"\nGame: {self.game_counter} | Turn: {self.turn_counter} | {self.player}'s Turn")
            print(f"{self.player} has resigned!")
        elif display_used_words:
            print(Fore.WHITE + Style.BRIGHT + " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players]), sep='', end='')
            print(f"\nGame: {self.game_counter} | Turn: {self.turn_counter} | {self.player}'s Turn")

            if self.used_words is not None:
                print(Fore.WHITE + Style.BRIGHT + "Word(s) used: " + Fore.RED + Style.BRIGHT + ', '.join(self.used_words))
            else:
                print(Fore.WHITE + Style.BRIGHT + "Word(s) used:")
        else:
            print(Fore.WHITE + Style.BRIGHT + " VS ".join([f"{i['name']} ({i['difficulty']})" if i['difficulty'] is not None else f"{i['name']}" for i in self.players]), sep='', end='')
            print(f"\nGame: {self.game_counter} | Turn: {self.turn_counter} | {self.player}'s Turn")

            if self.turn_counter == 0:
                print(f"Game {self.game_counter} has started!")
            else:
                print(f"{self.previous_player} placed down {self.word}")

    def display_board(self, board=None, colour_map=None, get_str_board=False, computer_player=False) -> int:
        """Display the board."""
        def chunks(data: Dict[Tuple[int, int], str], SIZE=10000) -> Generator[Dict[Tuple[int, int], str], any, None]:
            """Divide the data into chunks."""
            itt = iter(data)

            for i in range(0, len(data), SIZE):
                yield {k: data[k] for k in it.islice(itt, SIZE)}

        if colour_map is None:
            colour_map = self.colour_map

        if board is None:
            board = self.matrix

        # Colour the previous word placed by the player
        if self.previous_selected_path is not None:
            for key in self.colour_map:
                self.colour_map[key] = "WHITE"

            for coord in self.previous_selected_path:
                self.colour_map[coord] = "CYAN"

                if computer_player:
                    self.colour_map[coord] = "GREEN"

            if computer_player:
                self.colour_map[self.previous_selected_path[0]] = "YELLOW"

        # Create a list of chunks
        chunks_list = []

        # Create chunks of the colour map and store them in the chunks list
        for item in chunks(colour_map, self.length):
            chunks_list.append(item)

        # Display the game board
        if board is None:
            board = self.matrix

        # Create representation of the board
        str_board = Fore.WHITE + Style.BRIGHT + " "
        str_board += "  "

        # Labelling top columns
        for column_number in range(self.length):
            if column_number < 9:
                str_board += f"   {column_number + 1}"
            else:
                str_board += f"  {column_number + 1}"

        str_board +="\n    ┌───┬─"

        for _ in range(self.length - 2):
            str_board+= "──┬─"

        str_board += "──┐\n"

        # Labelling left rows
        lines = 0

        for chunk in chunks_list:
            if chunks_list.index(chunk) < 9:
                str_board += f"  {str(chunks_list.index(chunk) + 1)} "
            else:
                str_board += f" {str(chunks_list.index(chunk) + 1)} "

            # Assign each string to its corresponding colour depending on the coordinates
            for coord, colour in chunk.items():
                set_colour = getattr(Fore, colour)
                str_board += Fore.WHITE + "│" + set_colour + f" {board[coord]} " + Fore.WHITE

            # Labelling right rows
            str_board += f"│ {str(chunks_list.index(chunk) + 1)}\n    ├─"

            for _ in range(self.length - 1):
                str_board += "──┼─"

            if lines < self.length - 1:
                str_board += "──┤\n"
                lines += 1
            else:
                str_board += "\r"

        # Labelling bottom columns
        str_board +="    └───┴─"

        for _ in range(self.length - 2):
            str_board+= "──┴─"

        str_board += "──┘\n   "

        for column_number in range(self.length):
            if column_number < 9:
                str_board += f"   {column_number + 1}"
            else:
                str_board += f"  {column_number + 1}"

        if get_str_board:
            return str_board
        else:
            print(f"\n{str_board}\n")

    def place_word(self, word: str) -> None:
        """Place the word onto the game board."""
        self.word = word
        self.previous_selected_path = self.selected_path

        for coord in self.previous_selected_path:
            self.matrix[coord] = self.word[self.previous_selected_path.index(coord)]

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

        menu_item = ["Check files to find board size", "Display player statistics", "Display letter frequency bar graph", "Display word length frequency bar graph", "Display square usage heatmap", "Watch replays", "View README file", "Exit"]

        for i in menu_item:
            print([menu_item.index(i) + 1], i)

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
            clear_screen(0)
            open_replay()
        elif selection == "7":
            check_if_file_exists('README.txt')
            subprocess.call(['cmd', '/c', 'start', '/max', 'README.txt'])
        elif selection == "7":
            sys.exit(0)


if __name__ == "__main__":
    main()

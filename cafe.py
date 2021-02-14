from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import re

import pandas as pd

"""
Hey there :kissing_heart:

"""

# #############################
# Constants
# #############################


class Constants:
    """
    A class to hold all of the constants we need in the game.
    """
    COMMAND_TABLE_FILE = "command_table.csv"
    TARGET_TABLE_FILE = "target_table.csv"
    SCENE_TABLE_FILE = "scene_table.csv"
    SCENE_TARGET_TABLE_FILE = "scene_target_table.csv"
    FIRST_SCENE = "front"
    INITIAL_FLAG_DICT = {
        "DEFAULT": True,
        "BAGEL_PRESENT": True,
        "AMNIZU_PRESENT": True,
        "NOT_HAS_COIN": True,
        "GLASS_PRESENT": True,
        "APRON_PRESENT": True,
        "LUBE_PRESENT": True,
        "BROOM_PRESENT": True,
        "WAITRESS_PRESENT": True,
        "DOES_NOT_HAVE_APRON": True,
        "COFFEE_PRESENT": True,
        }
    COMMAND_PATTERN = "(\S+)[ ]*(\S*)"
    TABLE_FILE = "valentine.xlsx"
    TARGET_SHEET_NAME = "target"
    SCENE_SHEET_NAME = "scene"
    SCENE_TARGET_SHEET_NAME = "scene_target"
    SCENE_ACTION_SHEET_NAME = "scene_action"
    FUNCTION_SHEET_NAME = "function"
    INTRO_MESSAGE = (
        "Due to the unfortunate layover in Felpoint you and Conor are stuck in Hell this Valentine's day.\n"
        "Still, you are determined to make the best of it, and Conor has found a charming little cafe in the Infernal Markets\n"
        "that the two of you can make plans for how to spend the rest of the day in.\n"
        "Currently they are trying to decipher the tourist brochure, making use of their proficiency in Infernal. As they are \n"
        "otherwise occupied, and the Waitress seems to have been trapped in conversation by an Amnizu for the last half hour\n"
        "you have decided to take it upon yourself to head inside and place your order.\n"
        "You do wonder whether they will accept Euros though...\n"
    )
    WARNING_MISSING_ACTION = "You can't do that! Type \"?\" to see the available actions."
    WARNING_MISSING_TARGET = "There is no such target! Type \"?\" to see the available targets."
    FAILED_COMMAND = "You can't do that!"
    
    FORMAT = {
        # Foreground:
        "purple" :'\033[1;35;48m',
        "cyan" :'\033[1;36;48m',
        "bold" : '\033[1;37;48m',
        "blue" : '\033[1;34;48m',
        "green" : '\033[1;32;48m',
        "yellow" : '\033[1;33;48m',
        "red" : '\033[1;31;48m',
        "black": '\033[1;30;48m',
        "grey": '\033[1;38;2;107;107;107m',
        "cream": '\033[1;38;2;255;253;208m',
        "light_grey":"\033[1;38;2;211;211;211m",
        "light_purple": "\033[1;38;2;177;156;217m",
        "dark_purple": "\033[1;38;2;106;13;173m",
        "orange": "\033[1;38;2;255;165;0m",
        "yellow": "\033[1;38;2;255;255;0m",
        "brown": "\033[1;38;2;150;75;0m",
        "light_brown": "\033[1;38;2;195;155;119m",
        "dark_blue" : "\033[1;38;2;2;7;93m",
        "pink": "\033[1;38;2;255;192;203m",
        "white": "\033[1;38;2;255;255;255m",
        "light_blue": "\033[1;38;2;173;216;230m",
        "dark_grey": "\033[1;38;2;77;78;79m",
        "light_green": "\033[1;38;2;151;251;152m",
        "light_yellow": "\033[1;38;2;255;255;102m",
        "light_pink": "\033[1;38;2;255;192;203m",
        "light_grey": "\033[1;38;2;211;211;211m",
        "blue": "\033[1;38;2;0;0;255m",

        # Formatting
        "bold" : '\033[1m',
        "underline" : '\033[4m',    
        # End colored text
        "end" :'\033[0m',
        "nc" :'\x1b[0m' # No Color
    }

    DEBUG = False

# #############################
# Data
# #############################


@dataclass
class GameData:
    """
    A class to hold the static, unchanging data that describes the game
    """
    target_table: pd.DataFrame
    scene_table: pd.DataFrame
    scene_target_table: pd.DataFrame
    scene_action_table: pd.DataFrame
    function_table: pd.DataFrame

    
@dataclass
class Game:
    """
    A class to hold the game's mutable state
    """
    game_data: GameData
    scene: str
    flag_dict: Dict[str, bool]
    scene_target_dict: Dict[str, Target]
    scene_action_dict: Dict[str, Action]

    
@dataclass
class Target:
    """
    A class to associate the name of a target with the color to format it's name in display.
    """
    name: str
    color: str
 
 
@dataclass
class Action:
    """
    A class to help type which strings correspond to actions
    """
    name: str

    
@dataclass
class Command:
    """
    A class to contain the data necessary to change the game state and display the corresponding message.
    """
    message: str
    new_scene: str
    flag_off: list[str]
    flag_on: list[str]
       
@dataclass
class Scene:
    """
    A class to contain the game scene: a construct mostly used to help organise what functions, actions and targets are available
    """
    name: str
    description: str
    
       
# #############################
# Gt command
# #############################

def parse_player_input(raw_input: str):
    """
    Get the raw player input and use a regex to refine it into a action and target selection.
    
    If the regex fails, return None, None to signal the program that it is not in a valid format
    """
    pattern = Constants.COMMAND_PATTERN
    
    match = re.match(pattern, raw_input)
        
    if match:
        if match.group(2) == "":
            return match.group(1), None
        else: 
            return match.group(1), match.group(2)
        
    else:
        return None, None
    
def warning_missing_action():
    """
    A short function to give a warning if the player tries to use an action that isn't available
    """
    print(Constants.WARNING_MISSING_ACTION)
    
def warning_missing_target():
    """
    A short function to give a warning if the player tries to use a target that isn'tin the scene
    """
    
    print(Constants.WARNING_MISSING_TARGET)
    
def check_flags(row, flag_dict):
    """
    A stubby little function for use with pandas's apply to find whether all the pre-requisite flags for a action/interactable 
    pair being available are met. 
    """
    
    function_flags = row["flag"]
    if Constants.DEBUG: print(f"Function flags are: {function_flags}")
    
    
    if type(function_flags) == str:
    
        function_flags_list = function_flags.split(",")
        for function_flag in function_flags_list:
            if not function_flag in flag_dict:
                return False
            

        # Reaching here implies all flags in dictionary and hence can return True
        return True
    
    else:
        return False
    
def lookup_command(function_table, scene, action, target, flags):
    """
    Lookup whether there is a function corresponding to the action and interactable the player has specified, and find
    what effect it has on the game state if so.
    """
    
    # Get the masks
    scene_mask = function_table["scene"] == scene.name
    action_mask = function_table["action"] == action
    target_mask = function_table["target"] == target
    # flag_mask = function_table["flag"].str.contains("|".join(flags.keys()))
    flag_mask = function_table.apply(lambda x: check_flags(x, flags), axis=1)
    
    # Get the possible functions that agree with the game state
    possible_functions = function_table[scene_mask & action_mask & target_mask & flag_mask]
    
    # Check if there is no match
    if len(possible_functions) == 0:
        return None, None, None, None
    
    # Else get the function with highest presidence 
    else:
        command_info = possible_functions.iloc[0]
        if Constants.DEBUG: print(f"Command info: {command_info}")
        
        text = command_info["text"]
        new_scene = command_info["new_scene"]
        
        if type(command_info["flag_on"]) == str:
            flag_on = command_info["flag_on"].split(",")
        else:
            flag_on = []
            
        if type(command_info["flag_off"]) == str:
            flag_off = command_info["flag_off"].split(",")
        else:
            flag_off = []
        return  text, new_scene, flag_off, flag_on
    
    
def process_help(action_dict, target_dict):
    """
    Tell the player what the current actions they can take are, and what objects in the current scene are interactable.
    """
    
    action_message = "Actions you can currently take are:\n"
    action_message += "?: learn what actions you can take\n"
    action_message += "exit: exit the game\n"
    action_message += "look around: get a description of your enviroment\n"
    for action_name, action in action_dict.items():
        action_message += f"{action_name}\n"
    
    target_message = "Interactables in the area are:\n"
    for target_name, target in target_dict.items():
        target_message += f"{target_name}\n"
    
    message = action_message + "\n" + target_message
    
    return message, None, [], []

def process_quit():
    """
    Exit the game.
    """
    exit()
       
def process_look_around(scene):
    """
    A function to let the player inspect their enviroment.
    """
    
    return scene.description, None, [], []
    
def warming_failed_command():
    """
    If there is no corresponding command, print the failed command message
    """
    print(Constants.FAILED_COMMAND)

       
def get_command(game_data: GameData, scene, flags, action_dict, target_dict):
    """
    One of the main game functions: ask player for input, check that input is valid, and then check whether that input has a 
    corresponding game state change, and if so return it to be handled elsewhere.
    
    Failure to match a known command will cause an error to be printed and loop until a valid one is given.  
    """
    
    while True:
        # Get the raw player input
        raw_input = input(">>> ")
        
        if raw_input == "?":
            message, new_scene, flag_off, flag_on = process_help(action_dict, target_dict)
            
        elif raw_input == "exit":
            process_quit()
            
        elif raw_input == "look around":
            message, new_scene, flag_off, flag_on =process_look_around(scene)
            
        else:
                
            # Parse the player input
            action, target = parse_player_input(raw_input)
            
            # 
            if action not in [action.name for action in action_dict.values()]:
                warning_missing_action()
                continue
            
            #   
            if target is None:
                warning_missing_target()
                continue
            
            # 
            elif target not in [target.name for target in target_dict.values()]:
                warning_missing_target()
                continue
            
            # Lookup the command in the tables
            message, new_scene, flag_off, flag_on = lookup_command(game_data.function_table, scene, action, target, flags)
            
            if message is None:
                warming_failed_command()
                continue
            
        # Make a command object
        command = Command(message, new_scene, flag_off, flag_on)
        if Constants.DEBUG: print(command)
        
        return command
 
# #############################
# Apply command
# #############################
def get_new_flags(command: Command, flags: Dict[str, bool]):
    """
    A small function to get all the of new flags that result from a command that changes the game flags.
    """
    
    new_flags = {}
    
    for flag in flags:
        new_flags[flag] = True
    
    for flag in command.flag_off:
        if flag in new_flags:
            del new_flags[flag]

    for flag in command.flag_on:
        new_flags[flag] = True        
        
    return new_flags


def get_actions(scene_action_table, scene, flags):
    """
    A function to get the actions available to a player in any given scene, for use in determining input validity and 
    giving help on what actions are available.
    """
    scene_mask = scene_action_table["scene"] == scene.name
    flags_mask = scene_action_table["flag"].str.contains("|".join(flags.keys()))

    scene_action_filtered_table = scene_action_table[scene_mask & flags_mask]    

    
    actions = {
        action["action"]: Action(action["action"]) 
        for index, action 
        in scene_action_filtered_table.iterrows()
    }
    
    return actions


def get_targets(scene_target_table, target_table, scene: Scene, flags):
    """
    A function to get the targets available to a player in any givens scene, for use in determining player input
    validity and giving help
    """
    
    scene_mask = scene_target_table["scene"] == scene.name
    flags_mask = scene_target_table["flag"].str.contains("|".join(flags.keys()))
    
    scene_target_filtered_table = scene_target_table[scene_mask & flags_mask]    
    targets = {}
    for index, target_data in scene_target_filtered_table.iterrows():
        if Constants.DEBUG: print(f"Taget data: {target_data}")
        target_mask = target_table["target"] == target_data["target"]

        target_table_filtered = target_table[target_mask]
        target = target_table_filtered.iloc[0]
    
        targets[target["target"]] = Target(target["target"], target["color"]) 
    
    return targets


def get_scene(scene_table: GameData, scene_name: str) -> Scene:
    """
    A short function to get the scene associated with a name - used to change the scene. 
    """
    scene_data = scene_table[scene_table["scene"] == scene_name].iloc[0]

    scene: Scene = Scene(scene_data["scene"], scene_data["description"])
    
    return scene

    
def apply_command(command: Command, game: Game):
    """
    One of the main game functions. Creates a new object representing the game state that results from a command being applied.
    """
    if Constants.DEBUG: print(game.flag_dict)
    new_flags = get_new_flags(command, game.flag_dict)
    if Constants.DEBUG: print(new_flags)
    
    if type(command.new_scene) == str:
        new_scene = get_scene(game.game_data.scene_table, command.new_scene)
    else:
        new_scene = game.scene
    
    new_actions = get_actions(game.game_data.scene_action_table, new_scene, new_flags,)
    
    new_targets = get_targets(game.game_data.scene_target_table, game.game_data.target_table, new_scene, new_flags,)
    
    new_game = Game(
        game.game_data,
        new_scene,
        new_flags,
        new_targets,
        new_actions,
    )
    
    return new_game
    

# #############################
# Display
# #############################

def color_target_names(target_dict, message):
    """
    A function to automatically color any reference to a target in the text by using find replace.
    """
    
    formatted_message = message
    for target_name, target in target_dict.items():
        if Constants.DEBUG: print([target_name, target.color])
        color = Constants.FORMAT[target.color]
        end_color = Constants.FORMAT["end"]
        formatted_message = formatted_message.replace(target.name, color+target.name+end_color)
        
    return formatted_message
        

def display(target_dict, message: str):
    """
    One of the main game functions. Takes the message associated with a command and formats it for pretty printing.
    
    """
    
    message = color_target_names(target_dict, message)
    
    print(message)

# #############################
# Main
# #############################


def main():
    """
    The game main function. 
    This will:
     - read in all the data from an excel sheet
     - setup the initial game state
     - Create a game data object
     - Display the introduction
     - Start the game loop
     
    The game loop:
     - Processes player input into a valid change in game state
     - Applies that change in state
     - Displays the player facing outpu corresponding to that change
    
    """
    # Get the game data from the excel sheet
    target_table = pd.read_excel(Constants.TABLE_FILE, Constants.TARGET_SHEET_NAME, dtype=str)  # pd.read_csv(Constants.TARGET_TABLE_FILE)
    scene_table = pd.read_excel(Constants.TABLE_FILE, Constants.SCENE_SHEET_NAME, dtype=str)  # pd.read_csv(Constants.SCENE_TABLE_FILE)
    scene_target_table = pd.read_excel(Constants.TABLE_FILE, Constants.SCENE_TARGET_SHEET_NAME, dtype=str)  # pd.read_csv(Constants.SCENE_TARGET_TABLE_FILE)
    scene_action_table = pd.read_excel(Constants.TABLE_FILE, Constants.SCENE_ACTION_SHEET_NAME, dtype=str) # pd.read_csv(Constants.SCENE_ACTION_TABLE_FILE)
    function_table = pd.read_excel(Constants.TABLE_FILE, Constants.FUNCTION_SHEET_NAME, dtype=str)  # pd.read_csv(Constants.FUNCTION_TABLE_FILE)
    
    game_data = GameData(
        target_table,
        scene_table,
        scene_target_table,
        scene_action_table,
        function_table
    )

    # Get the initial scene
    initial_scene = get_scene(
        game_data.scene_table,
        Constants.FIRST_SCENE, 
        )

    # Get the intial targets and actions
    scene_target_dict = get_targets(game_data.scene_target_table, game_data.target_table, initial_scene, Constants.INITIAL_FLAG_DICT)
    scene_action_dict = get_actions(game_data.scene_action_table, initial_scene, Constants.INITIAL_FLAG_DICT)

    
    # Make the game object
    game: Game = Game(
        game_data,
        initial_scene,
        Constants.INITIAL_FLAG_DICT,
        scene_target_dict,
        scene_action_dict,
    )
    
    # Display the game introduction text    
    display(game.scene_target_dict, Constants.INTRO_MESSAGE)
    
    while True:
            
        # Request input from the player and parse it to a command for the game
        command = get_command(game.game_data, game.scene, game.flag_dict, game.scene_action_dict, game.scene_target_dict)
        
        # Update the scene and flags 
        game = apply_command(command, game)
    
        # Display the game message
        display(game.scene_target_dict, command.message)

if __name__ == "__main__":
    main()
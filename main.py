#
#                                     JSON CompileCommand Formatter v0.1
#   This script aim to split the "command" tag in the compile_commands.json file into an "arguments" array
#                   Copyright 2023 Geoffrey Côte - geoffrey.cote@centraliens-nantes.org
import os
import json

padding = lambda text, max_width: (max_width-len(text))//2


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


CONSOLE_WIDTH    = 80
SCRIPT_TITLE     = "JSON CompileCommand Formatter"
SCRIPT_COPYRIGHT = "v0.1 | Geoffrey Côte 2023"
print(bcolors.HEADER+"="*CONSOLE_WIDTH)
print(" "*padding(SCRIPT_TITLE, CONSOLE_WIDTH)+SCRIPT_TITLE)
print(" "*padding(SCRIPT_COPYRIGHT, CONSOLE_WIDTH)+SCRIPT_COPYRIGHT)
print("="*CONSOLE_WIDTH+bcolors.ENDC)


c_wd = os.getcwd()
print(f"Current working directory {bcolors.BOLD+c_wd+bcolors.ENDC}", end="\n\n")


# Checking workspace
def check(what: str, msg: str, condition, error: str) -> None:
    print(f"{bcolors.BOLD+bcolors.UNDERLINE+msg} :{bcolors.ENDC} ", end="")
    if not condition(what):
        print(f"{bcolors.FAIL}X{bcolors.ENDC} ({error})")
        exit(0)
    print(f"{bcolors.OKGREEN}V{bcolors.ENDC}")

file_exist = lambda file: os.path.exists(file)
check("./build", "Checking if is ROS2 Workspace", file_exist, "./build dir does not exist")
check("./build/compile_commands.json", "Checking if compile_commands.json is present", file_exist, "File not present")

with open("./build/compile_commands.json", "r") as h:
    print(f"{bcolors.BOLD + bcolors.UNDERLINE}Trying to decode the JSON :{bcolors.ENDC} ", end="")
    try:
        json_data = h.read()
        decoder = json.JSONDecoder()
        json_dict = decoder.decode(json_data)
        print(f"{bcolors.OKGREEN}V{bcolors.ENDC}")
    except json.JSONDecodeError as err:
        print(f"{bcolors.FAIL}X{bcolors.ENDC} ({err.__traceback__})")
        exit(-1)
    h.close()
    h = open("./build/compile_commands.json", "w")
    out_dict = []
    for item in json_dict:
        item_dict = {}
        for (key, value) in item.items():
            if key != "command":
                item_dict[key] = value
            else:
                item_dict["arguments"] = value.split()
        out_dict.append(item_dict)
    encoder = json.JSONEncoder(indent=4)
    h.write(encoder.encode(out_dict))
    h.close()
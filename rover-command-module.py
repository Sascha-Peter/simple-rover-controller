#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file contains the logic for the rover command module

author: Sascha Peter <sascha.o.peter@gmail.com>
version: 0.1.0-alpha
since: 2015-11-17
"""

import asyncio
import json
import random
import string
from io import StringIO

# Memo to myself: ensure_future() is async() in python33


@asyncio.coroutine
def read_command_file(command_file):
    """This coroutine reads the command file and decodes the json into python
    objects
    """
    with open(command_file, 'r+') as input_file:
        string_buffer = StringIO(input_file.read())
        song_library = json.loads(string_buffer.getvalue())
    return song_library


@asyncio.coroutine
def is_creation_command(command):
    """Checks if the command is a create_rover command, returns True if it is,
    else False
    """
    print(command['command'])
    if command['command'] == "new-rover":
        return True
    else:
        return False


@asyncio.coroutine
def calculate_moves_home(position, orientation):
    fuel_x = abs(int(position['x']))
    fuel_y = abs(int(position['y']))
    fuel_orientation = 0
    if fuel_x + fuel_y != 0:
        if fuel_x > 0:
            if orientation == 'east' or orientation == 'west':
                fuel_orientation += 1
        if fuel_y > 0:
            if orientation == 'north' or orientation == 'south':
                fuel_orientation += 1
    else:
        fuel_orientation = 0
    fuel_consumption = fuel_x + fuel_y + fuel_orientation
    return fuel_consumption


@asyncio.coroutine
def create_rover(position):
    rover_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))
    rover_data = {'rover_id': rover_id,
                  'orientation': 'north', 'fuel': 20, 'position': position}
    rover_file_name = None
    with open('rover-%s.json' % rover_id, 'w') as rover_file:
        json.dump(rover_data, rover_file)
        rover_file_name = rover_file
    return rover_file_name.name


@asyncio.coroutine
def execute_command(command, rover_data):
    """This method executes the command and updates the rover data
    accordingly. Returning the updated rover data int he end.
    """
    if "turn" in command['command']:
        print(command['command'])
    elif "move" in command['command']:
        print(command['command'])
    else:
        return "invalid command"


@asyncio.coroutine
def main_logic():
    """Main logic controller which reads, analyzes and executes the commands"""
    is_initialized = False
    result = yield from read_command_file('command-file.json')
    fuel_home = 0
    rover = None
    print(result)
    for command in result:
        print(command['command'])
        if is_creation_command(command):
            print("creation command")
            if is_initialized:
                return "Only one rover at a time"
            else:
                is_initialized = True
                moves_home = yield from calculate_moves_home(command['position'], "north")
                rover = yield from create_rover(command['position'])
                print(rover)
                continue
        else:
            print("not a creation command")
            moves_home = yield from calculate_moves_home(command['position'], "north")
            if rover:
                rover = yield from read_rover_file()
                with open(rover, 'rw') as active_rover:
                    string_buffer = StringIO(active_rover.read())
                    rover_data = json.loads(string_buffer.getvalue())
                    if moves_home < rover_data['fuel'] + 1:
                        # fuel + 1 to ensure one fuel bit is reserved for turning
                        yield from execute_command(command, rover_data)
                    elif moves == rover_data['fuel'] + 1:
                        # fuel + 1 for same reason again
                        return "Rover needs to go home now and can't move anymore"
                    else:
                        return "This rover is out of fuel and doomed."


loop = asyncio.get_event_loop()
loop.run_until_complete(main_logic())
loop.close()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file contains the logic for the rover command module

author: Sascha Peter <sascha.o.peter@gmail.com>
version: 0.1.0-alpha
since: 2015-11-17
"""

import asyncio
import json
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
def main_logic():
    """Main logic controller which reads, analyzes and executes the commands"""
    is_initialized = False
    result = yield from read_command_file('command-file.json')
    for command in result:
        if is_creation_command(command):
            if is_initialized:
                return "Only one rover at a time"
            else:
                is_initialized = True
        else:
            fuel_home = yield from calculate_moves_home(command['position'], "north")
        


loop = asyncio.get_event_loop()
loop.run_until_complete(main_logic())
loop.close()

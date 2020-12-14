#!/usr/bin/env python3

# TODO:
# - Add color

import os
import re
import sys
import click
import curses
from lib.Env import Env
from lib.Display import Display

# Disables curses
DEBUG = False

# Color key to curses pair number
COLOR_MAP = {
	'INFO': 1, # Cyan on black
	'WARN': 2, # Yellow on black
	'ERROR': 3, # Red on black
	'SUCCESS': 4, # Green on black
}

@click.command()
@click.option('-d', '--display', required=True, help='The display format to use (plain, json or a j2 template)')
@click.option('-f', '--filter', nargs=2, multiple=True, type=str, help='Key value filters from the config')
def main(display, filter):
	filters = { f[0]: f[1] for f in filter }
	env = Env(filters)

	if not DEBUG:
		# Set up screen
		screen = curses.initscr()
		screen.keypad(True)
		curses.noecho()
		curses.start_color()

		curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
		curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
		curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
		curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

		# Run
		err = None
		try:
			start(screen, env, display)
		except Exception as e:
			err = e
		finally:
			screen.keypad(False)
			curses.endwin()

		# Re-raise the error after curses is done
		if err:
			raise err

# Start the app
def start(screen, env, display_format):
	display = Display(display_format)
	current = env.next()

	total_pages = len(env.loaded)
	while True:
		screen.clear()
		screen.addstr("Controls:\nUse the left and right arrows to paginate, press 'q' to quit\n\n")

		current_page = env.index + 1
		screen.addstr(f'{current_page} / {total_pages}\n')

		# Output line by line so we can handle any color modifiers
		lines = display.build(current)
		for line in lines.split("\n"):
			if match := re.search('^!!\[(\w+)\]', line):
				line = re.sub('^!!\[\w+\]', '', line)
				color_pair = curses.color_pair(COLOR_MAP.get(match.group(1), 0))
				screen.addstr(line + "\n", color_pair)
			else:
				screen.addstr(line + "\n")

		# screen.addstr(display.build(current))
		screen.addstr("\n")
		screen.refresh()

		pressed = screen.getch()

		if pressed == curses.KEY_LEFT:
			current = env.prev()
		
		if pressed == curses.KEY_RIGHT:
			current = env.next()

		if pressed == ord('q'):
			break

	screen.addstr("Done, press enter to exit")
	screen.getch()

if __name__ == '__main__':
	# pylint: disable=no-value-for-parameter
	main()

#!/usr/bin/env python3

# TODO:
# - Add color

import os
import sys
import click
import curses
from lib.Env import Env
from lib.Display import Display

# Disables curses
DEBUG = False

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
		screen.addstr(display.build(current))
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

import os
import sys
import tty
import termios
import random
from maps_functions import *

COLOURS = {'X': '\x1b[0;31;41m'+'X'+'\x1b[0m', 'G': '\x1b[0;32;42m'+'G'+'\x1b[0m', 'N': '\x1b[0;34;44m'+'N'+'\x1b[0m'}
BLOCKERS = [COLOURS['X'], COLOURS['G'], COLOURS['N']]
board = []
mines = []





def calc_neighbours(board, x, y, distance=1):
    """calculating and set to list all board cells in given distance (default 1) from x, y"""
    neighbours = []
    for delta_y in range(-distance, distance + 1):
        for delta_x in range(-distance, distance + 1):
            if y + delta_y in range(len(board)) and x + delta_x in range(len(board[0])):
                neighbours.append((x + delta_x, y + delta_y))
    return neighbours


def show_neighbours(neighbours):
    """showing on board all hidden objects in distance
       (calculated by calc_neighbours) of player's position. return board"""
    global mines
    global board
    for (x, y) in neighbours:
        if (x, y) in mines:
            board[y][x] = "X"
    return board


def insert_player(x, y, detector=False):
    """inserting player on board on given position. in future, it may get players atributes, to diverse result"""
    global COLOURS
    global board
    if detector:
        see_distance = 5
    else:
        see_distance = 1
    hide_mines()
    neighbours = calc_neighbours(board, x, y, see_distance)
    show_neighbours(neighbours)
    board[y][x] = "@"
    return board


def getch():
    """read users input without pressing 'return'. returns one (first) char of input"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch.lower()


def move(x, y):
    """moving player basing on previous position on board, using getch()"""
    global BLOCKERS
    global board
    key = getch()
    board[y][x] = " "
    if key == "a" and board[y][x-1] not in BLOCKERS:
        x -= 1
    elif key == "d" and board[y][x+1] not in BLOCKERS:
        x += 1
    elif key == "w" and board[y-1][x] not in BLOCKERS:
        y -= 1
    elif key == "s" and board[y+1][x] not in BLOCKERS:
        y += 1
    elif key == "m":
        sys.exit()
    else:
        pass
    return x, y


def main():
    global mines
    global board
    height, width = 39, 100
    board = import_map('map1.txt')
    mines = put_mines(20)
    pos = 36, 13
    insert_player(pos[0], pos[1])
    print_board()
    while True:
        pos = move(pos[0], pos[1])
        insert_player(pos[0], pos[1])
        print_board()


if __name__ == '__main__':
    main()

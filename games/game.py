import random
import numpy as np


class Game:
    __commands = ['up', 'down', 'left', 'right']

    def __init__(self, f=np.array([[0, 0, 0, 0] for _ in range(4)])):
        self.__field = f
        self.__score = 0

    def __str__(self):
        return str(self.__field)

    def get_field(self):
        return self.__field

    # Function for adding a number to the empty cell in the field
    def __add_one(self) -> bool:
        # List for empty cells
        empty = []

        # Go through all the cells
        for i, row in enumerate(self.__field):
            for j, cell in enumerate(row):
                # Find empty and add it to the empty list
                if cell == 0:
                    empty.append((i, j))

        # End of the game because nowhere to insert a digit
        if not empty:
            return False

        rand_empty = random.choice(empty)

        if random.random() > 0.2:
            self.__field[rand_empty[0]][rand_empty[1]] = 2
            self.__score = self.__score + 2
        else:
            self.__field[rand_empty[0]][rand_empty[1]] = 4
            self.__score = self.__score + 4

        return True

    # Function for sliding the list in a certain direction and adding same close numbers
    def __move(self, row: list, where: str) -> list:

        if where in ['down', 'right']:
            z = 2
            while z >= 0:

                if row[z] == 0 or z == 3:

                    z -= 1

                elif row[z] > 0:

                    if row[z + 1] == 0:

                        row[z + 1] = row[z]
                        row[z] = 0
                        z += 1

                    elif row[z] == row[z + 1]:

                        row[z + 1] = row[z] * 2
                        self.__score = self.__score + row[z]
                        row[z] = 0
                        z += 1

                    else:
                        z -= 1
        elif where in ['up', 'left']:

            z = 1
            while z <= 3:

                if row[z] == 0 or z == 0:

                    z += 1

                elif row[z] > 0:

                    if row[z - 1] == 0:

                        row[z - 1] = row[z]
                        row[z] = 0
                        z -= 1

                    elif row[z] == row[z - 1]:

                        row[z - 1] = row[z] * 2
                        self.__score = self.__score + row[z]
                        row[z] = 0
                        z -= 1

                    else:
                        z += 1

        return row

    # matrix transform depend on direction
    def __transform_and_move(self, where: str) -> tuple[bool, int]:

        if where in ['up', 'down']:

            t_list = self.__field.T

            for i, l in enumerate(t_list):
                t_list[i] = self.__move(l, where)
            self.__field = t_list.T

        elif where in ['left', 'right']:

            t_list = self.__field

            for i, l in enumerate(t_list):
                t_list[i] = self.__move(l, where)

            self.__field = t_list
        # Adding a new number
        if not self.__add_one():
            return self.__game_over()
        else:
            return True, self.__score

    def __game_over(self) -> bool and int:
        print('Game Over')
        return False, self.__score

    # Commands: Start,EndGame,Up,Down,Left,Right
    # Returns True or False depending on the ability to add a number to game field
    # and score
    def input_command(self, command: str) -> tuple[bool, int]:

        if self.__score == 0 and command == 'start':
            return self.__add_one(), self.__score
        if self.__score != 0 and command in self.__commands:
            return self.__transform_and_move(command)
        if command == 'endgame':
            return self.__game_over()

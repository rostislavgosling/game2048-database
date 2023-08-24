from games import Game
import sqlite3 as sq
from datetime import datetime
import tkinter as tk


def game_commands(text, game, r):

    game_con, cur_score = gm.input_command(text)
    print(game)
    print(f'Score:{cur_score}')
    if not game_con:
        add_game(cur_score, user_cur_id)
        r.destroy()

# Create a database with users and games
def db_create():
    with sq.connect('GU_DB.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users
                    (user_id INTEGER PRIMARY KEY,
                    nickname TEXT NOT NULL UNIQUE,
                    max_score INTEGER DEFAULT 0
                    )""")
        cur.execute("""CREATE TABLE IF NOT EXISTS games
                            (games_id INTEGER PRIMARY KEY,
                            user_id INTEGER,
                            score INTEGER DEFAULT 0,
                            datetime TEXT NOT NULL
                            )""")


def add_user(username):
    with sq.connect('GU_DB.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT nickname FROM users")
        exist = False

        for u in cur.fetchall():
            if u[0] == username:
                exist = True

        if not exist:
            cur.execute(f"""INSERT INTO users(nickname) VALUES ('{username}')
            """)

        cur.execute(f"SELECT user_id FROM users WHERE nickname == '{username}'")
        user = cur.fetchone()[0]
    return int(user)


def add_game(score: int, user_id: int):
    game_time = datetime.strftime(datetime.now(), '%m/%d/%y %H:%M:%S')
    with sq.connect('GU_DB.db') as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO games(user_id, score, datetime) 
                    VALUES ({user_id},{score},'{game_time}')""")
    print('Thanks for a game')


def write_max_score(user_id):
    with sq.connect('GU_DB.db') as con:
        cur = con.cursor()
        cur.execute(f"""UPDATE users SET max_score = (SELECT MAX(score) 
        FROM games WHERE user_id == {user_id})
        WHERE user_id == {user_id}""")
    print('Max score is written')


if __name__ == '__main__':

    db_create()

    print("Welcome to the game\n Please enter your nickname:")

    nick = input()
    user_cur_id = add_user(nick)
    gm = Game()

    print('If you want to start enter "Start" if not enter "EndGame"')

    root = tk.Tk()
    root.title("Button Interface")

    button_names = ["up", "down", "left", "right", "Start", "EndGame"]

    for i, button_text in enumerate(button_names):

        button = tk.Button(root, text=button_text, command=lambda text=button_text: game_commands(text, gm, root))
        button.grid(row=i // 2, column=i % 2, padx=10, pady=10)

    root.mainloop()

    write_max_score(user_cur_id)

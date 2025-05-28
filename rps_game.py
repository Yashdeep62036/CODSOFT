import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

MAX_PLAYERS = 10
REGISTRATION_TIME = 40
CHOICES = ["Rock", "Paper", "Scissors"]

players = []
player_scores = {}
computer_scores = {}
current_player_index = 0

root = tk.Tk()
root.title("Rock Paper Scissors Game")
root.geometry("800x600")
root.configure(bg="#1e1e1e")

registration_frame = tk.Frame(root, bg="#1e1e1e")
registration_frame.pack(expand=True)

tk.Label(registration_frame, text="Enter Player Name:", font=("Arial", 16), fg="white", bg="#1e1e1e").pack(pady=10)
name_entry = tk.Entry(registration_frame, font=("Arial", 16))
name_entry.pack(pady=5)

tk.Label(registration_frame, text="Players:", font=("Arial", 16), fg="white", bg="#1e1e1e").pack(pady=10)
player_listbox = tk.Listbox(registration_frame, font=("Arial", 14), width=30)
player_listbox.pack(pady=5)

timer_label = tk.Label(registration_frame, text=f"Time Left: {REGISTRATION_TIME}", font=("Arial", 16), fg="red", bg="#1e1e1e")
timer_label.pack(pady=20)

def update_timer():
    for i in range(REGISTRATION_TIME, 0, -1):
        timer_label.config(text=f"Time Left: {i}")
        time.sleep(1)
    start_game()

def add_player():
    name = name_entry.get().strip()
    if not name:
        return
    if name in players:
        messagebox.showwarning("Duplicate Name", "This name is already registered.")
    elif len(players) >= MAX_PLAYERS:
        messagebox.showwarning("Limit Reached", "Maximum number of players reached.")
    else:
        players.append(name)
        player_scores[name] = 0
        computer_scores[name] = 0
        player_listbox.insert(tk.END, name)
        name_entry.delete(0, tk.END)

def start_game():
    if len(players) == 0:
        messagebox.showerror("No Players", "At least 1 player is required to start the game.")
        return
    registration_frame.pack_forget()
    play_game()

tk.Button(registration_frame, text="Add Player", font=("Arial", 14), command=add_player).pack(pady=10)
tk.Button(registration_frame, text="Start Game Now", font=("Arial", 14), command=start_game).pack(pady=10)

timer_thread = threading.Thread(target=update_timer, daemon=True)
timer_thread.start()

def play_game():
    global current_player_index
    game_frame = tk.Frame(root, bg="#1e1e1e")
    game_frame.pack(expand=True)

    current_label = tk.Label(game_frame, text="", font=("Arial", 18), fg="cyan", bg="#1e1e1e")
    current_label.pack(pady=20)

    result_label = tk.Label(game_frame, text="", font=("Arial", 20), fg="white", bg="#1e1e1e")
    result_label.pack(pady=20)

    def update_turn():
        player = players[current_player_index]
        current_label.config(text=f"{player}'s Turn: Choose Rock, Paper, or Scissors")
        result_label.config(text="")

    def player_choice(player_move):
        global current_player_index
        computer_move = random.choice(CHOICES)
        player = players[current_player_index]

        if player_move == computer_move:
            result = f"Tie! Both chose {player_move}"
        elif (player_move == "Rock" and computer_move == "Scissors") or \
             (player_move == "Paper" and computer_move == "Rock") or \
             (player_move == "Scissors" and computer_move == "Paper"):
            result = f"{player} Wins! {player_move} beats {computer_move}"
            player_scores[player] += 1
        else:
            result = f"Computer Wins! {computer_move} beats {player_move}"
            computer_scores[player] += 1

        result_label.config(text=result)
        current_player_index += 1

        if current_player_index < len(players):
            root.after(2000, update_turn)
        else:
            root.after(2000, lambda: show_scores(game_frame))

    btn_frame = tk.Frame(game_frame, bg="#1e1e1e")
    btn_frame.pack(pady=20)

    for choice in CHOICES:
        tk.Button(btn_frame, text=choice, font=("Arial", 16), width=10,
                  command=lambda c=choice: player_choice(c)).pack(side=tk.LEFT, padx=10)

    update_turn()

def show_scores(game_frame):
    game_frame.destroy()
    score_frame = tk.Frame(root, bg="#1e1e1e")
    score_frame.pack(expand=True)

    tk.Label(score_frame, text="🎉 Final Scores 🎉", font=("Arial", 24), fg="lime", bg="#1e1e1e").pack(pady=20)

    for player in players:
        score_text = f"{player} - You: {player_scores[player]} | Computer: {computer_scores[player]}"
        tk.Label(score_frame, text=score_text, font=("Arial", 16), fg="white", bg="#1e1e1e").pack(pady=5)

    tk.Button(score_frame, text="Exit", font=("Arial", 14), command=root.quit).pack(pady=20)

root.mainloop()

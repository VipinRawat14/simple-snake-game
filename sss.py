import tkinter as tk
import random
from tkinter import messagebox

# ---------- SETTINGS ----------
WIDTH = 800
HEIGHT = 600
SPACE_SIZE = 20
SPEED = 100

# ---------- WINDOW ----------
root = tk.Tk()
root.title("Snake Game")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

score = 0
high_score = 0
direction = "Right"

score_label = tk.Label(root, text="Score: 0   High Score: 0", font=("Arial", 14))
score_label.pack()

# ---------- GAME DATA ----------
snake_body = []
snake_squares = []
food_position = ()
running = True

# ---------- FUNCTIONS ----------

def update_score():
    score_label.config(text=f"Score: {score}   High Score: {high_score}")

def create_snake():
    for x, y in snake_body:
        square = canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill="green"
        )
        snake_squares.append(square)

def create_food():
    global food_position
    x = random.randrange(0, WIDTH, SPACE_SIZE)
    y = random.randrange(0, HEIGHT, SPACE_SIZE)
    food_position = (x, y)
    canvas.create_oval(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill="red", tag="food"
    )

def move_snake():
    global score, high_score, running

    if not running:
        return

    x, y = snake_body[0]

    if direction == "Up":
        y -= SPACE_SIZE
    elif direction == "Down":
        y += SPACE_SIZE
    elif direction == "Left":
        x -= SPACE_SIZE
    elif direction == "Right":
        x += SPACE_SIZE

    new_head = (x, y)
    snake_body.insert(0, new_head)

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill="green"
    )
    snake_squares.insert(0, square)

    if new_head == food_position:
        score += 1
        high_score = max(high_score, score)
        update_score()
        canvas.delete("food")
        create_food()
    else:
        snake_body.pop()
        canvas.delete(snake_squares.pop())

    if check_collision():
        game_over()
        return

    root.after(SPEED, move_snake)

def check_collision():
    x, y = snake_body[0]

    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True

    if snake_body[0] in snake_body[1:]:
        return True

    return False

def change_direction(new_direction):
    global direction
    opposite = {
        "Up": "Down",
        "Down": "Up",
        "Left": "Right",
        "Right": "Left"
    }
    if new_direction != opposite[direction]:
        direction = new_direction

def game_over():
    global running
    running = False

    answer = messagebox.askyesno(
        "Game Over",
        f"Game Over!\nScore: {score}\nHigh Score: {high_score}\n\nPlay again?"
    )

    if answer:
        restart_game()
    else:
        root.quit()

def restart_game():
    global snake_body, snake_squares, score, direction, running

    canvas.delete("all")
    score = 0
    direction = "Right"
    running = True

    snake_body = [(100, 100), (80, 100), (60, 100)]
    snake_squares = []

    update_score()
    create_snake()
    create_food()
    move_snake()

# ---------- CONTROLS ----------
root.bind("<Up>", lambda e: change_direction("Up"))
root.bind("<Down>", lambda e: change_direction("Down"))
root.bind("<Left>", lambda e: change_direction("Left"))
root.bind("<Right>", lambda e: change_direction("Right"))

# ---------- START ----------
restart_game()
root.mainloop()

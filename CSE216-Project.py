import turtle
import random
import time
import tkinter as tk

# Global Variables
snake = None
fruit = None
old_fruit = []
scoring = None
screen = None
score = 0
delay = 0.1
difficulty = "Medium"
paused = False
pause_message = None

# Start the game and show difficulty selection
def start_game():
    root.withdraw()
    show_difficulty_screen()

# Show difficulty selection screen
def show_difficulty_screen():
    difficulty_window = tk.Toplevel()
    difficulty_window.title("Select Difficulty")
    difficulty_window.geometry("400x300")
    difficulty_window.configure(bg="lightblue")

    label = tk.Label(difficulty_window, text="Select Difficulty Level", font=("Courier", 18, "bold"), bg="lightblue")
    label.pack(pady=20)

    tk.Button(difficulty_window, text="Easy", command=lambda: set_difficulty("Easy", difficulty_window), width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2).pack(pady=10)
    tk.Button(difficulty_window, text="Medium", command=lambda: set_difficulty("Medium", difficulty_window), width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2).pack(pady=10)
    tk.Button(difficulty_window, text="Hard", command=lambda: set_difficulty("Hard", difficulty_window), width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2).pack(pady=10)

# Set the difficulty and start the game
def set_difficulty(level, window):
    global difficulty, delay
    difficulty = level
    window.destroy()
    delay = {"Easy": 0.15, "Medium": 0.1, "Hard": 0.05}.get(difficulty, 0.1)
    start_game_with_difficulty()

# Initialize the game elements based on difficulty
def start_game_with_difficulty():
    global snake, fruit, old_fruit, scoring, screen, score, delay, paused, pause_message

    screen = turtle.Screen()
    screen.title('SNAKE GAME')
    screen.setup(width=700, height=700)
    screen.bgcolor('turquoise')
    screen.tracer(0)

    create_border()
    score = 0
    initialize_snake()
    initialize_fruit()
    old_fruit = []
    initialize_scoring()

    pause_message = turtle.Turtle()
    pause_message.speed(0)
    pause_message.hideturtle()

    screen.listen()
    screen.onkeypress(snake_go_up, "Up")
    screen.onkeypress(snake_go_down, "Down")
    screen.onkeypress(snake_go_left, "Left")
    screen.onkeypress(snake_go_right, "Right")
    screen.onkeypress(toggle_pause, "space")

    game_loop()

# Create the game border
def create_border():
    border = turtle.Turtle()
    border.speed(5)
    border.pensize(4)
    border.penup()
    border.goto(-310, 250)
    border.pendown()
    border.color('black')
    for _ in range(2):
        border.forward(600)
        border.right(90)
        border.forward(500)
        border.right(90)
    border.penup()
    border.hideturtle()

# Initialize the snake
def initialize_snake():
    global snake
    snake = turtle.Turtle()
    snake.speed(0)
    snake.shape('square')
    snake.color("black")
    snake.penup()
    snake.goto(0, 0)
    snake.direction = 'stop'

# Initialize the fruit
def initialize_fruit():
    global fruit
    fruit = turtle.Turtle()
    fruit.speed(0)
    fruit.shape('circle')
    fruit.color('red')
    fruit.penup()
    fruit.goto(30, 30)

# Initialize the scoring display
def initialize_scoring():
    global scoring
    scoring = turtle.Turtle()
    scoring.speed(0)
    scoring.color("black")
    scoring.penup()
    scoring.hideturtle()
    scoring.goto(0, 300)
    scoring.write("Score :", align="center", font=("Courier", 24, "bold"))

# Control snake movement
def snake_go_up():
    if snake.direction != "down":
        snake.direction = "up"

def snake_go_down():
    if snake.direction != "up":
        snake.direction = "down"

def snake_go_left():
    if snake.direction != "right":
        snake.direction = "left"

def snake_go_right():
    if snake.direction != "left":
        snake.direction = "right"

# Update snake's position
def snake_move():
    if snake.direction == "up":
        snake.sety(snake.ycor() + 20)
    elif snake.direction == "down":
        snake.sety(snake.ycor() - 20)
    elif snake.direction == "left":
        snake.setx(snake.xcor() - 20)
    elif snake.direction == "right":
        snake.setx(snake.xcor() + 20)

# Pause and unpause the game
def toggle_pause():
    global paused
    paused = not paused

    if paused:
        pause_message.clear()
        pause_message.penup()
        pause_message.goto(0, 260)
        pause_message.color("darkred")
        pause_message.write("Paused", align="center", font=("Courier", 24, "bold"))
    else:
        pause_message.clear()

# Handle game over state
def game_over(score):
    screen.clear()
    screen.bgcolor('turquoise')
    scoring.goto(0, 0)
    scoring.write(f"GAME OVER\nYour Score: {score}", align="center", font=("Courier", 30, "bold"))

# Main game loop
def game_loop():
    global score, delay, old_fruit, paused

    while True:
        screen.update()

        if paused:
            time.sleep(0.1)
            continue

        if snake.distance(fruit) < 20:
            fruit.goto(random.randint(-290, 270), random.randint(-240, 240))
            score += 1
            scoring.clear()
            scoring.write(f"Score: {score}", align="center", font=("Courier", 24, "bold"))
            delay = max(0.01, delay - 0.001)

            new_fruit = turtle.Turtle()
            new_fruit.speed(0)
            new_fruit.shape('square')
            new_fruit.color('red')
            new_fruit.penup()
            old_fruit.append(new_fruit)

        for index in range(len(old_fruit) - 1, 0, -1):
            old_fruit[index].goto(old_fruit[index - 1].xcor(), old_fruit[index - 1].ycor())

        if old_fruit:
            old_fruit[0].goto(snake.xcor(), snake.ycor())

        snake_move()

        if abs(snake.xcor()) > 280 or abs(snake.ycor()) > 240:
            game_over(score)
            break

        if any(food.distance(snake) < 20 for food in old_fruit):
            game_over(score)
            break

        time.sleep(delay)

# Exit the game
def exit_game():
    root.quit()

# Tkinter main menu setup
root = tk.Tk()
root.title("Snake Game Menu")
root.geometry("400x300")
root.configure(bg="lightblue")

tk.Button(root, text="Start Game", command=start_game, width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2).place(x=120, y=80)
tk.Button(root, text="Exit", command=exit_game, width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2).place(x=120, y=150)

root.mainloop()

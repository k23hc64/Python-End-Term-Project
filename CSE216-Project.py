import turtle
import random
import time
import tkinter as tk

# Initialize global variables for the snake and game elements
snake = None
fruit = None
old_fruit = []
scoring = None
screen = None
score = 0
delay = 0.1
difficulty = "Medium"
paused = False  # Track if the game is paused
pause_message = None  # Variable for the "Paused" message

# Function to start the game and show difficulty selection
def start_game():
    # Hide the Tkinter main menu
    root.withdraw()

    # Show the difficulty selection screen
    show_difficulty_screen()

# Function to show the difficulty selection screen
def show_difficulty_screen():
    # Create a new window for difficulty selection
    difficulty_window = tk.Toplevel()
    difficulty_window.title("Select Difficulty")
    difficulty_window.geometry("400x300")
    difficulty_window.configure(bg="lightblue")  # Set background to lightblue

    # Label for difficulty selection
    label = tk.Label(difficulty_window, text="Select Difficulty Level", font=("Courier", 18, "bold"), bg="lightblue")
    label.pack(pady=20)

    # Easy button
    easy_button = tk.Button(difficulty_window, text="Easy", command=lambda: set_difficulty("Easy", difficulty_window), width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2)
    easy_button.pack(pady=10)

    # Medium button
    medium_button = tk.Button(difficulty_window, text="Medium", command=lambda: set_difficulty("Medium", difficulty_window), width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2)
    medium_button.pack(pady=10)

    # Hard button
    hard_button = tk.Button(difficulty_window, text="Hard", command=lambda: set_difficulty("Hard", difficulty_window), width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2)
    hard_button.pack(pady=10)

# Function to set the difficulty and start the game
def set_difficulty(level, window):
    global difficulty, delay
    difficulty = level
    window.destroy()  # Close the difficulty selection window

    # Adjust the game delay based on the difficulty
    if difficulty == "Easy":
        delay = 0.15
    elif difficulty == "Medium":
        delay = 0.1
    elif difficulty == "Hard":
        delay = 0.05

    # Start the game with the selected difficulty
    start_game_with_difficulty()

# Function to start the game with the chosen difficulty
def start_game_with_difficulty():
    global snake, fruit, old_fruit, scoring, screen, score, delay, paused, pause_message

    # Initialize the turtle screen for the game
    global screen
    screen = turtle.Screen()
    screen.title('SNAKE GAME')
    screen.setup(width=700, height=700)
    screen.bgcolor("lightblue")  # Set the game background color to lightblue
    screen.tracer(0)

    # Create the game border
    create_border()

    # Initialize score and snake setup
    score = 0
    snake = turtle.Turtle()
    snake.speed(0)
    snake.shape('square')
    snake.color("black")
    snake.penup()
    snake.goto(0, 0)
    snake.direction = 'stop'

    # Fruit setup
    fruit = turtle.Turtle()
    fruit.speed(0)
    fruit.shape('circle')
    fruit.color('red')
    fruit.penup()
    fruit.goto(30, 30)

    # List to store the snake's body
    old_fruit = []

    # Scoring display
    scoring = turtle.Turtle()
    scoring.speed(0)
    scoring.color("black")
    scoring.penup()
    scoring.hideturtle()
    scoring.goto(0, 300)
    scoring.write("Score :", align="center", font=("Courier", 24, "bold"))

    # Pause message setup
    pause_message = turtle.Turtle()
    pause_message.speed(0)
    pause_message.hideturtle()

    # Keyboard bindings
    screen.listen()
    screen.onkeypress(snake_go_up, "Up")
    screen.onkeypress(snake_go_down, "Down")
    screen.onkeypress(snake_go_left, "Left")
    screen.onkeypress(snake_go_right, "Right")

    # Pause button binding
    screen.onkeypress(toggle_pause, "space")  # Press 'Space' to toggle pause

    # Main game loop
    game_loop()

# Function to create the game border
def create_border():
    turtle.speed(5)
    turtle.pensize(4)
    turtle.penup()
    turtle.goto(-310, 250)
    turtle.pendown()
    turtle.color('black')
    turtle.forward(600)
    turtle.right(90)
    turtle.forward(500)
    turtle.right(90)
    turtle.forward(600)
    turtle.right(90)
    turtle.forward(500)
    turtle.penup()
    turtle.hideturtle()

# Functions to control snake movement
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

def snake_move():
    if snake.direction == "up":
        y = snake.ycor()
        snake.sety(y + 20)

    if snake.direction == "down":
        y = snake.ycor()
        snake.sety(y - 20)

    if snake.direction == "left":
        x = snake.xcor()
        snake.setx(x - 20)

    if snake.direction == "right":
        x = snake.xcor()
        snake.setx(x + 20)

# Toggle pause
def toggle_pause():
    global paused
    paused = not paused

    if paused:
        # Display the "Paused" message in bold below the score with dark red color
        pause_message.clear()  # Clear any previous message
        pause_message.penup()
        pause_message.goto(0, 260)  # Position it directly below the score
        pause_message.color("darkred")  # Dark red color
        pause_message.write("Paused", align="center", font=("Courier", 24, "bold"))  # Same size as score
    else:
        # Hide the "Paused" message when unpaused
        pause_message.clear()

# Game over function
def game_over(score):
    screen.clear()
    screen.bgcolor('lightblue')  # Set background to lightblue on game over
    scoring.goto(0, 0)
    scoring.write(f"GAME OVER\nYour Score: {score}", align="center", font=("Courier", 30, "bold"))

# Main game loop
def game_loop():
    global score, delay, old_fruit, paused

    while True:
        screen.update()

        if paused:
            time.sleep(0.1)  # Pause the game
            continue

        # Snake and food collision detection
        if snake.distance(fruit) < 20:
            x = random.randint(-290, 270)
            y = random.randint(-240, 240)
            fruit.goto(x, y)
            score += 1
            scoring.clear()
            scoring.write(f"Score: {score}", align="center", font=("Courier", 24, "bold"))
            delay -= 0.001

            # Add new segment to the snake's body
            new_fruit = turtle.Turtle()
            new_fruit.speed(0)
            new_fruit.shape('square')
            new_fruit.color('red')
            new_fruit.penup()
            old_fruit.append(new_fruit)

        # Move the snake's body
        for index in range(len(old_fruit) - 1, 0, -1):
            a = old_fruit[index - 1].xcor()
            b = old_fruit[index - 1].ycor()
            old_fruit[index].goto(a, b)

        if len(old_fruit) > 0:
            a = snake.xcor()
            b = snake.ycor()
            old_fruit[0].goto(a, b)

        snake_move()

        # Check for snake collisions with borders
        if snake.xcor() > 280 or snake.xcor() < -300 or snake.ycor() > 240 or snake.ycor() < -240:
            game_over(score)
            break

        # Check for collision with itself
        for segment in old_fruit:
            if segment.distance(snake) < 20:
                game_over(score)
                break

        time.sleep(delay)

# Tkinter window setup
root = tk.Tk()
root.title("Snake Game")
root.geometry("400x300")
root.configure(bg="lightblue")  # Set background to lightblue

# Start button to start the game
start_button = tk.Button(root, text="Start Game", command=start_game, width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2)
start_button.pack(pady=50)

# Quit button to exit the game
exit_button = tk.Button(root, text="Exit", command=root.quit, width=20, height=2, font=("Courier", 14, "bold"), bg="white", fg="black", relief="solid", bd=2)
exit_button.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
